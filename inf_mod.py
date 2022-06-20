import pyupbit
import math
import datetime
import requests
import asyncio
import sys
import urllib3

def run():
    
    async def BTC():
        unit_price = 10000
        low = 0.98
        BTC_count = float(btc_count)
        BTC_avg = float(btc_avg)

        buy_order = False
        fin = False

        print("BTC start")

        while True:
            
            now = datetime.datetime.now()
            
            # 필수 매수

            if now.hour % 12 == 6 and now.minute == 0 and 0 <= now.second <= 2:
                if upbit.get_balance("KRW") < unit_price:
                    post_message(f"[INF][not enough money][exit]")
                    sys.exit()

                else:
                    if upbit.get_balance("KRW") < unit_price * 20:
                        current_balance = upbit.get_balance("KRW")
                        post_message(f"[INF][not enough money] 잔고 : {current_balance}")

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
                    if BTC_avg * low > pyupbit.get_current_price("KRW-BTC") or BTC_avg == 0:

                        prev_amount = upbit.get_balance("KRW-BTC")

                        order = pyupbit.get_orderbook("KRW-BTC")
                        bid1 = order[0]['orderbook_units'][0]['bid_price']
                        amount = math.floor(unit_price * 0.9995 / bid1 * 100000000) / 100000000

                        buy_ret = upbit.buy_limit_order("KRW-BTC", bid1, amount)
                        buy_order = True
                        await asyncio.sleep(4)

            # 매수 주문 체결 완료

            if buy_order == True and upbit.get_order("KRW-BTC") == []:
                BTC_avg = (BTC_avg * prev_amount + bid1 * amount) / upbit.get_balance("KRW-BTC")
                BTC_count += 1
                post_message(f"[INF][매수]\n{buy_ret['market']} {buy_ret['price']}\n평단가 : {BTC_avg : .3f}\n{BTC_count}차")
                buy_order = False
                update_state(BTC_count, BTC_avg, ETH_count, ETH_avg)

            # 매수 주문 미체결 & 취소

            if now.hour % 6 == 0 and now.minute == 15 and 0 <= now.second <= 3 and buy_order == True and upbit.get_order("KRW-BTC") != []:
                upbit.cancel_order(buy_ret['uuid'])
                post_message(f"[INF][매수 미체결]\n{buy_ret['market']} {buy_ret['price']}")
                buy_order = False

            # 5퍼 익절 매도 주문
            BTC_price = pyupbit.get_current_price("KRW-BTC")
            if BTC_price == None:
                if error <= 3:
                    error = error + 1
                    post_message(f"[INF][error] TypeError")
                    await asyncio.sleep(60)
                    continue
                elif error > 3:
                    post_message(f"[INF][error] TypeError")
                    await asyncio.sleep(3600)
                    continue
            else:
                error = 0

            if BTC_avg * 1.05 < BTC_price and upbit.get_balance("KRW-BTC") > 0.0001 and BTC_avg != 0:
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
                    
                    if bid1 > BTC_avg:
                        결과 = "이득"
                    else:
                        결과 = "손해"
                
                    잔고 = upbit.get_balance("KRW") + upbit.get_balance("KRW-BTC") * pyupbit.get_current_price("KRW-BTC") + upbit.get_balance("KRW-ETH") * pyupbit.get_current_price("KRW-ETH")
                    수익률 =  ((bid1 - BTC_avg) * balance ) / 1000000 * 100

                    post_message(f"[INF][{결과}] {수익률 : .3f} %\n변화 : {(bid1 - BTC_avg) * balance : .3f}\n잔고 : {잔고 : .3f}")
                    fin = True


            if fin == True:
                post_message("[INF][종료]")
                BTC_avg = 0
                BTC_count = 0
                fin = False
                update_state(BTC_count, BTC_avg, ETH_count, ETH_avg)

            await asyncio.sleep(0.5)

    async def ETH():
        unit_price = 10000
        low = 0.97
        
        ETH_buy_order = False
        ETH_fin = False
        ETH_count = float(eth_count)
        ETH_avg = float(eth_avg)

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
                update_state(BTC_count, BTC_avg, ETH_count, ETH_avg)

            # 매수 주문 미체결 & 취소

            if now.hour % 6 == 0 and now.minute == 15 and 0 <= now.second <= 3 and ETH_buy_order == True and upbit.get_order("KRW-ETH") != []:
                upbit.cancel_order(ETH_buy_ret['uuid'])
                post_message(f"[INF][매수 미체결]\n{ETH_buy_ret['market']} {ETH_buy_ret['price']}")
                ETH_buy_order = False

            # 5퍼 익절 매도 주문

            ETH_price = pyupbit.get_current_price("KRW-ETH")
            if ETH_price == None:
                if error <= 3:
                    error = error + 1
                    post_message(f"[INF][error] TypeError")
                    await asyncio.sleep(60)
                    continue
                elif error > 3:
                    post_message(f"[INF][error] TypeError")
                    await asyncio.sleep(3600)
                    continue
            else:
                error = 0

            if ETH_avg * 1.06 < ETH_price and upbit.get_balance("KRW-ETH") > 0.0001 and ETH_avg != 0:
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
                
                    ETH_잔고 = upbit.get_balance("KRW") + upbit.get_balance("KRW-BTC") * pyupbit.get_current_price("KRW-BTC") + upbit.get_balance("KRW-ETH") * pyupbit.get_current_price("KRW-ETH")
                    ETH_수익률 =  ((ETH_bid1 - ETH_avg) * ETH_balance ) / 1000000 * 100

                    post_message(f"[INF][{ETH_결과}] {ETH_수익률 : .3f} %\n변화 : {(ETH_bid1 - ETH_avg) * ETH_balance : .3f}\n잔고 : {ETH_잔고 : .3f}")
                    ETH_fin = True

            if ETH_fin == True:
                post_message("[INF][종료]")
                ETH_avg = 0
                ETH_count = 0
                ETH_fin = False
                update_state(BTC_count, BTC_avg, ETH_count, ETH_avg)

            await asyncio.sleep(0.5)

    async def main():
        coro1 = BTC()
        coro2 = ETH()
        await asyncio.gather(
            coro1,
            coro2
            )

    def post_message(text):
        myToken = token
        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+myToken},
            data={"channel": "#upbit","text": text},
            verify=False
        )
        print(response)

    def update_state(BTC_count, BTC_avg, ETH_count, ETH_avg):
        with open("coin_state.txt", "w") as f:
            f.write(BTC_count + "\n")
            f.write(BTC_avg + "\n")
            f.write(ETH_count + "\n")
            f.write(ETH_avg + "\n")

    

# running codes

    with open("upbit_key.txt", "r") as f:
        key1 = f.readline().strip()
        key2 = f.readline().strip()

    with open("coin_state.txt", "r") as f:
        btc_count = f.readline().strip()
        btc_avg = f.readline().strip()
        eth_count = f.readline().strip()
        eth_avg = f.readline().strip()    

    with open("slack_token.txt", "r") as f:
        token = f.readline().strip()    

    upbit = pyupbit.Upbit(key1, key2)
    error = 0

    BTC_count = 0
    BTC_avg = 0
    ETH_count = 0
    ETH_avg = 0

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    post_message("Start Infinite BTC, ETH Auto Trading Program For INF.")

    asyncio.run(main())