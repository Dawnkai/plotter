# 2D Plotter
![example workflow](https://github.com/Dawnkai/plotter/actions/workflows/lint.yml/badge.svg) [![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs) [![PyPi Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/) [![GitHub last commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat)]()

Project used for Embedded Systems project in Poznań University of Technology.
The goals of this project are:
* Extracting contours from images
* Drawing them on A5 paper
* Saving them in a database for later reusage

The project currently supports uploading images from computer or taking pictures with PiCamera.

## Hardware
* Raspberry Pi 2 Model B V1.1
* Raspbery Pi Camera Rev 1.3

## Repository structure
This repository contains the following files:
1. `static/css/styles.css` - global stylesheet with styles used in the whole webapp
2. `static/images` - this is where the app stores temporary images, **do not remove it**
3. `static/scripts/utls.js` - AJAX and vanilla JS functions used by the webapp
4. `static/scripts/camera.js` - script for interacting with camera API
5. `static/scripts/images.js` - script for fetching images from the database
6. `static/scripts/navigation.js` - script for navigating between pages
7. `static/scripts/plot.js` - script for interacting with the plotter
8. `static/scripts/stats.js` - script for fetching stats (plotter state, logs)
9. `static/scripts/upload.js` - script for uploading images to server
10. `templates/*.html` - pages of the webapp
11. `camera.py` - script controlling the camera
12. `database.py` - script for operating on the database
13. `entrypoint.sh` - bash script used to start the app
14. `extractor.py` - script for extracting contours from images using OpenCV library
15. `logger.py` - setup for logging:
* Logs of level `DEBUG` will be saved to a file named `plotter.log`
* Logs of level `INFO` will be printed to the console
16. `main.py` - main server with all the endpoints, merging all parts together
17. `plot.py` - script for working with the plotter
18. `requirements.pip` - list of libraries required in the project

## Installation
1. Install python on your Raspberry Pi (Python 3+):
```bash
wget https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tar.xz
tar xf Python-3.6.0.tar.xz
cd Python-3.6.0
./configure --enable-optimizations --prefix=/usr
make
```
2. Install pip:
```
sudo apt-get install python3-pip
```
3. Install requirements:
```
pip3 install -r requirements.pip
```
4. Ensure that the plotter is in starting position (0 on X and 0 on Y axis, plotter will move from and return there)!
5. Start the server:
```
sudo chmod 777 entrypoint.sh
./entrypoint.sh
```
6. Navigate to `http://127.0.0.1:5000/` or `http://0.0.0.0:5000/` in your browser and you are good to go!

## Contributing
Before submitting your pull request please check your code with pylint - settings for pylint are available in `.pylintrc` file. Github Actions will automatically run it on your code on every pull request. Please also remember this is a school project therefore the repository may become inactive after a while when its authors will graduate.

## Copyrights
This project is licensed under **MIT** license, which means that you have the right to distribute, modify and use this project in your own projects (even under more strict license) so long as you provide the original authors whose work you are using in your project and do not hold them liable.

## TODO
List of known bugs / possible improvements:
1. When removing (5\*n+1)-th image the JS will not reset the pagination

### Authors
1. Maciej Kleban ([DawnKai](https://github.com/Dawnkai))
2. Jakub Dunajko ([Cubaster](https://github.com/Cubaster))
3. Ariel Antonowicz as [teacher](http://www.cs.put.poznan.pl/aantonowicz/)
