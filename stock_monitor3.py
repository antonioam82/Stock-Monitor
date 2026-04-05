#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import yfinance as yf
from pynput import keyboard
from colorama import init, Fore, Back, Style
import time
import warnings
import pandas as pd
from tzlocal import get_localzone
import pandas_market_calendars as mcal

warnings.filterwarnings("ignore")

init()
stop = False

'''MARKET_SUFFIXS = {
    "": "NYSE",
    #"": "NASDAQ",   
    "T": "JPX",
    "L": "LSE",
    "TO": "TSX",
    "HK": "HKEX",
    "SS": "SSE",
    "AX": "ASX",
    "NS": "NSE",
    "BO": "BSE",
    "SW": "SIX",
}'''

def on_press(key):
    global stop
    if key == keyboard.Key.space:
        stop = True
        print('Wait until application ends...')
        return False

from tzlocal import get_localzone
import pandas as pd
import pandas_market_calendars as mcal
from colorama import Fore

def is_open_now():
    cal = mcal.get_calendar('NYSE')

    local_tz = get_localzone()

    now = pd.Timestamp.now(tz=local_tz)
    today = now.date()

    schedule = cal.schedule(start_date=today, end_date=today)

    if schedule.empty:
        print(Fore.BLUE + "NYSE MARKET CURRENTLY CLOSED TODAY" + Fore.RESET)

        five_days_later = today + pd.Timedelta(days=5)
        next_schedule = cal.schedule(start_date=today, end_date=five_days_later)

        if not next_schedule.empty:
            next_open_local = next_schedule.iloc[0]["market_open"].tz_convert(local_tz)
            print(Fore.BLUE + f'NEXT SESSION: {next_open_local}' + Fore.RESET)
        return False

    market_open = schedule.iloc[0]["market_open"]
    market_close = schedule.iloc[0]["market_close"]

    # CONVERSION A HORA LOCAL
    market_open_local = market_open.tz_convert(local_tz)
    market_close_local = market_close.tz_convert(local_tz)

    print(Fore.BLUE + f'OPEN (LOCAL): {market_open_local}' + Fore.RESET)
    print(Fore.BLUE + f'CLOSE (LOCAL): {market_close_local}' + Fore.RESET)

    if market_open <= now <= market_close:
        return True
    else:
        print(Fore.RED + "NYSE MARKET IS CLOSED NOW" + Fore.RESET)
        print(Fore.BLUE + f'NEXT OPEN: {market_open_local}' + Fore.RESET)
        return False

