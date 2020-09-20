import pytesseract
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
# from colorthief import Color
import cv2

img = pyautogui.screenshot()

x1 = 0
y1 = 0
x2 = img.width
y2 = img.height

im = img.crop((x1 + 125, y1 + 375, x2 * 0.5, y2 * 0.24))

print("image width: " + str(im.width) + "image height: " + str(im.height))

im.save('image.png')

img = cv2.imread('image.png')

cv2.imshow("cropped", img)

pixel_colour1 = im.getpixel((im.width * 0.5, im.height * 0.5))
pixel_colour2 = im.getpixel((im.width * 0.6, im.height * 0.5))
pixel_colour3 = im.getpixel((im.width * 0.7, im.height * 0.5))
pixel_colour4 = im.getpixel((im.width * 0.8, im.height * 0.5))
pixel_colour5 = im.getpixel((im.width * 0.9, im.height * 0.5))

pixel_sum1 = pixel_colour1[0] + pixel_colour1[1] + pixel_colour1[2] + pixel_colour1[3]
pixel_sum2 = pixel_colour2[0] + pixel_colour2[1] + pixel_colour2[2] + pixel_colour2[3]
pixel_sum3 = pixel_colour3[0] + pixel_colour3[1] + pixel_colour3[2] + pixel_colour3[3]
pixel_sum4 = pixel_colour4[0] + pixel_colour4[1] + pixel_colour4[2] + pixel_colour4[3]
pixel_sum5 = pixel_colour5[0] + pixel_colour5[1] + pixel_colour5[2] + pixel_colour5[3]

pixel_average = pixel_sum1 + pixel_sum2 + pixel_sum3 + pixel_sum4 + pixel_sum5

print("pixel average: " + str(pixel_average))

if pixel_average < 3000:
    new_img = 255 - img
    print('dark image')
    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 39, 11)
else:
    new_img = img
    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 15)
    print('light image')


config = "--psm 3"

text = pytesseract.image_to_string(adaptive_threshold, config=config)


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

print("longest sequence: " + longest_sequence)

with open("top500Domains.csv", "r") as f:
    reader = csv.DictReader(f)

    domains = [row["Root Domain"] for row in reader]

matches = get_close_matches(longest_sequence, domains, n=5, cutoff=0.1)

closest_match = matches[0]

print("closest match: " + closest_match)

domain_len = len(closest_match)

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
    elif '/' in link:
        first_slash_loc = link.index("/")
        slash_loc = first_slash_loc
        return link[slash_loc:].strip()
    else:
        linklist = [ x for x in link]
        del linklist[:domain_len]
        linklist[0] = '/'
        print("else print: ")
        print(linklist)
        print(type(linklist))
        link = ''.join(linklist)
        print(link)
        return link

new_path = build_url_path(longest_sequence, closest_match, domain_len)

print(new_path)

new_url = str(matches[0]) + str(new_path)

print("new url: " + new_url + " length: " + str(len(new_url)))

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
