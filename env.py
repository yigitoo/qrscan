#!/usr/bin/env python
# This script create an environment variable for
# accesing all that images from everywhere

import os
os.system(f"setx QRSCANNER_FOLDER {os.getcwd()}\\images")
