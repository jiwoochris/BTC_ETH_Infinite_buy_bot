import pyupbit
import math
import datetime
import requests
import asyncio
import sys

def post_message(text):
    myToken = 'aaaa-aaaaaaaaaaaaa-aaaaaaaaaaaaa-aaaaaaaaaaaaaaaaaaaaaaaa' # slack 토큰 입력
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+myToken},
        data={"channel": "#upbit","text": text}
    )
    print(response)

with open("upbit_key.txt", "r") as f: # txt 파일에 api key 입력
    key1 = f.readline().strip()
    key2 = f.readline().strip()

upbit = pyupbit.Upbit(key1, key2)

post_message("Start BTC, ETH Infinite Buying Program.")

async def BTC():
    unit_price = 10000
    low = 0.97

    buy_order = False
    fin = False
    count = 0
    avg = 0

    print("BTC start")

    while True:
        
        now = datetime.datetime.now()
        
        # 필수 매수

        if now.hour % 12 == 6 and now.minute == 0 and 0 <= now.second <= 2:
            if upbit.get_balance("KRW") < unit_price:
                post_message(f"[INF][not enough money][exit]")
                sys.exit()

            else:
                prev_amount = upbit.get_balance("KRW-BTC")

                order = pyupbit.get_orderbook("KRW-BTC")
                bid1 = order[0]['orderbook_units'][0]['bid_price']
                amount = math.floor(unit_price * 0.9995 / bid1 * 100000000) / 100000000

                buy_ret = upbit.buy_limit_order("KRW-BTC", bid1, amount)
                buy_order = True
                await asyncio.sleep(4)

        # 평단가보다 낮으면 매수

        if (now.hour % 12 == 0 and now.minute == 0 and 0 <= now.second <= 3):
            if upbit.get_balance("KRW") < unit_price:
                post_message(f"[INF][not enough money][exit]")
                sys.exit()

            else:
                if avg * low > pyupbit.get_current_price("KRW-BTC") or avg == 0:

                    prev_amount = upbit.get_balance("KRW-BTC")

                    order = pyupbit.get_orderbook("KRW-BTC")
                    bid1 = order[0]['orderbook_units'][0]['bid_price']
                    amount = math.floor(unit_price * 0.9995 / bid1 * 100000000) / 100000000

                    buy_ret = upbit.buy_limit_order("KRW-BTC", bid1, amount)
                    buy_order = True
                    await asyncio.sleep(4)

        # 매수 주문 체결 완료

        if buy_order == True and upbit.get_order("KRW-BTC") == []:
            avg = (avg * prev_amount + bid1 * amount) / upbit.get_balance("KRW-BTC")
            count += 1
            post_message(f"[INF][매수]\n{buy_ret['market']} {buy_ret['price']}\n평단가 : {avg : .3f}\n{count}차")
            buy_order = False

        # 매수 주문 미체결 & 취소

        if now.hour % 6 == 0 and now.minute == 15 and 0 <= now.second <= 3 and buy_order == True and upbit.get_order("KRW-BTC") != []:
            upbit.cancel_order(buy_ret['uuid'])
            post_message(f"[INF][매수 미체결]\n{buy_ret['market']} {buy_ret['price']}")
            buy_order = False

        # 5퍼 익절 매도 주문

        if avg * 1.05 < pyupbit.get_current_price("KRW-BTC") and upbit.get_balance("KRW-BTC") > 0.0001 and avg != 0:
            order = pyupbit.get_orderbook("KRW-BTC")
            bid1 = order[0]['orderbook_units'][0]['ask_price'] #리스트 내의 딕셔너리에 접근
            balance = upbit.get_balance("KRW-BTC")

            sell_ret = upbit.sell_limit_order("KRW-BTC", bid1, upbit.get_balance("KRW-BTC"))

            await asyncio.sleep(180)

            # 매도 주문 미체결 & 취소
            if upbit.get_order("KRW-BTC") != []:
                upbit.cancel_order(sell_ret['uuid'])
                post_message(f"[INF][매도 미체결]\n{buy_ret['market']} {buy_ret['price']}")

            # 매도 주문 체결
            elif upbit.get_order("KRW-BTC") == []:
                post_message(f"[INF][매도] {sell_ret['market']} {sell_ret['price']}")
                
                if bid1 > avg:
                    결과 = "이득"
                else:
                    결과 = "손해"
            
                잔고 = upbit.get_balance("KRW")
                수익률 =  ((bid1 - avg) * balance ) / 1000000 * 100

                post_message(f"[INF][{결과}] {수익률 : .3f} %\n변화 : {(bid1 - avg) * balance : .3f}\n잔고 : {잔고 : .3f}")
                fin = True


        if fin == True:
            post_message("[INF][종료]")
            avg = 0
            count = 0
            fin = False

        await asyncio.sleep(0.2)

