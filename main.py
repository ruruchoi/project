import streamlit as st
import random
import re
import nltk # NLTK는 여전히 다운로드 로직을 위해 필요합니다
from nltk.corpus import words # NLTK words 코퍼스는 이제 기본 단어로 사용되지 않습니다
from collections import Counter

# NLTK 단어 사전 다운로드 (코퍼스 존재 여부 확인용)
# 직접적인 영어 단어 게임에는 사용되지 않지만, nltk.data.find('corpora/words') 호출을 위해 유지
try:
    nltk.data.find('corpora/words')
except LookupError:
    st.info("NLTK 'words' 코퍼스를 다운로드 중입니다. 잠시 기다려 주세요.")
    nltk.download('words')
    st.success("NLTK 'words' 코퍼스 다운로드가 완료되었습니다!")
except Exception as e:
    st.error(f"NLTK 데이터 다운로드 중 예상치 못한 오류가 발생했습니다: {e}")


# 제공된 docx 파일의 'fullContent'에서 단어 사전 생성
# (실제 파일 업로드 방식이 아닌, 주어진 텍스트 내용으로 단어 사전을 구축)
# 각 줄에서 단어만 추출하고, 4~10글자 사이의 알파벳 단어만 포함
custom_english_words_raw = """
1 culture 문화, 교양
2 experience 경험
3 education 교육
4 symbol 상징
5 effect 결과, 영향, 효과
6 liberty 자유
7 affair 사건, 일
8 comfort 안락, 위안
9 tradition 전통, 전설
10 subject 학과, 주제, 주어
11 object 사물, 목적, (동)반대하다
12 source 출처, 근원
13 revolution 혁명
14 pollution 오염
15 system 조직, 체계, 지도
16 triumph 승리
17 respect 존경 동 존경하다
18 communication 전달, 교통
19 foundation 기초
20 glory 영광
21 situation 위치, 사태
22 competition 경쟁
23 prairie 대초원
24 effort 노력
25 section 부분, 구역
26 rein 고삐
27 solution 해결, 용해
28 hono(u)r 명예/경의, 동 존경하다
29 unity 통일/일치
30 population 인구
31 direction 방향, 지시
32 dialog(ue) 대화
33 republic 공화국
34 method 방법
35 increase 증가, [동]증가하다
36 decrease 감소, [동]감소하다
37 amount 양, 액수, 
총계
38 ancestor 조상, 선조
39 voyage 항해
40 sculpture 조각(품)
41 instrument 기계, 기구, 도구
42 figure 숫자, 계산, 모습, 인물
43 activity 활동
44 cause 원인, 이유
45 worth 가치, ~에 가치가 있는
46 accident 사고, 뜻밖의 사건
47 adventure 모험
48 view 경치, 의견
49 relative 친척, 관계가 있는
50 superstition 미신
51 habit 습관, 버릇
52 wealth 재산, 부
53 treasure 보물
54 universe 우주, 전 세계
55 adult 성인, 성인의
56 feast 향연, 잔치
57 resources 자원, 수단
58 ruin 파멸
59 monument 기념비, 기념물
60 information 정보, 지식, 통지
61 appetite 식욕
62 stethoscope 청진기
63 mystery 신비, 불가사의
64 thermometer 온도계
65 burden 무거운 짐, 짐을 지우다
66 series 연속, 시리즈
67 oath 맹세, 선서
68 appointment 임명, 약속
69 clue 실마리, 단서
70 debt 은혜, 
빚
71 hydrogen 수소
72 control 통제, 지배, 통제하다, 지배하다
73 uniform 제복, 한 모양의
74 design 계획, 설계, 계획하다, 디자인 하다
75 damage 손해, 손상
76 custom 습관, 풍습
77 traffic 교통
78 sophomore 2학년생
79 temperature 온도, 체온
80 limit 제한하다, 한계, 제한
81 statue 조각상
82 furniture 가구
83 parade 행렬
84 public 공중(사회), 공공의, 공중의
85 pilgrim 순례자
86 greeting 인사, 축하
87 language 언어
88 opinion 의견
89 athlete 운동선수
90 supply 공급, 공급하다
91 surface 표면
92 electricity 전기
93 order 순서, 명령
94 spirit 정신
95 purpose 목적
96 promise 가망, 전망, 약속
97 project 계획, 계획하다
98 government 정부, 정치의
99 exercise 운동, 연습하다
100 comparison 비교
101 interest 이익, 흥미
102 funeral 장례식
103 senior 선배, 손위에
104 junior 후배, 손아래에
105 democracy 민주주의, 민주정치
106 general 
육군 장군
107 admiral 해군대장
108 edge 날, 가장자리
109 biology 생물학
110 danger 위험
111 advice 충고
112 practice 연습하다
113 mammal 포유동물
114 grade 학년
115 score 점수
116 pause 중지, 멈추다
117 pronunciation 발음
118 stress 압박, 강조하다
119 contest 경쟁
120 horizon 수평선
121 principal 교장, 주요한, 長
122 might 힘
123 trouble 고생, 걱정하다
124 scar 상처
125 balance 균형
126 proverb 속담
127 semester 학기
128 election 선거
129 inning 회
130 hollow 구멍, 속이 빈
131 degree 도, 정도
132 cemetery 묘지
133 relay 교되자, 교대하다
134 spot 지점
135 exchange 교환하다
136 merchant 상인
137 saying 격언
138 refrigerator 냉장고
139 crack 갈라진 틈
140 judge 재판관
141 slave 노예
142 settler 이주민
143 fare 요금
144 gesture 몸짓
145 planet 유성
146 type 유형
147 secretary 비서
148 devil 악마
149 scholar 학자
150 pardon 
용서
151 kindergarten 유치원
152 detective 탐정
153 license 면허
154 palace 궁전
155 spade 삽
156 square 정사각형, 광장
157 fountain-pen 만년필
158 harvest 수확, 추수
159 tool 도구
160 sword 칼
161 magazine 잡지
162 stadium (육상)경기장
163 care 걱정, 조심
164 beauty 아름다움
165 museum 박물관
166 sentence 문장
167 memory 기억
168 delight 기쁨
169 passenger 승객
170 skill 숙련, 솜씨
171 journey 여행
172 ceremony 의식
173 hobby 취미
174 president 대통령
175 address 주소
176 continent 대륙
177 mankind 인간
178 patient 환자, 참을성 있는
179 site 부지
180 marble 대리석
181 stem 줄기
182 slip 미끄러짐
183 torch 횃불
184 composer 작곡가
185 invader 침입자
186 trick 계략, 속임수
187 flight 비행
188 castle 성
189 envelope 봉
190 pal 친구
191 vacation 휴가
192 desert 사막
193 event 사건
194 theater 극장
195 stage 무대
196 error 잘못
197 
area 면적, 지역
198 base 기초, 기초를 두다
199 basement 지하실
200 evil 악, 나쁜[200]
201 atom 원자
202 poet 시인
203 petal 꽃잎
204 chance 기회, 가능성
205 mind 마음
206 climate 기후, 풍토
207 suburb 교외
208 throat 목구멍
209 voice 목소리
210 valley 골짜기, 계곡
211 puritan 청교도
212 feather 깃털
213 amateur 아마추어
214 nation 국가
215 puzzle 수수께끼
216 riddle 수수께끼
217 rear 뒤쪽
218 battle 전투, 싸움
219 laundry 세탁소
220 shower 소나기, 샤워
221 navy 해군
222 mars 화성
223 gallery 화랑
224 guest 손님( visitor )
225 folk 사람들
226 problem 문제
227 jewel 보석
228 garage 차고
229 fault 결점, 잘못.
230 lantern 랜턴
231 import 수입(품)
232 angle 각도
233 match 시합
234 stripe 줄무늬
235 pulse 맥박
236 powder 가루, 화약
237 flood 홍수
238 bush 수풀, 덤불
239 branch 가지
240 hero 영웅 복수형:heroes
241 heaven 하늘
242 exit 출구
243 beast 짐승(=animal)
244 century 세기,100년
245 coeducation 남녀 공학
246 twin 쌍둥이의 한 사람
247 wound 상처, 부상
248 metal 금속
249 insect 곤충
250 track 지나간 자국, 선로
251 deserve 받을 가치가있다,~할 만하다
252 survive ~보다 오래 살다, ~에서 살아남다
253 create 창조하다
254 describe 묘사하다
255 select 고르다, 선발한
256 hesitate 주저하다, 망설이다
257 declare 선언하다
258 pretend ~인 체하다
259 struggle 분투노력하다, 싸우다
260 explore 탐험하다
261 astonish 놀라게 하다
262 disappoint 실망시키다
263 attract 끌다
264 celebrate 축하하다
265 explode 폭발시키다
266 include 포함하다
267 protect 보호하다
268 introduce 소개하다, 도입하다
269 
produce 생산하다
270 chase 쫓다, 추적
271 scratch 할퀴다, 긁다
272 crash 충돌(추락)하다, 와르르 무너지다
273 stare 응시하다
274 gaze 응시하다, 바라보다
275 scare 놀라게 하다, 놀라다
276 grab 움켜잡다 ★★★★★★★★★★★★★★
277 guard 지키다, 경계, 위병
278 discuss 토론하다
279 shrug 어깨를 으쓱하다
280 sniff 냄새 맡다
281 scream 날카롭게 소리치다
282 rid 제거 하다
283 surround 둘러싸다.
284 cleave 쪼개다, 찢다.
285 carve 새기다, 조각하다.
286 except 제외하다
287 invent 발명하다
288 search 찾다
289 abuse 남용하다, 학대하다.
290 owe 힘입다, 빛(의무)이 있다.
291 bless 축복하다
292 graduate 졸업하다
293 replace ~을 대신하다, 제 자리에 놓다.
294 collect 모으다, 수집하다.
295 upset 뒤엎다, 당황하게 한다.
296 arrest 체포하다, 체포
297 prove 증명하다
298 yell 외치다
299 howl 짖다, 울부짖다
300 halt 정지하다
301 leak 새다
302 behave 행동하다
303 wrap 싸다
304 locate 위치하다
305 charge 청구하다
306 review 복습하다
307 refuse 거절하다
308 complain 불평하다
309 remain 남다
310 warn 경고하다
311 bend 구부리다
312 suffer 겪다
313 whisper 속삭이다
314 prepare 준비하다
315 roar 으르렁거리다
316 float 뜨다
317 drag 질질 끌다
318 overhear 엿듣다
319 slide 미끄러지다
320 suck 빨다
321 bother 괴롭히다
322 deal 분배하다
323 treat 다루다
324 destroy 파괴하다
325 accept 받아들이다
326 depend ~에 의존하다
327 nod 끄덕이다
328 remove 옮기다
329 beat 때리다
330 clap 탁 치다
331 feed 먹을 것을 주다
332 obtain 얻다
333 drown 빠뜨리다 빠지다 빠져죽다
334 remind 생각나게 하다
335 occur 일어나다
336 ache 아프다
337 repeat 되풀이하다
338 
attend 참석하다
339 sigh 한숨 쉬다
340 pray 빌다
341 press 누르다
342 bear 낳다
343 follow 따르다
344 hate 미워하다
345 frighten 깜짝 놀라게 하다
346 shout 외치다
347 mention 말하다
348 waste 낭비하다
349 borrow 빌리다
350 complete 완성하다
351 excellent 뛰어난
352 competent 유능한
353 religious 종교적인
354 favorite 아주 좋아하는
355 entire 전체의
356 primary 본래의
357 similar 비슷한
358 precious 귀중한
359 normal 보통의
360 popular 인기 있는
361 compulsory 의무적인
362 curious 호기심이 강한
363 independent 독립의
364 intimate 친밀한
365 delicious 맛있는
366 valuable 귀중한
367 grave 중대한
368 elementary 초보의
369 crazy 미친
370 contrary 반대의
371 regular 규칙적인
372 social 사회의
373 straight 똑바른
374 noble 고귀한
375 anxious 걱정되는
376 international 국제적인
377 greedy 탐욕스러운
378 stupid 어리석은
379 silly 어리석은
380 lonely 고독한
381 dirty 더러운
382 various 여러 가지의
383 private 개인의
384 vain 
무익한
385 sore 아픈
386 fierce 사나운
387 firm 굳은
388 solar 태양의
389 smart 산뜻한
390 single 독신의
391 diligent 부지런한
392 serious 진지한
393 fresh 새로운
394 empty 빈
395 mild 온화한
396 amazing 놀라운
397 charming 매력적인
398 boring 지겨운
399 giant 거대한
400 huge 거대한
401 tiny 몹시 작은
402 fair 공명정대한
403 tough 단단한
404 foreign 외국의
405 modern 현대의
406 expensive 값비싼
407 harmful 해로운
408 calm 평온한
409 special 특별한
410 steady 확고한
411 hay 건초
412 revival 부활
413 million 백만
414 crop 농작물
415 shade 그늘
416 company 친구
417 canal 운하
418 wagon 짐마차
419 fact 사실
420 joy 기쁨
421 concert 음악회
422 rule 규정하다
423 suitcase 여행가방
424 weight 무게
425 hurray 만세
426 mail 우편물
427 log 통나무
428 hut 오두막집
429 tax 세금
430 dye 물감
431 earnings 벌이
432 flame 불꽃
433 shape 모양
434 
chest 가슴
435 chain 사슬
436 cost 비용
437 coast 해안
438 circle 원, 집단
439 heart 심장
440 nature 자연
441 fever 열
442 tongue 혀
443 trust 신용
444 whisker 구레나룻
445 prison 형무소
446 blood 피
447 loaf 빵 한 덩어리
448 list 명부
449 fence 울타리
450 enemy 적
451 thief 도둑
452 data 자료
453 soldier 군인, 병사
454 musician 음악가
455 capital 수도, 자본
456 course 진로, 과정
457 diary 일기
458 squirrel 다람쥐
459 dawn 새벽
460 shadow 그림자
461 ditch 도랑
462 crew 승무원
463 stomach 위
464 neighbor 이웃사람
465 servant 하인
466 hunger 굶주림
467 tomb 묘, 무덤
468 taste 맛, 취미
469 sign 신호, 구호
470 stair 계단
471 trip 여행
472 brain 뇌, 머리
473 trumpet 나팔
474 speech 말, 연설
475 thumb 엄지손가락
476 horn 뿔, 경적
477 chief 우두머리, 
주요한
478 trousers 바지
479 prince 왕자
480 force 힘, 강요하다
481 sight 광경, 경치
482 space 공간, 우주
483 wool 양모
484 expressway 고속도로
485 science 과학
486 examination 시험, 조사
487 jar 항아리
488 salt 소금
489 death 죽음, 사망
490 saw 톱, 톱으로 켜다
491 swing 그네, 진동
492 wish 소원, 원하다
493 grain 곡식, 낱알
494 eraser 지우개
495 alphabet 알파벳 문자
496 shoulder 어깨
497 nephew 조카
498 niece 조카딸
499 library 도서관
500 factory 공장 ★★★★★★★★★★★★★★
501 giraffe 기린
502 hawk 매
503 pigeon 비둘기
504 bowl 사발, 그릇
505 scene 장면, 현장
506 life 생명, 생활
507 earth 지구, 땅
508 pill 알약
509 math 수학
510 ocean 대양
511 price 값, 가격
512 row 줄, 열
513 schedule 예정표
514 machine 기계
515 route 길
516 ivy 담쟁이덩굴
517 gift 선물, 타고난 
재능
518 candle 양초, 촛불
519 joke 농담, 농담을 하다
520 art 예술, 미술
521 corn 곡물
522 pet 애완동물, 귀여워하는
523 robber 강도
524 cheek 볼
525 clerk 사무원, 점원
526 cookie 쿠키, 맛있는 작은 과자
527 army 육군, 군대
528 nurse 간호사
529 master 주인, 정복하다
530 lock 자물쇠, 자물쇠를 채우다
531 moment 순간
532 sheet 침대의 시트, 종이 한 장
533 monk 승려
534 teenager 10대 소년소녀
535 closet 벽장
536 handle 손잡이
537 guide 안내자, 안내하다
538 bar 막대기, 빗장
539 ostrich 타조, 방관자
540 knee 무릎
541 cricket 크리켓 경기
542 deck 갑판
543 bit 작은 조각, 조금
544 silk 비단
545 jean 진 바지, 진으로 만든 옷
546 cotton 솜, 면화
547 drum 북
548 sand 모래, 모래밭
549 shock 충격, 충격을 주다
550 march 행진, 행진하다
551 
cage 새장, 우리
552 whole 전부, 전부의
553 change 변화, 잔돈
554 department 부, 백화점의 매장
555 office 사무실, 회사
556 ticket 표, 입장권
557 energy 힘, 활기
558 idea 생각, 이념
559 hospital 병원
560 noise 소리, 소음
561 sample 견본
562 example 예, 보기
563 lesson 학과, 교훈
564 plenty 풍부, 많은
565 luck 행운
566 comedy 희극, 코미디
567 health 건강
568 history 역사
569 forest 숲
570 stream 흐름, 흐르다
571 future 미래, 미래의
572 state 상태, 국가
573 temple 절, 사원
574 dictionary 사전
575 grammar 문법
576 college 단과대학, 전문학교
577 husband 남편
578 daughter 딸
579 captain 우두머리, 선장
580 booth 오두막집, 작은 방
581 iceberg 빙산
582 bubble 거품
583 bottom 밑, 밑바닥
584 prize 상, 상품
585 bean 콩
586 race 경주, 민족
587 engineer 기사, 공학자
588 
photographer 사진사
589 reason 이유, 이성
590 subway 지하도, 지하철
591 fog 안개
592 answer 대답, 대답하다
593 dinning room 식당
594 step 걸음, 걷다
595 heat 열, 더위
596 bone 뼈
597 plant 식물, 식물을 심다
598 lamb 새끼냔
599 rate 비율, 속도
600 report 보고, 보고하다
601 turtle 바다거북
602 bay 만
603 holiday 휴일, 휴가
604 center 중심, 중심지
605 cash 현금, 현금으로 바꾸다
606 wolf 이리, 늑대
607 operator 교환수
608 fur 부드러운 털, 모피
609 shore 물가, 바닷가
610 owl 올빼미
611 hunter 사냥꾼
612 pumpkin 호박
613 handshake 악수
614 bike 자전거
615 beach 해안
616 god 신
617 cough 기침, 기침을 하다
618 shell 조개
619 business 사업, 일
620 restaurant 식당
621 sheep 양
622 officer 공무원, 장교
623 hometown 고향
624 coil 코일, 감긴 것
625 ceiling 천장
626 
turkey 칠면조
627 towel 수건, 타월
628 matter 일, 문제
629 chopstick 젓가락
630 seat 좌석, 앉히다
631 board 판자
632 goal 목표, 골
633 drugstore 약국
634 rat 쥐, 들쥐
635 butterfly 나비
636 flute 플루트, 피리
637 couple 한 쌍, 커플
638 beer 맥주
639 background 배경
640 bottle 병
641 body 몸, 신체
642 group 집단
643 village 마을
644 beef 쇠고기
645 load 짐, 부담
646 coin 동전, 화폐
647 bookstore 서점
648 label 꼬리표, 딱지
649 port 항구
650 quarter 4분의1, 15분
651 sunrise 해돋이
652 sunshine 햇빛
653 wedding 결혼, 결혼식
654 crown 왕관
655 seed 씨, 씨를 뿌리다
656 coal 석탄
657 comb 빗, 빗질하다
658 dream 꿈, 꿈을 꾸다
659 sugar 설탕
660 mile 마일
661 flashlight 카메라의 플래시, 회중전등
662 vegetable 야채
663 mouse 생쥐
664 wood 나무, 숲
665 
war 전쟁
666 ground 땅, 운동장
667 belt 띠, 허리띠
668 tourist 여행자, 관광객
669 airport 공항
670 passport 여권
671 plate 접시
672 stone 돌
673 downtown 번화가
674 cousin 사촌
675 tooth 이
676 potato 감자
677 blanket 담요
678 creek 시냇물
679 nail 손톱, 발톱
680 letter 편지, 문자
681 date 날짜, 데이트 약속
682 store 가게, 저축하다
683 beggar 거지
684 bedside 침대 곁
685 deer 사슴
686 bill 계산서, 지폐
687 doll 인형
688 pepper 후추
689 frog 개구리
690 rest 휴식, 나머지
691 tower 탑
692 bridge 다리
693 cloth 천, 직물
694 post 우편, 우편물
695 snake 뱀
696 job 직업, 일
697 town 읍, 도시
698 fun 놀이, 재미
699 bathroom 욕실
700 tail 꼬리
701 mayor 시장
702 piece 한 조각
703 fruit 과일
704 british 영국인, 영국의
705 french 프랑스 
사람, 프랑스어
706 German 독일사람, 독일어
707 sale 판매, 염가판매
708 rope 밧줄
709 umbrella 우산
710 dollar 달러
711 mistake 잘못, 잘못 알다
712 birth 출생
713 pilot 조종사, 안내인
714 none 아무도 ~않다
715 front 정면, 앞부분
716 present 현재, 선물
717 nickname 별명, 애칭
718 telephone 전화, 전화를 걸다
719 pair 한 쌍
720 weather 날씨
721 dish 접시, 요리
722 hole 구멍
723 plane 비행기
724 living room 거실
725 gun 총
726 meat 고기
727 cover 덮개, 덮다
728 grass 풀, 잔디
729 watch 손목시계, 주의
730 word 낱말, 단어
731 explain 설명하다
732 wear 입다, 착용하다
733 amuse 재미있게 하다
734 suppose 상상하다, 생각하다
735 leap 뛰다
736 bury 묻다
737 engage 고용하다, 약속하다
738 sow 씨를 뿌리다
739 lift 들어 올리다
740 bow 절하다, 절
741 rub 비비다, 문지르다
742 
bite 물다, 물어뜯다
743 vote 투표하다, 투표
744 hop 한발로 뛰다
745 imagine 상상하다, 생각하다
746 allow 허락하다
747 offer 제공하다
748 gain 얻다, 이기다
749 alarm 놀라게 하다, 경보하다
750 obey 복종하다
751 steal 훔치다
752 dig 파다
753 choose 고르다, 선택하다
754 receive 받다
755 bet 돈을 걸다
756 hurt 상처를 입히다
757 burn 타다, 태우다
758 sink 가라앉다
759 decide 결정하다, 결심하다
760 beg 구걸하다, 청하다
761 reply 대답(하다) ★★★★★★★★★★★★★
762 tear 찢다, 찢어지다
763 flow 흐르다, 넘쳐흐르다
764 remember 기억하다, 생각해내다
765 appear 나타나다, ~인 것 같다
766 breathe 숨 쉬다, 호흡하다
767 whistle 휘파람을 불다, 휘파람
768 draw 끌다, 당기다
769 sound 소리가 나다, 소리
770 save 구하다, 저축하다
771 continue 계속하다
772 check 저지하다, 대조하다
773 sail 항해하다, 돛
774 wake 깨다, 깨우다
775 agree 동의하다
776 hang 
걸다, 매달다
777 record 기록
778 drop 떨어지다, 떨어뜨리다
779 climb 기어오르다, 오르다
780 add 더하다, 보태다
781 shine 빛나다
782 invite 초대하다
783 join 결합하다, 참가하다
784 hide 감추다, 숨다
785 bring 가져오다, 데려오다
786 wink 눈을 깜박거리다, 눈짓하다
787 shoot 쏘다, 사격하다
788 roll 구르다, 굴리다
789 pull 잡아당기다, 끌다
790 push 밀다
791 guess 추측하다, 추측
792 belong 누구누구에게 속하다
793 happen 일어나다, 생기다
794 pick 고르다, 줍다
795 shake 떨다, 흔들다
796 fill 채우다, 가득하다
797 fail 실패하다
798 fight 싸우다, 전투
799 fear 두려워하다, 두려움
800 carry 나르다, 운반하다[800]
801 dive 다이빙하다, 잠수하다
802 win 이기다, 얻다
803 ride 타다, 타고 가다
804 turn 돌다, 변화하다
805 need 필요로 하다, 필요
806 build 짓다, 건축하다
807 hurry 서두르다, 서두름
808 return 돌아가다, 돌아오다
809 believe 믿다
810 surprise 놀라다, 
놀람
811 gather 모으다
812 throw 던지다
813 raise 올리다, 일으키다
814 count 세다, 계산하다
815 smell 냄새를 맡다, 냄새
816 spend 소비하다, 지내다
817 pitch 던지다
818 pop 펑하고 소리 나다, 대중음악
819 blow 불다
820 miss 놓치다, 그리워하다
821 excuse 용서하다, 변명하다
822 hit 치다
823 tie 매다, 묶다
824 touch 닿다, 감동시키다
825 stay 머무르다
826 enjoy 즐기다
827 lose 잃다, 지다
828 close 닫다, 끝나다
829 arrive 도착하다
830 travel 여행하다, 여행
831 reach 도착하다
832 hold 쥐다, 개최하다
833 worry 걱정하다, 괴롭히다
834 marry 결혼하다
835 expect 기대하다, ~라고 생각하다
836 understand 이해하다, 알다
837 become ~이 되다, 어울리다
838 break 부수다, 깨뜨리다
839 smoke 담배를 피우다, 연기
840 lend 빌려주다
841 shut 닫다
842 sleep 자다
843 lay 눕히다, 놓다
844 paint 그리다, 페인트를 칠하다
845 lead 인도하다, 지내다
846 
pass 지나가다, 합격하다
847 hand 주다, 건네주다
848 ancient 고대의
849 nuclear 핵의
850 necessary 필요한
851 common 공통의, 보통의
852 inner 안쪽의
853 thirsty 목마른
854 thin 얇은, 야윈
855 gray 회색, 회색의
856 famous 유명한
857 industrial 산업의, 공업의
858 silent 조용한, 침묵의
859 absent 결석한
860 flat 평평한
861 main 주요한
862 wild 야생의, 난폭한
863 wet 젖은
864 blind 눈먼
865 dumb 벙어리의
866 sharp 날카로운
867 terrible 끔직한, 무서운
868 grand 웅장한, 화려한
869 homesick 고향을 그리워하는, 향수병의
870 bound ~로 출발하려고 하는
871 fat 살찐, 지방
872 strange 이상한, 낯선
873 pleasant 기분 좋은, 유쾌한
874 handsome 잘생긴, 멋진
875 equal 같은, 동등한
876 dear 친애하는, 값비싼
877 sweet 달콤한
878 dull 우둔한, 무딘
879 weak 약한
880 bright 밝은, 영리한
881 honest 정직한
882 elder 손위의, 연상의
883 such 그러한, 
이러한
884 able 유능한, 할 수 있는
885 loud 목소리가 큰, 시끄러운
886 simple 간단한, 단순한
887 clever 영리한
888 proud 자랑스러운, 오만한
889 foolish 어리석은
890 possible 가능한
891 enough 충분한, 충분히
892 wise 현명한
893 wide 넓은, 널리
894 successful 성공한
895 clear 맑은, 명백한
896 clean 깨끗한
897 deep 깊은, 깊게
898 own 자기 자신의, 소유하다
899 cheap 값싼
900 certain 확실한, 어떤
901 important 중요한
902 stormy 폭풍의
903 true 진실한
904 sad 슬픈
905 gay 명랑한, 화려한
906 merry 즐거운
907 colorful 다채로운, 화려한
908 wonderful 놀랄만한, 훌륭한
909 peaceful 평화로운
910 angry 성난
911 dry 마른
912 wrong 나쁜, 틀린
913 heavy 무거운
914 quiet 조용한
915 several 여럿의, 몇몇의
916 alone 홀로, 다만 ~ 뿐
917 crowded 붐비는, 혼잡한
918 excited 흥분한
919 alive 살아있는
920 brown 갈색의, 갈색
921 different 
다른
922 difficult 어려운
923 interesting 재미있는
924 unlike 같지 않은
925 least 가장 적은, 최소한의
926 afraid 무서워하여
927 cool 서늘한, 냉정한
928 pretty 예쁜, 상당히
929 kind 친절한, 종류
930 sick 병든, 싫증난
931 useless 쓸모없는
932 busy 바쁜
933 early 일찍이
934 past 과거의, ~을 지나서
935 dark 어두운
936 cloudy 구름이 낀
937 short 짧은, 키가 작은
938 low 낮은, 낮게
939 sincerely 성실히
940 fortunately 운 좋게, 다행히
941 finally 최후로, 마침내
942 immediately 곧, 즉시
943 especially 특별히
944 else 그밖에
945 actually 실제로
946 hardly 거의 ~ 아니다
947 otherwise 다른 방법으로, 그렇지 않으면
948 tightly 단단히
949 recently 최근에
950 rapidly 빨리, 신속히
951 however 아무리 ~해도, 그러나
952 politely 공손히, 정중하게
953 rudely 무례하게
954 further 더욱이, 터먼
955 frankly 솔직히
956 properly 적당히, 올바르게
957 haste 
급함, 신속, 서두르다
958 rather 오히려, 얼마간
959 together 함께
960 altogether 전혀, 대체로
961 suddenly 갑자기
962 mostly 대개는
963 correctly 정확히
964 ahead 앞으로, 앞에
965 instead 대신에
966 quite 아주, 매우
967 nearly 거의
968 badly 나쁘게, 몹시
969 almost 거의
970 exactly 정확히
971 apart 떨어져서, 따로
972 afterward 후에, 나중에
973 later 후에, 나중에
974 maybe 아마
975 perhaps 아마
976 probably 아마
977 either ~도 또한 ~ 하지 않다
978 neigher ~도 아니고 ~도 아니다
979 besides 게다가, 그밖에
980 anyway 어쨌든, 아무튼
981 sometime 언젠가
982 forward 앞쪽에, 앞으로
983 since 그 후, 그 이래
984 once 한번, 한때
985 twice 두 번
986 indeed 참으로
987 seldom 좀처럼 ~하지 않다
988 upside down 거꾸로
889 whether ~인지 어떤지
990 unless ~하지 않으면
991 though 비록 ~일지라도
992 
while ~하는 동안
993 usually 보통, 대개
994 safely 안전하게
995 along ~을 따라서
996 without ~없이
997 behind ~의 뒤에
998 beyond ~의 저쪽에, ~이상으로
999 below ~의 아래에
1000 toward ~쪽으로
"""

