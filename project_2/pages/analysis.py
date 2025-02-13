import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import StandardScaler

def load_model_and_metrics():
    # 모델 및 메트릭스 로드 로직
    pass

def main():
    st.title("이탈자 상세 분석 📊")
    
    # 분석 섹션 선택
    analysis_type = st.selectbox(
        "분석 유형 선택",
        ["이탈자 프로필", "예측 모델 성능", "특성 중요도", "실시간 예측"]
    )
    
    if analysis_type == "이탈자 프로필":
        st.subheader("📊 이탈자 특성 분석")
        
        # 연령대별 이탈률
        age_data = pd.DataFrame({
            '연령대': ['20대', '30대', '40대', '50대', '60대 이상'],
            '이탈률': [0.15, 0.22, 0.18, 0.12, 0.08]
        })
        fig_age = px.bar(age_data, x='연령대', y='이탈률',
                        title='연령대별 이탈률')
        st.plotly_chart(fig_age)
        
        # 사용 기간별 이탈률
        usage_data = pd.DataFrame({
            '사용기간': ['1년 미만', '1-2년', '2-3년', '3년 이상'],
            '이탈률': [0.25, 0.18, 0.15, 0.12]
        })
        fig_usage = px.line(usage_data, x='사용기간', y='이탈률',
                          title='사용 기간별 이탈률')
        st.plotly_chart(fig_usage)
    
    elif analysis_type == "예측 모델 성능":
        st.subheader("🎯 모델 성능 지표")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("정확도", "85.2%")
        with col2:
            st.metric("정밀도", "78.9%")
        with col3:
            st.metric("재현율", "76.5%")
    
    elif analysis_type == "특성 중요도":
        st.subheader("🔍 주요 영향 요인")
        
        feature_importance = pd.DataFrame({
            '특성': ['가격부담', '앱사용량', '통신품질', '결제패턴', '연령'],
            '중요도': [0.35, 0.25, 0.20, 0.12, 0.08]
        })
        fig_importance = px.bar(feature_importance,
                              x='중요도',
                              y='특성',
                              orientation='h',
                              title='특성 중요도')
        st.plotly_chart(fig_importance)
    
    else:  # 실시간 예측
        st.subheader("🔮 이탈 가능성 예측")
        
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("연령", 20, 80, 30)
                price = st.number_input("기기 가격(만원)", 0, 200, 100)
                usage = st.slider("앱 사용량(시간/일)", 0, 12, 4)
            
            with col2:
                payment = st.number_input("월평균 결제액(만원)", 0, 100, 30)
                satisfaction = st.slider("서비스 만족도", 1, 5, 3)
            
            submit = st.form_submit_button("예측하기")
            
            if submit:
                # 예시 예측 결과
                churn_prob = 0.35
                st.metric("이탈 가능성", f"{churn_prob:.1%}")
                
                if churn_prob > 0.5:
                    st.warning("⚠️ 높은 이탈 위험이 감지되었습니다.")
                else:
                    st.success("✅ 안정적인 사용자로 예측됩니다.")

if __name__ == "__main__":
    main()