async def ETH():
    unit_price = 10000
    low = 0.97
    
    ETH_buy_order = False
    ETH_fin = False
    ETH_count = 0
    ETH_avg = 0

    print("ETH start")

    while True:
        
        now = datetime.datetime.now()
        
        # 필수 매수

        if now.hour % 12 == 6 and now.minute == 0 and 0 <= now.second <= 2:
            if upbit.get_balance("KRW") < unit_price:
                post_message(f"[INF][not enough money][exit]")
                sys.exit()

            else:
                ETH_prev_amount = upbit.get_balance("KRW-ETH")

                ETH_order = pyupbit.get_orderbook("KRW-ETH")
                ETH_bid1 = ETH_order[0]['orderbook_units'][0]['bid_price']
                ETH_amount = math.floor(unit_price * 0.9995 / ETH_bid1 * 100000000) / 100000000

                ETH_buy_ret = upbit.buy_limit_order("KRW-ETH", ETH_bid1, ETH_amount)
                ETH_buy_order = True
                await asyncio.sleep(4)

        # 평단가보다 낮으면 매수

        if (now.hour % 12 == 0 and now.minute == 0 and 0 <= now.second <= 3):
            if upbit.get_balance("KRW") < unit_price:
                post_message(f"[INF][not enough money][exit]")
                sys.exit()

            else:
                if  ETH_avg * low > pyupbit.get_current_price("KRW-ETH") or  ETH_avg == 0:

                    ETH_prev_amount = upbit.get_balance("KRW-ETH")

                    ETH_order = pyupbit.get_orderbook("KRW-ETH")
                    ETH_bid1 = ETH_order[0]['orderbook_units'][0]['bid_price']
                    ETH_amount = math.floor(unit_price * 0.9995 / ETH_bid1 * 100000000) / 100000000

                    ETH_buy_ret = upbit.buy_limit_order("KRW-ETH", ETH_bid1, ETH_amount)
                    ETH_buy_order = True
                    await asyncio.sleep(4)

        # 매수 주문 체결 완료

        if ETH_buy_order == True and upbit.get_order("KRW-ETH") == []:
            ETH_avg = (ETH_avg * ETH_prev_amount + ETH_bid1 * ETH_amount) / upbit.get_balance("KRW-ETH")
            ETH_count += 1
            post_message(f"[INF][매수]\n{ETH_buy_ret['market']} {ETH_buy_ret['price']}\n평단가 : {ETH_avg : .3f}\n{ETH_count}차")
            ETH_buy_order = False

        # 매수 주문 미체결 & 취소

        if now.hour % 6 == 0 and now.minute == 15 and 0 <= now.second <= 3 and ETH_buy_order == True and upbit.get_order("KRW-ETH") != []:
            upbit.cancel_order(ETH_buy_ret['uuid'])
            post_message(f"[INF][매수 미체결]\n{ETH_buy_ret['market']} {ETH_buy_ret['price']}")
            ETH_buy_order = False

        # 5퍼 익절 매도 주문

        if ETH_avg * 1.05 < pyupbit.get_current_price("KRW-ETH") and upbit.get_balance("KRW-ETH") > 0.0001 and ETH_avg != 0:
            ETH_order = pyupbit.get_orderbook("KRW-ETH")
            ETH_bid1 = ETH_order[0]['orderbook_units'][0]['ask_price'] #리스트 내의 딕셔너리에 접근
            ETH_balance = upbit.get_balance("KRW-ETH")

            ETH_sell_ret = upbit.sell_limit_order("KRW-ETH", ETH_bid1, upbit.get_balance("KRW-ETH"))

            await asyncio.sleep(180)

            # 매도 주문 미체결 & 취소
            if upbit.get_order("KRW-ETH") != []:
                upbit.cancel_order(ETH_sell_ret['uuid'])
                post_message(f"[INF][매도 미체결]\n{ETH_buy_ret['market']} {ETH_buy_ret['price']}")

            # 매도 주문 체결
            elif upbit.get_order("KRW-ETH") == []:
                post_message(f"[INF][매도] {ETH_sell_ret['market']} {ETH_sell_ret['price']}")
                
                if ETH_bid1 > ETH_avg:
                    ETH_결과 = "이득"
                else:
                    ETH_결과 = "손해"
            
                ETH_잔고 = upbit.get_balance("KRW")
                ETH_수익률 =  ((ETH_bid1 - ETH_avg) * ETH_balance ) / 1000000 * 100

                post_message(f"[INF][{ETH_결과}] {ETH_수익률 : .3f} %\n변화 : {(ETH_bid1 - ETH_avg) * ETH_balance : .3f}\n잔고 : {ETH_잔고 : .3f}")
                ETH_fin = True

        if ETH_fin == True:
            post_message("[INF][종료]")
            ETH_avg = 0
            ETH_count = 0
            ETH_fin = False

        await asyncio.sleep(0.2)

async def main():
    coro1 = BTC()
    coro2 = ETH()
    await asyncio.gather(
        coro1,
        coro2
        )

try:
    asyncio.run(main())

except Exception as e:
    # panic and halt the execution in case of any other error
    post_message(f"[INF][error]{type(e).__name__}\n{str(e)}")
    print(type(e).__name__, str(e))
    sys.exit()