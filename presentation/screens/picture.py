import os

from PIL import Image, ImageDraw, ImageFont
from data.plot import Plot
from presentation.observer import Observer
# from data.renko import renko as pyrenko

SCREEN_HEIGHT = 122
SCREEN_WIDTH = 250

FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'Roses.ttf'), 8)
FONT_MEDIUM = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), 20)
FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), 26)

class Picture(Observer):

    def __init__(self, observable, filename, mode):
        super().__init__(observable=observable)
        self.filename = filename
        self.mode = mode

    def form_image(self, prices, screen_draw):
        screen_draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="#ffffff")
        if self.mode == "candle":
            caption = prices[-1]
            del prices[-1]
            change = prices[-1]
            del prices[-1]
            last_element = prices[-1]
            del prices[-1]

            # flatten_prices = [item for sublist in prices for item in sublist]
            # print(flatten_prices)
            last_prices = [x[3] for x in prices]

            Plot.caption(last_element, caption, change, 100, SCREEN_WIDTH, FONT_MEDIUM, screen_draw)
            Plot.y_axis_labels(last_prices, FONT_SMALL, (0, 0), (38, 89), draw=screen_draw)
            Plot.candle(prices, size=(SCREEN_WIDTH - 45, 93), position=(41, 0), draw=screen_draw)

        elif self.mode == "line":
            array_length = len(prices)
            last_element = prices[array_length - 1]
            del prices[-1]
            array_length = len(prices)
            change = prices[array_length - 1]
            del prices[-1]
            Plot.line(prices, size=(SCREEN_WIDTH - 36, 79), position=(36, 0), draw=screen_draw)
            Plot.y_axis_labels(prices, FONT_SMALL, (0, 0), (38, 89), draw=screen_draw)
            Plot.caption(prices[len(prices) -1], last_element, change, 100, SCREEN_WIDTH, FONT_MEDIUM, screen_draw)

        # elif self.mode == "renko":
        #     array_length = len(prices)
        #     last_element = prices[array_length - 1]
        #     del prices[-1]
        #     array_length = len(prices)
        #     change = prices[array_length - 1]
        #     del prices[-1]

        #     renko_obj = pyrenko.renko()
        #     optimal_brick = renko_obj.set_brick_size(auto = True, HLC_history = prices)
        #     print("optimal")
        #     print(optimal_brick)

        #     Plot.caption(prices[len(prices) -1], last_element, change, 100, SCREEN_WIDTH, FONT_MEDIUM, screen_draw)

        screen_draw.line([(10, 98), (240, 98)])
        screen_draw.line([(39, 4), (39, 94)])
        #screen_draw.line([(60, 102), (60, 119)])
        #Plot.caption(flatten_prices[len(flatten_prices) - 1], 95, SCREEN_WIDTH, FONT_LARGE, screen_draw)

    def update(self, data):
        image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        screen_draw = ImageDraw.Draw(image)
        self.form_image(data, screen_draw)

        # if self.mode == "candle":
        #     Plot.candle(prices, size=(SCREEN_WIDTH - 45, 93), position=(41, 0), draw=screen_draw)
        # else:
        #     last_prices = [x for x in prices]
        #     Plot.line(last_prices, size=(SCREEN_WIDTH - 42, 93), position=(42, 0), draw=screen_draw)
        # screen_image_rotated = self.screen_image.rotate(180)

        # flatten_prices = [item for sublist in prices for item in sublist]
        # Plot.y_axis_labels(flatten_prices, FONT_SMALL, (0, 0), (38, 89), draw=screen_draw)
        # screen_draw.line([(10, 98), (240, 98)])
        # screen_draw.line([(39, 4), (39, 94)])
        # screen_draw.line([(60, 102), (60, 119)])
        # Plot.caption(flatten_prices[len(flatten_prices) - 1], 95, SCREEN_WIDTH, FONT_LARGE, screen_draw)
        image.save(self.filename)

    def close(self):
        pass

