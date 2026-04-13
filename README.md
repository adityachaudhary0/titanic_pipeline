# 🚢 Titanic Survival Prediction (End-to-End ML Project)

This project predicts whether a passenger survived the Titanic disaster using a **Machine Learning pipeline (SVM)**.
It is built as a **complete end-to-end application** with:

* 🧠 Machine Learning Model
* ⚙️ FastAPI Backend
* 🎨 Streamlit Frontend

---

## 🌍 Project Architecture

```
User → Streamlit UI → FastAPI API → ML Pipeline → Prediction
```

---

## 📁 Project Structure

```
titanic_pipeline/
 ├── ml/              # Training code, notebooks
 ├── fastapi/         # Backend API
 │    ├── app.py
 │    ├── utils.py
 │    ├── svm_model.pkl
 │    ├── requirements.txt
 │    ├── Procfile
 │
 ├── frontend/        # Streamlit UI
 │    ├── frontend.py
 │    ├── requirements.txt
 │
 ├── README.md
```

---

## 🧠 Machine Learning Details

* **Model**: Support Vector Machine (SVM)
* **Accuracy**: ~82%
* **Technique Used**:

  * Feature Engineering (`age_group`)
  * ColumnTransformer
  * Pipeline (end-to-end preprocessing + model)
  * OneHotEncoding
  * StandardScaler
  * Hyperparameter tuning (GridSearchCV)
  * Threshold tuning

---

## ⚙️ Backend (FastAPI)

* Built REST API using FastAPI
* Endpoint:

  * `POST /predict`
* Handles:

  * Input validation using Pydantic
  * Data preprocessing (via pipeline)
  * Model prediction

---

## 🎨 Frontend (Streamlit)

* User-friendly UI for input
* Sends request to FastAPI
* Displays prediction instantly

---

## 🚀 How to Run Locally

### 1️⃣ Start FastAPI

```bash
cd fastapi
uvicorn app:app --reload
```

👉 Open:

```
http://127.0.0.1:8000/docs
```

---

### 2️⃣ Start Frontend

```bash
cd frontend
streamlit run frontend.py
```

---

## 🧪 Example Input

```json
{
  "Pclass": 3,
  "Sex": "male",
  "Age": 25,
  "SibSp": 0,
  "Parch": 0,
  "Fare": 7.25,
  "Embarked": "S"
}
```

---

## 📚 What I Learned

This project helped me practice:

* ✅ Machine Learning pipeline design
* ✅ Feature engineering
* ✅ Model evaluation (Precision, Recall, F1)
* ✅ Hyperparameter tuning (GridSearchCV)
* ✅ Threshold tuning
* ✅ FastAPI backend development
* ✅ API design and testing
* ✅ Streamlit frontend development
* ✅ Connecting frontend with backend
* ✅ Debugging real-world issues:

  * Pickle errors
  * Version mismatch
  * Custom transformer issues
* ✅ Git & GitHub workflow

---

## 🌟 Future Improvements

* Add prediction probability
* Improve UI design
* Deploy using Render & Streamlit Cloud
* Add logging and monitoring

---

## 👨‍💻 Author

Aditya Chaudhary
B.Tech Student | Machine Learning Enthusiast
