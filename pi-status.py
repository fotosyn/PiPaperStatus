import socket
import subprocess
import qrcode

from PIL import Image, ImageFont, ImageDraw
from inky.auto import auto
from datetime import datetime

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode("utf-8")
    
# Get the IP address of the device (not 127.0.0.1) using a shell cmd    
ip = run_cmd("hostname -I")
device_ip = ip.split() #split the elements so we can grab the IP address
device_port = 8000 # This is the port localhost is serving on. Change to suit

# Create a string with these details to display
device_link = str(device_ip[0]) + ":" + str(device_port) 

# Get the hostname (eg. raspberrypi) to present on the display
device_name = run_cmd("hostname")
device_path = "/home/pi/your/path/"

# Give your device a legible name which shows in larger text
device_label = "DEVICE LABEL"

# Get the time this device was started at
now = datetime.now()
device_start = now.strftime("%d %b %Y at %H:%M:%S")

try:
    inky_display = auto(ask_user=True, verbose=True)
except TypeError:
    raise TypeError("You need to update the Inky library to >= v1.1.0")

scale_size = 1.0
padding_horiz = 10
padding_vert = 5
font_size = 14
text_line = font_size
qr_width = 50


# Sometimes it's nice to know what's going on. Some of the older displays output at the lowest res.
# Newer SSD1608 units will ouput at 250 x 122
print(inky_display.resolution)

# Accomodate a range of paper sizes
if inky_display.resolution == (600, 448):
    scale_size = 2.20
    padding_horiz = int(padding_horiz * scale_size)
    padding_vert = int(padding_vert * scale_size)
    font_size = int(font_size * scale_size)
    text_line = font_size
    
if inky_display.resolution == (400, 300):
    scale_size = 2.20
    padding_horiz = int(padding_horiz * scale_size)
    padding_vert = int(padding_vert * scale_size)
    font_size = int(font_size * scale_size)
    text_line = font_size

if inky_display.resolution == (250, 122):
    scale_size = 1.25
    padding_horiz = int(padding_horiz * scale_size)
    padding_vert = int(padding_vert * scale_size)
    font_size = int(font_size * scale_size)
    text_line = font_size
    
if inky_display.resolution == (212, 104):
    scale_size = 1.0
    qr_width = 40

# Generate a QR code to be scanned by another device's camera
qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=0)
qr.add_data("http://" + device_link)
qr.make(fit=True)
qr_height = qr_width
qr_size = qr_width, qr_height

# Render the QR code for display
device_qr = qr.make_image(fill='black', back_color='white')
device_qr.thumbnail(qr_size)

# Define some decent system fonts for the display
label_font = ImageFont.truetype("Roboto-Bold.ttf", font_size * 2)
detail_font = ImageFont.truetype("RobotoCondensed-Regular.ttf", font_size)

# Start the render process
img = Image.new('P', inky_display.resolution)
display = ImageDraw.Draw(img)

# Render the device details
display.text(((padding_horiz * 2) + qr_width, padding_vert), device_label, fill=inky_display.RED, anchor="ls", font=label_font)
display.text(((padding_horiz * 2) + qr_width, padding_vert + qr_height), device_link, fill=inky_display.BLACK, anchor="ls", font=detail_font)
display.text(((padding_horiz * 2) + qr_width, padding_vert+text_line+qr_height), device_name, fill=inky_display.BLACK, anchor="ls", font=detail_font)
display.text(((padding_horiz * 2) + qr_width, padding_vert+(text_line*2)+qr_height), device_start, fill=inky_display.BLACK, anchor="ls", font=detail_font)

# Show a neat little icon (change to suit)
berrycamicon = Image.open(device_path + "berrycam-icon-paper.png")
berrycamicon_resized = berrycamicon.resize((qr_width,qr_height))

# Map the icon to the 3 colour palette of the InkyPhat
imageWithColorPalette = device_qr.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=2)
palettedata = [255, 255, 255, 0, 0, 0, 255, 0, 0]
imageWithColorPalette.putpalette(palettedata)
img.paste(berrycamicon.resize((qr_width,qr_height)), (padding_horiz, padding_vert))
img.paste(imageWithColorPalette, (padding_horiz, (padding_vert * 2) + qr_height))

# Dependent on your device setup, rotate this 180 to show right way up. Or upside down. Depends really! 
inky_display.set_image(img.rotate(180))

# Output that shizz to the InkyPhat!
inky_display.show()
