import streamlit as st
import requests

API_DEFAULT = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Titanic Survival Predictor",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
  .block-container { padding-top: 2.2rem; padding-bottom: 2.2rem; }
  [data-testid="stMetricValue"] { font-size: 2rem; }
  .muted { opacity: 0.75; }
  .card {
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px 18px 10px 18px;
    background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
  }
  .pill {
    display: inline-block;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.12);
    font-size: 0.85rem;
  }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="card">
  <div style="display:flex; align-items:baseline; justify-content:space-between; gap:12px;">
    <div>
      <h2 style="margin:0;">🚢 Titanic Survival Predictor</h2>
      <div class="muted">Enter passenger details and get an instant survival prediction from your API.</div>
    </div>
    <div class="pill">FastAPI • Streamlit</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.subheader("Settings")
    api_url = st.text_input("Prediction API URL", value=API_DEFAULT, help="Your FastAPI endpoint.")
    timeout_s = st.slider("Request timeout (seconds)", 1, 30, 8)
    st.divider()
    st.caption("Tips")
    st.caption("- Run API first: `uvicorn main:app --reload`")
    st.caption("- Endpoint should accept JSON and return `{prediction: 0/1}`")

left, right = st.columns([1.1, 0.9], gap="large")

with left:
    st.subheader("Passenger information")
    with st.form("predict_form", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            Pclass = st.selectbox("Passenger Class", [1, 2, 3], index=2)
            Embarked = st.selectbox("Embarked", ["S", "C", "Q"])
        with c2:
            Sex = st.selectbox("Sex", ["male", "female"])
            Age = st.slider("Age", 0, 80, 28)
        with c3:
            Fare = st.number_input("Fare", min_value=0.0, max_value=600.0, value=32.2, step=0.1)
        c4, c5 = st.columns(2)
        with c4:
            SibSp = st.number_input("Siblings/Spouses (SibSp)", min_value=0, max_value=10, value=0, step=1)
        with c5:
            Parch = st.number_input("Parents/Children (Parch)", min_value=0, max_value=10, value=0, step=1)

        st.divider()
        submitted = st.form_submit_button("Predict survival", use_container_width=True)

with right:
    st.subheader("Result")
    result_placeholder = st.empty()
    details_placeholder = st.empty()

def _safe_float(x):
    try:
        return float(x)
    except Exception:
        return None

if submitted:

    data = {
        "Pclass": Pclass,
        "Sex": Sex,
        "Age": Age,
        "SibSp": SibSp,
        "Parch": Parch,
        "Fare": Fare,
        "Embarked": Embarked
    }

    try:
        with st.spinner("Contacting API and running prediction..."):
            response = requests.post(api_url, json=data, timeout=timeout_s)

        if response.status_code >= 400:
            try:
                err = response.json()
            except Exception:
                err = {"error": response.text.strip() or f"HTTP {response.status_code}"}
            raise RuntimeError(err.get("error") or f"HTTP {response.status_code}")

        result = response.json() if response.content else {}

        prediction = result.get("prediction", None)
        proba = result.get("probability", result.get("proba", result.get("survival_probability", None)))
        proba = _safe_float(proba)

        if prediction in (0, 1):
            if prediction == 1:
                result_placeholder.success("🎉 Predicted: **Survived**")
            else:
                result_placeholder.error("❌ Predicted: **Did Not Survive**")

            cols = st.columns(2)
            cols[0].metric("Prediction", "Survived" if prediction == 1 else "Not survived")
            if proba is not None:
                cols[1].metric("Survival probability", f"{proba*100:.1f}%" if proba <= 1 else f"{proba:.2f}")
            else:
                cols[1].metric("Survival probability", "—")

            with details_placeholder.container():
                st.caption("Sent payload")
                st.json(data, expanded=False)
                st.caption("Raw response")
                st.json(result, expanded=False)
        else:
            raise RuntimeError(result.get("error") or "Unexpected API response (missing `prediction`).")

    except Exception as e:
        result_placeholder.warning("Could not get a prediction.")
        st.error(f"Error: {e}")