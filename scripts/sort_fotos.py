from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

import os, sys

from dataclasses import dataclass, asdict

from pprint import pprint
from typing import Union

from datetime import datetime

IMAGE_FOLDER = "/home/hugo/MEGA/fotos/pictures"


image_filenames = os.listdir(IMAGE_FOLDER)
image_filenames = [os.path.join(IMAGE_FOLDER, filename) for filename in image_filenames]

#TODO: dingen met GPS

@dataclass
class MyGpsInfo():
    GPSAltitude: tuple
    GPSAltitudeRef: Union[bytes, str]
    GPSLatitude: tuple
    GPSLatitudeRef: Union[bytes, str]
    GPSLongitude: tuple
    GPSLongitudeRef: Union[bytes, str]

class MyImage():
    def __init__(self, filename:str):
        self.filename = filename
        self.image = Image.open(image_name)
        exifdata =  self.image.getexif()
        for tag_id in exifdata:
            self.__setattr__(TAGS.get(tag_id, tag_id), exifdata.get(tag_id))
        
        gps_info = {}
        for key in self.GPSInfo.keys():
            decode = GPSTAGS.get(key,key)
            gps_info[decode] = self.GPSInfo[key]
        
        try:
            mygpsinfo = MyGpsInfo(
                    GPSAltitude =gps_info["GPSAltitude"],
                    GPSAltitudeRef = gps_info["GPSAltitudeRef"],
                    GPSLatitude = gps_info['GPSLatitude'],
                    GPSLatitudeRef = gps_info['GPSLatitudeRef'],
                    GPSLongitude = gps_info["GPSLongitude"],
                    GPSLongitudeRef = gps_info["GPSLongitudeRef"]
                )
        except:
            mygpsinfo = None
            
        self.GpsData = mygpsinfo

        try:
            self.DateTime = datetime.strptime(self.DateTime, '%Y:%m:%d %H:%M:%S')
        except:
            self.DateTime = None
        
    def organize(self, image_root_destination:str='../pictures', remove_source:bool=False):
        if not os.path.exists(image_root_destination):
            os.makedirs(image_root_destination)
        



def print_exif(exifdata):
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag:25}({tag_id}): {data}")


for i, image_name in enumerate(image_filenames):
    # print(i)
    myimage = MyImage(image_name)
    
    # image = Image.open(image_name)

    # input("-"*50)
    