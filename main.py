import streamlit as st
import random
import re
import nltk
from nltk.corpus import words
from collections import Counter

# NLTK 단어 사전 다운로드 (변동 없음)
try:
    nltk.data.find('corpora/words')
except nltk.downloader.DownloadError:
    nltk.download('words')

english_vocab = [word.lower() for word in words.words() if 4 <= len(word) <= 10 and word.isalpha()]
english_vocab_set = set(english_vocab)

def make_num(digits):
    num_list = [str(random.randint(1, 9))]
    for _ in range(digits - 1):
        num_list.append(str(random.randint(0, 9)))
    return "".join(num_list)

def check(mission, guess):
    length = len(mission)
    result = [''] * length
    correct = 0

    mission_counter = Counter(mission)
    
    for i in range(length):
        if guess[i] == mission[i]:
            result[i] = "맞았어요!"
            correct += 1
            mission_counter[guess[i]] -= 1
            
    for i in range(length):
        if result[i] == '' and guess[i] in mission_counter and mission_counter[guess[i]] > 0:
            result[i] = "다른 자리에 넣어주세요!"
            mission_counter[guess[i]] -= 1
        elif result[i] == '':
            result[i] = "틀렸어요!"
            
    return result, correct

# 초기 세션 상태 설정 (변동 없음)
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = None
if 'mission' not in st.session_state:
    st.session_state.mission = None
if 'attempt' not in st.session_state:
    st.session_state.attempt = 0
if 'guess_history' not in st.session_state:
    st.session_state.guess_history = []
if 'selected_length' not in st.session_state:
    st.session_state.selected_length = None

# 앱 제목 및 설명 (변동 없음)
st.title("🎮 숫자/영어 추측 게임")
st.markdown("정답을 맞힐 때까지 숫자나 영어 단어를 추측해보세요! 각 문자에 대한 피드백을 받습니다.")

# 리셋 버튼 (수정된 부분)
if st.button("🔄 게임 리셋", help="현재 진행 중인 게임을 리셋하고 초기화합니다."):
    st.rerun(clear_session_state=True)
    st.stop() # <-- 이 부분을 추가합니다.
    # st.stop()은 st.rerun()이 호출된 직후 현재 스크립트 실행을 중단하여
    # Streamlit이 재실행을 더 깔끔하게 처리하도록 돕습니다.

# 게임 모드 선택 (변동 없음)
if st.session_state.game_mode is None:
    st.markdown("---")
    st.subheader("게임 모드 선택")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔢 숫자 모드", use_container_width=True):
            st.session_state.game_mode = "숫자"
    with col2:
        if st.button("🔠 영어 모드", use_container_width=True):
            st.session_state.game_mode = "영어"
else:
    st.markdown(f"### 현재 모드: **{st.session_state.game_mode} 추측 게임**")
    
    # 숫자 모드 (변동 없음)
    if st.session_state.game_mode == "숫자":
        if st.session_state.mission is None:
            digits = st.number_input(
                "자릿수를 입력하세요 (2~8)",
                min_value=2,
                max_value=8,
                value=st.session_state.selected_length if st.session_state.selected_length else 3,
                step=1,
                key='digits_input'
            )
            if st.button("게임 시작", key='start_num_game'):
                st.session_state.mission = make_num(digits)
                st.session_state.attempt = 0
                st.session_state.guess_history = []
                st.session_state.selected_length = digits
        
        if st.session_state.mission:
            st.markdown(f"**현재 {st.session_state.selected_length}자릿수 숫자 게임 진행 중입니다.**")
            guess = st.text_input(
                f"{st.session_state.attempt + 1}번째 시도 (예: {'_' * st.session_state.selected_length})",
                key=f'guess_num_{st.session_state.attempt}' 
            )
            if st.button("제출", key='submit_num_guess'):
                if len(guess) == st.session_state.selected_length and guess.isdigit():
                    if st.session_state.mission is None:
                        st.warning("먼저 '게임 시작' 버튼을 눌러주세요.")
                    else:
                        st.session_state.attempt += 1
                        result, correct = check(st.session_state.mission, guess)
                        st.session_state.guess_history.append((guess, result))
                        if correct == st.session_state.selected_length:
                            st.success(f"🎉 정답입니다! **{st.session_state.mission}**! 총 시도 횟수: {st.session_state.attempt}번")
                            st.balloons()
                            st.session_state.mission = None
                        else:
                            st.info("계속 시도해보세요!")
                else:
                    st.warning(f"올바른 {st.session_state.selected_length}자리의 숫자를 입력해주세요.")

    # 영어 모드 (변동 없음)
    elif st.session_state.game_mode == "영어":
        if st.session_state.mission is None:
            word_length = st.number_input(
                "단어 길이를 입력하세요 (4~10)",
                min_value=4,
                max_value=10,
                value=st.session_state.selected_length if st.session_state.selected_length else 5,
                step=1,
                key='word_len_input'
            )
            if st.button("게임 시작", key='start_word_game'):
                filtered_words = [w for w in english_vocab if len(w) == word_length]
                if not filtered_words:
                    st.error(f"⚠️ {word_length}자 길이의 단어를 찾을 수 없습니다. 다른 길이를 선택해주세요.")
                else:
                    st.session_state.mission = random.choice(filtered_words)
                    st.session_state.attempt = 0
                    st.session_state.guess_history = []
                    st.session_state.selected_length = word_length

        if st.session_state.mission:
            st.markdown(f"**현재 {st.session_state.selected_length}자 길이의 영어 단어 게임 진행 중입니다.**")
            guess = st.text_input(
                f"{st.session_state.attempt + 1}번째 시도 (예: {'_' * st.session_state.selected_length})",
                key=f'guess_word_{st.session_state.attempt}' 
            ).lower()

            if st.button("제출", key='submit_word_guess'):
                if len(guess) == st.session_state.selected_length and guess.isalpha():
                    if guess in english_vocab_set:
                        st.session_state.attempt += 1
                        result, correct = check(st.session_state.mission, guess)
                        st.session_state.guess_history.append((guess, result))
                        if correct == st.session_state.selected_length:
                            st.success(f"🎉 정답입니다! **{st.session_state.mission}**! 총 시도 횟수: {st.session_state.attempt}번")
                            st.balloons()
                            st.session_state.mission = None
                        else:
                            st.info("계속 시도해보세요!")
                    else:
                        st.warning("존재하지 않는 단어입니다. 영어 사전에 있는 단어를 입력해주세요.")
                else:
                    st.warning(f"올바른 {st.session_state.selected_length}자 길이의 알파벳 단어를 입력해주세요.")

# 피드백 이모지 매핑 (변동 없음)
color_map = {
    "맞았어요!": "🟩",
    "다른 자리에 넣어주세요!": "🟨",
    "틀렸어요!": "⬜"
}

# 시도 기록 출력 (변동 없음)
if st.session_state.guess_history:
    st.markdown("---")
    st.subheader("📜 이전 시도 기록")
    for idx, (guess, feedback) in enumerate(reversed(st.session_state.guess_history)):
        original_idx = len(st.session_state.guess_history) - 1 - idx
        emoji_summary = "".join([color_map.get(fb, '') for fb in feedback])
        st.markdown(f"**{original_idx + 1}번째 시도: {guess.upper()}** {emoji_summary}")
