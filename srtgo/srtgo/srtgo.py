# KTX
import base64
import itertools
import json
import re
import requests
import time
from time import sleep
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime, timedelta
from functools import reduce
# SRT
import abc
import json
import re
import requests
import time
from enum import Enum
from datetime import datetime
from typing import Dict, List, Pattern
# Main
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError
from random import gammavariate
from requests.exceptions import ConnectionError
from termcolor import colored
from typing import Awaitable, Callable, List, Optional, Tuple, Union

import asyncio
import click
import inquirer
import keyring
import telegram
import time
import re

import os
import keyring
import sys

# Ubuntu 환경에서는 SecretService 대신 파일 기반 Keyring 사용
try:
    from keyring.backends.file import PlaintextKeyring
except ImportError:
    from keyrings.alt.file import PlaintextKeyring  # keyrings.alt 사용

if os.name == "posix":  # Linux 환경인지 확인
    keyring.set_keyring(PlaintextKeyring())  # 파일 기반 Keyring 사용

# from .ktx import (
#     Korail,
#     KorailError,
#     ReserveOption,
#     TrainType,
#     AdultPassenger,
#     ChildPassenger, 
#     SeniorPassenger,
#     Disability1To3Passenger,
#     Disability4To6Passenger
# )

# from .srt import (
#     SRT,
#     SRTError,
#     SeatType,
#     Adult,
#     Child,
#     Senior,
#     Disability1To3,
#     Disability4To6
# )

# KTX
# Constants
KTX_EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
KTX_PHONE_NUMBER_REGEX = re.compile(r"(\d{3})-(\d{3,4})-(\d{4})")

KTX_USER_AGENT = "Dalvik/2.1.0 (Linux; U; Android 14; SM-S912N Build/UP1A.231005.007)"

KTX_DEFAULT_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent": KTX_USER_AGENT,
    "Host": "smart.letskorail.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

KORAIL_MOBILE = "https://smart.letskorail.com:443/classes/com.korail.mobile"
KTX_API_ENDPOINTS = {
    "login": f"{KORAIL_MOBILE}.login.Login",
    "logout": f"{KORAIL_MOBILE}.common.logout",

    "search_schedule": f"{KORAIL_MOBILE}.seatMovie.ScheduleView",

    "reserve": f"{KORAIL_MOBILE}.certification.TicketReservation",
    "cancel": f"{KORAIL_MOBILE}.reservationCancel.ReservationCancelChk",

    "myticketseat": f"{KORAIL_MOBILE}.refunds.SelTicketInfo",
    "myticketlist": f"{KORAIL_MOBILE}.myTicket.MyTicketList",
    "myreservationlist": f"{KORAIL_MOBILE}.reservation.ReservationView",

    "pay": f"{KORAIL_MOBILE}.payment.ReservationPayment",
    "refund": f"{KORAIL_MOBILE}.refunds.RefundsRequest",

    "code": f"{KORAIL_MOBILE}.common.code.do"
}
# SRT
# Constants
EMAIL_REGEX: Pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
PHONE_NUMBER_REGEX: Pattern = re.compile(r"(\d{3})-(\d{3,4})-(\d{4})")

USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 14; SM-S912N Build/UP1A.231005.007; wv) AppleWebKit/537.36"
    "(KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.260 Mobile Safari/537.36SRT-APP-Android V.2.0.33"
)

DEFAULT_HEADERS: Dict[str, str] = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
}

RESERVE_JOBID = {
    "PERSONAL": "1101",  # 개인예약
    "STANDBY": "1102",  # 예약대기
}

STATION_CODE = {
    "수서": "0551",
    "동탄": "0552", 
    "평택지제": "0553",
    "경주": "0508",
    "곡성": "0049",
    "공주": "0514",
    "광주송정": "0036",
    "구례구": "0050",
    "김천(구미)": "0507",
    "나주": "0037",
    "남원": "0048",
    "대전": "0010",
    "동대구": "0015",
    "마산": "0059",
    "목포": "0041",
    "밀양": "0017",
    "부산": "0020",
    "서대구": "0506",
    "순천": "0051",
    "여수EXPO": "0053",
    "여천": "0139",
    "오송": "0297",
    "울산(통도사)": "0509",
    "익산": "0030",
    "전주": "0045",
    "정읍": "0033",
    "진영": "0056",
    "진주": "0063",
    "창원": "0057",
    "창원중앙": "0512",
    "천안아산": "0502",
    "포항": "0515",
}

STATION_NAME = {code: name for name, code in STATION_CODE.items()}

TRAIN_NAME = {
    "00": "KTX",
    "02": "무궁화",
    "03": "통근열차", 
    "04": "누리로",
    "05": "전체",
    "07": "KTX-산천",
    "08": "ITX-새마을",
    "09": "ITX-청춘",
    "10": "KTX-산천",
    "17": "SRT",
    "18": "ITX-마음",
}

WINDOW_SEAT = {None: "000", True: "012", False: "013"}

SRT_MOBILE = "https://app.srail.or.kr:443"
API_ENDPOINTS = {
    "main": f"{SRT_MOBILE}/main/main.do",
    "login": f"{SRT_MOBILE}/apb/selectListApb01080_n.do",
    "logout": f"{SRT_MOBILE}/login/loginOut.do", 
    "search_schedule": f"{SRT_MOBILE}/ara/selectListAra10007_n.do",
    "reserve": f"{SRT_MOBILE}/arc/selectListArc05013_n.do",
    "tickets": f"{SRT_MOBILE}/atc/selectListAtc14016_n.do",
    "ticket_info": f"{SRT_MOBILE}/ard/selectListArd02019_n.do",
    "cancel": f"{SRT_MOBILE}/ard/selectListArd02045_n.do",
    "standby_option": f"{SRT_MOBILE}/ata/selectListAta01135_n.do",
    "payment": f"{SRT_MOBILE}/ata/selectListAta09036_n.do",
    "reserve_info": f"{SRT_MOBILE}/atc/getListAtc14087.do",
    "reserve_info_referer": f"{SRT_MOBILE}/common/ATC/ATC0201L/view.do?pnrNo=",
    "refund": f"{SRT_MOBILE}/atc/selectListAtc02063_n.do",
}
# MAIN


STATIONS = {
    "SRT": [
        "수서", "동탄", "평택지제", "경주", "곡성", "공주", "광주송정", "구례구", "김천(구미)",
        "나주", "남원", "대전", "동대구", "마산", "목포", "밀양", "부산", "서대구",
        "순천", "여수EXPO", "여천", "오송", "울산(통도사)", "익산", "전주",
        "정읍", "진영", "진주", "창원", "창원중앙", "천안아산", "포항"
    ],
    "KTX": [
        "서울", "용산", "영등포", "광명", "수원", "천안아산", "오송", "대전", "서대전",
        "김천구미", "동대구", "경주", "포항", "밀양", "구포", "부산", "울산(통도사)",
        "마산", "창원중앙", "경산", "논산", "익산", "정읍", "광주송정", "목포",
        "전주", "순천", "여수EXPO", "청량리", "강릉", "행신", "정동진"
    ]
}
DEFAULT_STATIONS = {
    "SRT": ['수서', '대전', '동대구', '부산'],
    "KTX": ['서울', '대전', '동대구', '부산']
}

# 예약 간격 (평균 간격 (초) = SHAPE * SCALE)
RESERVE_INTERVAL_SHAPE = 4
RESERVE_INTERVAL_SCALE = 0.25
RESERVE_INTERVAL_MIN = 0.5

WAITING_BAR = ["|", "/", "-", "\\"]

RailType = Union[str, None]
ChoiceType = Union[int, None]


@click.command()
@click.option("--debug", is_flag=True, help="Debug mode")
def srtgo(debug=False):
    MENU_CHOICES = [
        ("예매 시작", 1),
        ("예매 확인/취소", 2),
        ("로그인 설정", 3), 
        ("텔레그램 설정", 4),
        ("카드 설정", 5),
        ("역 설정", 6),
        ("역 직접 수정", 7),
        ("예매 옵션 설정", 8),
        ("나가기", -1)
    ]

    RAIL_CHOICES = [
        (colored("SRT", "red"), "SRT"),
        (colored("KTX", "cyan"), "KTX"),
        ("취소", -1)
    ]

    ACTIONS = {
        1: lambda rt: reserve(rt, debug),
        2: lambda rt: check_reservation(rt, debug),
        3: lambda rt: set_login(rt, debug),
        4: lambda _: set_telegram(),
        5: lambda _: set_card(),
        6: lambda rt: set_station(rt),
        7: lambda rt: edit_station(rt),
        8: lambda _: set_options()
    }

    while True:
        choice = inquirer.list_input(message="메뉴 선택", choices=MENU_CHOICES)
        sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
        sys.stdout.flush()

        if choice == -1:
            break

        if choice in {1, 2, 3, 6, 7}:
            rail_type = inquirer.list_input(
                message="열차 선택",
                choices=RAIL_CHOICES
            )
            if rail_type in {-1, None}:
                continue
        else:
            rail_type = None

        action = ACTIONS.get(choice)
        if action:
            action(rail_type)


def set_station(rail_type: RailType) -> bool:
    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    stations, default_station_key = get_station(rail_type)
    
    if not (station_info := inquirer.prompt([
        inquirer.Checkbox(
            "stations",
            message="역 선택", 
            choices=stations,
            default=default_station_key
        )
    ])):
        return False

    if not (selected := station_info["stations"]):
        print("선택된 역이 없습니다.")
        return False

    keyring.set_password(rail_type, "station", (selected_stations := ','.join(selected)))
    print(f"선택된 역: {selected_stations}")
    return True

def edit_station(rail_type: RailType) -> bool:
    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    stations, default_station_key = get_station(rail_type)
    station_info = inquirer.prompt([
        inquirer.Text("stations", message="역 수정 (예: 수서,대전,동대구)", default=keyring.get_password(rail_type, "station") or "")
    ])
    if not station_info:
        return False

    if not (selected := station_info["stations"]):
        print("선택된 역이 없습니다.")
        return False

    selected = [s.strip() for s in selected.split(',')]
    
    # Verify all stations contain Korean characters
    hangul = re.compile('[가-힣]+')
    for station in selected:
        if not hangul.search(station):
            print(f"'{station}'는 잘못된 입력입니다. 기본 역으로 설정합니다.")
            selected = DEFAULT_STATIONS[rail_type]
            break

    keyring.set_password(rail_type, "station", (selected_stations := ','.join(selected)))
    print(f"선택된 역: {selected_stations}")
    return True

def get_station(rail_type: RailType) -> Tuple[List[str], List[int]]:
    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    stations = STATIONS[rail_type]
    station_key = keyring.get_password(rail_type, "station")
    
    if not station_key:
        return stations, DEFAULT_STATIONS[rail_type]
        
    valid_keys = [x for x in station_key.split(',')]
    return stations, valid_keys


def set_options():
    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    default_options = get_options()
    choices = inquirer.prompt([
        inquirer.Checkbox(
            "options",
            message="예매 옵션 선택 (Space: 선택, Enter: 완료, Ctrl-A: 전체선택, Ctrl-R: 선택해제, Ctrl-C: 취소)",
            choices=[
                ("어린이", "child"),
                ("경로우대", "senior"),
                ("중증장애인", "disability1to3"),
                ("경증장애인", "disability4to6"),
                ("KTX만", "ktx")
            ],
            default=default_options
        )
    ])

    if choices is None:
        return
    
    options = choices.get("options", [])
    keyring.set_password("SRT", "options", ','.join(options))


