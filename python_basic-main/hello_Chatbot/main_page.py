import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Chatbot Demo",
    page_icon="🤖"
)

data = pd.DataFrame({
    "단어": ["you", "if", "why", "how", "is"],
    "선택횟수":[2024, 800, 3000, 420, 1000],
    "하나만 사용하는 경우": [800, 100, 4000, 2000, 300]
})


# 생성 페이지 내용
st.title("간단한 챗봇 구현하기")

# 제일 위 페이지를 보여준다.
st.subheader("제일 많이 물어보는 질문")
if st.button("클릭 시 통계로 나옴"):    
    st.dataframe(data, use_container_width=True)

    st.bar_chart(data.set_index('단어')['선택횟수'])
    st.line_chart(data.set_index('단어')['하나만 사용하는 경우'])
    fig = data.plot.pie(
        y="선택횟수",
        labels=data["단어"],  # 차트가 그려줄 이름
        autopct="%1.1f%%",      # 소숫점 첫 째 자리까지 
        figsize=(4,4),          # 사이즈
        legend=False,           # 범례 표시
        title="추천 단어어" # 제목
    ).get_figure()
    st.pyplot(fig)



if st.button('접속하기'):
     st.switch_page("pages/chatbot_page.py")

