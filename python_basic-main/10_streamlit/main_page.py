import streamlit as st

# 생성 페이지 내용
st.title("간단한 챗봇 구현하기")

# 제일 위 페이지를 보여준다.
st.header("오늘은 Streamlit 배우는 날!")

# header 밑으로 페이지를 보여준다.
st.subheader("Streamlit으로 만들어보자!")

my_site = st.text_input('무엇이든 물어보고 싶은 것을 물어봐!')
st.write(my_site)

if st.button(f'{my_site} 접속하기'):
    st.success(f"{my_site}로 접속 중⭐⭐⭐", icon="✅")

st.title('실습 페이지')