def get_options():
    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    options = keyring.get_password("SRT", "options") or ""
    return options.split(',') if options else []


def set_telegram() -> bool:
    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    token = keyring.get_password("telegram", "token") or ""
    chat_id = keyring.get_password("telegram", "chat_id") or ""

    telegram_info = inquirer.prompt([
        inquirer.Text("token", message="텔레그램 token (Enter: 완료, Ctrl-C: 취소)", default=token),
        inquirer.Text("chat_id", message="텔레그램 chat_id (Enter: 완료, Ctrl-C: 취소)", default=chat_id)
    ])
    if not telegram_info:
        return False

    token, chat_id = telegram_info["token"], telegram_info["chat_id"]

    try:
        keyring.set_password("telegram", "ok", "1")
        keyring.set_password("telegram", "token", token)
        keyring.set_password("telegram", "chat_id", chat_id)
        tgprintf = get_telegram()
        asyncio.run(tgprintf("[SRTGO] 텔레그램 설정 완료"))
        return True
    except Exception as err:
        print(err)
        keyring.delete_password("telegram", "ok")
        return False


def get_telegram() -> Optional[Callable[[str], Awaitable[None]]]:
    token = keyring.get_password("telegram", "token")
    chat_id = keyring.get_password("telegram", "chat_id")

    async def tgprintf(text):
        if token and chat_id:
            bot = telegram.Bot(token=token)
            async with bot:
                await bot.send_message(chat_id=chat_id, text=text)

    return tgprintf


def set_card() -> None:
    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    card_info = {
        "number": keyring.get_password("card", "number") or "",
        "password": keyring.get_password("card", "password") or "",
        "birthday": keyring.get_password("card", "birthday") or "",
        "expire": keyring.get_password("card", "expire") or ""
    }

    card_info = inquirer.prompt([
        inquirer.Password("number", message="신용카드 번호 (하이픈 제외(-), Enter: 완료, Ctrl-C: 취소)", default=card_info["number"]),
        inquirer.Password("password", message="카드 비밀번호 앞 2자리 (Enter: 완료, Ctrl-C: 취소)", default=card_info["password"]),
        inquirer.Password("birthday", message="생년월일 (YYMMDD) / 사업자등록번호 (Enter: 완료, Ctrl-C: 취소)", default=card_info["birthday"]),
        inquirer.Password("expire", message="카드 유효기간 (YYMM, Enter: 완료, Ctrl-C: 취소)", default=card_info["expire"])
    ])
    if card_info:
        for key, value in card_info.items():
            keyring.set_password("card", key, value)
        keyring.set_password("card", "ok", "1")


def pay_card(rail, reservation) -> bool:
    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    if keyring.get_password("card", "ok"):
        birthday = keyring.get_password("card", "birthday")
        return rail.pay_with_card(
            reservation,
            keyring.get_password("card", "number"),
            keyring.get_password("card", "password"),
            birthday,
            keyring.get_password("card", "expire"),
            0,
            "J" if len(birthday) == 6 else "S"
        )
    return False


def set_login(rail_type="SRT", debug=False):
    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    credentials = {
        "id": keyring.get_password(rail_type, "id") or "",
        "pass": keyring.get_password(rail_type, "pass") or ""
    }

    login_info = inquirer.prompt([
        inquirer.Text("id", message=f"{rail_type} 계정 아이디 (멤버십 번호, 이메일, 전화번호)", default=credentials["id"]),
        inquirer.Password("pass", message=f"{rail_type} 계정 패스워드", default=credentials["pass"])
    ])
    if not login_info:
        return False

    try:
        SRT(login_info["id"], login_info["pass"], verbose=debug) if rail_type == "SRT" else Korail(
            login_info["id"], login_info["pass"], verbose=debug)
        
        keyring.set_password(rail_type, "id", login_info["id"])
        keyring.set_password(rail_type, "pass", login_info["pass"])
        keyring.set_password(rail_type, "ok", "1")
        return True
    except SRTError as err:
        print(err)
        keyring.delete_password(rail_type, "ok")
        return False


def login(rail_type="SRT", debug=False):
    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    if keyring.get_password(rail_type, "id") is None or keyring.get_password(rail_type, "pass") is None:
        set_login(rail_type)
    
    user_id = keyring.get_password(rail_type, "id")
    password = keyring.get_password(rail_type, "pass")
    
    rail = SRT if rail_type == "SRT" else Korail
    return rail(user_id, password, verbose=debug)




def reserve(rail_type="SRT", debug=False):

    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    rail = login(rail_type, debug=debug)
    is_srt = rail_type == "SRT"

    # Get date, time, stations, and passenger info
    now = datetime.now() + timedelta(minutes=10)
    today = now.strftime("%Y%m%d")
    this_time = now.strftime("%H%M%S")

    defaults = {
        "departure": keyring.get_password(rail_type, "departure") or ("수서" if is_srt else "서울"),
        "arrival": keyring.get_password(rail_type, "arrival") or "동대구",
        "date": keyring.get_password(rail_type, "date") or today,
        "time": keyring.get_password(rail_type, "time") or "120000",
        "adult": int(keyring.get_password(rail_type, "adult") or 1),
        "child": int(keyring.get_password(rail_type, "child") or 0),
        "senior": int(keyring.get_password(rail_type, "senior") or 0),
        "disability1to3": int(keyring.get_password(rail_type, "disability1to3") or 0),
        "disability4to6": int(keyring.get_password(rail_type, "disability4to6") or 0)
    }

    # Set default stations if departure equals arrival
    if defaults["departure"] == defaults["arrival"]:
        defaults["arrival"] = "동대구" if defaults["departure"] in ("수서", "서울") else None
        defaults["departure"] = defaults["departure"] if defaults["arrival"] else ("수서" if is_srt else "서울")

    stations, station_key = get_station(rail_type)
    options = get_options()
    
    # Generate date and time choices
    date_choices = [((now + timedelta(days=i)).strftime("%Y/%m/%d %a"), 
                    (now + timedelta(days=i)).strftime("%Y%m%d")) for i in range(28)]
    time_choices = [(f"{h:02d}", f"{h:02d}0000") for h in range(24)]

    # Build inquirer questions
    q_info = [
        # (↕:이동, Enter: 선택, Ctrl-C: 취소)
        inquirer.List("departure", message="출발역 선택", 
                     choices=station_key, default=defaults["departure"]),
        # (↕:이동, Enter: 선택, Ctrl-C: 취소)
        inquirer.List("arrival", message="도착역 선택", 
                     choices=station_key, default=defaults["arrival"]),
        # (↕:이동, Enter: 선택, Ctrl-C: 취소)
        inquirer.List("date", message="출발 날짜 선택", 
                     choices=date_choices, default=defaults["date"]),
        # (↕:이동, Enter: 선택, Ctrl-C: 취소)
        inquirer.List("time", message="출발 시각 선택", 
                     choices=time_choices, default=defaults["time"]),
        # (↕:이동, Enter: 선택, Ctrl-C: 취소)
        inquirer.List("adult", message="성인 승객수",
                     choices=range(10), default=defaults["adult"]),
    ]

    passenger_types = {
        "child": "어린이",
        "senior": "경로우대", 
        "disability1to3": "1~3급 장애인",
        "disability4to6": "4~6급 장애인"
    }

    passenger_classes = {
        "adult": Adult if is_srt else KTXAdultPassenger,
        "child": Child if is_srt else KTXChildPassenger,
        "senior": Senior if is_srt else KTXSeniorPassenger,
        "disability1to3": Disability1To3 if is_srt else KTXDisability1To3Passenger,
        "disability4to6": Disability4To6 if is_srt else KTXDisability4To6Passenger
    }

    PASSENGER_TYPE = {
        passenger_classes["adult"]: '어른/청소년',
        passenger_classes["child"]: '어린이',
        passenger_classes["senior"]: '경로우대',
        passenger_classes["disability1to3"]: '1~3급 장애인',
        passenger_classes["disability4to6"]: '4~6급 장애인',
    }

    # Add passenger type questions if enabled in options
    for key, label in passenger_types.items():
        if key in options:
            q_info.append(inquirer.List(key, 
                # (↕:이동, Enter: 선택, Ctrl-C: 취소)
                message=f"{label} 승객수",
                choices=range(10), default=defaults[key]))
    
    answers = {}

    for question in q_info:
        os.system("cls" if os.name == "nt" else "clear")  # 질문 전 화면 clear
        result = inquirer.prompt([question])  # 질문은 리스트로 넘겨야 함
        if result is None:
            print("사용자에 의해 취소되었습니다.")
            return
        answers.update(result)

    info = answers
          
    # info = inquirer.prompt(q_info)
    # Validate input info
    if not info:
        print(colored("예매 정보 입력 중 취소되었습니다", "green", "on_red") + "\n")
        return

    if info["departure"] == info["arrival"]:
        print(colored("출발역과 도착역이 같습니다", "green", "on_red") + "\n")
        return

    # Save preferences
    for key, value in info.items():
        keyring.set_password(rail_type, key, str(value))

    # Adjust time if needed
    if info["date"] == today and int(info["time"]) < int(this_time):
        info["time"] = this_time

    # Build passenger list
    passengers = []
    total_count = 0
    for key, cls in passenger_classes.items():
        if key in info and info[key] > 0:
            passengers.append(cls(info[key]))
            total_count += info[key]

    # Validate passenger count
    if not passengers:
        print(colored("승객수는 0이 될 수 없습니다", "green", "on_red") + "\n")
        return

    if total_count >= 10:
        print(colored("승객수는 10명을 초과할 수 없습니다", "green", "on_red") + "\n")
        return

    msg_passengers = [f'{PASSENGER_TYPE[type(passenger)]} {passenger.count}명' for passenger in passengers]
    print(*msg_passengers)

    # Search for trains
    params = {
        "dep": info["departure"],
        "arr": info["arrival"], 
        "date": info["date"],
        "time": info["time"],
        "passengers": [passenger_classes["adult"](total_count)],
        **({"available_only": False} if is_srt else {
            "include_no_seats": True,
            **({"train_type": KTXTrainType.KTX} if "ktx" in options else {})
        })
    }

    trains = rail.search_train(**params)

    def train_decorator(train):
        msg = train.__repr__()
        return msg.replace('예약가능', colored('가능', "green")) \
                 .replace('가능', colored('가능', "green")) \
                 .replace('신청하기', colored('가능', "green"))

    if not trains:
        print(colored("예약 가능한 열차가 없습니다", "green", "on_red") + "\n")
        return

    tmp_departure = info["departure"]
    tmp_arrival = info["arrival"]
    tmp_mon=info["date"][4:6]
    tmp_date=info["date"][6:]
    message = f"예약할 열차 선택 ({tmp_mon}월 {tmp_date}일) - {tmp_departure} > {tmp_arrival}"
    os.system("cls" if os.name == "nt" else "clear")  # 질문 전 화면 clear
    # Get train selection
    q_choice = [
        # (↕:이동, Space: 선택, Enter: 완료, Ctrl-A: 전체선택, Ctrl-R: 선택해제, Ctrl-C: 취소)
        inquirer.Checkbox("trains", message=message, 
                         choices=[(train_decorator(train), i) for i, train in enumerate(trains)], default=None),
    ]
    
    choice = inquirer.prompt(q_choice)
    if choice is None or not choice["trains"]:
        print(colored("선택한 열차가 없습니다!", "green", "on_red") + "\n")
        return
    
    n_trains = len(choice["trains"])

    # Get seat type preference
    seat_type = SeatType if is_srt else KTXReserveOption

    os.system("cls" if os.name == "nt" else "clear")  # 질문 전 화면 clear
    q_options = ([
        inquirer.List("type", message="선택 유형",
                        choices=[("일반실 우선", seat_type.GENERAL_FIRST),
                                ("일반실만", seat_type.GENERAL_ONLY), 
                                ("특실 우선", seat_type.SPECIAL_FIRST),
                                ("특실만", seat_type.SPECIAL_ONLY)]),
        inquirer.Confirm("pay", message="예매 시 카드 결제", default=False)
    ])

    options = inquirer.prompt(q_options)
    if options is None:
        print(colored("예매 정보 입력 중 취소되었습니다", "green", "on_red") + "\n")
        return

    # Reserve function
    def _reserve(train):
        sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
        sys.stdout.flush()
        reserve = rail.reserve(train, passengers=passengers, option=options["type"])
        msg = (f"{reserve}\n" + "\n".join(str(ticket) for ticket in reserve.tickets)) if is_srt else str(reserve).strip()

        print(colored(f"\n\n🎫 🎉 예매 성공!!! 🎉 🎫\n{msg}\n", "red", "on_green"))

        if options["pay"] and not reserve.is_waiting and pay_card(rail, reserve):
            print(colored("\n\n💳 ✨ 결제 성공!!! ✨ 💳\n\n", "green", "on_red"), end="")
            msg += "\n결제 완료"

        tgprintf = get_telegram()
        asyncio.run(tgprintf(msg))

    # Reservation loop
    i_try = 0
    start_time = time.time()
    while True:
        try:
            i_try += 1
            elapsed_time = time.time() - start_time
            hours, remainder = divmod(int(elapsed_time), 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"\r예매 대기 중... {WAITING_BAR[i_try & 3]} {i_try:4d} ({hours:02d}:{minutes:02d}:{seconds:02d}) ",
                end="", flush=True)

            trains = rail.search_train(**params)
            for i in choice["trains"]:
                if _is_seat_available(trains[i], options["type"], rail_type):
                    _reserve(trains[i])
                    return
            _sleep()

        except SRTError as ex:
            msg = ex.msg
            if "정상적인 경로로 접근 부탁드립니다" in msg:
                if debug:
                    print(f"\nException: {ex}\nType: {type(ex)}\nArgs: {ex.args}\nMessage: {msg}")
                rail.clear()
            elif "로그인 후 사용하십시오" in msg:
                if debug:
                    print(f"\nException: {ex}\nType: {type(ex)}\nArgs: {ex.args}\nMessage: {msg}")
                rail = login(rail_type, debug=debug)
                if not rail.is_login and not _handle_error(ex):
                    return
            elif not any(err in msg for err in ("잔여석없음", "사용자가 많아 접속이 원활하지 않습니다", 
                                              "예약대기 접수가 마감되었습니다", "예약대기자한도수초과")):
                if not _handle_error(ex):
                    return
            _sleep()

        except KorailError as ex:
            if not any(msg in str(ex) for msg in ("Sold out", "잔여석없음", "예약대기자한도수초과")):
                if not _handle_error(ex):
                    return
            _sleep()

        except JSONDecodeError as ex:
            if debug:
                print(f"\nException: {ex}\nType: {type(ex)}\nArgs: {ex.args}\nMessage: {ex.msg}")
            _sleep()
            rail = login(rail_type, debug=debug)
        
        except ConnectionError as ex:
            if not _handle_error(ex, "연결이 끊겼습니다"):
                return
            rail = login(rail_type, debug=debug)

        except Exception as ex:
            if debug:
                print("\nUndefined exception")
            if not _handle_error(ex):
                return
            rail = login(rail_type, debug=debug)

