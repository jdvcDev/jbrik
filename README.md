# JBRIK 
My adaptaion of a Rubiks Cube solving robot. 

# Background/Components
Rubiks cube solving robot built from Legos, Raspberry Pi 3, Dexter BrickPi3, solved and controlled using libraries written in Python 2.7

The project is closely based on the original [BricKuber](https://www.dexterindustries.com/projects/brickuber-project-raspberry-pi-rubiks-cube-solving-robot-project/) project from Dexter Industries and has the following components:

- [Raspberry Pi](https://shop.dexterindustries.com/raspberry-pi-3/) - Will take pictures of the unsolved cube, process the solution and command the BrickPi.
- [BrickPi3](https://shop.dexterindustries.com/shop/robots/brickpi/brickpi-advanced-for-raspberry-pi) - Will controll the Lego motors.
- [Raspberr Pi Camera](https://shop.dexterindustries.com/raspberry-pi-camera/) - Will take pictures of the unsolved cube.
- [Raspbian for Robots](https://www.dexterindustries.com/howto/install-raspbian-for-robots-image-on-an-sd-card/) - Loaded onto an SD card, is the operating system for the Raspberry Pi.
- [LEGO Mindstorm](https://www.amazon.com/LEGO-6029291-Mindstorms-EV3-31313/dp/B00CWER3XY/ref=as_li_ss_tl?s=toys-and-games&ie=UTF8&qid=1477461771&sr=1-1&keywords=lego+mindstorms+ev3+31313&linkCode=sl1&tag=dexteindus-20&linkId=548432ea1fb981e344e36e80fb09b3fa) - Will be used to built the actual robot the solves the cube.
- [rubiks-color-tracker](https://github.com/dwalton76/rubiks-cube-tracker) - Python library used to convert an image of a cube into RGB values for each square.
- [rubiks-color-resolver](https://github.com/dwalton76/rubiks-color-resolver) - Python library to convert RGB values to 6 cube colors.
- [BrickPi3](https://github.com/DexterInd/BrickPi3/tree/master/Projects/BricKuber) - BrickPi3 drivers (https://github.com/DexterInd/BrickPi3/blob/master/Software/Python/brickpi3.py)
- JBRIK - Source code from this project used written to solve the cube.

Alogorithm being used to solve cube: https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/
