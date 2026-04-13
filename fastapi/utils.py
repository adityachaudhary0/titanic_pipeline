import pandas as pd

def create_age_group(X):
    X = X.copy()
    labels = ['Child','Teenager','Adult','Senior','Old']
    X['age_group'] = pd.cut(
        X['Age'],
        bins=[0,12,18,35,60,80],
        labels=labels
    )
    return X