def _sleep():
    time.sleep(gammavariate(RESERVE_INTERVAL_SHAPE, RESERVE_INTERVAL_SCALE) + RESERVE_INTERVAL_MIN)

def _handle_error(ex, msg=None):
    msg = msg or f"\nException: {ex}, Type: {type(ex)}, Message: {ex.msg if hasattr(ex, 'msg') else 'No message attribute'}"
    print(msg)
    tgprintf = get_telegram()
    asyncio.run(tgprintf(msg))
    return inquirer.confirm(message="계속할까요", default=True)

def _is_seat_available(train, seat_type, rail_type):
    if rail_type == "SRT":
        if not train.seat_available():
            return train.reserve_standby_available()
        if seat_type in [SeatType.GENERAL_FIRST, SeatType.SPECIAL_FIRST]:
            return train.seat_available()
        if seat_type == SeatType.GENERAL_ONLY:
            return train.general_seat_available()
        return train.special_seat_available()
    else:
        if not train.has_seat():
            return train.has_waiting_list()
        if seat_type in [KTXReserveOption.GENERAL_FIRST, KTXReserveOption.SPECIAL_FIRST]:
            return train.has_seat()
        if seat_type == KTXReserveOption.GENERAL_ONLY:
            return train.has_general_seat()
        return train.has_special_seat()


def check_reservation(rail_type="SRT", debug=False):
    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    rail = login(rail_type, debug=debug)

    while True:
        reservations = rail.get_reservations() if rail_type == "SRT" else rail.reservations()
        tickets = [] if rail_type == "SRT" else rail.tickets()

        all_reservations = []
        for t in tickets:
            t.is_ticket = True
            all_reservations.append(t)
        for r in reservations:
            if hasattr(r, "paid") and r.paid:
                r.is_ticket = True
            else:
                r.is_ticket = False
            all_reservations.append(r)

        if not reservations and not tickets:
            print(colored("예약 내역이 없습니다", "green", "on_red") + "\n")
            return

        cancel_choices = [
            (str(reservation), i) for i, reservation in enumerate(all_reservations)
        ] + [("텔레그램으로 예매 정보 전송", -2), ("돌아가기", -1)]
        
        cancel = inquirer.list_input(
            message="예약 취소 (Enter: 결정)",
            choices=cancel_choices
        )

        if cancel in (None, -1):
            return

        if cancel == -2:
            out = []
            if all_reservations:
                out.append("[ 예매 내역 ]")
                for reservation in all_reservations:
                    out.append(f"🚅{reservation}")
                    if rail_type == "SRT":
                        out.extend(map(str, reservation.tickets))
            
            if out:
                tgprintf = get_telegram()
                asyncio.run(tgprintf("\n".join(out)))
            return

        if inquirer.confirm(message=colored("정말 취소하시겠습니까", "green", "on_red")):
            try:
                if all_reservations[cancel].is_ticket:
                    rail.refund(all_reservations[cancel])
                else:
                    rail.cancel(all_reservations[cancel])
            except Exception as err:
                raise err
            return
# KTX Start
# Schedule classes
class KTXSchedule:
    """Base class for train schedules"""
    def __init__(self, data):
        self.train_type = data.get('h_trn_clsf_cd')
        self.train_type_name = data.get('h_trn_clsf_nm')
        self.train_group = data.get('h_trn_gp_cd')
        self.train_no = data.get('h_trn_no')
        self.delay_time = data.get('h_expct_dlay_hr')

        self.dep_name = data.get('h_dpt_rs_stn_nm')
        self.dep_code = data.get('h_dpt_rs_stn_cd')
        self.dep_date = data.get('h_dpt_dt')
        self.dep_time = data.get('h_dpt_tm')

        self.arr_name = data.get('h_arv_rs_stn_nm')
        self.arr_code = data.get('h_arv_rs_stn_cd')
        self.arr_date = data.get('h_arv_dt')
        self.arr_time = data.get('h_arv_tm')

        self.run_date = data.get('h_run_dt')

    def __repr__(self):
        dep_time = f"{self.dep_time[:2]}:{self.dep_time[2:4]}"
        arr_time = f"{self.arr_time[:2]}:{self.arr_time[2:4]}"
        return f'[{self.train_type_name[:3]}-{self.train_no}]\t{dep_time} ~ {arr_time} /'

class KTXTrain(KTXSchedule):
    """Train schedule with seat availability"""
    def __init__(self, data):
        super().__init__(data)
        self.reserve_possible = data.get('h_rsv_psb_flg')
        self.reserve_possible_name = data.get('h_rsv_psb_nm')
        self.special_seat = data.get('h_spe_rsv_cd')
        self.general_seat = data.get('h_gen_rsv_cd')
        self.wait_reserve_flag = data.get('h_wait_rsv_flg')
        if self.wait_reserve_flag:
            self.wait_reserve_flag = int(self.wait_reserve_flag)

    def __repr__(self):
        repr_str = super().__repr__()
        if self.reserve_possible_name:
            repr_str += f" 특실 {'가능' if self.has_special_seat() else '매진'}"
            repr_str += f", 일반실 {'가능' if self.has_general_seat() else '매진'}"
            if self.wait_reserve_flag >= 0:
                repr_str += f", 예약대기 {'가능' if self.has_general_waiting_list() else '매진'}"
        return repr_str

    def has_special_seat(self):
        return self.special_seat == '11'

    def has_general_seat(self):
        return self.general_seat == '11'

    def has_seat(self):
        return self.has_general_seat() or self.has_special_seat()

    def has_waiting_list(self):
        return self.has_general_waiting_list()

    def has_general_waiting_list(self):
        return self.wait_reserve_flag == 9

class KTXTicket(KTXTrain):
    """Train ticket information"""
    def __init__(self, data):
        raw_data = data['ticket_list'][0]['train_info'][0]
        super().__init__(raw_data)
        self.seat_no_end = raw_data.get('h_seat_no_end')
        self.seat_no_count = int(raw_data.get('h_seat_cnt'))
        self.buyer_name = raw_data.get('h_buy_ps_nm')
        self.sale_date = raw_data.get('h_orgtk_sale_dt')
        self.pnr_no = raw_data.get('h_pnr_no')
        self.sale_info1 = raw_data.get('h_orgtk_wct_no')
        self.sale_info2 = raw_data.get('h_orgtk_ret_sale_dt')
        self.sale_info3 = raw_data.get('h_orgtk_sale_sqno')
        self.sale_info4 = raw_data.get('h_orgtk_ret_pwd')
        self.price = int(raw_data.get('h_rcvd_amt'))
        self.car_no = raw_data.get('h_srcar_no')
        self.seat_no = raw_data.get('h_seat_no')

    def __repr__(self):
        repr_str = super(KTXTrain, self).__repr__()
        repr_str += f" => {self.car_no}호"
        if int(self.seat_no_count) != 1:
            repr_str += f" {self.seat_no}~{self.seat_no_end}"
        else:
            repr_str += f" {self.seat_no}"
        repr_str += f", {self.price}원"
        return repr_str

    def get_ticket_no(self):
        return "-".join(map(str, (self.sale_info1, self.sale_info2, self.sale_info3, self.sale_info4)))

