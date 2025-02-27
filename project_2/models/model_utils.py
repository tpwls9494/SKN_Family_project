import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import plotly.express as px

def train_random_forest(X, y):
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=7,
        random_state=42
    )
    model.fit(X, y)
    return model

def train_xgboost(X, y):
    model = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        random_state=42
    )
    model.fit(X, y)
    return model

def plot_feature_importance(model=None, features=None):
    # 임시 데이터로 예시 플롯
    if model is None:
        importance_df = pd.DataFrame({
            'feature': ['feature1', 'feature2', 'feature3'],
            'importance': [0.4, 0.3, 0.3]
        })
    else:
        importance_df = pd.DataFrame({
            'feature': features,
            'importance': model.feature_importances_
        })
    
    fig = px.bar(
        importance_df,
        x='importance',
        y='feature',
        orientation='h',
        title='Feature Importance'
    )
    return fig