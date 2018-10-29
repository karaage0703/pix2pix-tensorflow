from PIL import Image
import sys

def make_pix2pix(src_a, src_b):
    width, height = src_a.size
    dst_img = Image.new('RGB', (width*2, height))

    # combine image for pix2pix format
    dst_img.paste(src_a, (0, 0))
    dst_img.paste(src_b, (width, 0))

    return dst_img

if __name__ == '__main__':
    param = sys.argv
    if (len(param) != 3):
        print('Usage: $ python ' + param[0] + ' src_a.jpg src_b.jpg')
        quit()

    # input image
    src_a = Image.open(param[1])
    src_b = Image.open(param[2])
    # resize for pix2pix format
    src_a = src_a.resize((256, 256))
    src_b = src_b.resize((256, 256))

    output_img = make_pix2pix(src_a, src_b)
    output_img.save('pix2pix.png')