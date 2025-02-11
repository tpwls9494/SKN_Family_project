import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
import json
from sklearn.preprocessing import StandardScaler

# 모델과 메트릭스 로드
@st.cache_resource
def load_model_and_metrics():
    model = joblib.load('models/random_forest_model.joblib')
    with open('models/rf_metrics.json', 'r') as f:
        metrics = json.load(f)
    return model, metrics

# 데이터 전처리 함수
def preprocess_input(data):
    scaler = StandardScaler()
    # 실제 데이터의 전처리 로직을 여기에 구현
    return scaler.fit_transform(data)


# 페이지 설정
st.set_page_config(page_title="Random Forest", page_icon="🌲")

# 데이터 로드 (실제로는 캐싱 사용)

# 모델과 메트릭스 로드
model, metrics = load_model_and_metrics()


# 페이지 제목
st.title("Random Forest 모델 분석")

# 성능 지표 표시
st.header("모델 성능")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("정확도", f"{metrics['accuracy']:.4f}")
with col2:
    st.metric("F1 Score", f"{metrics['f1_score']:.4f}")
with col3:
    st.metric("특성 수", len(metrics['feature_names']))

# 특성 중요도 시각화
st.header("특성 중요도")
importance_df = pd.DataFrame({
    'feature': metrics['feature_names'],
    'importance': metrics['feature_importance']
})
importance_df = importance_df.sort_values('importance', ascending=False)

fig = px.bar(
    importance_df,
    x='importance',
    y='feature',
    orientation='h',
    title='Feature Importance'
)
st.plotly_chart(fig)

# 예측 시뮬레이션
st.header("이탈 예측 시뮬레이션")
with st.form("prediction_form"):
    # 예제: 주요 특성들에 대한 입력 필드
    cols = st.columns(2)
    input_data = {}
    
    with cols[0]:
        for feature in metrics['feature_names'][:len(metrics['feature_names'])//2]:
            if 'salary' in feature.lower():
                input_data[feature] = st.number_input(
                    f"{feature}",
                    min_value=0,
                    max_value=10000000
                )
            elif 'age' in feature.lower():
                input_data[feature] = st.number_input(
                    f"{feature}",
                    min_value=15,
                    max_value=100
                )
            else:
                input_data[feature] = st.number_input(
                    f"{feature}",
                    min_value=0,
                    max_value=100
                )
    
    with cols[1]:
        for feature in metrics['feature_names'][len(metrics['feature_names'])//2:]:
            input_data[feature] = st.number_input(
                f"{feature}",
                min_value=0,
                max_value=100
            )
            
    submitted = st.form_submit_button("예측하기")
    if submitted:
        # 입력 데이터를 모델 입력 형식으로 변환
        input_df = pd.DataFrame([input_data])
        
        # 예측 수행
        prediction = model.predict_proba(input_df)[0][1]
        
        # 결과 표시
        st.info(f"이탈 확률: {prediction:.2%}")

# 추가 분석: 이탈 요인 분석
st.header("주요 이탈 요인 분석")
top_features = importance_df.head(5)
st.write("상위 5개 이탈 영향 요인:")
st.dataframe(top_features)

# 모델 설명
st.header("모델 설명")
st.markdown("""
이 Random Forest 모델은 다음과 같은 특징을 가지고 있습니다:
- 전체 데이터 중 80%를 학습에 사용
- 200개의 의사결정 트리로 구성
- 클래스 불균형 문제를 SMOTE로 해결
- 교차 검증을 통한 모델 검증
""")