class KTXReservation(KTXTrain):
    """Train reservation information"""
    def __init__(self, data):
        super().__init__(data)
        self.dep_date = data.get('h_run_dt')
        self.arr_date = data.get('h_run_dt')
        self.rsv_id = data.get('h_pnr_no')
        self.seat_no_count = int(data.get('h_tot_seat_cnt'))
        self.buy_limit_date = data.get('h_ntisu_lmt_dt')
        self.buy_limit_time = data.get('h_ntisu_lmt_tm')
        self.price = int(data.get('h_rsv_amt'))
        self.journey_no = data.get('txtJrnySqno', "001")
        self.journey_cnt = data.get('txtJrnyCnt', "01")
        self.rsv_chg_no = data.get('hidRsvChgNo', "00000")
        self.is_waiting = self.buy_limit_date == "00000000" or self.buy_limit_time == "235959"

    def __repr__(self):
        repr_str = super().__repr__()
        repr_str += f", {self.price}원({self.seat_no_count}석)"
        if self.is_waiting:
            repr_str += ", 예약대기"
        else:
            buy_limit_time = f"{self.buy_limit_time[:2]}:{self.buy_limit_time[2:4]}"
            buy_limit_date = f"{int(self.buy_limit_date[4:6])}월 {int(self.buy_limit_date[6:])}일"
            repr_str += f", 구입기한 {buy_limit_date} {buy_limit_time}"
        return repr_str


# Passenger classes
class KTXPassenger:
    """Base class for passengers"""
    def __init_internal__(self, typecode, count=1, discount_type='000', card='', card_no='', card_pw=''):
        self.typecode = typecode
        self.count = count
        self.discount_type = discount_type
        self.card = card
        self.card_no = card_no
        self.card_pw = card_pw

    @staticmethod
    def reduce(passenger_list):
        if not all(isinstance(x, KTXPassenger) for x in passenger_list):
            raise TypeError("Passengers must be based on Passenger")
        groups = itertools.groupby(passenger_list, lambda x: x.group_key())
        return list(filter(lambda x: x.count > 0, [reduce(lambda a, b: a + b, g) for k, g in groups]))

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Cannot add different passenger types")
        if self.group_key() != other.group_key():
            raise TypeError(f"Cannot add passengers with different group keys: {self.group_key()} vs {other.group_key()}")
        return self.__class__(count=self.count + other.count, discount_type=self.discount_type,
                            card=self.card, card_no=self.card_no, card_pw=self.card_pw)

    def group_key(self):
        return f"{self.typecode}_{self.discount_type}_{self.card}_{self.card_no}_{self.card_pw}"

    def get_dict(self, index):
        index = str(index)
        return {
            f'txtPsgTpCd{index}': self.typecode,
            f'txtDiscKndCd{index}': self.discount_type,
            f'txtCompaCnt{index}': self.count,
            f'txtCardCode_{index}': self.card,
            f'txtCardNo_{index}': self.card_no,
            f'txtCardPw_{index}': self.card_pw,
        }

class KTXAdultPassenger(KTXPassenger):
    def __init__(self, count=1, discount_type='000', card='', card_no='', card_pw=''):
        KTXPassenger.__init_internal__(self, '1', count, discount_type, card, card_no, card_pw)

class KTXChildPassenger(KTXPassenger):
    def __init__(self, count=1, discount_type='000', card='', card_no='', card_pw=''):
        KTXPassenger.__init_internal__(self, '3', count, discount_type, card, card_no, card_pw)

class KTXToddlerPassenger(KTXPassenger):
    def __init__(self, count=1, discount_type='321', card='', card_no='', card_pw=''):
        KTXPassenger.__init_internal__(self, '3', count, discount_type, card, card_no, card_pw)

class KTXSeniorPassenger(KTXPassenger):
    def __init__(self, count=1, discount_type='131', card='', card_no='', card_pw=''):
        KTXPassenger.__init_internal__(self, '1', count, discount_type, card, card_no, card_pw)

class KTXDisability1To3Passenger(KTXPassenger):
    def __init__(self, count=1, discount_type='111', card='', card_no='', card_pw=''):
        KTXPassenger.__init_internal__(self, '1', count, discount_type, card, card_no, card_pw)   

class KTXDisability4To6Passenger(KTXPassenger):
    def __init__(self, count=1, discount_type='112', card='', card_no='', card_pw=''):
        KTXPassenger.__init_internal__(self, '1', count, discount_type, card, card_no, card_pw)   


# Options
class KTXTrainType:
    KTX = "100"
    SAEMAEUL = "101"
    MUGUNGHWA = "102"
    TONGGUEN = "103"
    NURIRO = "102"
    ALL = "109"
    AIRPORT = "105"
    KTX_SANCHEON = "100"
    ITX_SAEMAEUL = "101"
    ITX_CHEONGCHUN = "104"

class KTXReserveOption:
    GENERAL_FIRST = "GENERAL_FIRST"
    GENERAL_ONLY = "GENERAL_ONLY"
    SPECIAL_FIRST = "SPECIAL_FIRST"
    SPECIAL_ONLY = "SPECIAL_ONLY"


# Korail errors
class KorailError(Exception):
    """Base class for Korail errors"""
    def __init__(self, msg, code=None):
        self.msg = msg
        self.code = code

    def __str__(self):
        return f"{self.msg} ({self.code})"

class NeedToLoginError(KorailError):
    codes = {'P058'}
    def __init__(self, code=None):
        super().__init__("Need to Login", code)

class NoResultsError(KorailError):
    codes = {'P100', 'WRG000000', 'WRD000061', 'WRT300005'}
    def __init__(self, code=None):
        super().__init__("No Results", code)

class SoldOutError(KorailError):
    codes = {'IRT010110', 'ERR211161'}
    def __init__(self, code=None):
        super().__init__("Sold out", code)
    
class NetFunnelError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


# NetFunnel
class KTXNetFunnelHelper:
    NETFUNNEL_URL = "http://nf.letskorail.com/ts.wseq"

    WAIT_STATUS_PASS = "200"
    WAIT_STATUS_FAIL = "201" 
    ALREADY_COMPLETED = "502"

    OP_CODE = {
        "getTidchkEnter": "5101",
        "chkEnter": "5002", 
        "setComplete": "5004",
    }

    KTX_DEFAULT_HEADERS = {
        "Host": "nf.letskorail.com",
        "Connection": "Keep-Alive", 
        "User-Agent": "Apache-HttpClient/UNAVAILABLE (java 1.4)"
    }

    def __init__(self):
        self._session = requests.session()
        self._session.headers.update(self.KTX_DEFAULT_HEADERS)
        self._cached_key = None
        self._last_fetch_time = 0
        self._cache_ttl = 50  # 50 seconds

    def run(self):
        current_time = time.time()
        if self._is_cache_valid(current_time):
            return self._cached_key

        try:
            status, self._cached_key, nwait = self._start()
            self._last_fetch_time = current_time

            while status == self.WAIT_STATUS_FAIL:
                print(f"\r현재 {nwait}명 대기중...", end="", flush=True)
                time.sleep(1)
                status, self._cached_key, nwait = self._check()
            
            # Try completing once
            status, _, _ = self._complete()
            if status == self.WAIT_STATUS_PASS or status == self.ALREADY_COMPLETED:
                return self._cached_key

            self.clear()
            raise NetFunnelError("Failed to complete NetFunnel")

        except Exception as ex:
            self.clear()
            raise NetFunnelError(str(ex))

    def clear(self):
        self._cached_key = None
        self._last_fetch_time = 0

    def _start(self):
        return self._make_request("getTidchkEnter")

    def _check(self):
        return self._make_request("chkEnter")

    def _complete(self):
        return self._make_request("setComplete")

    def _make_request(self, opcode: str):
        params = self._build_params(self.OP_CODE[opcode])
        response = self._parse(self._session.get(self.NETFUNNEL_URL, params=params).text)
        return response.get("status"), response.get("key"), response.get("nwait")

    def _build_params(self, opcode: str, key: str = None) -> dict:
        params = {"opcode": opcode}

        if opcode in (self.OP_CODE["getTidchkEnter"], self.OP_CODE["chkEnter"]):
            params.update({"sid": "service_1", "aid": "act_8"})
            if opcode == self.OP_CODE["chkEnter"]:
                params.update({"key": key or self._cached_key, "ttl": "1"})
        elif opcode == self.OP_CODE["setComplete"]:
            params["key"] = key or self._cached_key

        return params

    def _parse(self, response: str) -> dict:
        status, params_str = response.split(":", 1)
        if not params_str:
            raise NetFunnelError("Failed to parse NetFunnel response")

        params = dict(param.split("=", 1) for param in params_str.split("&") if "=" in param)
        params["status"] = status
        return params

    def _is_cache_valid(self, current_time: float) -> bool:
        return bool(self._cached_key and (current_time - self._last_fetch_time) < self._cache_ttl)


