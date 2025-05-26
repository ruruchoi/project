import streamlit as st
from random import randint

attempt = 1

st.title('쉽게 즐기는 추론 게임')

game_mode = st.selectbox("게임 유형을 선택하세요", ["숫자","알파벳"])

if st.button('다음'):
  if game_mode == '숫자':
    num_digits = st.number_input("원하는 자릿수를 입력하세요", min_value=1, max_value=5, step=1)
    min_num = 10**(num_digits-1)
    max_num = int('9'*num_digits)
    num = randint(min_num, max_num)
    st.markdown(f"숫자는 {min_num}~{max_num}사이에 있습니다.")
    while True:
      num_input = st.number_input(f"{attempt}번째 시도", min_value = min_num, max_value = max_num, step=1)
      attempt += 1
