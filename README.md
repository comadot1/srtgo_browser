> [!IMPORTANT]
본 프로젝트는 https://github.com/lapis42/srtgo 를 기반으로 제작되었으며,
CLI로 제공되던 srtgo 프로그램을, 웹 터미널 형태로 제공하여 모바일로 사용하기 위해 제작되었습니다.

docker, docker-compose를 통해 배포되는 형태이며,

nextjs, node socket server, debian + srtgo CLI 프로그램으로 구성되어있습니다.
개선이 필요한 부분은 소스파일 원본 포함해서 업로드하였으니 참고바랍니다.



#### PASSWORD 입력 화면
![Image](https://github.com/user-attachments/assets/8c728bc4-d8b7-476b-901e-44ba03ee5f17)

#### Web UI
![Image](https://github.com/user-attachments/assets/c1e4b0ef-1db4-4546-a958-84f25b421c17)





# SRTgo: K-Train (KTX, SRT) Reservation Assistant
> [!WARNING]  
> 본 프로그램의 모든 상업적, 영리적 이용을 엄격히 금지합니다. 본 프로그램 사용에 따른 민형사상 책임을 포함한 모든 책임은 사용자에게 따르며, 본 프로그램의 개발자는 민형사상 책임을 포함한 어떠한 책임도 부담하지 아니합니다. 본 프로그램을 내려받음으로써 모든 사용자는 위 사항에 아무런 이의 없이 동의하는 것으로 간주됩니다.

> [!IMPORTANT]
> 본 프로그램에 입력하는 아이디, 비번, 카드번호, 예매 설정 등은 로컬 컴퓨터에 [keyring 모듈](https://pypi.org/project/keyring/)을 통하여 저장하며 그 이외의 위치에 네트워크 전송 등을 통하여 공유되지 않습니다.

## 주요 기능
- SRT 및 KTX 기차표 자동 예매
- 텔레그램 알림 전송
  - [Bot Token 및 Chat ID 얻기](https://gabrielkim.tistory.com/entry/Telegram-Bot-Token-%EB%B0%8F-Chat-Id-%EC%96%BB%EA%B8%B0)
- 자동 신용카드 결제
- 자주 사용하는 역 설정
- 어린이/우대 예매 지원
- 매진 시 예약대기 신청

---
> [!WARNING]
> All commercial and commercial use of this program is strictly prohibited. Use of this program is at your own risk, and the developers of this program shall not be liable for any liability, including civil or criminal liability. By downloading this program, all users agree to the above without any objection.

> [!IMPORTANT]  
> All sensitive data (login, payment info, settings) is stored locally via [keyring](https://pypi.org/project/keyring/) and never transmitted.

## Key Features
- Automated SRT/KTX ticket reservations
- Telegram notifications
- Automatic credit card payment
- Favorite station presets  
- Child/Senior ticket support
- Waitlist for sold-out trains

## Installation
Before running the project, please configure the .env file according to your environment.

#### 1. Configure Port Mappings
Update the port mappings for the following services as needed:

- ktx_front: Defaults to port 3000
- ktx_socket: Defaults to port 5000

Adjust these ports based on your system requirements.

#### 2. Set NEXT_PUBLIC_SOCKET_PROXY
This value represents the address of the ktx_socket service.

- If using a domain, provide the domain name.
- If not, use the IP address.

Make sure the protocol matches that of ktx_front:

- If ktx_front uses http, use ws:// for the socket proxy.
- If ktx_front uses https, use wss://.

#### 3. Set USE_PASSCHECK
This value enables or disables the password verification logic.

Supported values: true or false

##### 3.1 If USE_PASSCHECK is set to true:

You must also configure the following:

- ADMIN_PASSWORD: The password required to log in.
- SECRET_KEY: A secret used for token generation and validation.

#### 4. Run Containers.
```sh
$ docker compose up -d --build
```

```bash
[?] 메뉴 선택 (↕:이동, Enter: 선택): 예매 시작
 > 예매 시작
   예매 확인/취소
   로그인 설정
   텔레그램 설정
   카드 설정
   역 설정
   역 직접 수정
   예매 옵션 설정
   나가기

[?] 열차 선택 (↕:이동, Enter: 선택, Ctrl-C: 취소): SRT
 > SRT
   KTX
   취소

[?] 출발역 선택 (↕:이동, Enter: 완료, Ctrl-C: 취소): 수서
 > 수서
   대전
   동대구
   부산

[?] 도착역 선택 (↕:이동, Enter: 완료, Ctrl-C: 취소): 동대구
   수서
   대전
 > 동대구
   부산

[?] 출발 날짜 선택 (↕:이동, Enter: 완료, Ctrl-C: 취소): 2024/01/04 Thu
   2024/01/03 Wed
 > 2024/01/04 Thu
   2024/01/05 Fri
   2024/01/06 Sat
   2024/01/07 Sun
   2024/01/08 Mon
   2024/01/09 Tue
   2024/01/10 Wed
   2024/01/11 Thu
   2024/01/12 Fri
   2024/01/13 Sat
   2024/01/14 Sun
   2024/01/15 Mon

[?] 출발 시각 선택 (↕:이동, Enter: 완료, Ctrl-C: 취소): 10
   00
   02
   04
   06
   08
 > 10
   12
   14
   16
   18
   20
   22

[?] 승객수 (↕:이동, Enter: 완료, Ctrl-C: 취소): 1
 > 1
   2
   3
   4
   5
   6
   7
   8
   9

[?] 예약할 열차 선택 (↕:이동, Space: 선택, Enter: 완료, Ctrl-C: 취소): 
   [ ] [SRT 323] 01월 04일, 수서~동대구(10:00~11:40) 특실 매진, 일반실 매진, 예약대기 불가능
   [ ] [SRT 325] 01월 04일, 수서~동대구(10:30~12:17) 특실 매진, 일반실 매진, 예약대기 불가능
   [ ] [SRT 327] 01월 04일, 수서~동대구(10:50~12:30) 특실 매진, 일반실 매진, 예약대기 불가능
   [ ] [SRT 381] 01월 04일, 수서~동대구(12:04~13:55) 특실 매진, 일반실 매진, 예약대기 불가능
   [ ] [SRT 331] 01월 04일, 수서~동대구(12:28~14:08) 특실 매진, 일반실 매진, 예약대기 불가능
 > [ ] [SRT 333] 01월 04일, 수서~동대구(12:50~14:34) 특실 매진, 일반실 매진, 예약대기 불가능
   [X] [SRT 335] 01월 04일, 수서~동대구(13:00~14:46) 특실 매진, 일반실 예약가능, 예약대기 불가능
   [ ] [SRT 337] 01월 04일, 수서~동대구(13:30~15:16) 특실 매진, 일반실 매진, 예약대기 불가능
   [ ] [SRT 339] 01월 04일, 수서~동대구(13:55~15:25) 특실 매진, 일반실 예약가능, 예약대기 불가능
   [ ] [SRT 341] 01월 04일, 수서~동대구(14:30~16:10) 특실 매진, 일반실 매진, 예약대기 불가능

[?] 선택 유형 (↕:이동, Enter: 완료, Ctrl-C: 취소): 일반실 우선
 > 일반실 우선
   일반실만
   특실 우선
   특실만

[?] 예매 시 카드 결제 (y/N): N

예매 대기 중... |   16 (00:00:15)


🎊예매 성공!!!🎊
[SRT] 01월 04일, 수서~동대구(13:00~14:46) 36800원(1석), 구입기한 01월 03일 16:57
8호차 5B (일반실) 어른/청소년 [36800원(700원 할인)]


[?] 메뉴 선택 (↕:이동, Enter: 선택): 예매 확인/취소
   예매 시작
 > 예매 확인/취소
   로그인 설정
   텔레그램 설정
   카드 설정
   역 설정
   나가기

[?] 열차 선택 (↕:이동, Enter: 선택, Ctrl-C: 취소): SRT
 > SRT
   KTX
   취소

[?] 예약 취소 (Enter: 결정): [SRT] 01월 04일, 수서~동대구(13:00~14:46) 36800원(1석), 구입기한 01월 03일 16:57
 > [SRT] 01월 04일, 수서~동대구(13:00~14:46) 36800원(1석), 구입기한 01월 03일 16:57
   텔레그램으로 예매 정보 전송
   돌아가기
```

## Acknowledgments
- This project includes code from [SRT](https://github.com/ryanking13/SRT) by ryanking13, licensed under the MIT License, and [korail2](https://github.com/carpedm20/korail2) by carpedm20, licensed under the BSD License.


