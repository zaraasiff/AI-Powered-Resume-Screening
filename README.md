# AI-Powered-Resume-Screening

This project is the **final task** of my internship, where I built an **AI-powered Resume Screening and Ranking System**.  
The system evaluates resumes against a given job description using **NLP techniques** and **AI APIs**, providing match scores and rankings.  

---

## 📌 Project Description
The goal of this project is to:
- Parse resumes (PDF/DOCX) and extract text
- Match candidates with job descriptions
- Rank resumes using **TF-IDF + Cosine Similarity**
- Integrate with **Free AI APIs** (Gemini) for smarter scoring
- Provide a **Streamlit-based UI** for easy usage

---

## Colab Notebook
Click the badge below to open the full project in Google Colab:  

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1RhvYVLebUvQoB8-yjc0mk_vYSIvCo7qa?usp=sharing)

---

## Streamlit App (Local Run)
To run locally:  

```bash
# Clone repo
git clone https://github.com/yourusername/ai-resume-screener.git
cd ai-resume-screener

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
