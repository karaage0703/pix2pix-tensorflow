from PIL import Image
import numpy as np
import sys
import os
import glob
import shutil

def make_pixelart(src, dot_size):
    width, height = src.size
    dot_img = Image.new('RGB', (width, height))
    dst_img = Image.new('RGB', (width*2, height))

    img_pixels = np.array([[src.getpixel((x,y)) for y in range(height)] for x in range(width)])
    dot_pixels = np.zeros((dot_size, dot_size,3))

    div_x = int (width / dot_size)
    div_y = int (height / dot_size)

    # make dot pixel
    for x in range(0, dot_size):
        for y in range(0, dot_size):
            tmp_color = np.zeros(3)
            for i in range(0, div_x):
                for j in range(0, div_y):
                    tmp_color += img_pixels[x*div_x+i][y*div_y+j]

            dot_pixels[x][y] = list(map(int, tmp_color / (div_x*div_y)))

    # make dot picture
    for x in range(0, width):
        for y in range(0, height):
            dot_x = int(x / div_x)
            dot_y = int(y / div_y)
            if dot_x >= dot_size:
                dot_x = dot_size - 1
            if dot_y >= dot_size:
                dot_y = dot_size - 1
            dot_img.putpixel((x,y), (int(dot_pixels[dot_x][dot_y][0]), int(dot_pixels[dot_x][dot_y][1]), int(dot_pixels[dot_x][dot_y][2])))

    # reduce color
    dot_img = dot_img.quantize(16, kmeans=True).convert("RGB")

    # combine image for pix2pix format
    dst_img.paste(src, (0, 0))
    dst_img.paste(dot_img, (width, 0))

    return dst_img

if __name__ == '__main__':
    param = sys.argv
    if (len(param) != 2):
        print ("Usage: $ python " + param[0] + " /photo_directory")
        quit()

    # pwd = cmd('pwd')
    img_dir = os.path.dirname(os.path.abspath(__file__)) + "/pixelart"

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

        output_img = make_pixelart(input_img, 32)
        output_img.save(imagepath)
        cnt += 1
