import streamlit as st
import fitz  # PyMuPDF for PDFs
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ----------------------------
# Custom CSS (Cool Pastel Theme)
# ----------------------------
page_bg = """
<style>
body {
    background-color: #f5f7fa;
    color: #1e1e2f;
    font-family: 'Segoe UI', sans-serif;
    font-size: 18px;
}
[data-testid="stSidebar"] {
    background-color: #e8eaf6;
}
h1, h2, h3 {
    color: #4a148c;
    font-weight: bold;
}
.stButton>button {
    background: linear-gradient(to right, #7e57c2, #42a5f5);
    color: white;
    border-radius: 12px;
    padding: 0.8em 1.5em;
    border: none;
    font-size: 18px;
    font-weight: bold;
}
.stTextArea textarea {
    background-color: #ffffff;
    color: #1e1e2f;
    font-size: 16px;
    border-radius: 10px;
    border: 1px solid #c5cae9;
    padding: 10px;
}
.stFileUploader>div>div {
    background-color: #fafafa;
    border: 2px dashed #7e57c2;
    border-radius: 10px;
    padding: 12px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.title("⚡ Navigation")
page = st.sidebar.radio("Go to:", ["🏠 Home", "📂 Resume Screening", "📊 Results", "ℹ About"])

# ----------------------------
# Resume Parser
# ----------------------------
def parse_resume(file):
    text = ""
    if file.name.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()
    elif file.name.endswith(".docx"):
        text = docx2txt.process(file)
    return text

# ----------------------------
# Pages
# ----------------------------
if page == "🏠 Home":
    st.title("AI Resume Screening & Ranking System")
    st.markdown("*An intelligent system that matches resumes with job descriptions.*")
    st.image("https://cdn-icons-png.flaticon.com/512/2920/2920244.png", width=250)
    st.markdown("👉 Use the sidebar to start screening resumes!")

elif page == "📂 Resume Screening":
    st.title("📂 Upload Resumes & Job Description")

    job_desc = st.text_area("📝 Enter Job Description")
    uploaded_files = st.file_uploader(
        "Upload Resumes (PDF/DOCX)",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if "results" not in st.session_state:
        st.session_state.results = None

    if st.button("🚀 Screen Resumes"):
        if job_desc and uploaded_files:
            resumes, names = [], []

            for file in uploaded_files:
                text = parse_resume(file)
                resumes.append(text)
                names.append(file.name)

            # TF-IDF
            vectorizer = TfidfVectorizer(stop_words="english")
            vectors = vectorizer.fit_transform([job_desc] + resumes)
            scores = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

            # Results
            st.session_state.results = sorted(zip(names, scores), key=lambda x: x[1], reverse=True)
            st.success("✅ Screening completed! Check the Results page.")
        else:
            st.warning("⚠ Please provide a job description and upload resumes.")

elif page == "📊 Results":
    st.title("📊 Resume Ranking Results")

    if st.session_state.get("results"):
        for i, (name, score) in enumerate(st.session_state.results, 1):
            if score > 0.6:
                st.success(f"#{i} {name} — Match Score: {round(score*100,2)}% ✅")
            elif score > 0.3:
                st.warning(f"#{i} {name} — Match Score: {round(score*100,2)}% ⚠️")
            else:
                st.error(f"#{i} {name} — Match Score: {round(score*100,2)}% ❌")
    else:
        st.info("⚠ No results yet. Please upload resumes first from the 'Resume Screening' page.")

elif page == "ℹ About":
    st.title("ℹ About This App")
    st.markdown("""
    This **AI Resume Screening & Ranking System** helps recruiters:
    - 📂 Upload multiple resumes (PDF/DOCX)  
    - 📝 Match resumes against job descriptions  
    - 📊 Rank candidates based on similarity scores  

    💡 *Built with Streamlit, TF-IDF & Cosine Similarity*  
    """)