# 제공된 raw 텍스트에서 단어를 추출하여 단어 사전 생성
extracted_words_from_content = []
for line in custom_english_words_raw.splitlines():
    # 숫자와 괄호를 포함하는 단어 패턴 매칭 (정확도를 높이기 위해 수정)
    # 줄 시작의 숫자(선택적)와 공백(선택적) 이후에 오는 알파벳 문자열을 찾습니다.
    match = re.match(r'^\s*\d*\s*([a-zA-Z]+)', line.strip())
    if match:
        word = match.group(1).lower()
        # 단어 길이는 4~10 글자로 제한
        if 4 <= len(word) <= 10:
            extracted_words_from_content.append(word)

# 최종적으로 사용할 영어 단어 사전
# 이제 NLTK 'words' 코퍼스가 아닌, 제공된 'fullContent'에서 추출한 단어를 사용합니다.
english_vocab = list(set(extracted_words_from_content)) # 중복 제거 후 리스트로 변환
english_vocab_set = set(english_vocab) # 검색 효율성을 위한 집합

# 숫자 미션 생성 함수
def make_num(digits):
    num_list = [str(random.randint(1, 9))]
    for _ in range(digits - 1):
        num_list.append(str(random.randint(0, 9)))
    return "".join(num_list)

# 정답과 입력(추측)을 비교하여 피드백을 제공하는 함수
# (이전 개선된 로직 유지)
def check(mission, guess):
    length = len(mission)
    result = [''] * length
    correct = 0

    mission_chars_copy = list(mission)
    guess_list = list(guess) # guess도 리스트로 변환하여 처리된 문자 표시

    # 1. '맞았어요!' (스트라이크) 처리
    for i in range(length):
        if guess_list[i] == mission_chars_copy[i]:
            result[i] = "맞았어요!"
            correct += 1
            mission_chars_copy[i] = None # 처리되었음을 표시
            guess_list[i] = None # 처리되었음을 표시
    
    # 남은 글자들에 대한 Counter 생성
    mission_remaining_counter = Counter([c for c in mission_chars_copy if c is not None])

    # 2. '다른 자리에 넣어주세요!' (볼) 및 '틀렸어요!' 처리
    for i in range(length):
        if result[i] == '': # 아직 처리되지 않은 위치라면
            current_guess_char = guess_list[i] # 리스트에서 해당 위치의 문자 가져오기

            if current_guess_char is not None and current_guess_char in mission_remaining_counter and mission_remaining_counter[current_guess_char] > 0:
                result[i] = "다른 자리에 넣어주세요!"
                mission_remaining_counter[current_guess_char] -= 1
            else:
                result[i] = "틀렸어요!"
            
    return result, correct

