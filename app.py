import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

# Page config
st.set_page_config(
    page_title="AI Interviewer for AIML Projects",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .question-card {
        background: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 5px solid #1f77b4;
    }
    .score-card {
        background: linear-gradient(135deg, #1f77b4, #2ca02c);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'scores' not in st.session_state:
    st.session_state.scores = {}
if 'project_info' not in st.session_state:
    st.session_state.project_info = {}

# Enhanced AIML questions - UPDATED WITH MORE QUESTIONS
AIML_QUESTIONS = {
    "beginner": [
        {"q": "What is the difference between supervised and unsupervised learning?", 
         "category": "Fundamentals"},
        {"q": "Explain what overfitting is and how to prevent it.",
         "category": "Model Training"},
        {"q": "What evaluation metrics would you use for classification vs regression?",
         "category": "Evaluation"},
        {"q": "What is cross-validation and why is it important?",
         "category": "Validation"},
    ],
    "intermediate": [
        {"q": "How does a Random Forest algorithm work and what are its advantages?",
         "category": "Algorithms"},
        {"q": "Explain gradient descent optimization and different variants.",
         "category": "Optimization"},
        {"q": "How would you handle imbalanced datasets in classification?",
         "category": "Data Handling"},
        {"q": "Explain the bias-variance tradeoff with examples.",
         "category": "Theory"},
    ],
    "advanced": [
        {"q": "How does the attention mechanism work in transformers?",
         "category": "Deep Learning"},
        {"q": "How would you deploy a machine learning model in production?",
         "category": "MLOps"},
        {"q": "Explain backpropagation through time for RNNs.",
         "category": "Neural Networks"},
        {"q": "What are GANs and how do generator/discriminator work?",
         "category": "Advanced Models"},
    ]
}

def get_grade(score):
    if score >= 9:
        return "A+ 🏆"
    elif score >= 8:
        return "A 👍"
    elif score >= 7:
        return "B+ ✅"
    elif score >= 6:
        return "B 📈"
    elif score >= 5:
        return "C+ 💡"
    else:
        return "C 📚"

def evaluate_answer(answer):
    """Enhanced evaluation logic"""
    if not answer:
        return 0
    
    word_count = len(answer.split())
    
    # Score based on length and content
    length_score = min(word_count / 10, 3)
    
    # Check for technical terms
    tech_terms = ['algorithm', 'model', 'data', 'training', 'accuracy', 
                  'precision', 'recall', 'feature', 'parameter', 'hyperparameter']
    tech_score = sum(0.2 for term in tech_terms if term in answer.lower())
    
    # Structure bonus
    structure_indicators = ['first', 'second', 'because', 'therefore', 'for example']
    structure_score = 1 if any(indicator in answer.lower() for indicator in structure_indicators) else 0
    
    total = min(length_score + tech_score + structure_score, 10)
    return round(total, 1)

def main():
    st.markdown('<h1 class="main-title">🤖 AI Interviewer for AIML Projects</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Progress")
        st.write(f"Step {st.session_state.step} of 3")
        
        if st.button("🔄 Reset Interview", use_container_width=True):
            st.session_state.step = 1
            st.session_state.answers = {}
            st.session_state.scores = {}
            st.session_state.project_info = {}
            st.rerun()
    
    # Step 1
    if st.session_state.step == 1:
        st.header("📋 Step 1: Project Setup")
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name", placeholder="e.g., Customer Churn Prediction")
            project_type = st.selectbox(
                "Project Type",
                ["Classification", "Regression", "Clustering", "Deep Learning", "NLP", "Computer Vision"]
            )
        
        with col2:
            difficulty = st.select_slider(
                "Difficulty Level",
                options=["Beginner", "Intermediate", "Advanced"]
            )
            
            tech_stack = st.multiselect(
                "Technologies Used",
                ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", 
                 "Keras", "OpenCV", "NLTK", "Transformers", "XGBoost"],
                default=["Python", "Scikit-learn"]
            )
        
        if st.button("🚀 Start Interview", type="primary", use_container_width=True):
            if project_name:
                st.session_state.project_info = {
                    "name": project_name,
                    "type": project_type,
                    "difficulty": difficulty,
                    "tech": tech_stack
                }
                st.session_state.step = 2
                st.rerun()
            else:
                st.warning("Please enter a project name")
    
    # Step 2 - UPDATED: Shows ALL questions for selected difficulty
    elif st.session_state.step == 2:
        st.header("🎤 Step 2: Technical Interview")
        
        project_info = st.session_state.get('project_info', {})
        difficulty = project_info.get('difficulty', 'beginner').lower()
        
        st.info(f"**Project:** {project_info.get('name', 'AIML Project')} | **Difficulty:** {difficulty.title()}")
        
        # Get ALL questions for selected difficulty
        questions = AIML_QUESTIONS.get(difficulty, AIML_QUESTIONS['beginner'])
        
        for i, item in enumerate(questions):  # CHANGED: Show ALL questions
            with st.container():
                st.markdown(f"""
                <div class="question-card">
                    <h4>Question {i+1} ({item['category']})</h4>
                    <p>{item['q']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                answer_key = f"q_{i}"
                answer = st.text_area(
                    f"Your answer for Question {i+1}:",
                    value=st.session_state.answers.get(answer_key, ""),
                    height=100,
                    key=f"answer_{i}",
                    placeholder="Type your answer here..."
                )
                
                if answer:
                    st.session_state.answers[answer_key] = answer
                    score = evaluate_answer(answer)
                    st.session_state.scores[answer_key] = score
                    
                    # Show mini feedback
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Score", f"{score}/10")
                    with col2:
                        if score >= 8:
                            st.success("Excellent! 🎯")
                        elif score >= 6:
                            st.info("Good! 📝")
                        else:
                            st.warning("Keep going! 💪")
            
            st.markdown("---")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.step = 1
                st.rerun()
        with col3:
            if st.button("Evaluate →", type="primary", use_container_width=True):
                if st.session_state.answers:
                    st.session_state.step = 3
                    st.rerun()
                else:
                    st.warning("Please answer at least one question")
    
    # Step 3
    else:
        st.header("📊 Step 3: Evaluation Results")
        
        if not st.session_state.scores:
            st.warning("No answers to evaluate. Please go back and answer questions.")
            if st.button("← Back to Questions"):
                st.session_state.step = 2
                st.rerun()
            return
        
        scores = list(st.session_state.scores.values())
        avg_score = sum(scores) / len(scores)
        
        # Display overall score
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="score-card">
                <h3>Overall Score</h3>
                <h1>{avg_score:.1f}/10</h1>
                <h3>{get_grade(avg_score)}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            performance = "Excellent" if avg_score >= 8 else "Good" if avg_score >= 6 else "Needs Improvement"
            st.markdown(f"""
            <div style='padding: 20px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h4>Performance</h4>
                <h2>{performance}</h2>
                <p>{len(scores)} questions answered</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            project_info = st.session_state.get('project_info', {})
            st.markdown(f"""
            <div style='padding: 20px; background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h4>Project Details</h4>
                <p><strong>{project_info.get('name', 'Project')}</strong></p>
                <p>Type: {project_info.get('type', 'N/A')}</p>
                <p>Difficulty: {project_info.get('difficulty', 'Medium')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Score breakdown chart
        if len(scores) > 1:
            st.subheader("📈 Score Breakdown")
            fig = go.Figure(data=[
                go.Bar(
                    x=[f"Q{i+1}" for i in range(len(scores))],
                    y=scores,
                    marker_color=['#2ca02c' if s >= 7 else '#ff7f0e' if s >= 4 else '#d62728' for s in scores]
                )
            ])
            fig.update_layout(
                yaxis_title="Score (/10)",
                yaxis_range=[0, 10],
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed feedback
        st.subheader("📋 Detailed Feedback")
        for i in range(len(scores)):
            with st.expander(f"Question {i+1} - Score: {scores[i]}/10"):
                answer_key = f"q_{i}"
                answer = st.session_state.answers.get(answer_key, "No answer provided")
                st.markdown(f"**Your Answer:** {answer}")
                
                if scores[i] >= 8:
                    feedback = "Excellent answer with good technical depth and clear explanation."
                elif scores[i] >= 6:
                    feedback = "Good answer, consider adding more technical details or examples."
                else:
                    feedback = "Answer could be improved with more specific details and clearer structure."
                
                st.info(f"**Feedback:** {feedback}")
        
        st.markdown("---")
        
        # Export and restart
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download Report", use_container_width=True):
                report_data = {
                    'Project Name': [st.session_state.project_info.get('name', 'N/A')],
                    'Overall Score': [f"{avg_score:.1f}/10"],
                    'Grade': [get_grade(avg_score)],
                    'Questions Answered': [len(scores)]
                }
                df = pd.DataFrame(report_data)
                csv = df.to_csv(index=False)
                
                st.download_button(
                    label="Click to Download CSV",
                    data=csv,
                    file_name="interview_report.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("🔄 New Interview", type="primary", use_container_width=True):
                st.session_state.step = 1
                st.session_state.answers = {}
                st.session_state.scores = {}
                st.session_state.project_info = {}
                st.rerun()

if __name__ == "__main__":
    main()