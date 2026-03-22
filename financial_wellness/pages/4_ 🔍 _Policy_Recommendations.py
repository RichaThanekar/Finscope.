import streamlit as st
import pandas as pd
import re
import markdown

from search_serp import get_policy_recommendations_from_serpapi
from utils import build_prompt_with_search
from gemini_llm import query_gemini
from risk_assesment import calculate_risk_score

# Load dataset
df = pd.read_csv("data/data_synthetic.csv")

# Page setup
st.set_page_config(page_title="Policy Recommendation", layout="wide")

# Sidebar – Personal Information
st.sidebar.header("Personal Details")

age = st.sidebar.slider("Age", 18, 80)
gender = st.sidebar.selectbox("Gender", df["Gender"].dropna().unique())
marital_status = st.sidebar.selectbox("Marital Status", df["Marital Status"].dropna().unique())
occupation = st.sidebar.selectbox("Occupation", df["Occupation"].dropna().unique())
income = st.sidebar.number_input("Annual Income (₹)", min_value=10000, step=1000)
education = st.sidebar.selectbox("Education Level", df["Education Level"].dropna().unique())
location = st.sidebar.selectbox("Geographic Information", df["Geographic Information"].dropna().unique())
smoker = st.sidebar.radio("Do you smoke?", ["Yes", "No"])
driving_record = st.sidebar.selectbox("Driving Record", df["Driving Record"].dropna().unique())
policy_type = st.sidebar.selectbox("Insurance Type", [
    "Term Life Insurance",
    "Health Insurance",
    "Family Floater Plan",
    "Critical Illness Cover",
    "Group Health Insurance",
    "Group Life Insurance",
    "Personal Accident Insurance"
])
disease = st.sidebar.selectbox("Pre-existing Condition", ["None", "Diabetes", "Hypertension", "Asthma", "Heart Disease", "Cancer", "Thyroid", "Obesity", "Other"])
dependents = st.sidebar.slider("Number of Dependents", 0, 10, 0)

# Main Dashboard
st.title("📊 Policy Recommendations")

# Risk Score Calculation
risk_score = calculate_risk_score(age, income, driving_record, smoker, disease, dependents)

user_profile = {
    "Age": age,
    "Gender": gender,
    "Marital Status": marital_status,
    "Occupation": occupation,
    "Income Level": income,
    "Education Level": education,
    "Geographic Information": location,
    "Insurance Type": policy_type,
    "Smoker": smoker,
    "Driving Record": driving_record,
    "Pre-existing Condition": disease,
    "Dependents": dependents,
    "Risk Category": risk_score
}

st.markdown(f"### 🧾 Risk Category: **{risk_score}**")

if st.button("Generate Recommendations"):
    with st.spinner("Fetching policies..."):
        search_results = get_policy_recommendations_from_serpapi(user_profile)

    if not search_results:
        st.error("❌ No recommendations found.")
    else:
        prompt = build_prompt_with_search(user_profile, search_results)
        with st.spinner("Generating insights..."):
            try:
                recommendation = query_gemini(prompt)
                st.success("✅ Recommendations generated!")
                st.markdown(recommendation)
            except Exception as e:
                st.error(f"Error: {e}")

# import streamlit as st
# import pandas as pd
# import re
# import markdown

# from search_serp import get_policy_recommendations_from_serpapi
# from utils import build_prompt_with_search
# from gemini_llm import query_gemini
# from risk_assesment import calculate_risk_score

# # Load dataset
# df = pd.read_csv("data/data_synthetic.csv")

# # Page setup
# st.set_page_config(page_title="Policy Recommendation", layout="wide")

# # Sidebar – Personal Information
# st.sidebar.header("Personal Details")

# age = st.sidebar.slider("Age", 18, 80)
# gender = st.sidebar.selectbox("Gender", df["Gender"].dropna().unique())
# marital_status = st.sidebar.selectbox("Marital Status", df["Marital Status"].dropna().unique())
# occupation = st.sidebar.selectbox("Occupation", df["Occupation"].dropna().unique())
# income = st.sidebar.number_input("Annual Income (₹)", min_value=10000, step=1000)
# education = st.sidebar.selectbox("Education Level", df["Education Level"].dropna().unique())
# location = st.sidebar.selectbox("Geographic Information", df["Geographic Information"].dropna().unique())
# smoker = st.sidebar.radio("Do you smoke?", ["Yes", "No"])
# driving_record = st.sidebar.selectbox("Driving Record", df["Driving Record"].dropna().unique())
# policy_type = st.sidebar.selectbox("Insurance Type", [
#     "Term Life Insurance",
#     "Health Insurance",
#     "Family Floater Plan",
#     "Critical Illness Cover",
#     "Group Health Insurance",
#     "Group Life Insurance",
#     "Personal Accident Insurance"
# ])
# disease = st.sidebar.selectbox("Pre-existing Condition", ["None", "Diabetes", "Hypertension", "Asthma", "Heart Disease", "Cancer", "Thyroid", "Obesity", "Other"])

# # Main Dashboard
# st.title("📊 Policy Recommendations")

# # Risk Score Calculation
# risk_score = calculate_risk_score(age, income, driving_record, smoker)

# user_profile = {
#     "Age": age,
#     "Gender": gender,
#     "Marital Status": marital_status,
#     "Occupation": occupation,
#     "Income Level": income,
#     "Education Level": education,
#     "Geographic Information": location,
#     "Insurance Type": policy_type,
#     "Smoker": smoker,
#     "Driving Record": driving_record,
#     "Risk Score": risk_score,
#     "Family Members": "N/A",
#     "Pre-existing Condition": disease,
# }

# # Show summary cards


# # Recommendation Section
# # st.markdown("---")
# # st.markdown("### 🔍 Policy Recommendations")

# if st.button("Generate Recommendations"):
#     with st.spinner("Fetching policies..."):
#         search_results = get_policy_recommendations_from_serpapi(user_profile)

#     if not search_results:
#         st.error("❌ No recommendations found.")
#     else:
#         prompt = build_prompt_with_search(user_profile, search_results)
#         with st.spinner("Generating insights..."):
#             try:
#                 recommendation = query_gemini(prompt)
#                 st.success("✅ Recommendations generated!")
#                 st.markdown(recommendation)
#             except Exception as e:
#                 st.error(f"Error: {e}")
