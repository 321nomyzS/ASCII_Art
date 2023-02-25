from PIL import Image, ImageFont, ImageDraw
import cv2
import os
import json

with open("etc/settings.json", "r") as settings_file:
    settings = json.load(settings_file)
    ascii_signs = settings["ascii_signs"]
    background_color = tuple(settings["background_color"])
    font_color = tuple(settings["font_color"])


def progress_bar(nominator, denominator):
    percent = nominator * 100 // denominator
    progress = "".join(['#'] * (percent//10)) + "".join([' '] * (10 - percent//10))
    print(f"[{progress}] {percent}%\t{nominator} / {denominator}")


def scale_image(im_name, percent):
    image = Image.open(im_name)
    height_size = int((float(image.size[1]) * float(percent)))
    width_size = int((float(image.size[0]) * float(percent)))
    image = image.resize((width_size, height_size), Image.NEAREST)
    return image


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


def main(gif_name, percent):
    gif = Image.open(gif_name)
    clear_name = gif_name[:-4]
    frames = []
    i = 0

    # Convert GIF to list of Images
    for frame in range(0, gif.n_frames-1):
        frame_name = f"tmp/{clear_name}{i}.png"
        frames.append(frame_name)
        i += 1
        gif.seek(frame)
        gif.save(frame_name)

    result_name = f"{clear_name}-ASCII.gif"
    ascii_frames = []
    i = 0

    # Convert Images to ASCII
    for frame in frames:
        if percent == 100:
            ascii_frame = image_to_ascii_png(frame)
            ascii_frames.append(ascii_frame)
            os.remove(frame)
        else:
            tiny_frame = scale_image(frame, percent / 100)
            frame_tiny_name = f"tmp/{frame[:-4]}-tiny.png"
            tiny_frame.save(frame_tiny_name)
            ascii_frame = image_to_ascii_png(frame_tiny_name)
            ascii_frames.append(ascii_frame)
            os.remove(frame)
            os.remove(frame_tiny_name)
        i += 1

        os.system("cls")
        progress_bar(i, len(frames))

    # Create ASCII GIF from list of Images
    ascii_frames[0].save(result_name, format='GIF', append_images=ascii_frames[1:], save_all=True, duration=100, loop=0)
    print(result_name, "has just been generated")
    Image.open(result_name)


if __name__ == "__main__":
    gif_name = input("GIF File name: ")
    percent = int(input("Percent of compression [%]: "))
    main(gif_name, percent)