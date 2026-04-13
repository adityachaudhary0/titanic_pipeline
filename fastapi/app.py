from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional,Literal,Annotated
import pandas as pd
import pickle
from utils import create_age_group
#import ml model
with open('svm_model.pkl','rb') as f:
    model=pickle.load(f)
app=FastAPI()
class InputData(BaseModel):
    Pclass:Annotated[int,Field(...,description="The class of the passenger")]
    Sex:Annotated[Literal["male","female"],Field(description="The sex of the passenger")]
    Age:Annotated[int,Field(gt=0,lt=100,description="The age of the passenger")]
    SibSp:Annotated[int,Field(description="The number of siblings/spouses aboard")]
    Parch:Annotated[int,Field(description="The number of parents/children aboard")]
    Fare:Annotated[float,Field(...,description="The fare of the passenger")]
    Embarked:Annotated[Literal["S","C","Q"],Field(description="The port of embarkation of the passenger S:Southampton,C:Cherbourg,Q:Queenstown")]

@app.get("/")
def home():
    return {"message": "Titanic API is running 🚀"}
@app.post("/predict")
def predict(data:InputData):
    try:
        input_df=pd.DataFrame([
            {
                "Pclass":data.Pclass,
                "Sex":data.Sex,
                "Age":data.Age,
                "SibSp":data.SibSp,
                "Parch":data.Parch,
                "Fare":data.Fare,
                "Embarked":data.Embarked
            }
        ])
        prediction=int(model.predict(input_df)[0])
        return JSONResponse(content={"prediction":prediction},status_code=200)
    except Exception as e:
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"},
            status_code=500
        )
