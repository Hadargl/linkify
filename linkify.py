import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"
from PIL import Image, ImageEnhance, ImageGrab, ImageOps
import webbrowser
import requests
import difflib
from difflib import get_close_matches
import tkinter
import pyautogui
import csv
import sys
import cv2
import random
import math



img = pyautogui.screenshot()
print("image captured")

x1 = 0
y1 = 0
x2 = img.width
y2 = img.height

im = img.crop((x1 + 125, y1 + 375, x2 * 0.3, y2 * 0.24))

newsize = (im.width*2, im.height*2)
im = im.resize(newsize)

# print("image width: " + str(im.width) + "image height: " + str(im.height))

im.save("image.png")

img = cv2.imread("image.png")

# cv2.imshow("cropped", img)

no_of_pixels = 50

list_of_pixels = []

for i in range(no_of_pixels):
    list_of_pixels.append((math.floor(im.width * random.uniform(0, 0.9)), im.height / 2))

# print("pixel locations: " + str(list_of_pixels))

pixel_colours = []

for p in list_of_pixels:
    pixel_colours += im.getpixel(p)


# pixel tuple builder

# pixel_rgb = ()
# listofcolours = []

# for p in list_of_pixels:
#     pixel_rgb = im.getpixel(p)
#     listofcolours.append(pixel_rgb)

# print("tuple listofcolours: " + str(listofcolours))

# print("pixel colours: " + str(pixel_colours))

pixel_colours_total = sum(pixel_colours)

print("pixel colour total: " + str(pixel_colours_total))


if pixel_colours_total < 6000:
    new_img = 255 - img
    print("dark image detected")
    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    adaptive_threshold = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 11)
else:
    new_img = img
    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    adaptive_threshold = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 11)
    print("light image detected")

# cv2.imshow('ad', adaptive_threshold)

config = "-c tessedit_char_blacklist=¥—)] --psm 3 --oem 3"

text = pytesseract.image_to_string(adaptive_threshold, config=config)

# print(text)

hImg, wImg = adaptive_threshold.shape


box = pytesseract.image_to_boxes(adaptive_threshold)

# for b in box.splitlines():
#     print(b)
#     b = b.split(' ')
#     x,y,w,h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
#     cv2.rectangle(adaptive_threshold,(x,hImg - y),(w,hImg - h),(0,0,0),1)

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


# if the longest_sequence is too long, the matcher finds other terms inthe str that arent the root domain
# Here, long sequences are cut to 30 chars long and then used to find a matching domain
# further down we make a new variable called longest_sequence_for_path_build because we destroyed longest_sequence below
if len(longest_sequence) > 30:
    estimate_domain = [ x for x in longest_sequence]
    del estimate_domain[30:len(longest_sequence)-1]
    longest_sequence = ''.join(estimate_domain)
else:
    longest_sequence = longest_sequence


print("initial estimate: " + longest_sequence)

with open("top500Domains.csv", "r") as f:
    reader = csv.DictReader(f)

    domains = [row["Root Domain"] for row in reader]

matches = get_close_matches(longest_sequence, domains, n=5, cutoff=0.1)

closest_match = matches[0]

print("closest domain match: " + closest_match)

longest_sequence_for_path_build = extract_longest(text)

domain_len = len(closest_match)

# Old URL builder

# def build_url_path(link, match, domain_len):
#     first_slash_loc = link.index("/")
#     if "reddit" in match:
#         slash_loc = first_slash_loc + 3
#     elif link[0]=='/':
#         slash_loc = first_slash_loc
#     else:
#         link[0] = '/'
#     return link[slash_loc:].strip()

# def build_url_path(link, match):
#     first_slash_loc = link.index("/")
#     if "reddit" in match:
#         slash_loc = first_slash_loc + 3
#     else:
#         slash_loc = first_slash_loc
#     return link[slash_loc:].strip()

# this url path builder catches the youtube bug where the first "/" isnt recognised
def build_url_path(link, match, domain_len):
    if "reddit" in match:
        first_slash_loc = link.index("/")
        slash_loc = first_slash_loc + 3
        return link[slash_loc:].strip()
    # elif link[0]=='/':
    #     slash_loc = first_slash_loc
    elif "/" in link:
        first_slash_loc = link.index("/")
        slash_loc = first_slash_loc
        return link[slash_loc:].strip()
    else:
        linklist = [x for x in link]
        del linklist[:domain_len]
        linklist[0] = "/"
        # print("else print: ")
        # print(linklist)
        # print(type(linklist))
        link = "".join(linklist)
        # print(link)
        return link


new_path = build_url_path(longest_sequence_for_path_build, closest_match, domain_len)

print("estimated path: " + new_path)

new_url = str(matches[0]) + str(new_path)

print("sending you to: " + new_url)

cv2.imshow("adaptive th", adaptive_threshold)

webbrowser.register(
    "chrome",
    None,
    webbrowser.BackgroundBrowser(
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ),
)
webbrowser.get("chrome").open(new_url)


cv2.waitKey(0)
