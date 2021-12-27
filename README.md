# 2D Plotter
Project used for Embedded Systems project in Poznań University of Technology.
The goals of this project are:
* Taking pictures with PI camera
* Extracting their contours
* Drawing them on A5 paper
* Saving them in a database for later reusage

## Hardware
* Raspberry Pi 2 Model B V1.1
* Raspbery Pi Camera Rev 1.3

## Repository structure
This repository contains the following files:
1. `camera.py` - script controlling the camera (taking and saving pictures **locally**)
2. `logging.py` - setup for logging:
* Logs of level `DEBUG` will be saved to a file named `plotter.log`
* Logs of level `INFO` will be printed to the console
3. `database.pt` - script storing images and retrieving them from the database

## Contributing
Before submitting your pull request please check your code with pylint - settings for pylint are available in `.pylintrc` file. Github Actions will automatically run it on your code on every pull request. Please also remember this is a school project therefore the repository may become inactive after a while when its authors will graduate.

## Copyrights
This project is licensed under **MIT** license, which means that you have the right to distribute, modify and use this project in your own projects (even under more strict license) so long as you provide the original authors whose work you are using in your project and do not hold them liable.

### Authors
1. Maciej Kleban ([DawnKai](https://github.com/Dawnkai))
2. Ariel Antonowicz as [teacher](http://www.cs.put.poznan.pl/aantonowicz/)
