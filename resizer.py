from os import listdir
from PIL import Image

def resizer(img, dimensions, path):
    new = img.resize(dimensions)
    new.save(path)

def resize_all(folder_path):
    files = listdir(folder_path)
    for fic in files:
        full_path = folder_path + f"/{fic}"
        img = Image.open(full_path)
        resizer(img, (64, 64), full_path)

def splat_conversion(color_value, color_str):
    splat_path = "images/Default (256px)"
    test_files = listdir(splat_path)
    for i, item in enumerate(test_files):
        img = fill_pixel_of_same_colour(splat_path + f"/{item}", (255, 255, 255, 255), color_value)
        resizer(img, (64, 64), f"images/splats_{color_str}/splat{i}.png")


def fill_pixel_of_same_colour(img_path, target_colour, replacement_colour):
    img = Image.open(img_path).convert("RGBA")
    for row in range(img.height):
        for column in range(img.width):
            current_pixel_color = img.getpixel((column, row))
            if current_pixel_color == target_colour:
                img.putpixel((column, row), replacement_colour)
    return img

if __name__ == "__main__":
    resize_all("images/walkable_tiles")

