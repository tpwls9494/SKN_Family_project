import streamlit as st
import pandas as pd
import numpy as np

def main():
    st.set_page_config(
        page_title="휴대폰 브랜드 이탈 예측",
        page_icon="📱",
        layout="wide"
    )
    
    st.title("갤탈출 연구소")
    
    st.markdown("""
    ### 📊 프로젝트 개요
    이 웹 애플리케이션은 다양한 머신러닝 모델을 사용하여 휴대폰 브랜드 이탈을 예측하고 분석합니다.
    
    ### 🔍 제공되는 모델:
    - Random Forest
    - XGBoost
    - Deep Learning
    - Stacking Ensemble
    
    ### 📈 각 모델별 제공 기능:
    - 모델 성능 지표
    - 특성 중요도 시각화
    - 예측 결과 분석
    - 실시간 예측
    """)
    
    # 데이터 로드
    @st.cache_data
    def load_data():
        return pd.read_csv('data/phone_information.csv')
    
    data = load_data()
    
    # 데이터 개요 보여주기
    st.subheader("데이터셋 미리보기")
    st.dataframe(data.head())
    
    # 기본 통계 정보
    st.subheader("데이터 기본 통계")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"총 데이터 수: {len(data)}")
        st.info(f"특성 수: {len(data.columns)}")
    
    # 이탈률 분포
    with col2:
        st.subheader("연도별 이탈률")
        churn_22 = (data['brand_22'] != 1).mean()
        churn_23 = (data['brand_23'] != 1).mean()
        st.metric("2022년 이탈률", f"{churn_22:.2%}")
        st.metric("2023년 이탈률", f"{churn_23:.2%}")

if __name__ == "__main__":
    main()