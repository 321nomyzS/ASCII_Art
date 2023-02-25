from PIL import Image, ImageFont, ImageDraw
import cv2
import os
import json

with open("etc/settings.json", "r") as settings_file:
    settings = json.load(settings_file)
    ascii_signs = settings["ascii_signs"]
    background_color = tuple(settings["background_color"])
    font_color = tuple(settings["font_color"])


def image_to_ascii_png(im_name):
    im = cv2.imread(im_name)
    width, height, channel = im.shape
    im = Image.open(im_name)
    im = im.convert("RGB")
    image_matrix = []
    ascii_signs_limits = []

    # Loading image
    for j in range(width):
        line = []
        for i in range(height):
            coordinate = i, j
            pixel = list(im.getpixel(coordinate))
            grayscale = pixel[0]*0.3 + pixel[1]*0.59 + pixel[2]*0.11
            line.append(grayscale)
        image_matrix.append(line)

    # Setting limits for ascii characters
    for i in range(len(ascii_signs)):
        limits = [255*i/len(ascii_signs), 255*(i+1)/len(ascii_signs)]
        ascii_signs_limits.append(limits)

    # Create PixelArt
    image_pixelart = []
    for i in range(len(image_matrix)):
        line_matrix = image_matrix[i]
        line_pixelart = []
        for j in range(len(line_matrix)):
            pixel = line_matrix[j]
            for k in range(len(ascii_signs)):
                if ascii_signs_limits[k][0] <= pixel <= ascii_signs_limits[k][1]:
                    line_pixelart.append(ascii_signs[k])
                    break
        image_pixelart.append(line_pixelart)

    # Creating result file
    result = Image.new(mode="RGB", size=(height*15, width*15), color=background_color)

    fontC = ImageFont.truetype('cour.ttf', 15)
    result_edit = ImageDraw.Draw(result)
    temp_i = 0
    for i in range(0, height*15, 15):
        temp_j = 0
        for j in range(0, width*15, 15):
            text = image_pixelart[temp_j][temp_i]
            result_edit.text((i,j), text, font_color, font=fontC)
            temp_j += 1
        temp_i += 1
    return result


    return result


def scale_image(im_name, percent):
    image = Image.open(im_name)
    height_size = int((float(image.size[1]) * float(percent)))
    width_size = int((float(image.size[0]) * float(percent)))
    image = image.resize((width_size, height_size), Image.NEAREST)
    return image


def main(im_name, percent):
    im_result_name = f"{im_name[:-4]}-ASCII.png"

    if percent == 100:
        im = image_to_ascii_png(im_name)
    else:
        im = scale_image(im_name, percent / 100)
        im_tiny_name = f"tmp/{im_name[:-4]}-tiny.png"
        im.save(im_tiny_name)
        im = image_to_ascii_png(im_tiny_name)
        os.remove(im_tiny_name)
    im.save(im_result_name)

    print(im_result_name, "has been just generated")


if __name__ == "__main__":
    im_name = input("Image file name: ")
    percent = int(input("Percent of compression [%]: "))
    main(im_name, percent)