class Korail:
    """Main Korail API interface"""
    def __init__(self, korail_id, korail_pw, auto_login=True, verbose=False):
        self._session = requests.session()
        self._session.headers.update(KTX_DEFAULT_HEADERS)
        self._device = 'AD'
        self._version = '240531001'
        self._key = 'korail1234567890'
        self._idx = None
        self.korail_id = korail_id
        self.korail_pw = korail_pw
        self.verbose = verbose
        self.logined = False
        self.membership_number = None
        self.name = None
        self.email = None
        self.phone_number = None
        if auto_login:
            self.login(korail_id, korail_pw)
    
    def _log(self, msg: str) -> None:
        if self.verbose:
            print(f"[*] {msg}")

    def __enc_password(self, password):
        url = KTX_API_ENDPOINTS["code"]
        data = {'code': "app.login.cphd"}
        r = self._session.post(url, data=data)
        j = json.loads(r.text)

        if j['strResult'] == 'SUCC' and j.get('app.login.cphd'):
            self._idx = j['app.login.cphd']['idx']
            key = j['app.login.cphd']['key']
            encrypt_key = key.encode('utf-8')
            iv = key[:16].encode('utf-8')
            cipher = AES.new(encrypt_key, AES.MODE_CBC, iv)
            padded_data = pad(password.encode("utf-8"), AES.block_size)
            return base64.b64encode(base64.b64encode(cipher.encrypt(padded_data))).decode("utf-8")
        return False

    def login(self, korail_id=None, korail_pw=None):
        if korail_id:
            self.korail_id = korail_id
        if korail_pw:
            self.korail_pw = korail_pw

        txt_input_flg = '5' if KTX_EMAIL_REGEX.match(self.korail_id) else '4' if KTX_PHONE_NUMBER_REGEX.match(self.korail_id) else '2'

        data = {
            'Device': self._device,
            'Version': self._version,
            'Key': self._key,
            'txtMemberNo': self.korail_id,
            'txtPwd': self.__enc_password(self.korail_pw),
            'txtInputFlg': txt_input_flg,
            'idx': self._idx
        }

        r = self._session.post(KTX_API_ENDPOINTS["login"], data=data)
        self._log(r.text)
        j = json.loads(r.text)

        if j['strResult'] == 'SUCC' and j.get('strMbCrdNo'):
            # self._key = j['Key']
            self.membership_number = j['strMbCrdNo']
            self.name = j['strCustNm']
            self.email = j['strEmailAdr']
            self.phone_number = j['strCpNo']
            print(f"로그인 성공: {self.name} (멤버십번호: {self.membership_number}, 전화번호: {self.phone_number})")
            self.logined = True
            return True
        self.logined = False
        return False

    def logout(self):
        r = self._session.get(KTX_API_ENDPOINTS["logout"])
        self._log(r.text)
        self.logined = False

    def _result_check(self, j):
        if j.get('strResult') == 'FAIL':
            h_msg_cd = j.get('h_msg_cd')
            h_msg_txt = j.get('h_msg_txt')
            for error in (NoResultsError, NeedToLoginError, SoldOutError):
                if h_msg_cd in error.codes:
                    raise error(h_msg_cd)
            raise KorailError(h_msg_txt, h_msg_cd)
        return True

    def search_train(self, dep, arr, date=None, time=None, train_type=KTXTrainType.ALL,
                    passengers=None, include_no_seats=False, include_waiting_list=False):
        kst_now = datetime.now() + timedelta(hours=9)
        date = date or kst_now.strftime("%Y%m%d")
        time = time or kst_now.strftime("%H%M%S")
        passengers = passengers or [KTXAdultPassenger()]
        passengers = KTXPassenger.reduce(passengers)

        counts = {
            'adult': sum(p.count for p in passengers if isinstance(p, KTXAdultPassenger)),
            'child': sum(p.count for p in passengers if isinstance(p, KTXChildPassenger)),
            'toddler': sum(p.count for p in passengers if isinstance(p, KTXToddlerPassenger)),
            'senior': sum(p.count for p in passengers if isinstance(p, KTXSeniorPassenger)),
            'disability1to3': sum(p.count for p in passengers if isinstance(p, KTXDisability1To3Passenger)),
            'disability4to6': sum(p.count for p in passengers if isinstance(p, KTXDisability4To6Passenger)),
        }

        data = {
            'Device': self._device,
            'Version': self._version,
            'Sid': '',
            'txtMenuId': '11',
            'radJobId': '1',
            'selGoTrain': train_type,
            'txtTrnGpCd': train_type,
            'txtGoStart': dep,
            'txtGoEnd': arr,
            'txtGoAbrdDt': date,
            'txtGoHour': time,
            'txtPsgFlg_1': counts['adult'],
            'txtPsgFlg_2': counts['child'] + counts['toddler'],
            'txtPsgFlg_3': counts['senior'],
            'txtPsgFlg_4': counts['disability1to3'],
            'txtPsgFlg_5': counts['disability4to6'],
            'txtSeatAttCd_2': '000',
            'txtSeatAttCd_3': '000',
            'txtSeatAttCd_4': '015',
            'ebizCrossCheck': 'N',
            'srtCheckYn': 'N', # SRT 함께 보기
            'rtYn': 'N', # 왕복
            'adjStnScdlOfrFlg': 'N', # 인접역 보기
            'mbCrdNo': self.membership_number
        }

        r = self._session.get(KTX_API_ENDPOINTS["search_schedule"], params=data)
        self._log(r.text)
        j = json.loads(r.text)

        if self._result_check(j):
            trains = [KTXTrain(info) for info in j.get('trn_infos', {}).get('trn_info', [])]
            filter_fns = [lambda x: x.has_seat()]

            if include_no_seats:
                filter_fns.append(lambda x: not x.has_seat())
            if include_waiting_list:
                filter_fns.append(lambda x: x.has_waiting_list())

            trains = [t for t in trains if any(f(t) for f in filter_fns)]

            if not trains:
                raise NoResultsError()

            return trains

    def reserve(self, train, passengers=None, option=KTXReserveOption.GENERAL_FIRST):
        reserving_seat = train.has_seat() or train.wait_reserve_flag < 0
        if reserving_seat:
            is_special_seat = {
                KTXReserveOption.GENERAL_ONLY: False,
                KTXReserveOption.SPECIAL_ONLY: True,
                KTXReserveOption.GENERAL_FIRST: not train.has_general_seat(),
                KTXReserveOption.SPECIAL_FIRST: train.has_special_seat(),
            }[option]
        else:
            is_special_seat = {
                KTXReserveOption.GENERAL_ONLY: False,
                KTXReserveOption.SPECIAL_ONLY: True,
                KTXReserveOption.GENERAL_FIRST: False,
                KTXReserveOption.SPECIAL_FIRST: True,
            }[option]

        passengers = passengers or [KTXAdultPassenger()]
        passengers = KTXPassenger.reduce(passengers)
        cnt = sum(p.count for p in passengers)

        data = {
            'Device': self._device,
            'Version': self._version,
            'Key': self._key,
            'txtMenuId': '11',
            'txtJobId': '1101' if reserving_seat else '1102',
            'txtGdNo': '',
            'hidFreeFlg': 'N',
            'txtTotPsgCnt': cnt,
            'txtSeatAttCd1': '000',
            'txtSeatAttCd2': '000',
            'txtSeatAttCd3': '000',
            'txtSeatAttCd4': '015',
            'txtSeatAttCd5': '000',
            'txtStndFlg': 'N',
            'txtSrcarCnt': '0',
            'txtJrnyCnt': '1',
            'txtJrnySqno1': '001',
            'txtJrnyTpCd1': '11',
            'txtDptDt1': train.dep_date,
            'txtDptRsStnCd1': train.dep_code,
            'txtDptTm1': train.dep_time,
            'txtArvRsStnCd1': train.arr_code,
            'txtTrnNo1': train.train_no,
            'txtRunDt1': train.run_date,
            'txtTrnClsfCd1': train.train_type,
            'txtTrnGpCd1': train.train_group,
            'txtPsrmClCd1': '2' if is_special_seat else '1',
            'txtChgFlg1': '',
            'txtJrnySqno2': '',
            'txtJrnyTpCd2': '',
            'txtDptDt2': '',
            'txtDptRsStnCd2': '',
            'txtDptTm2': '',
            'txtArvRsStnCd2': '',
            'txtTrnNo2': '',
            'txtRunDt2': '',
            'txtTrnClsfCd2': '',
            'txtPsrmClCd2': '',
            'txtChgFlg2': '',
        }

        for i, psg in enumerate(passengers, 1):
            data.update(psg.get_dict(i))

        r = self._session.get(KTX_API_ENDPOINTS["reserve"], params=data)
        self._log(r.text)
        j = json.loads(r.text)
        if self._result_check(j):
            rsv_id = j.get('h_pnr_no')
            wct_no = j.get('h_wct_no')
            reservation = self.reservations(rsv_id)
            reservation.wct_no = wct_no
            return reservation
        else:
            raise SoldOutError()

    def tickets(self):
        data = {
            'Device': self._device,
            'Version': self._version,
            'Key': self._key,
            'txtDeviceId': '',
            'txtIndex': '1',
            'h_page_no': '1',
            'h_abrd_dt_from': '',
            'h_abrd_dt_to': '',
            'hiduserYn': 'Y'
        }

        r = self._session.get(KTX_API_ENDPOINTS["myticketlist"], params=data)
        self._log(r.text)
        j = json.loads(r.text)
        try:
            if self._result_check(j):
                tickets = []
                for info in j.get('reservation_list', []):
                    ticket = KTXTicket(info)
                    data = {
                        'Device': self._device,
                        'Version': self._version,
                        'Key': self._key,
                        'h_orgtk_wct_no': ticket.sale_info1,
                        'h_orgtk_ret_sale_dt': ticket.sale_info2,
                        'h_orgtk_sale_sqno': ticket.sale_info3,
                        'h_orgtk_ret_pwd': ticket.sale_info4,
                    }
                    r = self._session.get(KTX_API_ENDPOINTS["myticketseat"], params=data)
                    j = json.loads(r.text)
                    if self._result_check(j):
                        seat = j.get('ticket_infos', {}).get('ticket_info', [{}])[0].get('tk_seat_info', [{}])[0]
                        ticket.seat_no = seat.get('h_seat_no')
                        ticket.seat_no_end = None
                    tickets.append(ticket)
                return tickets
        except NoResultsError:
            return []

    def reservations(self, rsv_id=None):
        data = {
            'Device': self._device,
            'Version': self._version,
            'Key': self._key,
        }
        r = self._session.get(KTX_API_ENDPOINTS["myreservationlist"], params=data)
        self._log(r.text)
        j = json.loads(r.text)
        try:
            if not self._result_check(j):
                return []
                
            jrny_info = j.get('jrny_infos', {}).get('jrny_info', [])
            reserves = []
            
            for info in jrny_info:
                train_info = info.get('train_infos', {}).get('train_info', [])
                for tinfo in train_info:
                    reservation = KTXReservation(tinfo)
                    if rsv_id and reservation.rsv_id == rsv_id:
                        return reservation
                    reserves.append(reservation)
            return reserves
            
        except NoResultsError:
            return []

    def pay_with_card(self, rsv, card_number, card_password, birthday, card_expire, installment=0, card_type='J'):
        if not isinstance(rsv, KTXReservation):
            raise TypeError("rsv must be a Reservation instance")

        data = {
            'Device': self._device,
            'Version': self._version,
            'Key': self._key,
            'hidPnrNo': rsv.rsv_id,
            'hidWctNo': rsv.wct_no,
            'hidTmpJobSqno1': '000000',
            'hidTmpJobSqno2': '000000',
            'hidRsvChgNo': '000',
            'hidInrecmnsGridcnt': '1',
            'hidStlMnsSqno1': '1',
            'hidStlMnsCd1': '02',
            'hidMnsStlAmt1': str(rsv.price),
            'hidCrdInpWayCd1': '@',
            'hidStlCrCrdNo1': card_number,
            'hidVanPwd1': card_password,
            'hidCrdVlidTrm1': card_expire,
            'hidIsmtMnthNum1': installment,
            'hidAthnDvCd1': card_type,
            'hidAthnVal1': birthday,
            'hiduserYn': 'Y'
        }

        r = self._session.post(KTX_API_ENDPOINTS["pay"], data=data)
        self._log(r.text)
        j = json.loads(r.text)
        if self._result_check(j):
            return True
        return False

    def cancel(self, rsv):
        if not isinstance(rsv, KTXReservation):
            raise TypeError("rsv must be a Reservation instance")
        data = {
            'Device': self._device,
            'Version': self._version,
            'Key': self._key,
            'txtPnrNo': rsv.rsv_id,
            'txtJrnySqno': rsv.journey_no,
            'txtJrnyCnt': rsv.journey_cnt,
            'hidRsvChgNo': rsv.rsv_chg_no,
        }
        r = self._session.post(KTX_API_ENDPOINTS["cancel"], data=data)
        self._log(r.text)
        j = json.loads(r.text)
        return self._result_check(j)

    def refund(self, ticket):
        data = {
            'Device': self._device,
            'Version': self._version,
            'Key': self._key,
            'txtPrnNo': ticket.pnr_no,
            'h_orgtk_sale_dt': ticket.sale_info2,
            'h_orgtk_sale_wct_no': ticket.sale_info1,
            'h_orgtk_sale_sqno': ticket.sale_info3,
            'h_orgtk_ret_pwd': ticket.sale_info4,
            'h_mlg_stl': 'N',
            'tk_ret_tms_dv_cd': '21',
            'trnNo': ticket.train_no,
            'pbpAcepTgtFlg': 'N',
            'latitude': '',
            'longitude': ""
        }
        r = self._session.post(KTX_API_ENDPOINTS["refund"], data=data)
        self._log(r.text)
        j = json.loads(r.text)
        return self._result_check(j)

# KTX End

