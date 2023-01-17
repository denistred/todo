from PIL import Image, ImageDraw, ImageFont, ImageQt

def create_image(text):
    if len(text) > 50:
        text = text[:50] + '...'
    image = Image.new('RGBA', (355, 25))
    im = ImageDraw.Draw(image)
    im.rounded_rectangle(((0, 0), (355, 25)), 5, fill=(255, 255, 255))
    font = ImageFont.truetype('fonts/arial.ttf', 13)
    im.text((5, 7), text, fill=(0,0,0), font=font)
    return ImageQt.ImageQt(image)
