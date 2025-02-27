import streamlit as st
import pandas as pd

st.title('게임 캐릭터의 인지도')

data = pd.DataFrame({
    "캐릭터": ["전사", "법사", "힐러", "탱커", "궁수"],
    "선택횟수":[120, 95, 150, 80, 111],
    "승률 (%)": [52, 48, 56, 60, 49],
    "인지도 (%)": [25, 20, 30, 15, 22]
})

st.dataframe(data, use_container_width=True)

# edited_data = st.data_editor(data)
# st.data_editor(edited_data)

st.bar_chart(data.set_index('캐릭터')['선택횟수'])
st.line_chart(data.set_index('캐릭터')['승률 (%)'])
fig = data.plot.pie(
    y="인지도 (%)",
    labels=data["캐릭터"],  # 차트가 그려줄 이름
    autopct="%1.1f%%",      # 소숫점 첫 째 자리까지 
    figsize=(6,6),          # 사이즈
    legend=False,           # 범례 표시
    title="캐릭터 별 인지도" # 제목목
).get_figure()
st.pyplot(fig)
