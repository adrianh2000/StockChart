import random
from tkinter import *
import datetime
import StockData as SD

master = Tk()
canvas_width = 1200
canvas_height = 800
w = Canvas(master,
           width=canvas_width,
           height=canvas_height, bg='#AAAAAA')
w.pack()


def write_slogan():
    print("Tkinter is easy to use!")


def draw_candle(x0, y0, width, height, fill_color):
    w.create_line(x0 + width / 2, y0 - random.randint(0, 20), x0 + width / 2, y0 + height + random.randint(0, 20),
                  fill='black', width=3)
    w.create_rectangle(x0, y0, x0 + width, y0 + height, fill=fill_color)


# draw_candle(100, 100, 40, 100, "green")
# draw_candle(145, 120, 40, 100, "red")

# -------- initial code  ------------------------
# candle_width = 10
# y = canvas_height/2
# colors = ['cyan', 'blue']
# x_space = 2
# num_candles = int(canvas_width/(candle_width+x_space))
#
# for x in range(num_candles):
#     y += random.randint(-10, 5)
#     candle_height = random.randint(1, 50)
#     draw_candle(x * (candle_width + x_space), y, candle_width, candle_height, random.choice(colors))
# -------- end initial code ------------------------

# button = Button(w, text="QUIT", fg="red", command=quit)
# button.pack(side=LEFT)
# slogan = Button(w, text="Hello", command=write_slogan)
# slogan.pack(side=LEFT)

# my_candle = SD.Candle(10, 20, 5, 15, datetime.datetime(2020, 5, 17, 14, 30, 24))

# print(my_candle.to_string())
cd = SD.CandleData()
cd.load_data("xlk.txt")
# cd.print_all_candles()
blue_shades = ['#9CC0FE', '#032495']
classic_shades = ['green', 'red']
grayscale_shades = ['white', 'black']
purple_shades = ['#EDCFFF', '#AC29FA']
cd.draw_candles(w, 2100, 2180, 100, 100, canvas_width - 200, canvas_height - 200, purple_shades[0], purple_shades[1])

mainloop()
