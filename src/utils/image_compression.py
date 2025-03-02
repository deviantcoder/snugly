import os
from io import BytesIO

from django.core.files import File
from PIL import Image


def compress(file):
    try:
        with Image.open(file) as image:
            if image.mode in ('P', 'RGBA'):
                image = image.convert('RGB')

            image_io = BytesIO()

            image.save(image_io, format='JPEG', quality=50, optimize=True)

            return File(image_io, name=file.name)
    except Exception:
        pass