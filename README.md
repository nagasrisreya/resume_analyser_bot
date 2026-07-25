# 📄 AI Resume Analyzer Bot

An AI-powered Resume Screening Bot built using **Python**, **Telegram Bot API**, **Groq LLM**, and **Natural Language Processing** that evaluates multiple resumes against a Job Description (JD), ranks candidates using an ATS-inspired scoring system, identifies missing skills, and provides intelligent career recommendations through an interactive chatbot.

---

# Features

- Upload multiple resumes directly through Telegram
- Upload a Job Description (JD)
- Parse PDF and DOCX documents
- AI-based information extraction using Groq LLM
- ATS-style resume scoring
- Candidate ranking
- Skill gap analysis
- Resume improvement suggestions
- Interactive AI chatbot for resume queries
- Supports multiple resumes simultaneously

---

# Project Architecture

```
                    Telegram User
                          │
                          ▼
                Telegram Bot Interface
                          │
          ┌───────────────┴───────────────┐
          │                               │
     Resume Upload                  JD Upload
          │                               │
          ▼                               ▼
      PDF/DOCX Parser              PDF/DOCX Parser
          │                               │
          └───────────────┬───────────────┘
                          ▼
                Text Extraction Layer
                          │
                          ▼
                 Groq Large Language Model
                          │
                          ▼
          Structured Resume & JD Information
                          │
                          ▼
                ATS Scoring Engine
                          │
                          ▼
          Candidate Ranking & Skill Analysis
                          │
                          ▼
               AI Career Recommendation
                          │
                          ▼
                 Telegram Chat Assistant
```

---

# Tech Stack

### Backend

- Python 3.11+
- python-telegram-bot
- Groq API
- pdfplumber
- python-docx
- dotenv

### AI

- Groq Llama 3.3 70B
- Prompt Engineering
- NLP
- Information Extraction

### File Processing

- PDF Parsing
- DOCX Parsing
- Text Cleaning

---

# Project Structure

```
resume-analyzer-bot/

│
├── bot/
│   ├── main.py
│   ├── handlers.py
│
├── backend/
│   ├── parser.py
│   ├── extractor.py
│   ├── scorer.py
│   ├── groq_client.py
│   ├── chatbot.py
│   ├── json_parser.py
│
├── uploads/
│   ├── resumes/
│   └── jd/
│
├── .env
├── requirements.txt
└── README.md
```

---

# Workflow

## Step 1

User uploads one or more resumes.

```
/upload
```

The bot accepts multiple PDF or DOCX resumes.

---

## Step 2

User uploads the Job Description.

```
/jd
```

---

## Step 3

User starts ATS analysis.

```
/analyze
```

The system performs:

- Resume parsing
- JD parsing
- AI information extraction
- Skill matching
- Candidate scoring
- Ranking

---

## Step 4

Results

Example

```
Resume 1
ATS Score : 87%

Matched Skills
--------------
Python
React
Git
SQL

Missing Skills
--------------
Docker
Kubernetes
AWS

Recommended Courses
-------------------
Docker Essentials
AWS Cloud Practitioner
```

---

## Step 5

Interactive AI Chat

```
/ask
```

Example questions

```
Who has the highest ATS score?

Which resume matches the JD best?

Which candidate has React experience?

Suggest projects for Resume 2.

Suggest certifications.

Which candidate is strongest in backend development?

Why did Resume 1 score lower?

What skills are missing?

How can Resume 2 improve?
```

---

# Information Extracted

The AI extracts structured information including:

- Candidate Name
- Email
- Phone Number
- Degree
- University
- CGPA
- Graduation Year
- Technical Skills
- Soft Skills
- Certifications
- Projects
- Internship Experience
- Work Experience

---

# ATS Scoring Strategy

The scoring engine evaluates multiple dimensions.

| Category | Weight |
|----------|---------|
| Required Skills Match | 70% |
| Education | 10% |
| Projects | 10% |
| Certifications | 10% |

Final Score

```
ATS Score =
Skill Score
+ Education Score
+ Project Score
+ Certification Score
```

---

# AI Pipeline

```
Resume PDF
      │
      ▼
Text Extraction
      │
      ▼
Groq LLM
      │
      ▼
Structured JSON
      │
      ▼
ATS Scoring
      │
      ▼
Ranking
      │
      ▼
Chat Assistant
```

---

# Prompt Engineering

The project uses carefully designed prompts to extract:

- Technical Skills
- Required Skills
- Preferred Skills
- Projects
- Certifications
- Education
- Experience

The LLM returns structured JSON which is then consumed by the scoring engine.

---

# Why Groq?

Groq provides:

- Extremely fast inference
- Low latency
- High-quality reasoning
- Excellent structured JSON generation
- Reliable information extraction

This enables accurate resume parsing without training custom NLP models.

---

# Future Enhancements

- Semantic similarity using Sentence Transformers
- Vector Database (FAISS)
- Resume embedding search
- Multi-language resume support
- WhatsApp Integration
- Discord Integration
- Email Integration
- Resume rewriting assistant
- HR Dashboard
- Web Admin Portal
- Candidate shortlist generation
- Interview question generation
- AI Resume Builder

---

# Installation

Clone repository

```bash
git clone <repository-url>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create

```
.env
```

```
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN

GROQ_API_KEY=YOUR_GROQ_API_KEY
```

Run

```bash
python bot/main.py
```

---

# Commands

| Command | Description |
|----------|-------------|
| /start | Start the bot |
| /upload | Upload one or more resumes |
| /done | Finish resume upload |
| /jd | Upload Job Description |
| /analyze | Perform ATS analysis |
| /ask | Ask AI questions about analyzed resumes |

---

# Advantages

- No website required
- Accessible directly through Telegram
- Supports multiple candidates
- AI-powered resume understanding
- Fast ATS evaluation
- Interactive career guidance
- Lightweight architecture
- Easily deployable on cloud platforms

---

# Future Research

This project can be extended into a complete AI recruitment platform by integrating Retrieval-Augmented Generation (RAG), vector databases, semantic resume matching, and automated interview assistance, enabling end-to-end intelligent talent acquisition.

---

# Authors

Developed as an AI-powered Recruitment Assistant using Python, Telegram Bot API, Groq LLM, and Natural Language Processing.