# SRT Start
# Exception classes
class SRTError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

    def __str__(self):
        return self.msg

class SRTLoginError(SRTError):
    pass

class SRTResponseError(SRTError):
    pass

class SRTDuplicateError(SRTResponseError):
    pass

class SRTNotLoggedInError(SRTError):
    pass

class SRTNetFunnelError(SRTError):
    pass


# Passenger class
class Passenger(metaclass=abc.ABCMeta):
    """Base class for different passenger types."""

    @abc.abstractmethod
    def __init__(self):
        pass

    def __init_internal__(self, name: str, type_code: str, count: int):
        self.name = name
        self.type_code = type_code
        self.count = count

    def __repr__(self) -> str:
        return f"{self.name} {self.count}명"

    def __add__(self, other: "Passenger") -> "Passenger":
        if not isinstance(other, self.__class__):
            raise TypeError("Passenger types must be the same")
        if self.type_code == other.type_code:
            return self.__class__(count=self.count + other.count)
        raise ValueError("Passenger types must be the same")

    @classmethod
    def combine(cls, passengers: List["Passenger"]) -> List["Passenger"]:
        if not all(isinstance(p, Passenger) for p in passengers):
            raise TypeError("All passengers must be based on Passenger")

        passenger_dict = {}
        for passenger in passengers:
            key = passenger.__class__
            passenger_dict[key] = passenger_dict.get(key, passenger.__class__(0)) + passenger

        return [p for p in passenger_dict.values() if p.count > 0]

    @staticmethod
    def total_count(passengers: List["Passenger"]) -> str:
        if not all(isinstance(p, Passenger) for p in passengers):
            raise TypeError("All passengers must be based on Passenger")
        return str(sum(p.count for p in passengers))

    @staticmethod
    def get_passenger_dict(
        passengers: List["Passenger"],
        special_seat: bool = False,
        window_seat: str = None
    ) -> Dict[str, str]:
        if not all(isinstance(p, Passenger) for p in passengers):
            raise TypeError("All passengers must be instances of Passenger")

        combined_passengers = Passenger.combine(passengers)
        data = {
            "totPrnb": Passenger.total_count(combined_passengers),
            "psgGridcnt": str(len(combined_passengers)),
            "locSeatAttCd1": WINDOW_SEAT.get(window_seat, "000"),
            "rqSeatAttCd1": "015",
            "dirSeatAttCd1": "009",
            "smkSeatAttCd1": "000",
            "etcSeatAttCd1": "000",
            "psrmClCd1": "2" if special_seat else "1"
        }

        for i, passenger in enumerate(combined_passengers, start=1):
            data[f"psgTpCd{i}"] = passenger.type_code
            data[f"psgInfoPerPrnb{i}"] = str(passenger.count)

        return data


class Adult(Passenger):
    def __init__(self, count: int = 1):
        super().__init__()
        super().__init_internal__("어른/청소년", "1", count)


class Child(Passenger):
    def __init__(self, count: int = 1):
        super().__init__()
        super().__init_internal__("어린이", "5", count)


class Senior(Passenger):
    def __init__(self, count: int = 1):
        super().__init__()
        super().__init_internal__("경로", "4", count)


class Disability1To3(Passenger):
    def __init__(self, count: int = 1):
        super().__init__()
        super().__init_internal__("장애 1~3급", "2", count)


class Disability4To6(Passenger):
    def __init__(self, count: int = 1):
        super().__init__()
        super().__init_internal__("장애 4~6급", "3", count)


# Ticket class
class SRTTicket:
    SEAT_TYPE = {"1": "일반실", "2": "특실"}

    PASSENGER_TYPE = {
        "1": "어른/청소년", 
        "2": "장애 1~3급",
        "3": "장애 4~6급",
        "4": "경로",
        "5": "어린이"
    }

    DISCOUNT_TYPE = {
        "000": "어른/청소년",
        "101": "탄력운임기준할인", 
        "105": "자유석 할인",
        "106": "입석 할인",
        "107": "역방향석 할인",
        "108": "출입구석 할인", 
        "109": "가족석 일반전환 할인",
        "111": "구간별 특정운임",
        "112": "열차별 특정운임",
        "113": "구간별 비율할인(기준)",
        "114": "열차별 비율할인(기준)",
        "121": "공항직결 수색연결운임",
        "131": "구간별 특별할인(기준)",
        "132": "열차별 특별할인(기준)", 
        "133": "기본 특별할인(기준)",
        "191": "정차역 할인",
        "192": "매체 할인",
        "201": "어린이",
        "202": "동반유아 할인",
        "204": "경로",
        "205": "1~3급 장애인",
        "206": "4~6급 장애인"
    }

    def __init__(self, data: dict) -> None:
        self.car = data.get("scarNo")
        self.seat = data.get("seatNo")
        self.seat_type_code = data.get("psrmClCd")
        self.seat_type = self.SEAT_TYPE[self.seat_type_code]
        self.passenger_type_code = data.get("dcntKndCd")
        self.passenger_type = self.DISCOUNT_TYPE.get(self.passenger_type_code, "기타 할인")
        self.price = int(data.get("rcvdAmt"))
        self.original_price = int(data.get("stdrPrc")) 
        self.discount = int(data.get("dcntPrc"))
        self.is_waiting = self.seat == ""

    def __str__(self) -> str:
        return self.dump()

    __repr__ = __str__

    def dump(self) -> str:
        if self.is_waiting:
            return (
                f"예약대기 ({self.seat_type}) {self.passenger_type}"
                f"[{self.price}원({self.discount}원 할인)]"
            )
        return (
            f"{self.car}호차 {self.seat} ({self.seat_type}) {self.passenger_type} "
            f"[{self.price}원({self.discount}원 할인)]"
        )


class SRTReservation:
    def __init__(self, train, pay, tickets):
        self.reservation_number = train.get("pnrNo")
        self.total_cost = int(train.get("rcvdAmt"))
        self.seat_count = train.get("tkSpecNum") or int(train.get("seatNum"))

        self.train_code = pay.get("stlbTrnClsfCd")
        self.train_name = TRAIN_NAME[self.train_code]
        self.train_number = pay.get("trnNo")

        self.dep_date = pay.get("dptDt")
        self.dep_time = pay.get("dptTm")
        self.dep_station_code = pay.get("dptRsStnCd")
        self.dep_station_name = STATION_NAME[self.dep_station_code]

        self.arr_time = pay.get("arvTm")
        self.arr_station_code = pay.get("arvRsStnCd")
        self.arr_station_name = STATION_NAME[self.arr_station_code]

        self.payment_date = pay.get("iseLmtDt")
        self.payment_time = pay.get("iseLmtTm")
        self.paid = pay.get("stlFlg") == "Y"
        self.is_running = "tkSpecNum" not in train
        self.is_waiting = not (self.paid or self.payment_date or self.payment_time)

        self._tickets = tickets

    def __str__(self):
        return self.dump()

    __repr__ = __str__

    def dump(self):
        base = (
            f"[{self.train_name}] "
            f"{self.dep_date[4:6]}월 {self.dep_date[6:8]}일, "
            f"{self.dep_station_name}~{self.arr_station_name}"
            f"({self.dep_time[:2]}:{self.dep_time[2:4]}~{self.arr_time[:2]}:{self.arr_time[2:4]}) "
            f"{self.total_cost}원({self.seat_count}석)"
        )

        if not self.paid:
            if not self.is_waiting:
                base += (
                    f", 구입기한 {self.payment_date[4:6]}월 {self.payment_date[6:8]}일 "
                    f"{self.payment_time[:2]}:{self.payment_time[2:4]}"
                )
            else:
                base += ", 예약대기"
        
        if self.is_running:
            base += f" (운행중)"

        return base

    @property
    def tickets(self):
        return self._tickets


# SRTResponseData class
class SRTResponseData:
    """SRT Response data class that parses JSON response from API request"""

    STATUS_SUCCESS = "SUCC"
    STATUS_FAIL = "FAIL"

    def __init__(self, response: str) -> None:
        self._json = json.loads(response)
        self._status = self._parse()

    def __str__(self) -> str:
        return json.dumps(self._json)

    dump = __str__  # Alias dump() to __str__()

    def _parse(self) -> dict:
        if "resultMap" in self._json:
            return self._json["resultMap"][0]

        if "ErrorCode" in self._json and "ErrorMsg" in self._json:
            raise SRTResponseError(
                f'Undefined result status "[{self._json["ErrorCode"]}]: {self._json["ErrorMsg"]}"'
            )
        raise SRTError(f"Unexpected case [{self._json}]")

    def success(self) -> bool:
        result = self._status.get("strResult")
        if result is None:
            raise SRTResponseError("Response status is not given")
        
        if result == self.STATUS_SUCCESS:
            return True
        if result == self.STATUS_FAIL:
            return False
        
        raise SRTResponseError(f'Undefined result status "{result}"')

    def message(self) -> str:
        return self._status.get("msgTxt", "")

    def get_all(self) -> dict:
        return self._json.copy()

    def get_status(self) -> dict:
        return self._status.copy()


class SeatType(Enum):
    GENERAL_FIRST = 1  # 일반실 우선
    GENERAL_ONLY = 2   # 일반실만 
    SPECIAL_FIRST = 3  # 특실 우선
    SPECIAL_ONLY = 4   # 특실만


# Train class
class Train:
    pass


class SRTTrain(Train):
    def __init__(self, data):
        self.train_code = data["stlbTrnClsfCd"]
        self.train_name = TRAIN_NAME[self.train_code]
        self.train_number = data["trnNo"]
        
        # Departure info
        self.dep_date = data["dptDt"]
        self.dep_time = data["dptTm"]
        self.dep_station_code = data["dptRsStnCd"]
        self.dep_station_name = STATION_NAME[self.dep_station_code]
        self.dep_station_run_order = data["dptStnRunOrdr"]
        self.dep_station_constitution_order = data["dptStnConsOrdr"]

        # Arrival info  
        self.arr_date = data["arvDt"]
        self.arr_time = data["arvTm"]
        self.arr_station_code = data["arvRsStnCd"]
        self.arr_station_name = STATION_NAME[self.arr_station_code]
        self.arr_station_run_order = data["arvStnRunOrdr"]
        self.arr_station_constitution_order = data["arvStnConsOrdr"]

        # Seat availability info
        self.general_seat_state = data["gnrmRsvPsbStr"]
        self.special_seat_state = data["sprmRsvPsbStr"]
        self.reserve_wait_possible_name = data["rsvWaitPsbCdNm"]
        self.reserve_wait_possible_code = int(data["rsvWaitPsbCd"]) # -1: 예약대기 없음, 9: 예약대기 가능, 0: 매진, -2: 예약대기 불가능

    def __str__(self):
        return self.dump()

    def __repr__(self):
        return self.dump()

    def dump(self):
        dep_hour, dep_min = self.dep_time[0:2], self.dep_time[2:4]
        arr_hour, arr_min = self.arr_time[0:2], self.arr_time[2:4]
        month, day = self.dep_date[4:6], self.dep_date[6:8]

        msg = (
            f"[{self.train_name} {self.train_number}] "
            f"{month}월 {day}일, "
            f"{self.dep_station_name}~{self.arr_station_name}"
            f"({dep_hour}:{dep_min}~{arr_hour}:{arr_min}) "
            f"특실 {self.special_seat_state}, 일반실 {self.general_seat_state}"
        )
        if self.reserve_wait_possible_code >= 0:
            msg += f", 예약대기 {self.reserve_wait_possible_name}"
        return msg

    def general_seat_available(self):
        return "예약가능" in self.general_seat_state

    def special_seat_available(self):
        return "예약가능" in self.special_seat_state

    def reserve_standby_available(self):
        return self.reserve_wait_possible_code == 9

    def seat_available(self):
        return self.general_seat_available() or self.special_seat_available()


