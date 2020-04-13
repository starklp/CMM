# To demonstrate the usage of the device we'll initialize it and read the analog inputs from the Python REPL.
# Run the following code to import the necessary modules, initialize the SPI connection, assign a chip select pin, and create the MCP3008 object:

import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

# Next, we'll create an analog input channel on the MCP3008 pin 0:

channel = AnalogIn(mcp, MCP.P0)

# Now you're ready to read the raw ADC value and the channel voltage with the following properties:
# value - Returns the value of an ADC pin as an integer.
# voltage - Returns the voltage from the ADC pin as a floating point value, scaled 16 bits to remain consistent with other ADCs.

# For example, to print the raw ADC value and the channel voltage, run the following:

print('Raw ADC Value: ', channel.value)
print('ADC Voltage: ' + str(channel.voltage) + 'V')
