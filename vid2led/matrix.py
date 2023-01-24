from vid2led import util
import cv2
from rpi_ws281x import PixelStrip, Color


class Matrix:
    def __init__(self, width, height, led_pin,
                 serpentine=False, vertical=False,
                 led_freq_hz=800_000, led_dma=10, led_brightness=255,
                 led_invert=False, led_channel=0, led_strip_type=None,
                 simulated=False, simulation_magnifier=10):
        # setup some vars
        self.width = width
        self.height = height
        self.serpentine = serpentine
        self.vertical = vertical

        # is this a simulated matrix?
        self.simulated = simulated

        # the size of the output frame if this is simulated
        self.simulation_size = (self.width * simulation_magnifier, self.height * simulation_magnifier)

        # make the coordinate table
        self.coordinates = util.generate_coordinate_table(width, height,
                                                          serpentine=self.serpentine, vertical=self.vertical)

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
        if not self.simulated:
            # this is a real strip we are dealing with, so actually set the pixel

            # set each pixel using the frame
            for y in range(0, self.height):
                for x in range(0, self.width):
                    self.strip.setPixelColor(self.coordinates[(x, y)],  # get target led from table
                                             Color(int(frame[y, x][2]), int(frame[y, x][1]), int(frame[y, x][0])))  # get color from frame

            # display the changes
            self.strip.show()
        else:
            # this is a simulated strip, so attempt to display the frame using imshow

            # resize the frame
            img = cv2.resize(frame, self.simulation_size)

            # show the frame
            cv2.imshow(f'Simulated {self.width}x{self.height} Matrix', img)

    def clear(self):
        for i in range(0, self.width*self.height):
            self.strip.setPixelColorRGB(i, 0, 0, 0);
        self.strip.show()
