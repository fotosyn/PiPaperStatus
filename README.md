# Pi Paper Status

### A guide to setting up an e-Ink Paper status display with a Raspberry Pi

This is a simple script which allows you to show some usefule device information for those Raspberry Pi's you have running behind the scenes to make things happen. It is inspired from setup of the [BerryCam for Raspberry Pi](https://berrycam.io) camera units that I regularly access on my own home network and most of the examples illustrated here cover this application. 

That said, its application could be used for just about any Raspberry Pi device doing any type of function. The code is fairly simple and easily customised to suit your needs. Out of the box (or should I say, repo) it will do the following:

![\[Pi Paper status view\]](https://github.com/fotosyn/PiPaperStatus/blob/main/pi-status-output.png)

1. Display network information including hostname and IP address / port
2. Present a linkable QR code to allow directory / resource browsing from another device (on the same network) using that device's camera
3. Display an app icon of your choosing
4. Easy to identify at-a-glance-label
5. Start time (which gives an indication of device uptime)

![\[Pi Paper status view\]](https://github.com/fotosyn/PiPaperStatus/blob/main/pi-status-output.png)

### Getting started:
[1. What you need](#items-you-will-need) / [2. Getting started](#useful-guides-to-get-started) 

### Using the script:
[3. Configuring the script](#configuring-the-script) / [4. Running the script](#running-the-script) / [5. Troubleshooting](#troubleshooting)

### Additional setup
[6. Autostart Pi Paper Status on boot](#other-things-to-try) 

[Back to top](#top)

---

# Items you will need

The mix of configuations is extensive, and can run on any type of Raspberry Pi that has 40-pin GPIO headers, including (Raspberry Pi 2,3,4 and Zero)

1. A Raspberry Pi computer (any model) with network connectivity.
2. An SD card. Most models now take the Micro SD type although some work with standard sized SD cards.
3. All the necessary leads (power supply, HDMI cable, mouse and keyboard, if working from Raspberry Pi OS desktop).
4. A working network connection.
5. An e-Ink Paper Display. 

While there are many available, installation can differ from model to model. For the purposes of this example I am using the [Pimoroni Inky pHAT EPD Display](https://shop.pimoroni.com/products/inky-phat)

 *I am in no way affiliated with Pimoroni*. Their stuff is pretty nice and these were the displays I had available at the time of authoring this script. And they are really easy to get set up and running. If you're using a different type of e-Ink display, you may need to consider additional steps.

The libraries above, and the example script in this repo also make extensive use of the [Pillow](https://pillow.readthedocs.io/en/stable/) imaging library. There are limitless possibilities and we only scratch the surface here.

QR codes are generated using [qrcode](https://pypi.org/project/qrcode/) which should be installed as part of the Pimoroni Inky pHAT installation.

---

# Useful guides to get started

> Here are some useful resources. It's worthwhile taking the time to explore these pages as they will help you get your Raspberry Pi up and running for the first time. If you're familiar with all of this you may wish to [skip this part](#configuring-the-script)

[Setting up your Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)
Here you’ll learn about your Raspberry Pi, what things you need to use it, and how to set it up.

[Using your Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-using)
Learn about Raspberry Pi OS, included software, and how to adjust some key settings to your needs.

 [Remote access using the Terminal/SSH](https://www.raspberrypi.org/documentation/remote-access/)
It's recommended you take a look at the resources here as you will need to use Terminal and some basic commands to install and run the Python script.

[Other Frequently Asked Questions](https://www.raspberrypi.org/documentation/faqs/)
A wide range of information related to the hardware and software to get up and running with the various models of Raspberry Pi. 

[Raspberry Pi OS](https://downloads.raspberrypi.org/raspios_full_armhf/release_notes.txt) is well maintained and receives regular updates. This may change the instructions here from time to time. If you notice any differences, please let me know by raising an issue and I'll update the documentation, with thanks in advance.

[Pimoroni Inky pHAT installation guide](https://github.com/pimoroni/inky)
The Inky pHAT resource has a straightforward installation process, plenty of supporting Python examples as well as useful support documentation. It should install dependencies that are used in this source code for QR code generation.

[Pillow Imaging Library](https://pillow.readthedocs.io/en/stable/)
The Python Imaging Library adds image processing capabilities to your Python interpreter.
This library provides extensive file format support, an efficient internal representation, and fairly powerful image processing capabilities.

[Back to top](#top)

---

# Configuring the script

> Setup involves editing the Python source code from this repo. If you're unfamiliar with this process, there are tools to help make this easy. [Thonny](https://thonny.org/) which is a popular Python IDE is bundled with the Rpasberry Pi OS Desktop, and is available for MacOS, Linux and Windows. You should also check out alternatives such as [Sublime Text](https://www.sublimetext.com/) and [PyCharm](https://www.jetbrains.com/pycharm/). Or indeed, if you prefer, simply edit in nano or pico in the shell itself.

The `pi-status.py` file has a number of config settings, primarily related to layout for different e-Ink display sizes. Play around with these to suit your own needs.

Most e-Ink displays have max. 3 colours (generally Black and white with either Red or Yellow). In cases where a yellow coloured display is used, red is automatically supplemented within the palette.

To ensure that any icon files are loaded in correctly, make sure the pathway is set correctly in:

```
device_path = "/home/<your_user_name>/path-to/pipaperstatus"
```

You can also change the device label for the device for quick and easy reference or when glancing at the device from further away.

```
device_label = "DEVICE LABEL"
```

Make sure the path reflects where you have installed this script, and that the username matches your own configuration. This will allow you to load in an icon file as part of the display.

### Making your own icon files

You can easily do this using any image editing tool that supports Indexed colour spaces. This means a defined number of colours in the palette, saved in the PNG file format. The icons attached in the repo give an example of how these are set up, with the colours set up as White (colour 0), Black (1) and Red / Yellow (2)

![\[Editing the icon file\]](https://github.com/fotosyn/PiPaperStatus/blob/main/pi-status-iconedit.png)

I use [Aseprite](https://www.aseprite.org/) which is a popular tool with pixel artists, although other tools are available including [GIMP](https://www.gimp.org/) and [Adobe Photoshop](https://adobe.com/photoshop). If you have any other suggestions, please let me know and I'll add them to the list for reference.


[Back to top](#top)

---

# Running the script

Pi Paper Status needs to run as a Python process to capture the detail from your Raspberry Pi device, render and display on the e-Ink paper display. In the simplest case, you can do this using:

```
python3 pi-status.py
```

After a brief pause, the display will flicker and show your information. It's also really useful to bundle this as part of any device startup, which means it will automatically update when you start or reset the Raspberry Pi itself.


[Back to top](#top)

---

# Troubleshooting

If you are running an earlier version of Python, pre version 3 then it is necessary to update or install the [latest version](https://www.python.org/downloads/)

### Check your version of Python3

To check the version supply the command

```
python3 --version
```

#### Things you can do:

**1. Upgrade your Raspberry Pi OS**

You could install a newer version of Raspberry Pi OS which has newer versions of Python. This is definitely the most direct route to consider if you're blowing the dust off a trusty Pi that's been sitting in the cupboard. 

See [Setting up your Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up) to get the latest version of Raspberry Pi OS and flash to your SD card.

**2. Update Python3 to version 3.7.0**

Alternatively, you can update your version of Python3. Be aware that this will a fair amount of time and involves a number of steps that need to be followed in this specific order. To update to the newest version with the following commands:

**Download and extract the latest version of Python3 logged in as root**

```
sudo su
```
```
cd /usr/src
```
```
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
```
```
tar -xf Python-3.7.0.tgz
```

**Install dependencies**

```
apt-get update
```
```
apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
```

**Configure and install Python 3 (this part may take some time)**

```
cd Python-3.7.0
```
```
./configure --enable-optimizations
```
```
make altinstall
```

**Update the link to the newly installed version of Python**

```
ln -s /usr/local/bin/python3.7 /usr/local/bin/python3
```

**Check the version of Python (should return 3.7.0)**

```
python3 --version
```

Thanks to [Samx18](https://samx18.io/blog/2018/09/05/python3_raspberrypi.html) for the original guide to this detail. **Perform a reboot of the Pi to be doubly sure that this has been applied.** 

---

# Other things to try

### Autostart Pi Paper Status on boot

If you regularly use your Raspberry Pi, set this script to launch automatically when the Pi is booted. This is quite an easy process and is particularly useful if you want to be able to plug your Pi in to power headless, and have it run each time without configuration or a manual start.

For more information on editing the `rc.local` file please refer to the [Raspberry Pi documentation](https://www.raspberrypi.org/documentation/linux/usage/rc-local.md)

On your Pi, edit the file /etc/rc.local using the editor of your choice. You must edit with root, for example:

```
sudo nano /etc/rc.local
```

In the line **before** `exit 0` add the following lines. Be sure to reference absolute filenames rather than relative to your `/home` folder replacing `<your_user_name>` with your own user name (in many cases this is `pi`):

```
cd /home/<your_user_name>/path-to/pi-paper-status
nohup python3 pi-status.py > pi-status.log
wait
```

Save this file `CTRL x` confirming with `Y` and `Enter` then restart your Raspberry Pi. If this has been set up correctly and your e-Ink display should refresh and update once reboot has completed.

[Back to top](#top)