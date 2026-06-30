# 🎤 AI Mock Interview System

An AI-powered mock interview platform that helps users practice technical interviews by generating personalized questions, evaluating responses using NLP, and providing detailed feedback reports.

## 🚀 Live Demo

https://ai-mock-interview-system-bahtelvsep4eukg9nstieu.streamlit.app/

---

## ✨ Features

- 📄 Upload Resume (PDF)
- 🛠 Automatic Skill Extraction
- 🤖 Personalized Interview Questions
- 🏢 Company-specific Questions (Google, Amazon, Microsoft, etc.)
- ⏱ Real-time Interview Timer
- 📝 LeetCode-style Question Navigation
- 📊 NLP-based Answer Evaluation
- 📥 PDF Report Generation
- 🎨 Modern Dark-Themed UI

---

## 🛠 Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Machine Learning / NLP
- Scikit-learn
- TF-IDF Vectorization
- Cosine Similarity

### Libraries
- Streamlit
- PyPDF2
- ReportLab
- Pandas
- NumPy

---

## 🧠 How It Works

1. User uploads a resume.
2. Skills are extracted from the resume.
3. Interview questions are generated based on:
   - Selected role
   - Difficulty level
   - Company preference
   - Resume skills
4. User answers questions in an interview environment.
5. Answers are evaluated using TF-IDF and cosine similarity.
6. A final score and report are generated.

---

## 📂 Project Structure

```bash
AI_Mock_Interview_System/
│
├── app/
│   └── streamlit_app.py
│
├── core/
│   ├── evaluator.py
│   ├── question_generator.py
│   ├── report_generator.py
│   └── skill_extractor.py
│
├── data/
│   ├── question_bank.py
│   ├── company_questions.py
│   └── reference_answers.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/AI-Mock-Interview-System.git
```

Navigate to the project folder:

```bash
cd AI-Mock-Interview-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app/streamlit_app.py
```

---

## 🎯 Future Improvements

- AI-generated feedback using LLMs
- Voice-based interviews
- Video interview support
- Behavioral interview analysis
- Database integration

---

## 👩‍💻 Author

Shruti
