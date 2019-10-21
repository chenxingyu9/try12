"""
Usage:
# Create train data:
python xml_to_csv.py -i [PATH_TO_IMAGES_FOLDER]/train -o [PATH_TO_ANNOTATIONS_FOLDER]/train_labels.csv

# Create test data:
python xml_to_csv.py -i [PATH_TO_IMAGES_FOLDER]/test -o [PATH_TO_ANNOTATIONS_FOLDER]/test_labels.csv
"""

import os
import glob
import pandas as pd
import argparse
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    """
    Extracts content from all .xml files present in 'path' & creates single
    dataframe containing all data.

    args : path of folder containing .xml files.
    returns : dataframe containing all information.
    """
    xml_list = []
    # iterates through all .xml files
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)						# Converts .xml file into tree structure
        root = tree.getroot()
        # iterates through all '<object>' tags
        for member in root.findall('object'):
            value = (root.find('filename').text,		# filename
                        int(root.find('size')[0].text),  # width
                        int(root.find('size')[1].text),  # height
                        member[0].text,					# class (eg. apple)
                        # starting row pixel for bounding box
                        int(member[4][0].text),
                        # starting column pixel for bounding box
                        int(member[4][1].text),
                        # ending row pixel for bounding box
                        int(member[4][2].text),
                        # ending column pixel for bounding box
                        int(member[4][3].text)
                        )
            # appends object's attribute tuple to list
            xml_list.append(value)
    column_name = ['filename', 'width', 'height',
        'class', 'xmin', 'ymin', 'xmax', 'ymax']
    # creates dataframe containing information of all images in path
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    for folder in ['train','test']:
        image_path = os.path.join(os.getcwd(), ('/content/try12/data/images/' + folder))
        xml_df = xml_to_csv(image_path)
        
        # saving dataframe as *.csv in 'images/' folder.
        xml_df.to_csv(('/content/try12/data/annotations/' + folder + '_labels.csv'), index=None)
        print('Successfully converted '+folder+' xml to csv.')



if __name__ == "__main__":
    main()