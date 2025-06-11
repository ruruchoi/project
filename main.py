import streamlit as st
import random
import re
import nltk
from nltk.corpus import words
from collections import Counter

# NLTK 단어 사전 다운로드
try:
    nltk.data.find('corpora/words')
except nltk.downloader.DownloadError:
    nltk.download('words')

# 영어 단어 사전 로드 (NLTK 사용)
# 4자 이상 10자 이하의 알파벳 단어만 필터링합니다.
english_vocab = [word.lower() for word in words.words() if 4 <= len(word) <= 10 and word.isalpha()]
english_vocab_set = set(english_vocab) # 빠른 검색을 위해 set으로 변환

# 숫자 미션 생성 함수
def make_num(digits):
    # 지정된 자릿수의 고유한 숫자를 생성합니다. (예: 3자릿수 -> '123' 또는 '580')
    # 첫 자리는 0이 될 수 없도록 1-9 사이에서 선택하고, 나머지는 0-9 사이에서 선택합니다.
    num_list = [str(random.randint(1, 9))]
    for _ in range(digits - 1):
        num_list.append(str(random.randint(0, 9)))
    return "".join(num_list)

# 정답과 입력 비교 함수
def check(mission, guess):
    # 주어진 미션(정답)과 추측을 비교하여 각 문자의 상태를 반환합니다.
    # - '맞았어요!': 문자와 위치 모두 일치 (스트라이크)
    # - '다른 자리에 넣어주세요!': 문자는 일치하지만 위치는 다름 (볼)
    # - '틀렸어요!': 문자가 미션에 없음
    length = len(mission)
    result = [''] * length # 각 문자에 대한 피드백을 저장할 리스트
    correct = 0 # '맞았어요!' 개수

    mission_counter = Counter(mission) # 미션 단어의 각 문자 개수를 셉니다.
    
    # 1단계: 스트라이크 (문자와 위치 모두 일치) 처리
    for i in range(length):
        if guess[i] == mission[i]:
            result[i] = "맞았어요!"
            correct += 1
            mission_counter[guess[i]] -= 1 # 스트라이크로 처리된 문자는 카운터에서 제외

    # 2단계: 볼 (문자는 일치하지만 위치는 다름) 처리
    for i in range(length):
        # 아직 피드백이 없는 문자이고, 미션에 해당 문자가 남아있다면 '다른 자리에 넣어주세요!'
        if result[i] == '' and guess[i] in mission_counter and mission_counter[guess[i]] > 0:
            result[i] = "다른 자리에 넣어주세요!"
            mission_counter[guess[i]] -= 1 # 볼로 처리된 문자는 카운터에서 제외
        # 아직 피드백이 없으면 '틀렸어요!'
        elif result[i] == '':
            result[i] = "틀렸어요!"
            
    return result, correct

# 초기 세션 상태 설정
# 게임 시작 시 또는 리셋 시 초기화됩니다.
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = None # 현재 게임 모드 (숫자/영어)
if 'mission' not in st.session_state:
    st.session_state.mission = None # 현재 맞혀야 할 정답
if 'attempt' not in st.session_state:
    st.session_state.attempt = 0 # 시도 횟수
if 'guess_history' not in st.session_state:
    st.session_state.guess_history = [] # 이전 추측 기록
if 'selected_length' not in st.session_state:
    st.session_state.selected_length = None # 선택된 숫자 자릿수 또는 단어 길이

# 앱 제목 및 설명
st.title("🎮 숫자/영어 추측 게임")
st.markdown("정답을 맞힐 때까지 숫자나 영어 단어를 추측해보세요! 각 문자에 대한 피드백을 받습니다.")

# 리셋 버튼 (언제나 노출)
# 이 버튼은 항상 `st.rerun()`을 호출하여 앱을 완전히 초기화합니다.
if st.button("🔄 게임 리셋", help="현재 진행 중인 게임을 리셋하고 초기화합니다."):
    st.session_state.game_mode = None
    st.session_state.mission = None
    st.session_state.attempt = 0
    st.session_state.guess_history = []
    st.session_state.selected_length = None
    st.rerun() # 게임 상태를 완전히 초기화하기 위해 명시적으로 재실행

# 게임 모드 선택
if st.session_state.game_mode is None:
    st.markdown("---")
    st.subheader("게임 모드 선택")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔢 숫자 모드", use_container_width=True):
            st.session_state.game_mode = "숫자"
            # st.rerun() # 여기서는 제거합니다. Streamlit이 상태 변경을 감지하고 자동으로 재실행합니다.
    with col2:
        if st.button("🔠 영어 모드", use_container_width=True):
            st.session_state.game_mode = "영어"
            # st.rerun() # 여기서는 제거합니다. Streamlit이 상태 변경을 감지하고 자동으로 재실행합니다.
