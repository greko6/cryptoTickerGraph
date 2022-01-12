import os

from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in13_V2

from data.plot import Plot
from presentation.observer import Observer

SCREEN_HEIGHT = epd2in13_V2.EPD_WIDTH  # 122
SCREEN_WIDTH = epd2in13_V2.EPD_HEIGHT  # 250

FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'Roses.ttf'), 8)
FONT_MEDIUM = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), 20)
FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), 26)

class Epd2in13v2(Observer):

    def __init__(self, observable, mode):
        super().__init__(observable=observable)
        self.epd = epd2in13_V2.EPD()
        self.screen_image = self._init_display(self.epd)
        self.screen_draw = ImageDraw.Draw(self.screen_image)
        self.mode = mode

    @staticmethod
    def _init_display(epd):
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)
        screen_image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        epd.displayPartBaseImage(epd.getbuffer(screen_image))
        epd.init(epd.PART_UPDATE)
        return screen_image

    def form_image(self, prices, screen_draw):
        screen_draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="#ffffff")
        screen_draw = self.screen_draw
        if self.mode == "candle":
            array_length = len(prices)
            last_element = prices[array_length - 1]
            del prices[-1]
            array_length = len(prices)
            change = prices[array_length - 1]
            del prices[-1]
            Plot.candle(prices, size=(SCREEN_WIDTH - 45, 93), position=(41, 0), draw=screen_draw)
        else:
            array_length = len(prices)
            last_element = prices[array_length - 1]
            del prices[-1]
            array_length = len(prices)
            change = prices[array_length - 1]
            del prices[-1]
            Plot.line(prices, size=(SCREEN_WIDTH - 36, 79), position=(36, 0), draw=screen_draw)

#        Plot.y_axis_labels(prices, FONT_SMALL, (0, 0), (32, 76), draw=screen_draw)
        Plot.y_axis_labels(prices, FONT_SMALL, (0, 0), (38, 89), draw=screen_draw)
        screen_draw.line([(10, 98), (240, 98)])
        screen_draw.line([(39, 4), (39, 94)])
        #screen_draw.line([(60, 102), (60, 119)])
        Plot.caption(prices[len(prices) -1], last_element, change, 100, SCREEN_WIDTH, FONT_MEDIUM, screen_draw)
        #Plot.caption(flatten_prices[len(flatten_prices) - 1], 95, SCREEN_WIDTH, FONT_LARGE, screen_draw)

    def update(self, data):
        self.form_image(data, self.screen_draw)
        screen_image_rotated = self.screen_image.rotate(180)
        # TODO: add a way to switch bewen partial and full update
        # epd.presentation(epd.getbuffer(screen_image_rotated))
        self.epd.displayPartial(self.epd.getbuffer(screen_image_rotated))

    @staticmethod
    def close():
        epd2in13_V2.epdconfig.module_exit()
