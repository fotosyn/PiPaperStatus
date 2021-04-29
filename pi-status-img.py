import socket
import subprocess
import qrcode

from PIL import Image, ImageFont, ImageDraw
from datetime import datetime

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode("utf-8")

def quantizetopalette(silf, palette, dither=False):
    """Convert an RGB or L mode image to use a given P image's palette."""

    silf.load()

    # use palette from reference image
    palette.load()
    if palette.mode != "P":
        raise ValueError("bad mode for palette image")
    if silf.mode != "RGB" and silf.mode != "L":
        raise ValueError(
            "only RGB or L mode images can be quantized to a palette"
            )
    im = silf.im.convert("P", 1 if dither else 0, palette.im)
    # the 0 above means turn OFF dithering

    # Later versions of Pillow (4.x) rename _makeself to _new
    try:
        return silf._new(im)
    except AttributeError:
        return silf._makeself(im)
    
ip = run_cmd("hostname -I")
device_ip = ip.split()
device_port = 8000
device_link = str(device_ip[0]) + ":" + str(device_port)
print(device_link)
device_name = run_cmd("hostname")
device_path = "/home/pi/berrycam/status/"
device_label = "WIDE"

now = datetime.now()
device_start = now.strftime("%d %b %Y at %H:%M:%S")

scale_size = 1.0
padding_horiz = 10
padding_vert = 5
font_size = 14
text_line = font_size
qr_width = 40

qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=0)
qr.add_data("http://" + device_link)
qr.make(fit=True)
qr_height = qr_width
qr_size = qr_width, qr_height

device_qr = qr.make_image(fill='black', back_color='white')
device_qr.thumbnail(qr_size)

label_font = ImageFont.truetype("Piboto-Bold.ttf", font_size * 2)
detail_font = ImageFont.truetype("PibotoCondensed-Regular.ttf", font_size)

img = Image.new('RGB', (212,104), "white")
display = ImageDraw.Draw(img)
display.text(((padding_horiz * 2) + qr_width, padding_vert), device_label, fill="red", anchor="ls", font=label_font)
display.text(((padding_horiz * 2) + qr_width, padding_vert + qr_height), device_link, fill="black", anchor="ls", font=detail_font)
display.text(((padding_horiz * 2) + qr_width, padding_vert+text_line+qr_height), device_name, fill="black", anchor="ls", font=detail_font)
display.text(((padding_horiz * 2) + qr_width, padding_vert+(text_line*2)+qr_height), device_start, fill="black", anchor="ls", font=detail_font)

berrycamicon = Image.open(device_path + "berrycam-icon-paper.png")
berrycamicon_resized = berrycamicon.resize((qr_width,qr_height))

imageWithColorPalette = device_qr.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=2)
palettedata = [255, 255, 255, 0, 0, 0, 255, 0, 0]
imageWithColorPalette.putpalette(palettedata)
img.paste(berrycamicon.resize((qr_width,qr_height)), (padding_horiz, padding_vert))
img.paste(imageWithColorPalette, (padding_horiz, (padding_vert * 2) + qr_height))

img.save("output.png", "PNG")
