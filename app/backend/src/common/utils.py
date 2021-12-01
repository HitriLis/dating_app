from PIL import Image, ImageEnhance
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
import os
from django.core.mail import send_mail
from django.conf import settings
from math import sin, cos, radians, acos

def add_watermark(image, opacity=1, wm_interval=0):
    filename = image.name
    content_type = image.content_type
    image = Image.open(image)
    format_file = image.format
    watermark = Image.open(os.path.join(settings.STATIC_ROOT, 'watermark.png'))
    assert 0 <= opacity <= 1
    if opacity < 1:
        if watermark.mode != 'RGBA':
            watermark = watermark.convert('RGBA')
        else:
            watermark = watermark.copy()
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    for y in range(0, image.size[1], watermark.size[1] + wm_interval):
        for x in range(0, image.size[0], watermark.size[0] + wm_interval):
            layer.paste(watermark, (x, y))

    canvas = Image.composite(layer, image, layer)
    buffer_file = BytesIO()
    canvas.save(fp=buffer_file, format=format_file)
    buff_val = buffer_file.getvalue()
    pillow_image = ContentFile(buff_val)
    return InMemoryUploadedFile(pillow_image, None, filename, content_type, pillow_image.tell, None)


def mail_sender(user, subscriber):
    try:
        send_mail('Взаимная симпатия', f'Вы понравились: {user.first_name}! Почта участника: {user.email}',
                  settings.EMAIL_HOST_USER, [user.email, subscriber.email])
    except Exception as e:
        return e
