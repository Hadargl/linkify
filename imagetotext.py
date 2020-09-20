import pytesseract as tess

tess.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"
from PIL import Image, ImageEnhance, ImageGrab, ImageOps
import webbrowser
import requests
import difflib
from difflib import get_close_matches
import tkinter
import pyautogui
import csv
import sys
from colorthief import ColorThief
import cv2

img = pyautogui.screenshot()

img.save('image.png')



x1 = 0
y1 = 0
x2 = img.width
y2 = img.height

print("resolution: ", x2, y2)

im = img.resize((img.width * 2, img.height * 2), 0)


# im.show()

imx1 = 0
imy1 = 0
imx2 = im.width
imy2 = im.height

# enhancer = ImageEnhance.Contrast(im)

# contrastimg = enhancer.enhance(0.9)



cropped = im.crop((x1, y1 + 750, imx2 * 0.4, imy2 * 0.24))

sharpened = ImageEnhance.Sharpness(cropped)

# sharpened_img = sharpened.enhance(6.0)
sharpened_img = sharpened.enhance(6.0)

print(sharpened_img.getpixel((sharpened_img.width * 0.5, sharpened_img.height * 0.5)))

pixel_colour1 = sharpened_img.getpixel((sharpened_img.width * 0.5, sharpened_img.height * 0.5))
# pixel_colour2 = sharpened_img.getpixel((sharpened_img.width * 0.6, sharpened_img.height * 0.5))
# pixel_colour3 = sharpened_img.getpixel((sharpened_img.width * 0.7, sharpened_img.height * 0.5))
# pixel_colour4 = sharpened_img.getpixel((sharpened_img.width * 0.8, sharpened_img.height * 0.5))
# pixel_colour5 = sharpened_img.getpixel((sharpened_img.width * 0.9, sharpened_img.height * 0.5))



pixel_sum1 = pixel_colour1[0] + pixel_colour1[1] + pixel_colour1[2] + pixel_colour1[3]
# pixel_sum2 = pixel_colour2[0] + pixel_colour2[1] + pixel_colour2[2] + pixel_colour2[3]
# pixel_sum3 = pixel_colour3[0] + pixel_colour3[1] + pixel_colour3[2] + pixel_colour3[3]
# pixel_sum4 = pixel_colour4[0] + pixel_colour4[1] + pixel_colour4[2] + pixel_colour4[3]
# pixel_sum5 = pixel_colour5[0] + pixel_colour5[1] + pixel_colour5[2] + pixel_colour5[3]

# pixel_average = pixel_sum1 + pixel_sum2 + pixel_sum3 + pixel_sum4 + pixel_sum5
pixel_average = pixel_sum1

print(pixel_average)

if pixel_average < 912:
    inv_img = ImageOps.invert(sharpened_img.convert('RGB'))
    enhancer = ImageEnhance.Contrast(inv_img)
    contrast_img = enhancer.enhance(3.5)
    new_img = contrast_img
    print('dark image')
else:
    new_img = sharpened_img.convert('RGB')
    print('light image')



# enhancer = ImageEnhance.Contrast(im)


# if pixel_average < 912:
#     contrastimg = enhancer.enhance(2.0)
# else:
#     contrastimg = enhancer.enhance(0.9)



text = tess.image_to_string(new_img)

# sharpened_img.show()
new_img.show()

print(text)


# new_size = sharpened_img.resize((x2 * 2, y2 * 2))
# new_size.show()


def extract_longest(text):
    sequences = []
    sequence = ""

    for c in text:
        if not c.isspace():
            sequence += c
        else:
            sequences.append(sequence)
            sequence = ""

    longest_sequence = sequences[0]

    for s in sequences:
        if len(s) > len(longest_sequence):
            longest_sequence = s

    return longest_sequence


longest_sequence = extract_longest(text)

print(text)
print(longest_sequence)



# r = requests.get('http://' + longest_sequence)
# # import pdb; pdb.set_trace()
# if not r.ok or longest_sequence in r.text:
#     print('url doesnt exist :' + longest_sequence)
# else:
#     url = longest_sequence


with open("top500Domains.csv", "r") as f:
    reader = csv.DictReader(f)

    domains = [row["Root Domain"] for row in reader]



matches = get_close_matches(longest_sequence, domains, n=5, cutoff=0.1)

closest_match = matches[0]

print(matches)


def build_url_path(link, match):
    first_slash_loc = link.index("/")
    if "reddit" in match:
        slash_loc = first_slash_loc + 3
    else:
        slash_loc = first_slash_loc
    return link[slash_loc:].strip()


new_path = build_url_path(longest_sequence, closest_match)

new_url = matches[0] + new_path

print("new url: " + new_url + " length: " + str(len(new_url)))


webbrowser.register(
    "chrome",
    None,
    webbrowser.BackgroundBrowser(
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ),
)
webbrowser.get("chrome").open(new_url)

# sys.exit(imagetotext.py)
