#!/usr/bin/env python
# author: yigitoo.
# License: MIT License.
import cv2 as cv
from pandas import DataFrame
import sys
from glob import glob

from clipboard import ClipboardClient

class QRCodeScanner:
    def __init__(self):
        pass

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
        print(f"Result is: {result}.")

    else:
        if sys.argv[-1] == "-d":
            import os
            os.system(f"del {os.getenv('QRSCANNER_FOLDER')}")
            os.system(f"echo This folder is created for saving qrcode image files > {os.getenv('QRSCANNER_FOLDER')}\\note.txt")
            raise SystemExit(0)
        file_name: str = sys.argv[-1]
        result: str = scanner.read_qr_code(file_name)
        print(f"Result is: {result}.")
