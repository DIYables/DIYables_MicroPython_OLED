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

# Set the cursor to the top-left corner
oled.set_cursor(0, 0)
oled.set_text_size(2)

# Print a message to the display
oled.println("Hello, World!")
oled.display()
