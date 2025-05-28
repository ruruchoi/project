import random

#미션 숫자 생성
def make_num(digits):
    arrange = 0
    mission_num = None
    for _ in range(digits):
        if arrange == 0:
            mission_num = str(random.randint(1,9))
            arrange = 1
        else:
            mission_num += str(random.randint(0,9))
    return mission_num

#숫자 비교
def check(mission, guess, digits):
    correct = 0
    for i in range(digits):
        if mission[i] == guess[i]:
            print(f"{i + 1}번째 숫자 : 맞았어요!")
            correct += 1
        elif guess[i] in mission:
            print(f"{i + 1}번째 숫자 : 다른 자리에 넣어주세요!")
        else:
            print(f"{i + 1}번 숫자 : 틀렸어요!")
    return correct

#미션 단어 생성
def make_word():
    

game_mode = input("원하시는 게임을 선택해 주세요")


if game_mode == "숫자":
    while True:
    #자릿수 입력
        attempt = 0
        num_digits = int(input("자릿수를 입력하세요 : "))

        mission_num = make_num(num_digits)

        while True:
            attempt += 1
            my_guess = (input(f"{attempt}번째 시도 : "))
            #자릿수 확인(첫 숫자 0 확인) 
            if len(my_guess) != num_digits or not my_guess.isdigit():
                print("입력이 잘못되었습니다. 다시 시도하세요.")
                attempt -= 1
                continue
            if check(mission_num, my_guess, num_digits) == num_digits:
                print(f"정답입니다! 축하합니다! 총 시도 횟수 : {attempt}번")
                break

        restart = input("게임을 다시 시작하시겠습니까? (y/n): ")
        if restart != 'y':
            print("게임을 종료합니다. 감사합니다!")
            break
else:
    while True:
        attempt = 0
        mission_word = make_word()
        print(f"알파벳 {len(mission_word)}개로 이루어진 단어입니다.")
        while True:
            attempt += 1
            my_guess = (input(f"{attempt}번째 시도 : "))
            #영어 형태 확인
            
