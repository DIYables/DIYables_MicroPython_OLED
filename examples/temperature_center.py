from machine import I2C, Pin
from DIYables_MicroPython_OLED import OLED_SSD1306_I2C
import utime

# Initialize I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)  # Adjust pins according to your setup

# Initialize the OLED display
oled = OLED_SSD1306_I2C(128, 64, i2c)

# Clear the display
oled.clear_display()
oled.display()

def oled_display_center(oled, text):
    # Get the text bounds (width and height) of the string
    x1, y1, width, height = oled.get_text_bounds(text, 0, 0)

    # Set cursor to the calculated centered position
    cursor_x = (oled.WIDTH - width) // 2
    cursor_y = (oled.HEIGHT - height) // 2
    oled.set_cursor(cursor_x, cursor_y)

    # Print the text on the display
    oled.println(text)

    # Refresh the display to show the text
    oled.display()

oled.set_text_size(3)
temperature = "23.7" + OLED_SSD1306_I2C.DEGREE_SYMBOL + "C"
oled_display_center(oled, temperature)

