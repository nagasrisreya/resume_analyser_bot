from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from dotenv import load_dotenv
import os

from bot.handlers import (
    start,
    upload_command,
    receive_resume,
    receive_question,
    analyze_command,
    ask_command,
    done_command,
    jd_command,
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("upload", upload_command))
    app.add_handler(CommandHandler("done", done_command))
    app.add_handler(CommandHandler("jd", jd_command))
    app.add_handler(CommandHandler("analyze", analyze_command))
    app.add_handler(CommandHandler("ask", ask_command))
    
    # Document uploads (PDF/DOCX)
    app.add_handler(
        MessageHandler(
            filters.Document.ALL,
            receive_resume
        )
    )

    # Text questions from /ask mode
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receive_question
        )
    )

    print("🤖 Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()
