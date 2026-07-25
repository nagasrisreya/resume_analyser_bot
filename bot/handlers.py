import os

from telegram import Update
from telegram.ext import ContextTypes
from backend.parser import parse_document
# from backend.ats import calculate_score

from backend.scorer import calculate_score
from backend.extractor import (
    extract_resume_info,
    extract_jd_info
)
from backend.chatbot import ask_resume_question

UPLOAD_FOLDER = "uploads/resumes"
JD_FOLDER = "uploads/jd"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(JD_FOLDER, exist_ok=True)

# -----------------------------
# Temporary memory
# -----------------------------
user_files = {}      # Stores uploaded resumes
user_jd = {}         # Stores uploaded JDs (list now)
user_mode = {}       # "resume" or "jd"
analysis_results = {}  # Stores structured analysis per user
ask_mode_users = set()  # Users who have entered /ask and are waiting for a question


# -----------------------------
# Start Command
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Use /upload to upload resumes."
    )


# -----------------------------
# Upload Resume Command
# -----------------------------
async def upload_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    user_mode[user_id] = "resume"
    user_files[user_id] = []

    await update.message.reply_text(
        "📄 Send one or more PDF/DOCX resumes.\n\n"
        "When finished, type /done"
    )


# -----------------------------
# Upload JD Command
# -----------------------------
async def jd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    user_mode[user_id] = "jd"
    user_jd.setdefault(user_id, [])

    await update.message.reply_text(
        "📄 Upload one or more Job Descriptions (PDF/DOCX).\n\n"
        "When finished, type /done"
    )


# -----------------------------
# Receive Documents
# -----------------------------
async def receive_resume(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    document = update.message.document

    if document is None:
        return

    filename = document.file_name

    if not filename.lower().endswith((".pdf", ".docx")):
        await update.message.reply_text(
            "❌ Only PDF and DOCX files are allowed."
        )
        return

    file = await context.bot.get_file(document.file_id)

    mode = user_mode.get(user_id)

    # -----------------------------
    # Resume Upload
    # -----------------------------
    if mode == "resume":

        save_path = os.path.join(
            UPLOAD_FOLDER,
            f"{user_id}_{filename}"
        )

        await file.download_to_drive(save_path)

        user_files.setdefault(user_id, []).append(save_path)

        await update.message.reply_text(
            f"✅ Resume uploaded: {filename}"
        )

    # -----------------------------
    # JD Upload
    # -----------------------------
    elif mode == "jd":

        save_path = os.path.join(
            JD_FOLDER,
            f"{user_id}_{filename}"
        )

        await file.download_to_drive(save_path)

        user_jd.setdefault(user_id, []).append(save_path)

        await update.message.reply_text(
            f"✅ JD uploaded: {filename}"
        )

    else:

        await update.message.reply_text(
            "⚠️ Please use /upload to upload resumes or /jd to upload a Job Description first."
        )


# -----------------------------
# Done Command
# -----------------------------
async def done_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    files = user_files.get(user_id, [])
    jds = user_jd.get(user_id, [])

    msg_parts = []

    if len(files) > 0:
        msg_parts.append("✅ Resumes received:\n")
        for f in files:
            msg_parts.append(f"• {os.path.basename(f)}\n")

    if len(jds) > 0:
        msg_parts.append("\n✅ JDs received:\n")
        for j in jds:
            msg_parts.append(f"• {os.path.basename(j)}\n")

    if not files and not jds:
        await update.message.reply_text(
            "❌ You haven't uploaded any resumes or JDs."
        )
        return

    if len(files) == 0:
        msg_parts.append("\nUse /upload to upload resumes.\n")

    if len(jds) == 0:
        msg_parts.append("\nUse /jd to upload Job Descriptions.\n")

    msg_parts.append("\nType /analyze to start ATS analysis.")

    await update.message.reply_text("".join(msg_parts))


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if not context.args:
        ask_mode_users.add(user_id)
        await update.message.reply_text(
            "❓ Ask a question about the analyzed resumes, for example:\n\n"
            "• Who has the highest CGPA?\n"
            "• Which candidate knows React?\n"
            "• Why did Resume 2 score lower?"
        )
        return

    question = " ".join(context.args)
    analysis = analysis_results.get(user_id)

    if not analysis:
        await update.message.reply_text(
            "⚠️ No analysis results found. Run /analyze first."
        )
        return

    await update.message.reply_text("🧠 Thinking...")
    answer = ask_resume_question(question, analysis)
    await update.message.reply_text(answer)


async def receive_question(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in ask_mode_users:
        return

    text = (update.message.text or "").strip()
    if not text:
        return

    if text.startswith("/"):
        return

    analysis = analysis_results.get(user_id)
    if not analysis:
        await update.message.reply_text("⚠️ No analysis results found. Run /analyze first.")
        ask_mode_users.discard(user_id)
        return

    await update.message.reply_text("🧠 Thinking...")
    answer = ask_resume_question(text, analysis)
    await update.message.reply_text(answer)
    ask_mode_users.discard(user_id)


async def analyze_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    resumes = user_files.get(user_id, [])
    jds = user_jd.get(user_id, [])

    if not resumes:
        await update.message.reply_text(
            "❌ No resumes uploaded."
        )
        return

    if not jds:
        await update.message.reply_text(
            "❌ Please upload at least one Job Description first using /jd."
        )
        return

    await update.message.reply_text(
        "⏳ Analyzing resumes against all JDs...\nThis may take a few seconds."
    )

    results = []
    stored_resumes = []
    stored_jds = []

    # -----------------------
    # Parse all JDs
    # -----------------------
    for jd_path in jds:
        jd_text = parse_document(jd_path)
        jd_json = extract_jd_info(jd_text)
        stored_jds.append({
            "name": os.path.basename(jd_path),
            "data": jd_json
        })

    # -----------------------
    # Analyze each Resume against each JD
    # -----------------------
    for resume in resumes:

        resume_text = parse_document(resume)
        resume_json = extract_resume_info(resume_text)

        # Score against each JD and take the best match
        best_score = 0
        best_matched = []
        best_missing = []

        for jd_json in [j["data"] for j in stored_jds]:
            result = calculate_score(resume_json, jd_json)
            if result["score"] > best_score:
                best_score = result["score"]
                best_matched = result["matched"]
                best_missing = result["missing"]

        result_entry = {
            "name": os.path.basename(resume),
            "data": resume_json,
            "score": best_score,
            "matched": best_matched,
            "missing": best_missing
        }

        results.append({
            "resume": resume,
            "score": best_score,
            "matched": best_matched,
            "missing": best_missing
        })
        stored_resumes.append(result_entry)

    # -----------------------
    # Ranking
    # -----------------------
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    analysis_results[user_id] = {
        "jd": stored_jds,
        "resumes": stored_resumes
    }

    message = "🏆 ATS Ranking\n\n"

    for idx, result in enumerate(results, start=1):

        message += (
            f"{idx}. {os.path.basename(result['resume'])}\n"
            f"⭐ Score: {result['score']}%\n"
            f"✅ Matched Skills: {', '.join(result['matched']) if result['matched'] else 'None'}\n"
            f"❌ Missing Skills: {', '.join(result['missing']) if result['missing'] else 'None'}\n\n"
        )

    message += "\nYou can now ask questions with /ask, such as who has the highest CGPA or which resume matches the job best."

    await update.message.reply_text(message)
