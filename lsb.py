from PIL import Image
import sys
import qrcode
import random

class lsbQR:
    def __init__(self, r_txt, g_txt, b_txt, size):
        r_channel = qrcode.make(r_txt, border=0, box_size=5)
        g_channel = qrcode.make(g_txt, border=0, box_size=5)
        b_channel = qrcode.make(b_txt, border=0, box_size=5)
        if max(r_channel.size[0], g_channel.size[0], b_channel.size[0]) > size:
            raise IndexError
        self.r_pix = r_channel.load()
        self.g_pix = g_channel.load()
        self.b_pix = b_channel.load()

    def get_pixel(self, x, y):
        try:
            r = self.r_pix[(x, y)]
        except IndexError:
            r = 1
        try:
            g = self.g_pix[(x, y)]
        except IndexError:
            g = 1
        try:
            b = self.b_pix[(x, y)]
        except IndexError:
            b = 1
        try:
            alpha = 0
            for i in range(0, 8):
                alpha = alpha << 1
                alpha += (self.alpha[i][(x, y)] & 1)
        except (IndexError, AttributeError):
            alpha = 255
        return r, g, b, alpha

    def random_alpha(self):
        self.alpha = list()
        for i in range(0, 8):
            self.alpha.append(qrcode.make(random.randint(1, 1000), border=0, box_size=5).load())

def main():
    if len(sys.argv) < 2:
        exit()

    try:
        source = Image.open(sys.argv[1])
        if source.format != 'PNG':
            print("Source file is not a png file.")
            exit()
    except FileNotFoundError:
        print("Source file dose not exist.")
        exit()

    source_pix = source.load()
    source_width, source_height = source.size

    r_txt = input("R channel:")
    g_txt = input("G channel:")
    b_txt = input("B channel:")

    try:
        qr = lsbQR(r_txt, g_txt, b_txt, min(source_width, source_height))
        # qr.random_alpha()
    except IndexError:
        print("Overflow")
        exit()

    target = Image.new("RGBA", (source_width, source_height))

    for y in range(source_height):
        for x in range(source_width):
            r, g, b, alpha = qr.get_pixel(x, y)
            _r, _g, _b, _ = source_pix[(x, y)]
            _r = (_r & 0xFE) | (r & 1)
            _g = (_g & 0xFE) | (g & 1)
            _b = (_b & 0xFE) | (b & 1)
            target.putpixel((x, y) ,(_r, _g, _b, alpha))

    target.save("target.png")

if __name__ == "__main__":
    main()