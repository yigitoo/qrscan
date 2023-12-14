#!/usr/bin/env python
# author: yigitoo.
# License: MIT License.
import cv2 as cv
from pandas import DataFrame
from glob import glob
from PIL import Image
import requests


from uuid import uuid4 as random_id_generator
import sys
import os
from io import BytesIO, StringIO

from clipboard import ClipboardClient

class QRCodeScanner:
    def __init__(self):
        self.predefined_save_area = os.getenv('QRSCANNER_FOLDER')

    def read_qr_code(self, image_filename: str) -> str:
        """Read an imaeg and read the QR Code

        Args:
            image_filename (string): Path to file

        Returns:
            qr (String): Value from the QRCode data.
        """

        try:
            img = cv.imread(image_filename)
            detect = cv.QRCodeDetector()
            value, points, straight_qrcode = detect.detectAndDecode(img)
            return value

        except:
            print("Error: Could not read QR Code.")
            return "/COULD NOT RESOLVE QR CODE/"

    def read_from_url(self, url: str) -> str:
        response: bytes = requests.get(url).content
        image: Image = Image.open(BytesIO(response))
        image = image.convert('RGB') if image.mode != 'RGB' else image

        file_id: str = str(random_id_generator())
        file_path: str = self.predefined_save_area+f'\\{file_id}.jpg'
        image.save(file_path)

        result: str = self.read_qr_code(file_path)
        return result


    def multi_read_qr_code(self, folder_path):
        df = DataFrame(columns=['filename', 'qrcode'])
        files = glob.glob('data/*.jpg')

        for file in files:
            qr = self.read_qr_code(file)
            row = {'filename': file, 'qr': qr}

            df = df.append(row, ignore_index = True)

        df.head()

if __name__ == '__main__':
    scanner = QRCodeScanner()

    if len(sys.argv) == 1:
        _clipboard = ClipboardClient()
        file_id: str = _clipboard.save_as_image()
        file_name: str = _clipboard.get_full_name(file_id)
        result: str = scanner.read_qr_code(file_name)
        print(f"Result is: {result if result != '' else 'This is not a QRCode image'}.")

    else:
        if sys.argv[-1] == "-d":
            import os
            os.system(f"del {os.getenv('QRSCANNER_FOLDER')}")
            os.system(f"echo This folder is created for saving qrcode image files > {os.getenv('QRSCANNER_FOLDER')}\\note.txt")
        elif "http" in sys.argv[-1]:
            result: str = scanner.read_from_url(sys.argv[-1])
            print(f"Result is: {result if result != '' else 'This is not a QRCode image'}")
        else:
            file_name: str = sys.argv[-1]
            result: str = scanner.read_qr_code(file_name)
            print(f"Result is: {result if result != '' else 'This is not a QRCode image'}.")