else:
    st.markdown(f"### 현재 모드: **{st.session_state.game_mode} 추측 게임**")
    
    # 숫자 모드
    if st.session_state.game_mode == "숫자":
        if st.session_state.mission is None: # 아직 미션이 설정되지 않았다면
            digits = st.number_input(
                "자릿수를 입력하세요 (2~8)",
                min_value=2,
                max_value=8,
                value=st.session_state.selected_length if st.session_state.selected_length else 3, # 이전 선택 값 유지
                step=1,
                key='digits_input'
            )
            if st.button("게임 시작", key='start_num_game'):
                st.session_state.mission = make_num(digits)
                st.session_state.attempt = 0
                st.session_state.guess_history = []
                st.session_state.selected_length = digits
                # st.rerun() # 여기서는 제거합니다. Streamlit이 상태 변경을 감지하고 자동으로 재실행합니다.
        
        if st.session_state.mission: # 미션이 설정되었다면 게임 진행
            st.markdown(f"**현재 {st.session_state.selected_length}자릿수 숫자 게임 진행 중입니다.**")
            # 추측 입력 필드, 시도 횟수에 따라 고유한 키를 부여하여 입력값 초기화
            guess = st.text_input(
                f"{st.session_state.attempt + 1}번째 시도 (예: {'_' * st.session_state.selected_length})",
                key=f'guess_num_{st.session_state.attempt}' 
            )
            if st.button("제출", key='submit_num_guess'):
                # 입력 유효성 검사 (길이와 숫자 여부)
                if len(guess) == st.session_state.selected_length and guess.isdigit():
                    if st.session_state.mission is None:
                        st.warning("먼저 '게임 시작' 버튼을 눌러주세요.")
                    else:
                        st.session_state.attempt += 1 # 시도 횟수 증가
                        result, correct = check(st.session_state.mission, guess) # 정답 확인
                        st.session_state.guess_history.append((guess, result)) # 기록에 추가
                        if correct == st.session_state.selected_length:
                            st.success(f"🎉 정답입니다! **{st.session_state.mission}**! 총 시도 횟수: {st.session_state.attempt}번")
                            st.balloons() # 정답 시 풍선 효과
                            st.session_state.mission = None # 미션 초기화 (새 게임 시작 준비)
                        else:
                            st.info("계속 시도해보세요!")
                        # st.rerun() # 여기서는 제거합니다. Streamlit이 상태 변경을 감지하고 자동으로 재실행합니다.
                else:
                    st.warning(f"올바른 {st.session_state.selected_length}자리의 숫자를 입력해주세요.")

    # 영어 모드
    elif st.session_state.game_mode == "영어":
        if st.session_state.mission is None: # 아직 미션이 설정되지 않았다면
            word_length = st.number_input(
                "단어 길이를 입력하세요 (4~10)",
                min_value=4,
                max_value=10,
                value=st.session_state.selected_length if st.session_state.selected_length else 5, # 이전 선택 값 유지
                step=1,
                key='word_len_input'
            )
            if st.button("게임 시작", key='start_word_game'):
                filtered_words = [w for w in english_vocab if len(w) == word_length]
                if not filtered_words: # 해당 길이의 단어가 없으면 오류 메시지
                    st.error(f"⚠️ {word_length}자 길이의 단어를 찾을 수 없습니다. 다른 길이를 선택해주세요.")
                    # 이 경우, `st.rerun()`을 넣지 않으면 오류 메시지가 사라지지 않고 유지됩니다.
                    # 사용자에게 다음 행동을 유도하는 방식으로는 이 편이 더 자연스러울 수 있습니다.
                else:
                    st.session_state.mission = random.choice(filtered_words) # 무작위 단어 선택
                    st.session_state.attempt = 0
                    st.session_state.guess_history = []
                    st.session_state.selected_length = word_length
                    # st.rerun() # 여기서는 제거합니다. Streamlit이 상태 변경을 감지하고 자동으로 재실행합니다.

        if st.session_state.mission: # 미션이 설정되었다면 게임 진행
            st.markdown(f"**현재 {st.session_state.selected_length}자 길이의 영어 단어 게임 진행 중입니다.**")
            # 추측 입력 필드, 시도 횟수에 따라 고유한 키를 부여하여 입력값 초기화
            guess = st.text_input(
                f"{st.session_state.attempt + 1}번째 시도 (예: {'_' * st.session_state.selected_length})",
                key=f'guess_word_{st.session_state.attempt}' 
            ).lower() # 입력 단어는 소문자로 변환

            if st.button("제출", key='submit_word_guess'):
                # 입력 유효성 검사 (길이와 알파벳 여부)
                if len(guess) == st.session_state.selected_length and guess.isalpha():
                    if guess in english_vocab_set: # 영어 사전에 있는 단어인지 확인
                        st.session_state.attempt += 1 # 시도 횟수 증가
                        result, correct = check(st.session_state.mission, guess) # 정답 확인
                        st.session_state.guess_history.append((guess, result)) # 기록에 추가
                        if correct == st.session_state.selected_length:
                            st.success(f"🎉 정답입니다! **{st.session_state.mission}**! 총 시도 횟수: {st.session_state.attempt}번")
                            st.balloons() # 정답 시 풍선 효과
                            st.session_state.mission = None # 미션 초기화 (새 게임 시작 준비)
                        else:
                            st.info("계속 시도해보세요!")
                        # st.rerun() # 여기서는 제거합니다. Streamlit이 상태 변경을 감지하고 자동으로 재실행합니다.
                    else:
                        st.warning("존재하지 않는 단어입니다. 영어 사전에 있는 단어를 입력해주세요.")
                else:
                    st.warning(f"올바른 {st.session_state.selected_length}자 길이의 알파벳 단어를 입력해주세요.")

# 피드백 이모지 매핑
# 각 피드백 문구에 해당하는 이모지입니다.
color_map = {
    "맞았어요!": "🟩",
    "다른 자리에 넣어주세요!": "🟨",
    "틀렸어요!": "⬜"
}

# 시도 기록 출력
if st.session_state.guess_history:
    st.markdown("---")
    st.subheader("📜 이전 시도 기록")
    # 최신 시도가 가장 위에 오도록 기록을 뒤집어서 출력합니다.
    for idx, (guess, feedback) in enumerate(reversed(st.session_state.guess_history)):
        original_idx = len(st.session_state.guess_history) - 1 - idx # 원래 시도 번호 계산
        emoji_summary = "".join([color_map.get(fb, '') for fb in feedback]) # 피드백을 이모지로 변환
        st.markdown(f"**{original_idx + 1}번째 시도: {guess.upper()}** {emoji_summary}")
