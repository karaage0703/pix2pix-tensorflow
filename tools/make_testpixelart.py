from PIL import Image
import numpy as np
import sys
import os
import glob
import shutil

def make_testdata(src):
    width, height = src.size
    dst_img = Image.new('RGB', (width*2, height))

    # combine image for pix2pix format
    dst_img.paste(src, (0, 0))
    dst_img.paste(src, (width, 0))

    return dst_img

if __name__ == '__main__':
    param = sys.argv
    if (len(param) != 2):
        print ("Usage: $ python " + param[0] + " /photo_directory")
        quit()

    # pwd = cmd('pwd')
    img_dir = os.path.dirname(os.path.abspath(__file__)) + "/test_pixelart"

    # delete directory
    if os.path.exists(img_dir):
        shutil.rmtree(img_dir)

    # make directories
    os.makedirs(img_dir)

    workdir = os.getcwd()+"/"+sys.argv[1]
    images = glob.glob(workdir+'/*.jpg')
    images += glob.glob(workdir+'/*.png')
    images += glob.glob(workdir+'/*.bmp')

    cnt = 0

    for image in images:
        imagepath = img_dir+"/image%07d" %cnt +".png"
        print(imagepath)

        # input image
        input_img = Image.open(image)
        # resize for pix2pix format
        input_img = input_img.resize((256, 256))

        output_img = make_testdata(input_img)
        output_img.save(imagepath)
        cnt += 1
