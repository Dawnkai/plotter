# 2D Plotter
![example workflow](https://github.com/Dawnkai/plotter/actions/workflows/lint.yml/badge.svg) [![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs) [![PyPi Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/) [![GitHub last commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat)]()

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
3. `database.py` - script storing images and retrieving them from the database
4. `app/server.py` - web server hosting the frontend app
5. `app/static/*` - static files (stylesheets, script files) used in webpages
6. `app/templates/*` - webpages used in the project

## Contributing
Before submitting your pull request please check your code with pylint - settings for pylint are available in `.pylintrc` file. Github Actions will automatically run it on your code on every pull request. Please also remember this is a school project therefore the repository may become inactive after a while when its authors will graduate.

## Copyrights
This project is licensed under **MIT** license, which means that you have the right to distribute, modify and use this project in your own projects (even under more strict license) so long as you provide the original authors whose work you are using in your project and do not hold them liable.

### Authors
1. Maciej Kleban ([DawnKai](https://github.com/Dawnkai))
2. Ariel Antonowicz as [teacher](http://www.cs.put.poznan.pl/aantonowicz/)
