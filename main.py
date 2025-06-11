import streamlit as st
import random
import re
import nltk
from nltk.corpus import words
from collections import Counter
from docx import Document

# NLTK 단어 사전 다운로드
nltk.download('words')
english_vocab = set(words.words())

# 숫자 미션 생성 함수
def make_num(digits):
    num = str(random.randint(1, 9))
    for _ in range(digits - 1):
        num += str(random.randint(0, 9))
    return num

# .docx 파일에서 단어 리스트 추출
@st.cache_data
def load_words_from_docx(file_path):
    doc = Document(file_path)
    word_list = []
    for para in doc.paragraphs:
        match = re.match(r'\d+\s+([a-zA-Z\(\)]+)', para.text)
        if match:
            word = match.group(1).split('(')[0].lower()
            word_list.append(word)
    return word_list

# 정답과 입력 비교
def check(mission, guess):
    length = len(mission)
    result = [''] * length
    correct = 0
    mission_counter = Counter(mission)
    used_in_mission = [False] * length
    used_in_guess = [False] * length

    # 스트라이크
    for i in range(length):
        if guess[i] == mission[i]:
            result[i] = "맞았어요!"
            correct += 1
            mission_counter[guess[i]] -= 1
            used_in_mission[i] = True
            used_in_guess[i] = True

    # 볼
    for i in range(length):
        if not used_in_guess[i]:
            if guess[i] in mission_counter and mission_counter[guess[i]] > 0:
                result[i] = "다른 자리에 넣어주세요!"
                mission_counter[guess[i]] -= 1
            else:
                result[i] = "틀렸어요!"
    return result, correct

# 초기 세션 상태
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = None
if 'mission' not in st.session_state:
    st.session_state.mission = None
if 'attempt' not in st.session_state:
    st.session_state.attempt = 0
if 'guess_history' not in st.session_state:
    st.session_state.guess_history = []

# 앱 제목
st.title("🎮 숫자/영어 추측 게임")

# 리셋 버튼 (언제나 노출)
if st.button("🔄 게임 리셋", key="reset_button"):
    st.session_state.game_mode = None
    st.session_state.mission = None
    st.session_state.attempt = 0
    st.session_state.guess_history = []
    st.experimental_rerun()

# 게임 모드 선택
if st.session_state.game_mode is None:
    st.session_state.game_mode = st.selectbox("게임 모드를 선택하세요", ["숫자", "영어"])

# 숫자 모드
if st.session_state.game_mode == "숫자":
    digits = st.number_input("자릿수를 입력하세요", min_value=2, max_value=8, step=1)
    if st.button("게임 시작") and st.session_state.mission is None:
        st.session_state.mission = make_num(digits)
        st.session_state.attempt = 0
        st.session_state.guess_history = []

    if st.session_state.mission:
        guess = st.text_input(
            f"{st.session_state.attempt + 1}번째 시도 (예: {'_' * digits})", key='guess_num'
        )
        if st.button("제출"):
            if len(guess) == digits and guess.isdigit():
                st.session_state.attempt += 1
                result, correct = check(st.session_state.mission, guess)
                st.session_state.guess_history.append((guess, result))
                if correct == digits:
                    st.success(f"🎉 정답입니다! 총 시도 횟수: {st.session_state.attempt}번")
                    st.balloons()
            else:
                st.warning("올바른 숫자를 입력해주세요.")

# 영어 모드
elif st.session_state.game_mode == "영어":
    try:
        word_list = load_words_from_docx("/mnt/data/english_word.docx")
    except Exception as e:
        st.error("⚠️ 단어 파일을 불러올 수 없습니다. 파일 경로 또는 형식을 확인해주세요.")
        st.stop()

    if st.button("게임 시작") and st.session_state.mission is None:
        st.session_state.mission = random.choice(word_list)
        st.session_state.attempt = 0
        st.session_state.guess_history = []

    if st.session_state.mission:
        word_len = len(st.session_state.mission)
        guess = st.text_input(
            f"{st.session_state.attempt + 1}번째 시도 (예: {'_' * word_len})", key='guess_word'
        )
        if st.button("제출"):
            if len(guess) == word_len and guess.isalpha():
                if guess.lower() in english_vocab:
                    st.session_state.attempt += 1
                    result, correct = check(st.session_state.mission, guess.lower())
                    st.session_state.guess_history.append((guess.lower(), result))
                    if correct == word_len:
                        st.success(f"🎉 정답입니다! 총 시도 횟수: {st.session_state.attempt}번")
                        st.balloons()
                else:
                    st.warning("존재하지 않는 단어입니다.")
            else:
                st.warning("올바른 알파벳 단어를 입력해주세요.")

# 피드백 이모지 매핑
color_map = {
    "맞았어요!": "🟩",
    "다른 자리에 넣어주세요!": "🟨",
    "틀렸어요!": "⬜"
}

# 시도 기록 출력
if st.session_state.guess_history:
    st.subheader("📜 이전 시도 기록")
    for idx, (guess, feedback) in enumerate(st.session_state.guess_history):
        st.markdown(f"**{idx + 1}번째 시도: {guess}**")
        for i, fb in enumerate(feedback):
            st.write(f"{i + 1}번째 문자: {color_map.get(fb, '')} {fb}")