def quoter(args):
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    prev_value = None
    downloaded = False

    ticker_symbol = f"^{args.ticker}" if args.use_index else args.ticker
    '''ticker_symbol = args.ticker
    if "." in ticker_symbol:
        market = ticker_symbol.split(".")[1]
    else:
        market = ""
    print("MERCADO: ",market)'''

    #######################################################################3
    '''cal = mcal.get_calendar("NYSE")
    today = pd.Timestamp.today().date()
    five_days_later = today + pd.Timedelta(days=5)
    schedule = cal.schedule(start_date=today, end_date=today)
    if len(schedule) == 0:
        print("empty")
    #print(Fore.BLUE + f'NEXT SESSION: {schedule.iloc[0]["market_open"]}' + Fore.RESET)'''
    
    #######################################################################
        
    try:
        print(Fore.BLACK + Back.WHITE + f"\nREAL TIME {ticker_symbol} QUOTATION -[PRESS SPACE BAR TO EXIT]" + Fore.RESET + Back.RESET)

        try:
            prev_day = yf.download(ticker_symbol, period="5d", interval="1d")
            #prev_day = yf.download(ticker_symbol, period="5d", interval="1d", auto_adjust=False, multi_level_index=False)
        

            # Convertimos todos los valores en float
            last_day_open_price = float(prev_day["Open"].iloc[-2])
            last_day_high_price = float(prev_day["High"].iloc[-2])
            last_day_low_price = float(prev_day["Low"].iloc[-2])
            last_day_close_price = float(prev_day["Close"].iloc[-2])
            last_day_volume = float(prev_day["Volume"].iloc[-2])

            dec = args.decimals
            last_datetime = prev_day.index[-2]

            print(Fore.YELLOW + Style.BRIGHT + f"{last_datetime} | Ticker: {ticker_symbol} | Low: {last_day_low_price:.{dec}f} | High: {last_day_high_price:.{dec}f} |"
                    f" Open: {last_day_open_price:.{dec}f} | Volume: {last_day_volume:.{dec}f} | Close: {last_day_close_price:.{dec}f}" + Fore.RESET + Style.RESET_ALL)
            downloaded = True

            if not args.active_calendar:
                is_open = is_open_now()###############################
            else:
                is_open = True
                
        
        except Exception as e:
            print(Fore.RED + Style.BRIGHT + f"ERROR: {str(e)}" + Fore.RESET + Style.RESET_ALL)
            #stop = True

        if downloaded and is_open:
            while not stop:
                try:
                    stock_data = yf.download(ticker_symbol, period="1d", interval="1m").tail(1)

                    # Convertimos a float los valores más recientes
                    last_open_price = float(stock_data["Open"].iloc[-1])
                    last_high_price = float(stock_data["High"].iloc[-1])
                    last_low_price = float(stock_data["Low"].iloc[-1])
                    last_close_price = float(stock_data["Close"].iloc[-1])
                    last_volume = float(stock_data["Volume"].iloc[-1])

                    current_datetime = stock_data.index[-1]

                    # Determinar color de línea
                    if args.color:
                        line_color = Fore.BLUE
                        if prev_value is None or last_close_price == prev_value:
                            color = Fore.YELLOW
                        elif last_close_price > prev_value:
                            color = Fore.GREEN
                        else:
                            color = Fore.RED
                    else:
                        color = Fore.GREEN
                        line_color = Fore.GREEN

                    # Diferencias y porcentaje
                    diference = last_close_price - last_day_close_price
                    percentage = (diference / last_day_close_price) * 100

                    if diference > 0:
                        diference_color = Fore.GREEN + "+"
                    elif diference < 0:
                        diference_color = Fore.RED
                    else:
                        diference_color = Fore.YELLOW

                    print(line_color + Style.BRIGHT + f"{current_datetime} | Ticker: {ticker_symbol} | Low: {last_low_price:.{dec}f} | High: {last_high_price:.{dec}f} | Open: {last_open_price:.{dec}f} |"
                            f" Volume: {last_volume:.{dec}f} | Close: " + color + f"{last_close_price:.{dec}f}    "
                            + diference_color + f"{diference:.{dec}f} ({percentage:.{dec}f}%)" + Fore.RESET + Style.RESET_ALL)

                    prev_value = last_close_price
                    time.sleep(args.time_delay)

                    if stop:
                        print("\nProcess terminated by user.")
                        break

                except Exception as e:
                    print(Fore.RED + Style.BRIGHT + "\nUNEXPECTED ERROR: " + str(e) + Fore.RESET + Style.RESET_ALL)
                    break
         
                
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + str(e) + Fore.RESET + Style.RESET_ALL)

    #print("NADA POR AQUI")

def main():
    parser = argparse.ArgumentParser(prog="STOCK MONITOR 1.1", description="Show stock quotation in real time",
                                     epilog="REPO: https://github.com/antonioam82/Stock-Monitor")
    parser.add_argument('-tick', '--ticker', required=True, type=str, help='Ticker name')
    parser.add_argument('-clr', '--color', action='store_true', help='Use this action for color close values')
    parser.add_argument('-delay', '--time_delay', type=float, default=5, help='Call delay to the API, in seconds')
    parser.add_argument('-uind', '--use_index', action='store_true', default=None, help='Use index')
    parser.add_argument('-decim', '--decimals', type=int, default=2, help="Number of value decimals")
    parser.add_argument('-atc', '--active_calendar', action='store_true', help='Force to show results despite market currently closed')

    args = parser.parse_args()
    if args.time_delay >= 0.5:
        quoter(args)
    else:
        parser.error(Fore.RED + Style.BRIGHT + "time delay value must be greater than or equal to 0.5" + Fore.RESET + Style.RESET_ALL)

if __name__ == '__main__':
    main()

