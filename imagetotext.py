import pytesseract as tess

tess.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"
from PIL import Image, ImageEnhance, ImageGrab
import webbrowser
import requests
import difflib
from difflib import get_close_matches
import tkinter
import pyautogui
import csv


img = pyautogui.screenshot()
# img = Image.open('Screenshot 2020-09-19 at 18.32.29.png')

x1 = 0
y1 = 0
x2 = img.width
y2 = img.height

print("resolution: ", x2, y2)

enhancer = ImageEnhance.Contrast(img)

# contrastimg = enhancer.enhance(0.9)
contrastimg = enhancer.enhance(0.9)

cropped = contrastimg.crop((x1 + 100, y1 + 350, x2 * 0.5, y2 * 0.25))

sharpened = ImageEnhance.Sharpness(cropped)

# sharpened_img = sharpened.enhance(6.0)
sharpened_img = sharpened.enhance(3.0)

text = tess.image_to_string(sharpened_img)

sharpened_img.show()
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
