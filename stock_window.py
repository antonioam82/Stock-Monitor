import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import yfinance as yf
from matplotlib import style
import argparse
import threading
import warnings
import os
warnings.filterwarnings("ignore")

style.use('dark_background')
root = tk.Tk()
root.title("Stock Window")
root.configure(background="gray")
root.geometry("900x650")

current_dir = tk.StringVar()
current_dir.set(os.getcwd())

tk.Entry(root, textvariable=current_dir,state="readonly").pack(side=tk.TOP,fill=tk.X)


root.mainloop()
