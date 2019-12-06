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

Here is a breakdown of all parts needed:
| Component      | Number |
| ----------- | ----------- |
| 23x11 sheet of 3mm cast acrylic      | 1       |
| m2.5 screws   | 4        |
| m2.5 nuts   | 4        |
| m2 screws   | 2        |
| m2 nuts   | 2        |
| 6 pin header   | 1        |
| 4 pin header   | 1        |
| VL53L0X sensor   | 1        |
| 4 F-F wire connectors| 1        |

These components comme with a Raspberry Pi Kit
| Component      | Number |
| Raspberry Pi   | 1        |
| MicroSD card with Raspian   | 1        |
| Raspberry Pi power supply   | 1        |
| HDMI cable   | 1        |

These components are expected to have no cost, as they are common enough that they are likely already possessed. The electronics are necessary to interface to the Raspberry Pi.
| Glue   | 1        |
| Monitor with HDMI port   | 1        |
| USB mouse   | 1        |
| USB keyboard   | 1        |

As shown below, the other main costs are the V53L0X sensor and a sheet of 3mm cast acrylic for the enclosure. 

I have included resources to places where some of the resources can be purchased in the budget. Some components, such as the cast acrylic may have different availabilities depending on your location. Other components such as screws can be purchased at a local hardware store. 

I created my PCB in the Humber Prototype Lab, but you can order one from any PCB manufacturer, such as [Express PCB](https://www.expresspcb.com/how-to-order-pcbs/).
The PCB design can be edited in Fritzing, and can be found [here](https://github.com/BW25/Resistor-value-recognizer/blob/master/electronics/TOFsensorDesign.fzz).


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


## PCB / Soldering

Once your PCB has arrived, it must be soldered. 
If you are unfamiliar with soldering, you can find a beginning tutorial [here](https://www.youtube.com/watch?v=vIT4ra6Mo0s).

If you did not get a board with plated through holes, you will need to solder the center holes to ensure a connection between both sides of the boards. These holes are marked on the image below with black centers. Simply insert a short length of wire into the hole and solder on both ends.

![PCB](https://github.com/BW25/Resistor-value-recognizer/blob/master/electronics/TOFsensorDesign_pcb.jpg "PCB")

The top side of the board is the side with the text. Do not solder the sensor directly onto the board. Instead, use a 6-pin header so the sensor can be inserted and removed without permanently attaching it to the board. Solder the 6-pin header to the bottom side of the board, and the 4 pin header to the top. The 4 pin header is where you will attach the wires between the board and the Raspberry Pi.

![Soldered PCB](https://github.com/BW25/Resistor-value-recognizer/blob/master/images/pcb_soldered.jpg "Soldered PCB")

## Unit testing 2: PCB
One your PCB is soldered, use a multimeter to ensure all of the pins are connected correctly. Refer to the labelling on the PCB itself and the schematic to ensure all pins are appropriately connected with no shorts. 
Then connect the PCB to the Raspberry Pi. You may use the same wiring on the Pi as in Unit testing 1, and the pins on the PCB are labelled, so this should be simple. Then run the code from Unit testing 1 to ensure the sensor and board are connected correctly. 
If it does not work, then recheck you interface board with a multimeter as above. If you cannot find a problem with the PCB, it may be necessary to recheck your sensor or Pi setup by repeating unit testing 1.

## Mechanical assembly

If you are unfamiliar with laser cutting, you can find a guide here. [Introduction to laser cutting](https://makerdesignlab.com/tutorials-tips/laser-cutting-beginners-guide/)
Laser cutting can be done in your local makerspace. A quick Internet search should let you find the one closest to you.

This project is designed for 3mm cast acrylic; colour is irrelevant, although I used transparent acrylic. You can cut other materials, but keep in mind the slots on the design are designed for a 3mm thick material. You may need to alter the design if you want to use something else. 
The AutoCAD files can be found at this link. I recommend altering it to change the text at minimum; you want it to say your name, not mine! [Hardware enclosure](https://github.com/BW25/Resistor-value-recognizer/blob/master/mechanical/hardwareEnclosure.dwg)

After editing the AutoCAD files, go to the "Output" tab and select "Plot". Change the plot scale to 1:1 in mm. Use the Preview button and the Plot offset to ensure your design is centered on the paper. Then select "Ok" to output your design to a PDF. 

If you do not wish to alter the enclosure, you may use this PDF output instead. [Hardware PDF](https://github.com/BW25/Resistor-value-recognizer/blob/master/mechanical/hardwareEnclosure-Model.pdf)

Bring your output PDF and and AutoCad files to the makerspace where you will laser cut your case. As the makerspace where you cut the acrylic could have a different model of laser cutter, please speak to the staff there for instructions on its use.

![Laser cut pieces](https://raw.githubusercontent.com/BW25/Resistor-value-recognizer/master/images/laser_cut_parts.jpg "Laser cut pieces")

The design is assembled shown in the image. Be sure that the side pieces with the holes are lined up with the ports on you Raspberry Pi. The small donut shaped pieces are standoffs for mounting your Raspberry Pi and PCB. Use the four larger standoffs and 4 m2.5 screws and nuts for the Raspberry Pi. The 2 smaller standoffs and 2 m2 screws and nuts are for your PCB. You may use acrylic glue to hold your case together. However, be sure not to glue the tops onto the case; friction will hold it in place, and gluing it shut means you can't remove your Raspberry Pi and PCB!

![The final product](https://raw.githubusercontent.com/BW25/Resistor-value-recognizer/master/images/pcb_enclosure.jpg "The final product")

## Power up: and Unit testing 3: Final testing (Production testing)

The final test is to interface our sensor to the Raspberry Pi in the case. Once the case is assembled, you will notice a small hole in the lid of the case. You can run the wires through here to connect the sensor and Raspberry Pi. Then run the code as explained in Unit testing 1.

If you are assembling this project in larger numbers or are pressed for time, the multiple stages of unit testing may be undesirable or redundant. Therefore, this final check can be used for production testing.

If any clarification or assistance is required, please post in the Issues section.

