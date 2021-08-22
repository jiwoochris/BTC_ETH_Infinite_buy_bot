import pyupbit
import time
import math
import datetime
import requests

def post_message(text):
    myToken = 'aaaa-aaaaaaaaaaaaa-aaaaaaaaaaaaa-aaaaaaaaaaaaaaaaaaaaaaaa' # slack 토큰 입력
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+myToken},
        data={"channel": "#upbit","text": text} # slack 채널명 입력
    )
    print(response)

with open("upbit_key.txt", "r") as f: # txt 파일에 api key 입력
    key1 = f.readline().strip()
    key2 = f.readline().strip()

upbit = pyupbit.Upbit(key1, key2)

post_message("Start Infinite ETH Auto Trading Program.")

before_krw = upbit.get_balance("KRW")
buy_order = False
fin = False
count = 0
avg = 0

while True:
    
    now = datetime.datetime.now()
    
    # 필수 매수

    if now.hour % 12 == 6 and now.minute == 0 and 0 <= now.second <= 2:
        if upbit.get_balance("KRW") < 10000:
            fin = True

        else:
            prev_amount = upbit.get_balance("KRW-ETH")

            order = pyupbit.get_orderbook("KRW-ETH")
            bid1 = order[0]['orderbook_units'][0]['bid_price']
            amount = math.floor(10000 * 0.9995 / bid1 * 100000000) / 100000000

            buy_ret = upbit.buy_limit_order("KRW-ETH", bid1, amount)
            buy_order = True
            time.sleep(4)

    # 평단가보다 낮으면 매수

    if (now.hour % 12 == 0 and now.minute == 0 and 0 <= now.second <= 3):
        if upbit.get_balance("KRW") < 10000:
            fin = True

        else:
            if avg * 0.985 > pyupbit.get_current_price("KRW-ETH") or avg == 0:

                prev_amount = upbit.get_balance("KRW-ETH")

                order = pyupbit.get_orderbook("KRW-ETH")
                bid1 = order[0]['orderbook_units'][0]['bid_price']
                amount = math.floor(10000 * 0.9995 / bid1 * 100000000) / 100000000

                buy_ret = upbit.buy_limit_order("KRW-ETH", bid1, amount)
                buy_order = True
                time.sleep(4)

    # 매수 주문 체결 완료

    if buy_order == True and upbit.get_order("KRW-ETH") == []:
        avg = (avg * prev_amount + bid1 * amount) / upbit.get_balance("KRW-ETH")
        count += 1
        post_message(f"[ETH inf][매수]\n{buy_ret['market']} {buy_ret['price']}\n평단가 : {avg : .3f}\n{count}차")
        buy_order = False

    # 매수 주문 미체결 & 취소

    if now.hour % 6 == 0 and now.minute == 15 and 0 <= now.second <= 3 and buy_order == True and upbit.get_order("KRW-ETH") != []:
        upbit.cancel_order(buy_ret['uuid'])
        post_message(f"[ETH inf][매수 미체결]\n{buy_ret['market']} {buy_ret['price']}")
        buy_order = False

    # 5퍼 익절 매도 주문

    if avg * 1.05 < pyupbit.get_current_price("KRW-ETH") and upbit.get_balance("KRW-ETH") > 0.0001 and avg != 0:
        order = pyupbit.get_orderbook("KRW-ETH")
        bid1 = order[0]['orderbook_units'][0]['ask_price'] #리스트 내의 딕셔너리에 접근

        sell_ret = upbit.sell_limit_order("KRW-ETH", bid1, upbit.get_balance("KRW-ETH"))

        time.sleep(180)

        # 매도 주문 미체결 & 취소
        if upbit.get_order("KRW-ETH") != []:
            upbit.cancel_order(sell_ret['uuid'])
            post_message(f"[ETH inf][매도 미체결]\n{buy_ret['market']} {buy_ret['price']}")

        # 매도 주문 체결
        elif upbit.get_order("KRW-ETH") == []:
            post_message(f"[ETH inf][매도] {sell_ret['market']} {sell_ret['price']}")
            after_krw = upbit.get_balance("KRW")

            if after_krw > before_krw:
                결과 = "이득"
            else:
                결과 = "손해"
        
            수익률 = after_krw / before_krw * 100 - 100

            post_message(f"[ETH inf][{결과}] {수익률 : .3f} %\n변화 : {after_krw - before_krw : .3f}\n잔고 : {after_krw : .3f}")
            fin = True


    if fin == True:
        post_message("[ETH inf][종료]")
        before_krw = upbit.get_balance("KRW")
        avg = 0
        count = 0
        fin = False

    time.sleep(0.1)