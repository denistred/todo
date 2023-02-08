from PIL import Image, ImageDraw, ImageFont, ImageQt, ImageFilter


def create_image(text):
    if len(text) > 50:
        text = text[:50] + '...'
    image = Image.new('RGBA', (365, 35))
    im = ImageDraw.Draw(image)
    im.rectangle(((7, 7), (343, 28)), fill=(0, 0, 0, 100))
    image = image.filter(ImageFilter.GaussianBlur(radius=3))
    im = ImageDraw.Draw(image)
    im.rounded_rectangle(((7, 7), (343, 28)), 3, fill=(255, 255, 255))
    font = ImageFont.truetype('fonts/arial.ttf', 13, )
    im.text((10, 10), text, fill=(0, 0, 0), font=font)
    return ImageQt.ImageQt(image)
