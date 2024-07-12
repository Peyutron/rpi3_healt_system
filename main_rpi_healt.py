# Fuente original: https://github.com/adafruit/Adafruit_Python_SSD1306/blob/master/examples/stats.py
# sudo apt-get install python-smbus
# sudo apt-get install i2c-tools
# sudo i2cdetect -y 1
# sudo i2cdetect -y 0
# sudo apt install python3-pip
# pip3 install Adafruit_GPIO
# crontab -e
# @reboot sleep 30 && python3 /home/user/rpi3_healt_system/main_rpi_healt.py > /home/user/cron.log 2>&1


from healt_functions_class import *
from healt_pwm_class import *
from healt_file_class import *
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

keys = ["ip", "m0_cpul",
	"m0_cput", "m0_raml",
	"m0_cpuf", "m0_ut",
	"m0_os"
	]

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

# 128x64 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
#print("width: {}, height: {}".format(width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((2,2,width - 2,height - 2), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = +2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

hfic = System_Files()
hfc = System_Functions()
hpc = System_PWM_Fan(14, 0, 1) # pwm_pin, mode, perfil

def Save_basic_JSON(hfic_):
	hfic_.Add_json_value(keys[0], hfc.GetIP())
	hfic_.Add_json_value(keys[1], hfc.GetCPU())
	hfic_.Add_json_value(keys[2], hfc.GetTemp())
	hfic_.Add_json_value(keys[3], hfc.GetRAM())
	hfic_.Add_json_value(keys[4], hfc.GetFanPWM(hpc, 0)) #0=Proporcionar, 1=Por pasos de temperatura
	hfic_.Add_json_value(keys[5], hfc.GetUpTime())
	hfic_.Add_json_value(keys[6], hfc.GetOS())
	# print("Data Saved")

if hfic.Read_Dict() == -1:
	Save_basic_JSON(hfic)

def main():
	contador = 0
	while True:
		# Draw a black filled box to clear the image.
		draw.rectangle((0,0,width,height), outline=0, fill=0)

	    # Write two lines of text.

		draw.text((x, top),       	"IP: "	+ str(hfc.GetIP()) , font=font, fill=255)
		draw.text((x, top + 12),    	"Load: "+ str(hfc.GetCPU()) + "% ", font=font, fill=255 )
		draw.text((x + 68, top + 12,),	"T:" 	+ str(hfc.GetTemp()) + "ºC", font=font, fill=255)
		draw.text((x, top + 24),    	"RAM: " + str(hfc.GetRAM()) + "%", font=font, fill=255)
		draw.text((x, top + 36),    	"Fan: " + str(hfc.GetFanPWM(hpc, 0)) + "%", font=font, fill=255)
		draw.text((x, top + 48),    	"Ut " 	+ hfc.GetUpTime(), font=font, fill=255)

		# Display image.
		disp.image(image)
		disp.display()
		# time.sleep(0.5)
		contador = contador + 1
		if contador == 15:
			Save_basic_JSON(hfic)
			contador = 0

if __name__ == '__main__':
	main()
