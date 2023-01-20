import util
import cv2
from rpi_ws281x import PixelStrip, Color


class Matrix:
    def __init__(self, width, height, led_pin,
                 led_freq_hz=800_000, led_dma=10, led_brightness=255,
                 led_invert=False, led_channel=0, serpentine=False,
                 led_strip_type=None):
        # setup some vars
        self.width = width
        self.height = height
        self.serpentine = serpentine

        # make the coordinate table
        self.coordinates = util.generate_coordinate_table(width, height, serpentine)

        # setup the led strip
        self.strip = PixelStrip(self.width * self.height,
                                led_pin,
                                led_freq_hz,
                                led_dma,
                                led_invert,
                                led_brightness,
                                led_channel,
                                strip_type=led_strip_type)
        self.strip.begin()

    def display(self, frame):
        # set each pixel using the frame
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.strip.setPixelColor(self.coordinates[(x, y)],  # get target led from table
                                         Color(frame[x, y][0], frame[x, y][1], frame[x, y][2]))  # get color from frame

        # display the changes
        self.strip.show()
