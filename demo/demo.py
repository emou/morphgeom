#!/usr/bin/env python2
import os
import sys
import Tkinter
from tkFileDialog import askopenfilename

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)))
from morphlib.image import GrayscaleImage

def main(args):
    root = Tkinter.Tk()
    image_filename = askopenfilename(filetypes=[
        ("allfiles", "*"),
        ("images", "*.jpg *.jpeg *.png"),
    ])
    if not image_filename:
        return 1
    i=GrayscaleImage.load(image_filename)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
