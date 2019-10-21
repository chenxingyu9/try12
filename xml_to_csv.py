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
    # Initiate argument parser
    parser = argparse.ArgumentParser(
        description="Sample TensorFlow XML-to-CSV converter"
    )
    parser.add_argument(
        "-i",
        "--inputDir",
        help="Path to the folder where the input .xml files are stored",
        type=str,
    )
    parser.add_argument(
        "-o", "--outputFile", help="Name of output .csv file (including path)", type=str
    )

    parser.add_argument(
        "-l",
        "--labelMapDir",
        help="Directory path to save label_map.pbtxt file is specified.",
        type=str,
        default="",
    )

    args = parser.parse_args()

    if args.inputDir is None:
        args.inputDir = os.getcwd()
    if args.outputFile is None:
        args.outputFile = args.inputDir + "/labels.csv"

    assert os.path.isdir(args.inputDir)
    os.makedirs(os.path.dirname(args.outputFile), exist_ok=True)
    xml_df, classes_names = xml_to_csv(args.inputDir)
    xml_df.to_csv(args.outputFile, index=None)
    print("Successfully converted xml to csv.")



if __name__ == "__main__":
    main()