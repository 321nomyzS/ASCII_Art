# ASCII Art
This is a Python program that generates ASCII art from png and gif files. The program consists of two scripts, "ASCII Gif Generator.py" and "ASCII png Generator.py". The program has two folders, "etc" and "tmp". The "etc" folder contains the "settings.json" file, which allows customization of the ASCII art output.

![ASCII Auto](samples/ASCI2auto.gif)

## How to use
To use the program, simply run the desired script and follow the instructions on the command line interface. You will be prompted to enter the file name of the png or gif file you wish to convert to ASCII art, as well as the desired width of the output.

If you want to customize the output, you can modify the "settings.json" file located in the "etc" folder.

## Settings.json
```
{
  "ascii_signs": "#@?%&!*`,. ",
  "font_color": [0, 0, 0],
  "background_color": [255, 255, 255]
}
```
The "settings.json" file contains the following options:

- ascii_signs: A string of ASCII characters that will be used to represent the varying shades of gray in the image. The characters on the left of the string correspond to darker shades, while characters on the right correspond to lighter shades.
- font_color: A list of RGB values (0-255) representing the font color of the ASCII art output.
- background_color: A list of RGB values (0-255) representing the background color of the ASCII art output.
By modifying these options, you can create custom ASCII art output to suit your preferences.

## Requirements
- PIL (Python Imaging Library)
- cv2 (OpenCV)
