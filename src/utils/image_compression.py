import os

from PIL import Image
from io import BytesIO
from django.core.files import File


def compress(file):
    """
    Compresses an image file by converting it to JPEG format with reduced quality.
    Returns:
        File: A new image file object in JPEG format with reduced quality.
    Notes:
        - If the image is in 'P' or 'RGBA' mode, it will be converted to 'RGB' mode before compression.
    """
    
    with Image.open(file) as image:
        if image.mode in ('P', 'RGBA'):
            image = image.convert('RGB')

        image_io = BytesIO()

        image.save(image_io, format='JPEG', quality=50, optimize=True)

        return File(image_io, name=file.name)