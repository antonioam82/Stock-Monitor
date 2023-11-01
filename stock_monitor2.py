#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import yfinance as yf
from pynput import keyboard
from colorama import init, Fore, Back, Style
import time

init()

stop = False

def on_press(key):
    global stop
    if key == keyboard.Key.space:
        stop = True
        print('Wait until application ends...')
        return False

def quoter(args):
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    prev_value = ""
    
    if args.use_index:
        ticker_symbol = '^'+args.ticker
    else:
        ticker_symbol = args.ticker
    #prev_day = stock_data = yf.download(ticker_symbol, period="1d",interval="1d").tail(1)
    try:
        print(Fore.BLACK + Back.WHITE + f"\nREAL TIME {ticker_symbol} QUOTATION -[PRESS SPACE BAR TO EXIT]" + Fore.RESET + Back.RESET)
        prev_day = yf.download(ticker_symbol, period="2d", interval="1d")#["Close"].iloc[-2]
    
        last_day_open_price = prev_day["Open"].iloc[-2]
        last_day_high_price = prev_day["High"].iloc[-2]
        last_day_low_price = prev_day["Low"].iloc[-2]
        last_day_close_price = prev_day["Close"].iloc[-2]
        last_day_volume = prev_day["Volume"].iloc[-2]

        dec = args.decimals

        last_datetime = prev_day.index[-2]
    
        print(Fore.YELLOW + Style.BRIGHT + f"{last_datetime} | Ticker: {ticker_symbol} | Low: {last_day_low_price:.{dec}f} | High: {last_day_high_price:.{dec}f} | "
          f" Open: {last_day_open_price:.{dec}f} | Volume: {last_day_volume:.{dec}f} | Close: {last_day_close_price:.{dec}f}" + Fore.RESET + Style.RESET_ALL) 
        while stop == False:
            stock_data = yf.download(ticker_symbol, period="1d",interval="1m").tail(1)
            #print(stock_data)

            last_open_price = stock_data["Open"].iloc[-1]
            last_high_price = stock_data["High"].iloc[-1]
            last_low_price = stock_data["Low"].iloc[-1]
            #last_adj_close = stock_data["Adj Close"].iloc[-1]
            last_close_price = stock_data["Close"].iloc[-1]
            last_volume = stock_data["Volume"].iloc[-1]

            current_datetime = stock_data.index[-1]

            if args.color:
                line_color = Fore.BLUE
                if last_close_price == prev_value or prev_value == "":
                    color = Fore.YELLOW
                elif last_close_price > prev_value:
                    color = Fore.GREEN
                else:
                    color = Fore.RED
            else:
                color = Fore.GREEN
                line_color = Fore.GREEN

            
            diference = last_close_price - last_day_close_price
            percentage = (diference / last_day_close_price) * 100
            
            if diference > 0:
                diference_color = Fore.GREEN + "+"
            elif diference < 0:
                diference_color = Fore.RED
            else:
                diference_color = Fore.YELLOW
            
            
            print(line_color + Style.BRIGHT + f"{current_datetime} | Ticker: {ticker_symbol} | Low: {last_low_price:.{dec}f} | High: {last_high_price:.{dec}f} | Open: {last_open_price:.{dec}f} |"
                  f" Volume: {last_volume:.{dec}f} | Close: " + color + f"{last_close_price:.{dec}f}    " + diference_color + f"{diference:.{dec}f} ({percentage:.{dec}f}%)" + Fore.RESET + Style.RESET_ALL)

            prev_value = last_close_price
            time.sleep(args.time_delay)

            if stop == True:
                print("\nProcess terminated by user.")
                break
                
    except Exception as e:
        print(Fore.RED + Style.BRIGHT + str(e) + Fore.RESET + Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(prog="STOCK MONITOR 1.1",description="Show stock quotation in real time",
                                     epilog="REPO:https://github.com/antonioam82/Stock-Monitor")
    parser.add_argument('-tick', '--ticker', required=True, type=str, help='Ticker name')
    parser.add_argument('-clr', '--color', action='store_true', help='Use this action for color close values')
    parser.add_argument('-delay', '--time_delay', type=float, default=5, help='Call delay to the API, in seconds')
    parser.add_argument('-uind', '--use_index', action='store_true', default=None, help='Use index')
    parser.add_argument('-decim', '--decimals', type=int, default=2, help="Number of values decimals")

    
    args = parser.parse_args()
    if args.time_delay >= 0.5:
        quoter(args)
    else:
        parser.error(Fore.RED+Style.BRIGHT+"time delay value must be greater than or equal to 0.5"+Fore.RESET+Style.RESET_ALL)

if __name__ == '__main__':
    main()
