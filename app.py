import streamlit as st
import pandas as pd
import pickle


@st.cache_resource
def load_model():
    with open("student_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

st.title("Student Performance Predictor (Multi-Subject)")


student_name = st.text_input("Student Name")
gender = st.selectbox("Gender", ["male", "female"])


st.sidebar.header(" Setup Subjects")
num_subjects = st.sidebar.number_input("Number of subjects", min_value=1, max_value=10, value=3)

subject_names = []
for i in range(num_subjects):
    name = st.sidebar.text_input(f"Name of subject {i+1}", value=f"Subject{i+1}")
    subject_names.append(name)


st.sidebar.markdown("---")
health_option = st.sidebar.selectbox(" Health Status (asked once)", ["Good", "Fine", "Mild", "Bad"])

health_map = {
    "Good": 1 if gender == 'male' else 5,
    "Mild": 4 if gender == 'male' else 2,
    "Fine": 2 if gender == 'male' else 1,
    "Bad": 5 if gender == 'male' else 4
}
health = health_map[health_option]

st.markdown("---")

subject_results = []

for subj in subject_names:
    st.subheader(f" Input details for **{subj}**")

    study_time = st.slider(f"Weekly Study Time ({subj})", 1, 4, 2, key=f"studytime_{subj}")
    fam_sup = st.selectbox(f"Family Support ({subj})", ["yes", "no"], key=f"famsup_{subj}")
    internet = st.selectbox(f"Internet Access ({subj})", ["yes", "no"], key=f"internet_{subj}")
    failure_count = st.slider(f"Number of Past Failures ({subj})", 0, 4, 0, key=f"failures_{subj}")
    absences = st.slider(f"Number of Absences ({subj})", 0, 50, 4, key=f"absences_{subj}")

    data = {
        'sex': 1 if gender == 'male' else 0,
        'studytime': study_time,
        'famsup': 1 if fam_sup == 'yes' else 0,
        'internet': 1 if internet == 'yes' else 0,
        'failures': failure_count,
        'absences': absences,
        'health': health
    }

    input_df = pd.DataFrame([data])

    pred = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    subject_results.append((subj, pred, prob))

st.markdown("---")

if st.button("🔍 Predict Overall Result"):
    st.write(f"### Results for student: **{student_name}**")
    total_prob = 0
    st.write("####  Subject-wise Results:")
    for subj, pred, prob in subject_results:
        if pred == 1:
            st.success(f"{subj}:  PASS with confidence {prob*100:.2f}%")
        else:
            st.error(f"{subj}:  FAIL with confidence {(1-prob)*100:.2f}%")
        total_prob += prob

    avg_prob = total_prob / num_subjects

    if avg_prob >= 0.5:
        st.success(f"###  Overall Prediction: PASS with average confidence {avg_prob*100:.2f}%")
    else:
        st.error(f"###  Overall Prediction: FAIL with average confidence {(1-avg_prob)*100:.2f}%")

st.markdown("---")
st.caption("Made by Tanishq Kumar | Supervised ML Project")
