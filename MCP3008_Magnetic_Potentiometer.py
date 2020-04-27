from time import sleep
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
chan_0 = AnalogIn(mcp, MCP.P0)
chan_1 = AnalogIn(mcp, MCP.P1)
while True:
    print((chan_1.value / 181.867) - 37.4776072)
    sleep(1.0)




