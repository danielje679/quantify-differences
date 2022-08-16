# Generate the dataset /data/covid19/03_mosmed in medical decathlon format

import argparse
import os
import pathlib
import json
import inspect
import data as utils


def move_images(img_paths, destination_path):
    """
    :param img_paths: list of exact paths of the images to be moved
    :param destination_path: the destination dir
    :return:
    """
    for source_file in img_paths:
        filename = os.path.basename(source_file)
        destination_file = os.path.join(destination_path, filename)
        os.replace(source_file, destination_file)


def create_json(destination):
    """
    Creates the json file for the medical decathlon directory
    :param destination: directory of the medical decathlon dir
    """

    json_file = os.path.join(destination, "dataset.json")

    images_tr_dir = os.path.join(destination, "imagesTr")
    images_ts_dir = os.path.join(destination, "imagesTs")
    labels_tr_dir = os.path.join(destination, "labelsTr")

    # get number of training and test images
    num_tr = len([name for name in os.listdir(images_tr_dir)])
    num_ts = len([name for name in os.listdir(images_ts_dir)])

    tr_label_paths = []
    ts_paths = []

    images_tr_list = os.listdir(images_tr_dir)
    labels_tr_list = os.listdir(labels_tr_dir)
    images_tr_list.sort()
    labels_tr_list.sort()

    # get the paths of each training label pair and store them in a dict
    for filename in zip(images_tr_list, labels_tr_list):
        if filename[0].endswith(".nii.gz"):
            image_tr_file = os.path.join("./imagesTr", filename[0])
            label_file = os.path.join("./labelsTr", filename[1])

            tr_label_paths.append({
                "image": image_tr_file,
                "label": label_file
            })

    data = {
        "name": "MosMedData",
        "description": "Segmentation of Covid19 regions of interest (ground-glass opacifications and consolidation)",
        "reference": "Morozov, S., Andreychenko, A., Blokhin, I., Vladzymyrskyy, A., Gelezhe, P., Gombolevskiy, V., Gonchar, A., Ledikhova, N., Pavlov, N., Chernina, V. MosMedData: Chest CT Scans with COVID-19 Related Findings, 2020,",
        "licence": "CC BY NC ND 3.0",
        "release": "28/04/2020",
        "modality": {
            "0": "CT"
        },
        "labels": {
            "0": "infection"
        },
        "numTraining": num_tr,
        "numTest": num_ts,
        "training": tr_label_paths,
        "test": ts_paths
    }

    #  store the json file
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)


def create_medical_decathlon_structure(image_path, label_path):
    """
    :param image_path: path of the downloaded image files from mosmed
    :param label_path: path of the downloaded labels from mosmed
    """
    cwd = os.path.abspath(inspect.getsourcefile(lambda: 0))
    root = pathlib.PurePath(cwd).parents[4]

    # destination paths
    relative_destination = "data/03_mosmed"
    images_tr_dir = os.path.join(root, relative_destination, "imagesTr")
    images_ts_dir = os.path.join(root, relative_destination, "imagesTs")
    labels_tr_dir = os.path.join(root, relative_destination, "labelsTr")

    # create new directories
    os.makedirs(images_tr_dir)
    os.makedirs(images_ts_dir)
    os.makedirs(labels_tr_dir)

    # move the files to the new destination
    img_paths = []
    img_start_idx = 255
    img_end_idx = 305
    for img_idx in range(img_start_idx, img_end_idx):
        filename = "study_0" + str(img_idx) + ".nii.gz"
        file_path = os.path.join(image_path, filename)
        img_paths.append(file_path)

    move_images(img_paths, images_tr_dir)
    utils.move_files(label_path, labels_tr_dir)

    # create the dataset.json file
    create_json(os.path.join(root, relative_destination))


def main():
    # ARGUMENT PARSING
    parser = argparse.ArgumentParser(description='Retrieve statistics about the dataset')

    parser.add_argument('-ip', '--image_path', type=str, help='path to the image data', required=True)
    parser.add_argument('-lp', '--label_path', type=str, help='path to the label data', required=True)

    args = parser.parse_args()

    create_medical_decathlon_structure(args.image_path, args.label_path)


if __name__ == '__main__':
    main()
