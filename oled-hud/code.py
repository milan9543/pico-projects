# lib contents:
#  - adafruit_bitmap_font            
#  - adafruit_display_text     
#  - adafruit_imageload     
#  - adafruit_framebuf.mpy           
#  - adafruit_register
#  - adafruit_bus_device             
#  - adafruit_displayio_ssd1306.mpy  adafruit_gps.mpy                
#  - adafruit_ssd1306.mpy
#
# GPS wiring:       Screen wiring:
# VCC - 3.3v        GND - GND
# GND - GND         VDD - 3.3v
# RX  - GP8         SDA - GP0
# TX  - GP9         SCK - GP1

import board
import busio
# GPS
import adafruit_gps
# SSD1306
import displayio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
from adafruit_bitmap_font import bitmap_font
import terminalio

# GPS setup
uart = busio.UART(board.GP8, board.GP9, baudrate=9600, timeout=10)
gps = adafruit_gps.GPS(uart, debug=False) 
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
gps.send_command(b"PMTK220,500")

# Display setup
displayio.release_displays()

DISPLAY_WIDTH=128
DISPLAY_HEIGHT=64
i2c = busio.I2C(board.GP1, board.GP0)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)

satellite_group = displayio.Group()
bitmap = displayio.OnDiskBitmap("/gps.bmp")
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, x=32, y=0)
satellite_count_label = label.Label(
    terminalio.FONT, text="", color=0xFFFFFF, x=0, y=58
)

satellite_group.append(satellite_count_label)
satellite_group.append(tile_grid)



font = bitmap_font.load_font("/hud-font-64-64.bdf")


text_group = displayio.Group()
text_area = label.Label(
    font, text="", color=0xFFFFFF, x=0, y=32
)
text_group.append(text_area)



while True:
    gps.update()
    
    if not gps.has_fix:
        print("Waiting for fix - {} satellite(s)".format(gps.satellites))
        satellite_count_label.text = str(gps.satellites)
        display.show(satellite_group)
        continue

    speed = 0
    if gps.speed_knots is not None:
        speed_kph = gps.speed_knots * 1.85200
        if speed_kph > 5:
            speed = round(speed_kph)
        
    text_area.text = str(speed)
    display.show(text_group)
    
        


