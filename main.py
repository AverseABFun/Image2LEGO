import PIL.Image
import PIL.ImageColor
import os
import math
#from flask import Flask, request
#from flask_restful import Resource, Api, reqparse

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lego_colors = [
    "#81007B", "#0055BF", "#237841", "#F2CD37", "#583927", "#C91A09",
    "#FFFFFF", "#9BA19D", "#000000", "#5A93DB", "#73DCA1", "#352100",
    "#FECCCF", "#FF698F", "#3CB371"
]
substitutes = {
    PIL.ImageColor.getrgb("#FF698F"): PIL.ImageColor.getrgb("#9BA19D")
}
new_colors = []
for color in lego_colors:
    new_colors.append(PIL.ImageColor.getrgb(color))
lego_colors = new_colors


def pixilate_image(image_name, pixel_count=6, new_image_name="image"):
    if new_image_name == "image":
        new_image_name = image_name
    image = PIL.Image.open(image_name)

    new_image = image.resize((pixel_count, pixel_count),
                             resample=PIL.Image.Resampling.BILINEAR)

    new_image.save(new_image_name)


def match_colors(image_name, colors=lego_colors):

    def nearest_colour( subjects, query ):
        return min( subjects, key = lambda subject: sum( (s - q) ** 2 for s, q in zip( subject, query ) ) )

    image = PIL.Image.open(image_name)

    for x in range(image.width):
        for y in range(image.height):
            color = image.getpixel((x, y))
            nearest_color = nearest_colour(colors,color)
            try:
                nearest_color = substitutes[nearest_color]
            except KeyError:
                pass
            image.putpixel((x, y), nearest_color)
    image.save(image_name)


def pixilate_images(folder, pixel_count=6):
    files = os.listdir(folder)
    for file in files:
        pixilate_image(folder + "/" + file, pixel_count=pixel_count)


def match_colors_images(folder, colors=lego_colors):
    files = os.listdir(folder)
    for file in files:
        match_colors(folder + "/" + file, colors=colors)


def modify_images(folder, pixel_count=6, colors=lego_colors):
    pixilate_images(folder, pixel_count=pixel_count)
    match_colors_images(folder, colors=colors)
    return


def split_image(image_name, num_pixels_per_sub=6):
    image = PIL.Image.open(image_name)

    width, height = image.size
    column_width = num_pixels_per_sub
    row_height = num_pixels_per_sub

    rows = int(height / row_height)
    columns = int(width / column_width)

    for i in range(rows):
        for j in range(columns):

            x = i * column_width
            y = j * row_height

            smaller_image = image.crop(
                (x, y, x + column_width, y + row_height))

            smaller_image.save(f"images/{image_name.split('.')[0]}/{letters[j]}{i+1}.png")


def make_joined(file):
    pixilate_image(file,
                   pixel_count=56,
                   new_image_name="pixilated_horse.png")
    match_colors("pixilated_horse.png")
    image = PIL.Image.open("pixilated_horse.png")
    image.resize((1000,1000))
    image.save("pixilated_horse.png")

"""
app = Flask(__name__)
api = Api(app)


class Image(Resource):
    def post(self):
        file = request.files['file']
        file.save("uploads/" + file.filename)

api.add_resource(Image, '/image')"""

if __name__ == '__main__':
    #app.run()
    make_joined("base.png")
