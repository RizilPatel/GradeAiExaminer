import streamlit as st
import streamlit.components.v1 as components
from LLM import infer
from util import write_answer
from trans import speak

# Set page configuration
st.set_page_config(
    page_title="Grade Guru AI Examiner",
    page_icon="./grade-guru.png", 
    layout="wide"
)

# Inject custom CSS for better UI
st.markdown(
    """
    <style>
        /* Center align title */
        .stTitle {
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            color: #4B0082;
        }

        /* Style for buttons */
        div.stButton > button {
            background-color: #4B0082 !important;
            color: white !important;
            font-size: 18px !important;
            font-weight: bold;
            border-radius: 8px;
            padding: 12px 24px;
            border: none;
            transition: 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #6A0DAD !important;
        }

        /* Style for text areas */
        textarea {
            background-color: #f4f4f4 !important;
            color: #4B0082 !important;
            border: 2px solid #4B0082 !important;
            border-radius: 8px;
            font-size: 16px;
            padding: 10px;
        }

        /* Sidebar design */
        [data-testid="stSidebar"] {
            background-color: #1e1e2d !important;
            color: white !important;
        }

        /* Adjust columns layout */
        .st-emotion-cache-1wivap2 {
            margin: auto;
            text-align: center;
        }
        
    </style>
    """,
    unsafe_allow_html=True
)

# Page Title
st.markdown("<h1 class='stTitle'>📘 Grade Guru - The AI Examiner</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #4B0082;'>Where AI meets A+!</h3>", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([4, 8])

# Display the logo in the first column
with col1:
    st.image("./grade-guru.png", width=120)

# Display the title in the second column
with col2:
    st.write("")  # Adding space
    st.subheader("Your AI-Powered Exam Assistant 🎓")
    st.write("💡 Upload student answers and let AI grade with precision!")

# **Step 1: Upload Student Answer Photo**
st.markdown("### 📝 Step 1: Upload Student Answer Photo")
components.html(
    """
    <iframe
        src="https://merve-llava-next.hf.space"
        frameborder="0"
        width="100%"
        height="300px"
    ></iframe>
    """,
    height=300
)

# **Step 2: Enter Extracted Student Answer**
st.markdown("### 🖋️ Step 2: Enter Student's Extracted Answer")
student_answer = st.text_area("📌 Paste the extracted text here", height=150)

# **Step 3: Enter Teacher's Answer**
st.markdown("### 🧑‍🏫 Step 3: Enter Teacher's Answer")
teacher_answer = st.text_area("📌 Paste the teacher's answer here", height=150)

# **Step 4: Enter Total Marks**
st.markdown("### 🎯 Step 4: Enter Total Marks for the Question")
total_marks = st.text_input("🏆 Enter total marks for this question", max_chars=10)

# **Submit Button**
if st.button("🚀 Examine Result", key="submit_button", help="Click to evaluate the answer."):
    with st.spinner("🔍 Analyzing the answers... Please wait!"):
        Evaluation = infer(student_answer, teacher_answer, total_marks)

    # Display AI-generated feedback
    st.markdown("## 🎓 AI Evaluation Result:")
    write_answer(Evaluation, max_line_length)
    
    # Text-to-Speech feature
    speak(Evaluation)
