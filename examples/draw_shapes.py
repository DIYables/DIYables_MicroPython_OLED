from machine import I2C, Pin
from DIYables_MicroPython_OLED import OLED_SSD1306_I2C

# Initialize I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)  # Adjust pins according to your setup

# Initialize the OLED display
oled = OLED_SSD1306_I2C(128, 64, i2c)

# Clear the display
oled.clear_display()
oled.display()

# Draw a rectangle
oled.draw_rect(10, 20, 50, 30, 1)
#oled.fill_rect(10, 20, 50, 30, 1)
oled.display()

# Draw a circle
#oled.draw_circle(64, 32, 20, 1)
oled.fill_circle(64, 32, 20, 1)
oled.display()

# Draw a triangle
oled.draw_triangle(10, 10, 60, 10, 35, 50, 1)
#oled.fill_triangle(10, 10, 60, 10, 35, 50, 1)
oled.display()

