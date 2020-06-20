import csv
import json
import urllib.request
import os
import shutil
from tqdm import tqdm
import sys
import glob
from ModelClasses import ModelClasses


class CSVReader:
    IMAGE_URL_CSV_INDEX = 27
    ANNOTATIONS_CSV_INDEX = 28
    IMAGE_HEIGHT_CSV_INDEX = 29
    IMAGE_WIDTH_CSV_INDEX = 30

    DATASET_ROOT_FOLDER = 'dataset'
    DATASET_FOLDERS = ["backup", "images", "labels"]

    def __init__(self, csv_file):
        self.object_classes = []
        self.dataset_objects = self.parse_csv_file(csv_file)

    def parse_csv_file(self, filename):
        dataset = []
        with open(filename, encoding='utf-8') as csv_file:
            read_csv = csv.reader(csv_file, delimiter=',')

            for index, row in enumerate(read_csv):
                if index > 1:
                    image_heigth = row[self.IMAGE_HEIGHT_CSV_INDEX]
                    image_width = row[self.IMAGE_WIDTH_CSV_INDEX]
                    list_of_bounding_boxes = json.loads(row[self.ANNOTATIONS_CSV_INDEX], strict=False)

                    bounding_boxes = []
                    for box in list_of_bounding_boxes:
                        if box['label'] not in self.object_classes:
                            self.object_classes.append(box['label'])

                        object_class_index = ModelClasses.get_class_index(box['label'])
                        if object_class_index != ModelClasses.INVALID_CLASS:
                            x = (int(box['left']) + int(box['width']) / 2.0) / float(image_width)
                            y = (int(box['top']) + int(box['height']) / 2.0) / float(image_heigth)
                            width = int(box['width']) / float(image_width)
                            height = int(box['height']) / float(image_heigth)

                            bounding_boxes.append({
                                'object_class': object_class_index,
                                'annotation': f"{x} {y} {width} {height}"
                            })

                    dataset.append({
                        'x': row[self.IMAGE_URL_CSV_INDEX],
                        'y': bounding_boxes
                    })

        return dataset

    def download_images(self):
        index = 0
        for data in tqdm(self.dataset_objects):
            index += 1
            urllib.request.urlretrieve(data['x'], f"{self.DATASET_ROOT_FOLDER}/images/{index}.jpg")

    def create_directory_structure(self):
        if os.path.exists(self.DATASET_ROOT_FOLDER):
            shutil.rmtree(self.DATASET_ROOT_FOLDER, ignore_errors=True)
        try:
            os.makedirs(self.DATASET_ROOT_FOLDER)
            for folder in tqdm(self.DATASET_FOLDERS):
                os.makedirs(f"{self.DATASET_ROOT_FOLDER}/{folder}")

        except OSError:
            print("Creation of the structure failed")
            sys.exit()
        else:
            print("Successfully created structure")

    def include_annotations_to_images(self):
        index = 0
        for data in tqdm(self.dataset_objects):
            index += 1
            file_images = open(f"{self.DATASET_ROOT_FOLDER}/images/{index}.txt", "w")
            file_labels = open(f"{self.DATASET_ROOT_FOLDER}/labels/{index}.txt", "w")
            for y in data['y']:
                file_images.write(f"{y['object_class']} {y['annotation']}\n")
                file_labels.write(f"{y['object_class']} {y['annotation']}\n")
            file_images.close()
            file_labels.close()

    def split_data_into_train_and_test(self):
        # Current directory
        current_dir = '/home/cbusa/github/from-amazon-mechanical-turk-to-yolo/dataset/images'

        # Percentage of images to be used for the test set
        percentage_test = 30

        # Create and/or truncate train.txt and test.txt
        file_train = open(f'{self.DATASET_ROOT_FOLDER}/train.txt', 'w')
        file_test = open(f'{self.DATASET_ROOT_FOLDER}/test.txt', 'w')

        # Populate train.txt and test.txt
        counter = 1
        index_test = round(100 / percentage_test)

        for file_path in glob.iglob(os.path.join(current_dir, "*.jpg")):
            title, ext = os.path.splitext(os.path.basename(file_path))
            if counter == index_test:
                counter = 1
                file_test.write(current_dir + "/" + title + '.jpg' + "\n")
            else:
                file_train.write(current_dir + "/" + title + '.jpg' + "\n")
                counter = counter + 1

        file_test.close()
        file_train.close()

    def write_classes_names_file(self):
        file = open(f"{self.DATASET_ROOT_FOLDER}/classes.names", "w")
        for class_name, index in ModelClasses.CLASS_NAMES:
            file.write(f"{class_name}\n")
        file.close()

    def write_configuration_data_file(self):
        file = open(f"{self.DATASET_ROOT_FOLDER}/configuration.data", "w")
        file.write(f'classes = {ModelClasses.count_classes()}\n')
        file.write(f'train = /home/cbusa/github/from-amazon-mechanical-turk-to-yolo/dataset/train.txt\n')
        file.write(f'valid = /home/cbusa/github/from-amazon-mechanical-turk-to-yolo/dataset/test.txt\n')
        file.write(f'names = /home/cbusa/github/from-amazon-mechanical-turk-to-yolo/dataset/classes.names\n')
        file.write(f'backup = /home/cbusa/github/from-amazon-mechanical-turk-to-yolo/dataset/backup\n')
        file.close()

    def run(self):
        print("Creating the file structure...")
        self.create_directory_structure()

        print("\nDownloading images...")
        self.download_images()

        print("\nIncluding the annotations to the images...")
        self.include_annotations_to_images()

        print("\nSplitting data into train.txt and test.txt")
        self.split_data_into_train_and_test()

        print("\nWriting the classes.names file")
        self.write_classes_names_file()

        print("\nWriting the configuration.data file...")
        self.write_configuration_data_file()
