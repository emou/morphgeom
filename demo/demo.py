#!/usr/bin/env python2
import os
import sys
import ImageTk
import Tkinter
import tkMessageBox
from tkFileDialog import askopenfilename

import PIL

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)))
from morphlib.image import GrayscaleImage
from morphlib.operator import Dilation, ReconstructionByDilation, CloseHoles, StructuralElement

class Main(object):
    def initialize(self):
        self.mask_image = self.image = None
        self.images = []
        self.root = Tkinter.Tk()
        self.menu = Tkinter.Menu(self.root)
        self.menu.add_command(label="Load Image...",
                              command=self.menu_load_image)
        self.menu.add_command(label="Load Mask Image...",
                              command=self.menu_load_mask)
        self.root.config(menu=self.menu)

    def get_filename(self):
        return askopenfilename(filetypes=[
            ("allfiles", "*"),
            ("images", "*.jpg *.jpeg *.png"),
        ])

    def menu_load_image(self):
        self.image_filename, self.image = self.load_image()
        self.refresh_images()

    def menu_load_mask(self):
        self.mask_name, self.mask_image = self.load_image()
        self.refresh_images()

    def load_image(self):
        image_filename = self.get_filename()
        if not image_filename:
            raise SystemExit(1)
        self.root.title(image_filename)
        try:
            return image_filename, GrayscaleImage.load(image_filename)
        except IOError:
            tkMessageBox.showerror(
                "Error while opening image",
                "Cannot open %s. Looks like it's not a valid image." % image_filename,
            )
            return None, None

    def image_to_pil_image(self, i):
        """
        Convert morphlib.image.GrayscaleImage to a PIL.Image.
        """
        pil_image = PIL.Image.new(mode="L", size=i.size)
        pil_image.putdata(i.getdata())
        return pil_image

    def image_to_tk(self, i):
        """
        Convert morphlib.image.GrayscaleImage to ImageTk.PhotoImage.
        Goes through converting it to PIL.Image first.
        """
        return ImageTk.PhotoImage(self.image_to_pil_image(i))

    def original(self, i):
        return self.image_to_tk(i)

    def mask(self, i):
        return self.image_to_tk(i)

    def dilated(self, i):
        dilate = Dilation(StructuralElement.predefined('rhombus'))
        return self.image_to_tk(dilate(i))

    def reconstruct_by_dilation(self, i, mask):
        dilate = ReconstructionByDilation(StructuralElement.predefined('rhombus'),
                                          mask=mask)
        return self.image_to_tk(dilate(i))

    def close_holes(self, i):
        close_holes = CloseHoles()
        return self.image_to_tk(close_holes(i))

    def refresh_images(self):
        self.images = []
        if self.image:
            self.images.append(('Original Image', self.original(self.image)))
            self.images.append(('Dilated Image', self.dilated(self.image)))
            self.images.append(('Close holes', self.close_holes(self.image)))
            #self.images.append(('Inverted Image', self.image_to_tk(self.image.invert())))
            #self.images.append(('Border of Image', self.image_to_tk(self.image.border(pixels=10))))
        if self.mask_image:
            self.images.append(('Mask', self.mask(self.mask_image)))
        if self.image and self.mask_image:
            self.images.append(
                ('Reconstruction by dilation',
                 self.reconstruct_by_dilation(self.image, self.mask_image)))
        i = 0
        for txt, img in self.images:
            image_label = Tkinter.Label(self.root, image=img)
            image_label.grid(row=i, column=0)
            text_label = Tkinter.Label(self.root, text=txt)
            text_label.grid(row=i, column=1)
            i+=1

    def __call__(self, args):
        self.initialize()
        self.root.mainloop()
        return 0

if __name__ == '__main__':
    sys.exit(Main()(sys.argv[1:]))
