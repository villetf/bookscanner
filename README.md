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
| LED module Red/Green 3mm | Give the user visual feedback on the state of the scanner | 15 SEK [Electrokit](https://www.electrokit.com/en/led-modul-rod/gron-3mm) | Separate green and red lights |
| Hook-up wire AWG24 red, 1 metre | Connect everything nicely | 6 SEK [Electrokit](https://www.electrokit.com/en/kopplingstrad-awg24-flertradig-rod-/m) | Regular dupont wires |
| Hook-up wire AWG24 black, 1 metre | Connect everything nicely | 6 SEK [Electrokit](https://www.electrokit.com/en/kopplingstrad-awg24-flertradig-svart-/m) | Regular dupont wires |
| Resistor carbon film 0.25W 180ohm | Connect the red part of the LED module | 1 SEK [Electrokit](https://www.electrokit.com/en/motstand-kolfilm-0.25w-180ohm-180r) | A 330ohm resistor will also work, but with a less bright red
| Resistor carbon film 0.25W 100ohm | Connect the green part of the LED module | 1 SEK [Electrokit](https://www.electrokit.com/en/motstand-kolfilm-0.25w-180ohm-180r) | You can parallell connect three 330ohm resistors with about the same result |
| Battery holder 4x AA with on/off switch | Holding the batteries, turning the unit on and off | 30 SEK [Electrokit](https://www.electrokit.com/en/batterihallare-4xaa-box-brytare-sladd) | USB, or any other power source |
| 4x LADDA AA 1.2V 2450 mAh rechargeable batteries | Powering the unit | 99 SEK [IKEA](https://www.ikea.com/se/en/p/ladda-rechargeable-battery-hr06-aa-1-2v-50504692/) | Any other 1,2V AA rechargeable batteries, alternatively 3x 1,5V non-rechargeable batteries (requires the battery holder to be replaced with one for 3 batteries) |

Total cost: 723 SEK

## Computer setup

A s my IDE, I am using Visual Studio Code together with the MicroPico plugin. 