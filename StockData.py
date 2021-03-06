import datetime
import math


class Candle:
    def __init__(self, open_, high_, low_, close_, date_: datetime):
        self.open = open_
        self.high = high_
        self.low = low_
        self.close = close_
        self.date = date_

    def to_string(self):
        return "o=" + str(self.open) + ", h=" + str(self.high) + ", l=" + str(self.low) + ", c=" + \
               str(self.close) + ", d=" + str(self.date)


class CandleData:
    def __int__(self):
        self.all_candles = []
        pass

    def load_data(self, filename, filepath=''):
        self.all_candles = []

        f = open(filepath + filename, "r")

        # read header
        f.readline()

        # read all candles
        cur_line = f.readline()
        while "end" not in cur_line:
            candle_info = cur_line.split(',')
            candle_date = datetime.datetime.strptime(candle_info[0], '%Y-%m-%d')
            candle_open = float(candle_info[1])
            candle_high = float(candle_info[2])
            candle_low = float(candle_info[3])
            candle_close = float(candle_info[4])

            new_candle = Candle(candle_open, candle_high, candle_low, candle_close, candle_date)
            self.all_candles.append(new_candle)
            cur_line = f.readline()

    # returns a list with lowest low and highest high for the selected period
    def get_bounds(self, index_from, index_to):
        min_low = self.all_candles[index_from].low
        max_high = self.all_candles[index_from].high
        for index in range(index_from, index_to):
            if self.all_candles[index].low < min_low:
                min_low = self.all_candles[index].low

            if self.all_candles[index].high > max_high:
                max_high = self.all_candles[index].high

        scale = self.get_axe_y_prices(min_low, max_high)
        return [scale[0], scale[-1]]

    def print_all_candles(self):
        for cur_candle in self.all_candles:
            print(cur_candle.to_string())

    @staticmethod
    def convert_price_to_display_coordinates(price, min_price, max_price, y0, display_height):
        ratio_y = (price - min_price) / (max_price - min_price)
        coord_y = y0 + (1-ratio_y) * display_height

        return coord_y

    # returns a list with the vertical labels
    @staticmethod
    def get_axe_y_prices(min_price, max_price):
        min_power_10 = int(math.log(min_price, 10))

        min_price_y = min_price - min_price % min_power_10
        max_price_y = max_price
        num_divisions = 1000
        prices_list_y = []
        target_num_divisions = 10
        step_list = [.5, 1, 2, 5, 10, 50, 100, 200, 500, 1000]
        step_list_index = -1

        while (num_divisions > target_num_divisions) and (step_list_index < len(step_list)):
            step_list_index += 1
            step_y = step_list[step_list_index]
            num_divisions = (max_price_y - min_price_y) / step_y

        cur_price_y = min_price_y
        div_ctr = 0
        while div_ctr < num_divisions+1:
            prices_list_y.append(cur_price_y)
            cur_price_y += step_y
            div_ctr += 1

        return prices_list_y

    def draw_vertical_axe(self, canvas, x0, min_price, max_price, y0, display_width, display_height, num_divisions,
                          line_color='black'):
        # step_y = (max_price - min_price) / num_divisions

        scale = self.get_axe_y_prices(min_price, max_price)
        # scale_low = scale[0]
        # scale_high = scale[-1]
        i = 0

        while i < len(scale):
            cur_price = scale[i]
            y = self.convert_price_to_display_coordinates(cur_price, min_price, max_price, y0, display_height)
            canvas.create_line(x0-5, y, x0+5, y, fill=line_color, width=3)
            canvas.create_line(x0+5, y, x0+display_width, y, fill=line_color, width=1, dash=(2, 4))
            s_price = str(int(cur_price * 100)/100)
            canvas.create_text(x0 - 5 - len(s_price)*3, y, text=s_price)
            i += 1

    def draw_candles(self, canvas, index_from, index_to, x0, y0, display_width, display_height,
                     color_up='green', color_down='red'):
        num_candles = index_to - index_from
        total_col_width = display_width / num_candles
        candle_separation = int(total_col_width * .2)
        candle_width = int(total_col_width) - candle_separation
        vertical_bounds = self.get_bounds(index_from, index_to)
        min_price = vertical_bounds[0]
        max_price = vertical_bounds[1]

        # draw background box
        canvas.create_rectangle(x0, y0, x0 + display_width, y0 + display_height, fill='#DDDDDD')

        # draw axes
        self.draw_vertical_axe(canvas, x0, min_price, max_price, y0, display_width, display_height, 10, '#FF00FF')

        for index in range(index_from, index_to):
            cur_candle = self.all_candles[index]
            candle_x = x0 + (index - index_from) * int(total_col_width)
            candle_openY = self.convert_price_to_display_coordinates(cur_candle.open, min_price, max_price, y0,
                                                                     display_height)
            candle_highY = self.convert_price_to_display_coordinates(cur_candle.high, min_price, max_price, y0,
                                                                     display_height)
            candle_lowY = self.convert_price_to_display_coordinates(cur_candle.low, min_price, max_price, y0,
                                                                    display_height)
            candle_closeY = self.convert_price_to_display_coordinates(cur_candle.close, min_price, max_price, y0,
                                                                      display_height)

            # draw candle
            fill_color = 'black'
            if cur_candle.open > cur_candle.close:
                fill_color = color_up
            elif cur_candle.open < cur_candle.close:
                fill_color = color_down

            canvas.create_line(candle_x + int(candle_width/2), candle_highY, candle_x + int(candle_width/2),
                               candle_lowY, fill='black', width=3)

            canvas.create_rectangle(candle_x, candle_openY, candle_x + candle_width, candle_closeY, fill=fill_color)