# NetFunnel
class NetFunnelHelper:
    WAIT_STATUS_PASS = "200"
    WAIT_STATUS_FAIL = "201" 
    ALREADY_COMPLETED = "502"

    OP_CODE = {
        "getTidchkEnter": "5101",
        "chkEnter": "5002", 
        "setComplete": "5004",
    }

    DEFAULT_HEADERS = {
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": "ko,en;q=0.9,en-US;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive", 
        "Pragma": "no-cache",
        "Referer": SRT_MOBILE,
        "Sec-Fetch-Dest": "script",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "cross-site",
    }

    def __init__(self, debug=False):
        self._session = requests.session()
        self._session.headers.update(self.DEFAULT_HEADERS)
        self._cached_key = None
        self._last_fetch_time = 0
        self._cache_ttl = 48  # 48 seconds
        self.debug = debug

    def run(self):
        current_time = time.time()
        if self._is_cache_valid(current_time):
            return self._cached_key

        try:
            status, self._cached_key, nwait, ip = self._start()
            self._last_fetch_time = current_time

            # Keep checking until we get a pass status
            while status == self.WAIT_STATUS_FAIL:
                print(f"\r현재 {nwait}명 대기중...", end="", flush=True)
                time.sleep(1)
                status, self._cached_key, nwait, ip = self._check(ip)
            
            # Complete the funnel process
            status, *_ = self._complete(ip)
            if status in (self.WAIT_STATUS_PASS, self.ALREADY_COMPLETED):
                return self._cached_key

            self.clear()
            raise SRTNetFunnelError("Failed to complete NetFunnel")

        except Exception as ex:
            self.clear()
            raise SRTNetFunnelError(str(ex))

    def clear(self):
        self._cached_key = None
        self._last_fetch_time = 0

    def _start(self):
        return self._make_request("getTidchkEnter")

    def _check(self, ip: str | None = None):
        return self._make_request("chkEnter", ip)

    def _complete(self, ip: str | None = None):
        return self._make_request("setComplete", ip)

    def _make_request(self, opcode: str, ip: str | None = None):
        url = f"http://{ip or 'nf.letskorail.com'}/ts.wseq"
        params = self._build_params(self.OP_CODE[opcode])
        r = self._session.get(url, params=params)
        if self.debug:
            print(r.text)
        response = self._parse(r.text)
        return map(response.get, ('status', 'key', 'nwait', 'ip'))

    def _build_params(self, opcode: str, timestamp: str = None, key: str = None) -> dict:
        params = {
            "opcode": opcode,
            "nfid": "0",
            "prefix": f"NetFunnel.gRtype={opcode};",
            "js": "true",
            str(int(time.time() * 1000) if timestamp is None else timestamp): ""
        }

        if opcode in (self.OP_CODE["getTidchkEnter"], self.OP_CODE["chkEnter"]):
            params.update({"sid": "service_1", "aid": "act_10"})
            if opcode == self.OP_CODE["chkEnter"]:
                params.update({"key": key or self._cached_key, "ttl": "1"})
        elif opcode == self.OP_CODE["setComplete"]:
            params["key"] = key or self._cached_key

        return params

    def _parse(self, response: str) -> dict:
        result_match = re.search(r"NetFunnel\.gControl\.result='([^']+)'", response)
        if not result_match:
            raise SRTNetFunnelError("Failed to parse NetFunnel response")

        code, status, params_str = result_match.group(1).split(":", 2)
        if not params_str:
            raise SRTNetFunnelError("Failed to parse NetFunnel response")

        params = dict(param.split("=", 1) for param in params_str.split("&") if "=" in param)
        params.update({"code": code, "status": status})
        return params

    def _is_cache_valid(self, current_time: float) -> bool:
        return bool(self._cached_key and (current_time - self._last_fetch_time) < self._cache_ttl)


