import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

# Load trained model (you must save this using pickle in your notebook)
@st.cache_resource
def load_model():
    with open("student_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# Title
st.title("🎓 Student Performance Predictor")
st.markdown("Predict whether a student will **pass or fail** based on their academic and personal attributes.")

# Sidebar inputs
st.sidebar.header("📋 Input Student Details")

gender = st.sidebar.selectbox("Gender", ["male", "female"])
study_time = st.sidebar.slider("Weekly Study Time (1=low, 6=high)", 1, 6, 2)
fam_sup = st.sidebar.selectbox("Family Support", ["yes", "no"])
internet = st.sidebar.selectbox("Internet Access", ["yes", "no"])
failure_count = st.sidebar.slider("Number of Past Failures", 0, 5, 0)
absences = st.sidebar.slider("Number of Absences", 0, 100, 4)
health = st.sidebar.slider("Health (1=very bad, 10=very good)", 1, 10, 3)

def encode_inputs():
    data = {
        'sex': 1 if gender == 'male' else 0,
        'studytime': study_time,
        'famsup': 1 if fam_sup == 'yes' else 0,
        'internet': 1 if internet == 'yes' else 0,
        'failures': failure_count,
        'absences': absences,
        'health': health
    }
    return pd.DataFrame([data])

input_df = encode_inputs()

# Predict
if st.button("Predict"):
    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]
    
    if prediction == 1:
        st.success(f"✅ The student is likely to PASS with {prob * 100:.2f}% confidence.")
    else:
        st.error(f"❌ The student is likely to FAIL with {(1 - prob) * 100:.2f}% confidence.")

# Optional: Show user inputs
with st.expander("Show Inputs"):
    st.write(input_df)

st.markdown("---")
st.markdown("Made by Tanishq Kumar | Supervised ML Project")
