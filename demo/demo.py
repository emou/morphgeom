#!/usr/bin/env python2
import os
import sys
import ImageTk
import Tkinter
from tkFileDialog import askopenfilename

import PIL

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)))
from morphlib.image import GrayscaleImage
from morphlib.operator import Dilation, ReconstructionByDilation, StructuralElement

class Main(object):
    def initialize(self):
        self.images = {}
        self.root = Tkinter.Tk()

    def get_filename(self):
        return askopenfilename(filetypes=[
            ("allfiles", "*"),
            ("images", "*.jpg *.jpeg *.png"),
        ])

    def load_image(self):
        self.image_filename = self.get_filename()
        if not self.image_filename:
            raise SystemExit(1)
        self.root.title(self.image_filename)
        try:
            return GrayscaleImage.load(self.image_filename)
        except IOError:
            sys.stderr.write('Error reading image. Exiting.\n')
            raise SystemExit(2)

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

    def original(self):
        return self.image_to_tk(self.image)

    def dilated(self, i):
        dilate = Dilation(StructuralElement.predefined('rhombus'))
        return self.image_to_tk(dilate(self.image))

    def reconstruct_by_dilation(self, i):
        dilate = ReconstructionByDilation(StructuralElement.predefined('rhombus'),
                                          mask=None)
        return self.image_to_tk(dilate(self.image))

    def __call__(self, args):
        self.initialize()
        self.image = self.load_image()

        self.images = (
            ('Original Image', self.original()),
            ('Dilated Image', self.dilated(self.image)),
        )

        i = 0
        for txt, img in self.images:
            image_label = Tkinter.Label(self.root, image=img)
            image_label.grid(row=i, column=0)
            text_label = Tkinter.Label(self.root, text=txt)
            text_label.grid(row=i, column=1)
            i+=1

        self.root.mainloop()
        return 0

if __name__ == '__main__':
    sys.exit(Main()(sys.argv[1:]))
