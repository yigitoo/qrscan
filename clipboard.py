from PIL import (
    Image,
    ImageGrab
)

import os
from uuid import uuid4 as random_id_generator

class ClipboardClient:
    def __init__(self):
        self.predefined_save_area: str = os.getenv('QRSCANNER_FOLDER')

    def get_image(self) -> Image:
        image = ImageGrab.grabclipboard()
        return image

    def save_as_image(self, image: Image = None) -> str:
        file_id: str = str(random_id_generator())

        if image is None:
            try:
                img: Image = self.get_image()
                img.save(self.predefined_save_area+f'\\{file_id}.jpg')
            except:
                print('Error: You should copy the image to the clipboard.')
                exit(1)
        else:
            image.save(self.predefined_save_area+f'\\{file_id}.jpg')

        return file_id

    def get_full_name(self, file_id: str) -> str:
        return f'{self.predefined_save_area}\\{file_id}.jpg'
