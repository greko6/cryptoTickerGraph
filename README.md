# cryptoTickerGraph

## Installation

1. Turn on SPI via `sudo raspi-config`
    ```
    Interfacing Options -> SPI
   ```
2. Install dependencies
    ```
    sudo apt update
    sudo apt-get install python3-pip python3-pil python3-numpy git
    pip3 install RPi.GPIO spidev
    ```

3. Install drivers for your display
    1. Waveshare display
    ```
    git clone https://github.com/waveshare/e-Paper.git ~/e-Paper
    pip3 install ~/e-Paper/RaspberryPi_JetsonNano/python/
    ```
   for more information refer to: https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT
    2. Inky wHAT display
    ```
    pip3 install inky[rpi]
    ```

![Image Preview](https://github.com/Shaun-Harrison/cryptoTickerGraph/blob/main/eth_screenshot.jpg?raw=true)

Modified version of https://github.com/dr-mod/zero-btc-screen 

Follow all setup instructions in this repo before cloning this repo

Changes include
-   Use coingecko to get price information - This API has more options than the previous
-   Multiple Tokens - see main.py line 21 & 34 to modify token list
-   Daily percentage - Added in the coins daily percentage change
-   Change to looping logic - This was so that the screen would loop through the different tokens & for if the API returns non 200 it doesn't exit the script
-   Minor changes - such as font / removal of lines / font sizes all to suit my needs / wants
