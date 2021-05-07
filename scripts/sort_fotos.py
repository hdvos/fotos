from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

import os, sys

from dataclasses import dataclass, asdict

from pprint import pprint
from typing import Union

from datetime import datetime

from csv import writer as CsvWriter

import shutil

IMAGE_FOLDER = "/home/hugo/MEGA/fotos/pictures"


image_filenames = os.listdir(IMAGE_FOLDER)
image_filenames = [os.path.join(IMAGE_FOLDER, filename) for filename in image_filenames]

#TODO: dingen met GPS

#%% Utils
def print_exif(exifdata):
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag:25}({tag_id}): {data}")

#%% Datastructures
@dataclass
class MyGpsInfo():
    GPSAltitude: tuple
    GPSAltitudeRef: Union[bytes, str]
    GPSLatitude: tuple
    GPSLatitudeRef: Union[bytes, str]
    GPSLongitude: tuple
    GPSLongitudeRef: Union[bytes, str]


#%% MyImage Class
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
        
    def organize(self, image_root_destination:str='../pictures', remove_source:bool=False, update_self:bool = True):
        if not os.path.exists(image_root_destination):
            os.makedirs(image_root_destination)
        
        year = str(self.DateTime.year)
        month = self.DateTime.strftime('%m_%B')

        file_destination_folder = os.path.join(image_root_destination, year, month)
    
        if not os.path.exists(file_destination_folder):
            os.makedirs(file_destination_folder)

        file_path = os.path.join(file_destination_folder, os.path.basename(self.filename))
        # input(file_path)
        if remove_source:
            shutil.move(self.filename, file_path)
        else:
            shutil.copy2(self.filename, file_path)

        if update_self:
            self.filename = file_path

    #TODO: adapt as to easily add new fieldnames
    def _initialize_index_file(self, index_file:str):
        assert not os.path.exists(index_file), 'Cannot initialize, file already exists.'

        with open(index_file, 'wt') as out:
            writer = CsvWriter(out, delimiter='\t')
            writer.writerow(["Description", "Filename", "Location", "DateTime"])

    #TODO: adapt as to easily add new fieldnames
    def add_to_index(self, index_file:str = "../index.csv"):
        if not os.path.exists(index_file):
            self._initialize_index_file(index_file)

        description = ''
        filename = os.path.basename(self.filename)
        location = self.filename
        date_and_time = self.DateTime.strftime('%Y:%m:%d %H:%M:%S')

        with open(index_file, 'a') as out:
            writer = CsvWriter(out, delimiter='\t')
            writer.writerow([description, filename, location, date_and_time])


#%% Main
if __name__ == '__main__':
    os.chdir(os.path.split(__file__)[0])   
    assert os.getcwd() == os.path.split(__file__)[0]
    for i, image_name in enumerate(image_filenames):
        # print(i)
        myimage = MyImage(image_name)
        myimage.organize()
        myimage.add_to_index()
        # print(os.getcwd())
        # image = Image.open(image_name)

        # input("-"*50)
