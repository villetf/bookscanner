# Book scanner

Vilhelm Fontell (vf222it)

## Introduction

This tutorial describes how to build a scanner for quickly adding information about books to a custom made book organization system. The goal is that you scan the barcode of a book, and data about the book is fetched from Google Books and Open Library based on the ISBN number. The data is then automatically inserterted into a Node-Red dashboard where the user can check the information and change or complete it if something is wrong or missing. The user then saves the book, and it is inserted into the book system via an API call.

Estimated time to complete this tutorial is 4-8 hours.

### About the book system

The book organisation system previously mentioned is called [Bokportalen](https://github.com/villetf/bokportalen/tree/dev) and is a web system that I am currently building in Node.js and Angular. The purpose of it is to create a complete database of all the books that you own and make it possible to view statistics and keep track of which books you own. Even though it is theoretically possible to set up yourself, it would require a lot of configuration, and would not be complete since the work is not done yet.

However, it would be possible to modify the API calls to suit any other book system, such as Goodreads or Hardcover. Since the final API calls to post the book are just a fraction of the project, it should not be too much work.

## Objective

I chose this project because manually adding books to the system is a lot of work, and I have been thinking that there should be a way to make it faster and easier. When using the scanner, the time to add books is significantly reduced, and the risk of errors decreases. If you use the scanner and add all the books you own, you will not only have an overview of the books you own, but you can also get an insight of how your collection is divided, for example by language, genre, nationality and gender of authors, and so on.

## Material

The following material is required to build the project:

| Component | Purpose | Cost | Alternative |
| --------- | ------- | ---- | ----------- |
| Raspberry Pi Pico WH | Main MCU | 99 SEK [Electrokit](https://www.electrokit.com/en/raspberry-pi-pico-wh) | Any other MCU that supports UART |
| UART Barcode reader | Scanning book barcodes | 359 SEK [Electrokit](https://www.electrokit.com/en/streckkods-qr-kodlasare-uart) | Any other barcode reader that can be connected to a MCU (make sure to check the specifications for what barcode types are supported) |
| Breadboard 400 tie-points | Connect everything | 49 sek [Electrokit](https://www.electrokit.com/en/kopplingsdack-400-anslutningar) | Any other breadboard, or a soldered solution for a more durable install |
| Passive piezo buzzer | Give the user audial feedback, for example when scanning a book | 29 SEK [Electrokit](https://www.electrokit.com/en/piezohogtalare-passiv) | Any other buzzer, for example the active equivalent |
| LED module Red/Green 5mm | Give the user visual feedback on the state of the scanner | 18 SEK [Electrokit](https://www.electrokit.com/en/led-modul-rod/gron-5mm) | Separate green and red lights |
| Hook-up wire AWG24 red, 1 metre | Connect everything nicely | 6 SEK [Electrokit](https://www.electrokit.com/en/kopplingstrad-awg24-flertradig-rod-/m) | Regular dupont wires |
| Hook-up wire AWG24 black, 1 metre | Connect everything nicely | 6 SEK [Electrokit](https://www.electrokit.com/en/kopplingstrad-awg24-flertradig-svart-/m) | Regular dupont wires |
| Resistor carbon film 0.25W 180ohm | Connect the red part of the LED module | 1 SEK [Electrokit](https://www.electrokit.com/en/motstand-kolfilm-0.25w-180ohm-180r) | A 330ohm resistor will also work, but with a less bright red
| Resistor carbon film 0.25W 100ohm | Connect the green part of the LED module | 1 SEK [Electrokit](https://www.electrokit.com/en/motstand-kolfilm-0.25w-180ohm-180r) | You can parallell connect three 330ohm resistors with about the same result |
| Battery holder 4x AA with on/off switch | Holding the batteries, turning the unit on and off | 30 SEK [Electrokit](https://www.electrokit.com/en/batterihallare-4xaa-box-brytare-sladd) | USB, or any other power source |
| 4x LADDA AA 1.2V 2450 mAh rechargeable batteries | Powering the unit | 99 SEK [IKEA](https://www.ikea.com/se/en/p/ladda-rechargeable-battery-hr06-aa-1-2v-50504692/) | Any other 1,2V AA rechargeable batteries, alternatively 3x 1,5V non-rechargeable batteries (requires the battery holder to be replaced with one for 3 batteries) |

Total cost: 726 SEK

## Computer setup

As my IDE, I am using Visual Studio Code (VSCode) together with the MicroPico plugin. Version control is done via Git with Github. To get your Pico and your IDE ready for development, use the following steps:

1. In Visual Studio Code, install the [MicroPico](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) plugin. Install the recommended additional plugins.
2. Clone this project (or download it as a zip) and open the folder in VSCode.
3. In the project folder, create a folder named "config", and inside it, create a file named keys.py. Fill it with the follwing content:

   ```python
   WIFI_SSID = 'Your_network_name'
   WIFI_PASS = 'Your_network_password'

   # MQTT server's configuration
   MQTT_SERVER = "ip_of_mosquitto_server"
   MQTT_PORT = 1883
   MQTT_CLIENT_ID = "id-1223"
   ```

4. Connect a micro-USB cable to your Pico.
5. While holding the BOOTSEL button on your Pico, insert the other end of the USB cable into your computer. Your Pico will connect as an external drive to your computer.
6. Download [this file](https://micropython.org/resources/firmware/RPI_PICO_W-20250415-v1.25.0.uf2) (for the RP2040) and place it on your Pico. The Pico will disappear as an external drive.
7. Unplug the Pico and plug it back in. It should connect automatically to MicroPico, and you should see a green line in the terminal with some info about your Pico.
8. Press Cmd/Ctrl+Shift+P and type "micropico". Select the option "MicroPico: Upload project to Pico". The project will be copied to the Pico.
9. Open the file main.py and click "Start" in the lower left bar of VSCode. The project will run and, if everything on the board is correctly connected, you will hear three beeps from the buzzer if the network connection was successful. The scanner is ready to scan.

## Putting everything together

This circuit diagram describes how to connect your components:

![Image with circuit diagram](./img/Ritning.png)

Note that:
- The barcode scanner comes with a connector that connect to six wires, but just four of them are used (3.3V, GND, RX, TX). Therefore, it might be useful to fasten the two unconnected wires with a ziptie, or just cut them.
- The four wires from the camera may vary in color, so always check the [documentation](https://www.waveshare.com/wiki/Barcode_Scanner_Module_(D)) for the camera to make sure that you connect the right wires.
- The ground for the scanner is connected directly to the Pico's ground. The reason for this is that I experienced some interference noise from the buzzer when having the scanner's ground connected to the horizontal ground row.

### Electrical calculations

The table describes the power consumption for the components:

| Component | Power consumption |
| --------- | ----------------- |
| Pico | ~50 mA |
| Barcode scanner | 120 mA |
| LED | 10 mA |
| Buzzer | Negligible consumption, since it only makes very short sounds |

This sums up to a total consumption of about 180 mA.

The four AA batteries have a capacity of 2450 mAh each, adding up to a total of 9800 mAh. But since the batteries are connected in series and not parallell, we only get 2450 mAh at 4.8V for all of the four batteries.

We divide the battery capacity with the power consumption:

2450 / 180 = 13.6

This means that with fully charged batteries, the appliance should be able to run for at least 13 hours.

## Platform

When the user have scanned a book, it is important that the fetched data can be shown, corrected, and manually confirmed before it is saved to the database. If the data would be saved immediately, you could end up with inaccurate or incomplete data in the database. This also makes it possible to fill in fields that cannot be fetched from the API. For example, original language is not somthing that the API:s return, so that always has to be filled in manually.

To accomplish this I used Node-red, which is a tool used for low-code visual programming. Together with the palette (module) node-red-dashboard, it has support for creating interactive dashboards. Node-red is a self-hosted solution, and I run it in a Docker environment. 

Node-red is very suitable for this kind of project
