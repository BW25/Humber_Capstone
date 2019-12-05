# Humber_Capstone
2019-2020 Computer Engineering Capstone Project at Humber College


## Introduction

This guide will help you build a time-of-flight sensor, interface board, and laser-cut case for a Raspberry Pi development platform. The TOF sensor used is the V53L0X sensor. This project was designed to serve as a piece of the hardware for a Resistor Value Recognizer device, but it can be used for other projects as well.

The Raspberry Pi development platform connects to the V53L0X through an I2C bus. To make the connecttion and mounting of the sensor easier and more streamlined, an interface PCB was designed in Fritzing. The Raspberry Pi, sensor, and PCB are then enclosed in a laser-cut case for protection.

![System Diagram 2](https://raw.githubusercontent.com/BW25/Resistor-value-recognizer/master/images/system%20diagram%202.PNG "System Diagram 2")
![System Diagram 1](https://raw.githubusercontent.com/BW25/Resistor-value-recognizer/master/images/system%20diagram%201.PNG "System Diagram 1")

## Budget
[Full budget file](https://github.com/BW25/Resistor-value-recognizer/blob/master/documentation/Hardware%20(Ceng%20317)/Ceng317%20Budget%20BWoo%202019.xlsx)

The expected budget for the project is $118.69. However, the primary cost is a Raspberry Pi kit. If you already have one, then the cost will be $33.32. 

TODO: Create detailed inventory of parts needed

As shown below, the other main costs are the V53L0X sensor and a sheet of 3mm cast acrylic for the enclosure. 

I have included resources to places where some of the resources can be purchased in the budget. Some components, such as the cast acrylic may have different availabilities depending on your location. Other components such as screws can be purchased at a local hardware store. 

I created my PCB in the Humber Prototype Lab, but you can order one from any PCB manufacturer, such as [Express PCB](https://www.expresspcb.com/how-to-order-pcbs/).


![Budget](https://raw.githubusercontent.com/BW25/Resistor-value-recognizer/master/images/budget.PNG "Budget")


## Time committment
As all design files are provided here, there is not a large expected time requirement for this project. As some components must be acquired from local retailers, additional time has been allotted to this part of the project. 
The total expected time is 3.5 hours. However, keep in mind it may take a few weeks for your parts and PCB to arrive after they have been ordered. 

| Task      | Time |
| ----------- | ----------- |
| Parts order      | 60 minutes       |
| Breadboarding   | 30 minutes        |
| Soldering   | 30 minutes        |
| Laser cutting   | 30 minutes        |
| Mechanical assembly   | 30 minutes        |
| Power up   | 15 minutes        |
| Additional testing   | 15 weeks        |

## Software setup and Unit testing 1: Breadboard
It is recommended to test your sensor once it arrives to ensure it is functional.
This step also involves setting up the software. 

If your Raspberry Pi has not yet been set up with Raspian, you can find a step-by-step guide here.
[Raspberry Pi Tutorial](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)

Once your Raspberry Pi has been set up, you will need to enable the I2C bus. From the terminal, use the command "sudo raspi-config" to open the configuration window. 
Select "Interfacing Options". 
Highlight the “I2C” option and select it by pressing Enter. 
Select "Yes"
Close the configuration window

Now download the Raspberry Pi Python API.
It can be downloaded as a zip from this repository [here](https://github.com/BW25/Resistor-value-recognizer/blob/master/software/VL53L0X_rasp_python-master.zip).
Alternatively, you can download it from the [original source](https://github.com/johnbryanmoore/VL53L0X_rasp_python).

Set up your breadboard according to the wiring diagram provided. Now run the python code you downloaded. 
![Wiring diagram](https://github.com/BW25/Resistor-value-recognizer/blob/master/electronics/TOFsensorDesignWPi_bb.jpg "Wiring diagram")

Navigate to the code you downloaded and open the "python" folder. Run the python script "VL53L0X_example.py" in the command line.
If you are successful, you should see the code giving output similar to the image below. The value displayed should display the distance from the sensor to an object above it. 
Test it by moving your hand above the sensor while the code is running.

![Sample output](https://raw.githubusercontent.com/BW25/Resistor-value-recognizer/master/images/breadboardDemoCode.PNG "Sample output")


## PCB / Soldering and Unit testing 2: PCB

Once your PCB has arrived, it must be soldered. 
If you are unfamiliar with soldering, you can find a beginning tutorial [here](https://www.youtube.com/watch?v=vIT4ra6Mo0s).

If you did not get a board with plated through holes, you will need to solder the center holes to ensure a connection between both sides of the boards. These holes are marked on the image below with black centers. Simply insert a short length of wire into the hole and solder on both ends.

![PCB](https://github.com/BW25/Resistor-value-recognizer/blob/master/electronics/TOFsensorDesign_pcb.jpg "PCB")

TODO:

To solder the header pins

![Soldered PCB](https://github.com/BW25/Resistor-value-recognizer/blob/master/images/pcb_soldered.jpg "Soldered PCB")


## Mechanical assembly



## Power up

![The final product](https://raw.githubusercontent.com/BW25/Resistor-value-recognizer/master/images/pcb_enclosure.jpg "The final product")

## Unit testing

## Production testing


