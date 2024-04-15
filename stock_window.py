import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import yfinance as yf
from matplotlib import style
import warnings
warnings.filterwarnings("ignore")

style.use('dark_background')
root = tk.Tk()
root.title("Stock Window")
root.configure(background="gray")
root.geometry("900x650")


root.mainloop()
