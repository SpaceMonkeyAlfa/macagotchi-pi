# Macagotchi (For Pi)

## Overview



<img src="https://github.com/SpaceMonkeyAlfa/macagotchi-pi/assets/138901665/390c440f-8e48-4cad-9735-f42e349a2169" width="500">

Macagotchi for the Raspberry Pi is a tamagotchi-like pet ([macOS](https://github.com/SpaceMonkeyAlfa/macagotchi-macos) / [Windows](https://github.com/SpaceMonkeyAlfa/macagotchi-windows) codebases are also available). It interacts with the user by displaying a virtual pet on the screen while it scans for nearby Wi-Fi networks, and it will become happy when it’s found new SSIDs. Your Macagotchi will also track how many days in a row you’ve been able to keep it happy. While the code is very different, the idea is based on the excellent [pwnagotchi](https://github.com/evilsocket/pwnagotchi) project. The difference here is that Macagotchi doesn’t do anything sinister which might get you arrested or annoy people sitting around you. But seriously, check it out.

As [pwnagotchi](https://github.com/evilsocket/pwnagotchi)'s less sinister cousin it only collects SSIDs to keep score, which it keeps locally in a log. It doesn’t export data, and doesn’t contain any marketing or tracking code. By design, if you want to share how many SSIDs you’ve collected and/or how happy your Macagotchi is, take a photo.



## Prerequisites

- Python 3.x

- A Waveshare 2in13 **touch** e-paper HAT
  
- Raspbian

- Pi Zero 2 W

## Program Components





1. **Wi-Fi Network Scanning**
   - Scan for nearby Wi-Fi networks using the 'iwlist' command.
   - Parse the scan results and extract network information.

2. **Wi-Fi Network Tracking**
   - Store scanned network SSIDs and dates in a log file.
   - Calculate the number of unique networks found today.
   - Make your macagotchi happy or sad depending on how many unique ssids it has found today. 

3. **Display Update**
   - Create an image for the E-Paper display.
   - Draw user information,  streak, network data, and your macagotchi's face on the screen.
   - Update the E-Paper display with the image.


4. **Shutdown Functionality**
   - Press and hold the off icon in the bottem left hand corner for 2 seconds and let go to power off. **Only unplug from power once the green light on the pi has switched off**
   - To power on again, unplug and plugin the pi.




## Program Outputs

- The program displays a tamagotchi-like pet face, which changes based on user interaction and network scanning results.
- User data, such as the username and network count, is displayed on the E-Paper screen.
- Loyalty streak information is tracked and displayed.
- Network scanning results, including the number of unique networks found today, are displayed.


## Dependencies

- External libraries for the E-Paper display and touch functionality.
- Touch-enabled E-Paper display hardware.
- Python 3.x


## Additional Notes

- This program is designed for a Raspberry Pi Zero 2 W using that includes a Waveshare 2in13 **touch** E-Paper HAT. [macOS](https://github.com/SpaceMonkeyAlfa/macagotchi-macos) and [Windows](https://github.com/SpaceMonkeyAlfa/macagotchi-windows) codebases are also available.
- Unlike the macOS and Windows versions, macagotchi for pi **does not*** support wardriving mode. Instead, Macagotchi scans every 30 seconds, and then after 6 scans (3 minutes) the screen updates. This is because of the limitations of e-paper screens.
- Unlike macOS and Windows versions, your Macagotchi's expressions and commentary are based on data from that day, not from sessions, as, as you'll probably discover, you can leave your macagotchi on for a long time on a power bank before it runs out of power.

## Install Proccess

*Note that you will need adminstrator priveleges on the raspberry pi that you are using.*
1. Install the 2 in 13 *touch* E-paper HAT.
2. Follow [this tutorial](https://www.waveshare.com/wiki/2.13inch_Touch_e-Paper_HAT_Manual#Raspberry_Pi) until it the "Download the Demo" stage begins. Since macagotchi comes pre-installed with the waveshare drivers, you will not need to complete this step.
3. Run `git clone https://github.com/SpaceMonkeyAlfa/macagotchi-pi` in your home/[your username here] directory.
4. Run `sudo crontab -e` and select the nano text editor
5. At the end of the document, type `@reboot sudo python3 /home/[your username here]/macagotchi/scripts/macagotchi.py` with [your username here] replaced with, you guessed it, your username.
6. Press ^S and ^X to save and exit crontab.
7. Run `sudo reboot`
Once the pi reboots, the screen should update to show your macagotchi's face after about 20 seconds. Congratulations! You are now the proud owner of a macagotchi.

## Changing the name of your macagotchi 

By default, your macagotchi's name is set to the current username. To change the name, simply:
1. Run `cd macagotchi/scripts` to enter the scripts and save files directory
2. Run `nano name.txt`
3. Type in the new name for your macagotchi.
4. Press ^S ^X to save and exit.
5. The next time the screen refreshes, you should see the new name. If not, you may need to reboot your pi.  You can do that by pressing and holding on the power button for 2 seconds, then releasing, then waiting for the green light from your pi to go off, unplugging it and plugging it in again.

## License:
[Mozzila 2.0](https://github.com/SpaceMonkeyAlfa/macagotchi-macos/blob/main/LICENSE)

## (◕ ‿ ◕) Bye!

