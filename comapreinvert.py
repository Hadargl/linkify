def img_brightness(img, no_of_pixels, img_width, img_height, no_of_pixels,):

    list_of_pixels = []

    for i in range(no_of_pixels):
        list_of_pixels.append((math.floor(img.width * random.uniform(0, 0.9)), img.height / 2))

    pixel_colours = []

    for p in list_of_pixels:
        pixel_colours += im.getpixel(p)

    pixel_colours_total = sum(pixel_colours)

    return pixel_colours_total











def which_image_is_brighter(img, img_invert, img_brightness):
    if img_brightness(img) > img_brightness(img_invert):
        return img
    else:
        return img_invert