# SRT class
class SRT:
    """SRT client class for interacting with the SRT train booking system.

    Args:
        srt_id (str): SRT account ID (membership number, email, or phone)
        srt_pw (str): SRT account password 
        auto_login (bool): Whether to automatically login on initialization
        verbose (bool): Whether to print debug logs

    Examples:
        >>> srt = SRT("1234567890", YOUR_PASSWORD) # with membership number
        >>> srt = SRT("def6488@gmail.com", YOUR_PASSWORD) # with email
        >>> srt = SRT("010-1234-xxxx", YOUR_PASSWORD) # with phone number
    """

    def __init__(
        self, srt_id: str, srt_pw: str, auto_login: bool = True, verbose: bool = False
    ) -> None:
        self._session = requests.session()
        self._session.headers.update(DEFAULT_HEADERS)
        self._netfunnel = NetFunnelHelper(debug=verbose)
        self.srt_id = srt_id
        self.srt_pw = srt_pw
        self.verbose = verbose
        self.is_login = False
        self.membership_number = None
        self.membership_name = None
        self.phone_number = None

        if auto_login:
            self.login()

    def _log(self, msg: str) -> None:
        if self.verbose:
            print("[*] " + msg)

    def login(self, srt_id: str | None = None, srt_pw: str | None = None) -> bool:
        """Login to SRT server.

        Usually called automatically on initialization.

        Args:
            srt_id: Optional override of instance srt_id
            srt_pw: Optional override of instance srt_pw

        Returns:
            bool: Whether login was successful

        Raises:
            SRTLoginError: If login fails
        """
        srt_id = srt_id or self.srt_id
        srt_pw = srt_pw or self.srt_pw

        login_type = "2" if EMAIL_REGEX.match(srt_id) else (
            "3" if PHONE_NUMBER_REGEX.match(srt_id) else "1"
        )

        if login_type == "3":
            srt_id = re.sub("-", "", srt_id)

        data = {
            "auto": "Y",
            "check": "Y", 
            "page": "menu",
            "deviceKey": "-",
            "customerYn": "",
            "login_referer": API_ENDPOINTS["main"],
            "srchDvCd": login_type,
            "srchDvNm": srt_id,
            "hmpgPwdCphd": srt_pw,
        }

        r = self._session.post(url=API_ENDPOINTS["login"], data=data)
        self._log(r.text)

        if "존재하지않는 회원입니다" in r.text:
            raise SRTLoginError(r.json()["MSG"])
        if "비밀번호 오류" in r.text:
            raise SRTLoginError(r.json()["MSG"])
        if "Your IP Address Blocked" in r.text:
            raise SRTLoginError(r.text.strip())

        self.is_login = True
        user_info = json.loads(r.text)["userMap"]
        self.membership_number = user_info["MB_CRD_NO"]
        self.membership_name = user_info["CUST_NM"]
        self.phone_number = user_info["MBL_PHONE"]

        print(f"로그인 성공: {self.membership_name} (멤버십번호: {self.membership_number}, 전화번호: {self.phone_number})")
        return True

    def logout(self) -> bool:
        """Logout from SRT server.

        Returns:
            bool: Whether logout was successful

        Raises:
            SRTResponseError: If server returns error
        """
        if not self.is_login:
            return True

        r = self._session.post(url=API_ENDPOINTS["logout"])
        self._log(r.text)

        if not r.ok:
            raise SRTResponseError(r.text)

        self.is_login = False
        self.membership_number = None
        return True

    def search_train(
        self,
        dep: str,
        arr: str,
        date: str | None = None,
        time: str | None = None,
        time_limit: str | None = None,
        passengers: list[Passenger] | None = None,
        available_only: bool = True,
    ) -> list[SRTTrain]:
        """Search for available trains.

        Args:
            dep: Departure station name
            arr: Arrival station name
            date: Date in YYYYMMDD format (default: today)
            time: Time in HHMMSS format (default: 000000)
            time_limit: Only return trains before this time
            passengers: List of passengers (default: 1 adult)
            available_only: Only return trains with available seats

        Returns:
            List of matching SRTTrain objects

        Raises:
            ValueError: If invalid station names provided
        """
        if dep not in STATION_CODE or arr not in STATION_CODE:
            raise ValueError(f'Invalid station: "{dep}" or "{arr}"')

        now = datetime.now()
        today = now.strftime("%Y%m%d")
        date = date or today
        
        if date < today:
            raise ValueError("Date cannot be before today")
            
        time = (
            max(time or "000000", now.strftime("%H%M%S")) 
            if date == today
            else time or "000000"
        )

        passengers = Passenger.combine(passengers or [Adult()])

        data = {
            "chtnDvCd": "1",
            "dptDt": date,
            "dptTm": time,
            "dptDt1": date,
            "dptTm1": time[:2] + "0000",
            "dptRsStnCd": STATION_CODE[dep],
            "arvRsStnCd": STATION_CODE[arr],
            "stlbTrnClsfCd": "05",
            "trnGpCd": 109,
            "trnNo": "",
            "psgNum": str(Passenger.total_count(passengers)),
            "seatAttCd": "015", 
            "arriveTime": "N",
            "tkDptDt": "",
            "tkDptTm": "",
            "tkTrnNo": "",
            "tkTripChgFlg": "",
            "dlayTnumAplFlg": "Y",
            "netfunnelKey": self._netfunnel.run()
        }

        r = self._session.post(url=API_ENDPOINTS["search_schedule"], data=data)
        self._log(r.text)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        return [
            train for train in (
                SRTTrain(t) for t in parser.get_all()["outDataSets"]["dsOutput1"] 
                if t["stlbTrnClsfCd"] == '17'
            )
            if (not available_only or train.seat_available()) and
               (not time_limit or train.dep_time <= time_limit)
        ]

    def reserve(
        self,
        train: SRTTrain,
        passengers: list[Passenger] | None = None,
        option: SeatType = SeatType.GENERAL_FIRST,
        window_seat: bool | None = None,
    ) -> SRTReservation:
        """Reserve a train.

        Args:
            train: Train to reserve
            passengers: List of passengers (default: 1 adult)
            option: Seat type preference
            window_seat: Whether to prefer window seats

        Returns:
            SRTReservation object for the reservation

        Examples:
            >>> trains = srt.search_train("수서", "부산", "210101", "000000")
            >>> srt.reserve(trains[0])
        """
        if not train.seat_available() and train.reserve_wait_possible_code >= 0:
            reservation = self.reserve_standby(train, passengers, option=option, mblPhone=self.phone_number)
            if self.phone_number:
                agree_class_change = option == SeatType.SPECIAL_FIRST or option == SeatType.GENERAL_FIRST
                self.reserve_standby_option_settings(reservation, isAgreeSMS=True, isAgreeClassChange=agree_class_change, telNo=self.phone_number)
            return reservation

        return self._reserve(
            RESERVE_JOBID["PERSONAL"],
            train,
            passengers,
            option,
            window_seat=window_seat,
        )

    def reserve_standby(
        self,
        train: SRTTrain,
        passengers: list[Passenger] | None = None,
        option: SeatType = SeatType.GENERAL_FIRST,
        mblPhone: str | None = None,
    ) -> SRTReservation:
        """Request waitlist reservation.

        Args:
            train: Train to waitlist
            passengers: List of passengers (default: 1 adult) 
            option: Seat type preference
            mblPhone: Phone number for notifications

        Returns:
            SRTReservation object for the waitlist

        Examples:
            >>> trains = srt.search_train("수서", "부산", "210101", "000000")
            >>> srt.reserve_standby(trains[0])
        """
        if option == SeatType.SPECIAL_FIRST:
            option = SeatType.SPECIAL_ONLY
        elif option == SeatType.GENERAL_FIRST:
            option = SeatType.GENERAL_ONLY
        return self._reserve(
            RESERVE_JOBID["STANDBY"],
            train,
            passengers,
            option,
            mblPhone=mblPhone
        )

    def _reserve(
        self,
        jobid: str,
        train: SRTTrain,
        passengers: list[Passenger] | None = None,
        option: SeatType = SeatType.GENERAL_FIRST,
        mblPhone: str | None = None,
        window_seat: bool | None = None,
    ) -> SRTReservation:
        """Common reservation request handler.

        Args:
            jobid: Type of reservation (personal/standby)
            train: Train to reserve
            passengers: List of passengers
            option: Seat type preference
            mblPhone: Phone number for standby notifications
            window_seat: Window seat preference for personal reservations

        Returns:
            SRTReservation object

        Raises:
            SRTNotLoggedInError: If not logged in
            TypeError: If train is not SRTTrain
            ValueError: If train is not SRT
            SRTError: If reservation not found after creation
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        if not isinstance(train, SRTTrain):
            raise TypeError('"train" must be SRTTrain instance')

        if train.train_name != "SRT":
            raise ValueError(f'Expected "SRT" train, got {train.train_name}')

        passengers = Passenger.combine(passengers or [Adult()])

        is_special_seat = {
            SeatType.GENERAL_ONLY: False,
            SeatType.SPECIAL_ONLY: True,
            SeatType.GENERAL_FIRST: not train.general_seat_available(),
            SeatType.SPECIAL_FIRST: train.special_seat_available()
        }[option]

        data = {
            "jobId": jobid,
            "jrnyCnt": "1",
            "jrnyTpCd": "11",
            "jrnySqno1": "001",
            "stndFlg": "N",
            "trnGpCd1": "300",
            "trnGpCd": "109",
            "grpDv": "0",
            "rtnDv": "0",
            "stlbTrnClsfCd1": train.train_code,
            "dptRsStnCd1": train.dep_station_code,
            "dptRsStnCdNm1": train.dep_station_name,
            "arvRsStnCd1": train.arr_station_code,
            "arvRsStnCdNm1": train.arr_station_name,
            "dptDt1": train.dep_date,
            "dptTm1": train.dep_time,
            "arvTm1": train.arr_time,
            "trnNo1": f"{int(train.train_number):05d}",
            "runDt1": train.dep_date,
            "dptStnConsOrdr1": train.dep_station_constitution_order,
            "arvStnConsOrdr1": train.arr_station_constitution_order,
            "dptStnRunOrdr1": train.dep_station_run_order,
            "arvStnRunOrdr1": train.arr_station_run_order,
            "mblPhone": mblPhone,
            "netfunnelKey": self._netfunnel.run()
        }

        if jobid == RESERVE_JOBID["PERSONAL"]:
            data["reserveType"] = "11"

        data.update(Passenger.get_passenger_dict(
            passengers, 
            special_seat=is_special_seat,
            window_seat=window_seat
        ))

        r = self._session.post(url=API_ENDPOINTS["reserve"], data=data)
        self._log(r.text)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        reservation_number = parser.get_all()["reservListMap"][0]["pnrNo"]

        for ticket in self.get_reservations():
            if ticket.reservation_number == reservation_number:
                return ticket

        raise SRTError("Ticket not found: check reservation status")

    def reserve_standby_option_settings(
        self,
        reservation: SRTReservation | int,
        isAgreeSMS: bool,
        isAgreeClassChange: bool,
        telNo: str | None = None,
    ) -> bool:
        """Configure waitlist options.

        Args:
            reservation: Reservation object or number
            isAgreeSMS: Whether to receive SMS notifications
            isAgreeClassChange: Whether to accept seat class changes
            telNo: Phone number for notifications

        Returns:
            bool: Whether update was successful

        Examples:
            >>> trains = srt.search_train("수서", "부산", "210101", "000000")
            >>> res = srt.reserve_standby(trains[0])
            >>> srt.reserve_standby_option_settings(res, True, True, "010-1234-xxxx")
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        reservation_number = getattr(reservation, 'reservation_number', reservation)

        data = {
            "pnrNo": reservation_number,
            "psrmClChgFlg": "Y" if isAgreeClassChange else "N",
            "smsSndFlg": "Y" if isAgreeSMS else "N",
            "telNo": telNo if isAgreeSMS else "",
        }

        r = self._session.post(url=API_ENDPOINTS["standby_option"], data=data)
        self._log(r.text)
        return r.status_code == 200

    def get_reservations(self, paid_only: bool = False) -> list[SRTReservation]:
        """Get all reservations.

        Args:
            paid_only: Whether to only return paid reservations

        Returns:
            List of SRTReservation objects

        Raises:
            SRTNotLoggedInError: If not logged in
            SRTResponseError: If server returns error
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        r = self._session.post(url=API_ENDPOINTS["tickets"], data={"pageNo": "0"})
        self._log(r.text)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        return [
            SRTReservation(train, pay, self.ticket_info(train["pnrNo"]))
            for train, pay in zip(
                parser.get_all()["trainListMap"],
                parser.get_all()["payListMap"]
            )
            if not paid_only or pay["stlFlg"] != "N"
        ]

    def ticket_info(self, reservation: SRTReservation | int) -> list[SRTTicket]:
        """Get detailed ticket information.

        Args:
            reservation: Reservation object or number

        Returns:
            List of SRTTicket objects

        Raises:
            SRTNotLoggedInError: If not logged in
            SRTResponseError: If server returns error
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        reservation_number = getattr(reservation, 'reservation_number', reservation)
        
        r = self._session.post(
            url=API_ENDPOINTS["ticket_info"],
            data={"pnrNo": reservation_number, "jrnySqno": "1"}
        )
        self._log(r.text)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        return [SRTTicket(ticket) for ticket in parser.get_all()["trainListMap"]]

    def cancel(self, reservation: SRTReservation | int) -> bool:
        """Cancel a reservation.

        Args:
            reservation: Reservation object or number

        Returns:
            bool: Whether cancellation was successful

        Examples:
            >>> reservation = srt.reserve(train)
            >>> srt.cancel(reservation)
            >>> reservations = srt.get_reservations()
            >>> srt.cancel(reservations[0])

        Raises:
            SRTNotLoggedInError: If not logged in
            SRTResponseError: If server returns error
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        reservation_number = getattr(reservation, 'reservation_number', reservation)

        data = {
            "pnrNo": reservation_number,
            "jrnyCnt": "1",
            "rsvChgTno": "0"
        }

        r = self._session.post(url=API_ENDPOINTS["cancel"], data=data)
        self._log(r.text)
        parser = SRTResponseData(r.text)

        if not parser.success():
            raise SRTResponseError(parser.message())

        return True

    def pay_with_card(
        self,
        reservation: SRTReservation,
        number: str,
        password: str,
        validation_number: str,
        expire_date: str,
        installment: int = 0,
        card_type: str = "J",
    ) -> bool:
        """Pay for a reservation with credit card.

        Args:
            reservation: Reservation to pay for
            number: Card number (no hyphens)
            password: First 2 digits of card password
            validation_number: Birth date (card_type=J) or business number (card_type=S)
            expire_date: Card expiry date (YYMM)
            installment: Number of installments (0,2-12,24)
            card_type: Card type (J=personal, S=corporate)

        Returns:
            bool: Whether payment was successful

        Examples:
            >>> reservation = srt.reserve(train)
            >>> srt.pay_with_card(reservation, "1234567890123456", "12", "981204", "2309")

        Raises:
            SRTNotLoggedInError: If not logged in
            SRTResponseError: If payment fails
        """
        if not self.is_login:
            raise SRTNotLoggedInError()

        data = {
            "stlDmnDt": datetime.now().strftime("%Y%m%d"),
            "mbCrdNo": self.membership_number,
            "stlMnsSqno1": "1",
            "ststlGridcnt": "1",
            "totNewStlAmt": reservation.total_cost,
            "athnDvCd1": card_type,
            "vanPwd1": password,
            "crdVlidTrm1": expire_date,
            "stlMnsCd1": "02",
            "rsvChgTno": "0",
            "chgMcs": "0",
            "ismtMnthNum1": installment,
            "ctlDvCd": "3102",
            "cgPsId": "korail",
            "pnrNo": reservation.reservation_number,
            "totPrnb": reservation.seat_count,
            "mnsStlAmt1": reservation.total_cost,
            "crdInpWayCd1": "@",
            "athnVal1": validation_number,
            "stlCrCrdNo1": number,
            "jrnyCnt": "1",
            "strJobId": "3102",
            "inrecmnsGridcnt": "1",
            "dptTm": reservation.dep_time,
            "arvTm": reservation.arr_time,
            "dptStnConsOrdr2": "000000",
            "arvStnConsOrdr2": "000000",
            "trnGpCd": "300",
            "pageNo": "-",
            "rowCnt": "-",
            "pageUrl": "",
        }

        r = self._session.post(url=API_ENDPOINTS["payment"], data=data)
        self._log(r.text)
        response = json.loads(r.text)

        if response["outDataSets"]["dsOutput0"][0]["strResult"] == "FAIL":
            raise SRTResponseError(response["outDataSets"]["dsOutput0"][0]["msgTxt"])

        return True
    
    def reserve_info(self, reservation: SRTReservation | int) -> bool:
        referer = API_ENDPOINTS["reserve_info_referer"] + reservation.reservation_number
        self._session.headers.update({"Referer": referer})
        r = self._session.post(url=API_ENDPOINTS["reserve_info"])
        self._log(r.text)
        response = json.loads(r.text)
        if response.get("ErrorCode") == "0" and response.get("ErrorMsg") == "":
            return response.get("outDataSets").get("dsOutput1")[0]
        else:
            raise SRTResponseError(response.get("ErrorMsg"))
    
    def refund(self, reservation: SRTReservation | int) -> bool:
        info = self.reserve_info(reservation)
        data = {
            "pnr_no": info.get("pnrNo"),
            "cnc_dmn_cont": "승차권 환불로 취소",
            "saleDt": info.get("ogtkSaleDt"),
            "saleWctNo": info.get("ogtkSaleWctNo"),
            "saleSqno": info.get("ogtkSaleSqno"),
            "tkRetPwd": info.get("ogtkRetPwd"),
            "psgNm": info.get("buyPsNm"),
        }

        r = self._session.post(url=API_ENDPOINTS["refund"], data=data)
        self._log(r.text)
        response = SRTResponseData(r.text)

        if not response.success():
            raise SRTResponseError(response.message())

        return True
    
    def clear(self):
        self._log("Clearing the netfunnel key")
        self._netfunnel.clear()

# SRT End
if __name__ == "__main__":
    sys.stdout.write("\x1b[2J\x1b[H")  # clear screen + move cursor to top-left
    sys.stdout.flush()
    srtgo()