# 초기 세션 상태 설정
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


# 앱의 제목과 간단한 설명 표시
st.title("🎮 숫자/영어 추측 게임")
st.markdown("정답을 맞힐 때까지 숫자나 영어 단어를 추측해보세요! 각 문자에 대한 피드백을 받습니다.")

# 리셋 버튼
if st.button("🔄 게임 리셋", help="현재 진행 중인 게임을 리셋하고 초기화합니다."):
    for key in list(st.session_state.keys()): # 모든 세션 상태 키를 명시적으로 삭제
        del st.session_state[key]
    st.rerun() # 앱을 다시 로드하여 초기화된 세션 상태를 적용
    st.stop()  # 현재 스크립트 실행 중지

# 게임 모드 선택 화면
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
    
    # 숫자 모드 게임 로직
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

    # 영어 모드
    elif st.session_state.game_mode == "영어":
        if st.session_state.mission is None:
            # 여기서는 파일 업로드 대신, 코드에 포함된 단어 목록을 사용합니다.
            st.info("제공된 텍스트 파일의 단어 목록을 사용하여 게임을 진행합니다.")

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
                    # 게임 시작 시, 현재 사용되는 단어 사전을 세션 상태에 저장 (유효성 검사용)
                    st.session_state.current_word_source_set = english_vocab_set # 제공된 단어 셋 사용

        if st.session_state.mission:
            st.markdown(f"**현재 {st.session_state.selected_length}자 길이의 영어 단어 게임 진행 중입니다.**")
            guess = st.text_input(
                f"{st.session_state.attempt + 1}번째 시도 (예: {'_' * st.session_state.selected_length})",
                key=f'guess_word_{st.session_state.attempt}' 
            ).lower()

            if st.button("제출", key='submit_word_guess'):
                if len(guess) == st.session_state.selected_length and guess.isalpha():
                    if guess in st.session_state.current_word_source_set: # 제공된 단어 셋으로 유효성 검사
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
                        st.warning("존재하지 않는 단어입니다. 제공된 사전에 있는 단어를 입력해주세요.")
                else:
                    st.warning(f"올바른 {st.session_state.selected_length}자 길이의 알파벳 단어를 입력해주세요.")

# 피드백 이모지 매핑
color_map = {
    "맞았어요!": "🟩",
    "다른 자리에 넣어주세요!": "🟨",
    "틀렸어요!": "⬜"
}

# 시도 기록 출력 섹션
if st.session_state.guess_history:
    st.markdown("---")
    st.subheader("📜 이전 시도 기록")
    for idx, (guess, feedback) in enumerate(reversed(st.session_state.guess_history)):
        original_idx = len(st.session_state.guess_history) - 1 - idx
        emoji_summary = "".join([color_map.get(fb, '') for fb in feedback])
        st.markdown(f"**{original_idx + 1}번째 시도: {guess.upper()}** {emoji_summary}")
    
    # 이모지 색상 설명
    st.markdown("---")
    st.subheader("색상 설명")
    st.markdown("🟩: **맞았어요!** - 해당 글자/숫자가 정답에 **포함**되어 있고, **위치도 정확**합니다.")
    st.markdown("🟨: **다른 자리에 넣어주세요!** - 해당 글자/숫자가 정답에 **포함**되어 있지만, **위치가 다릅니다**.")
    st.markdown("⬜: **틀렸어요!** - 해당 글자/숫자가 정답에 **포함되어 있지 않습니다**.")
