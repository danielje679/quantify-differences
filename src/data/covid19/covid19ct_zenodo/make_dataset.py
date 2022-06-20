# Generate the dataset /data/covid19/01_covid19ct_zenodo in medical decathlon format

import argparse
import os
import pathlib
import json
import inspect


def move_files(source_path, destination_path, only_nifti_files=True):
    """Moves files from one directory to another.
    :param source_path: source directory from which to move files
    :param destination_path: destination directory to move the files
    :param only_nifti_files: (default=True) if only .nii.gz files should be moved
    """
    for filename in os.listdir(source_path):
        if only_nifti_files and not filename.endswith(".nii.gz"):
            continue

        source_file = os.path.join(source_path, filename)
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

    # get the paths of each training label pair and store them in a dict
    for filename in zip(os.listdir(images_tr_dir), os.listdir(labels_tr_dir)):
        if filename[0].endswith(".nii.gz"):
            image_tr_file = os.path.join("./imagesTr", filename[0])
            label_file = os.path.join("./labelsTr", filename[1])

            tr_label_paths.append({
                "image": image_tr_file,
                "label": label_file
            })

    data = {
        "name": "Covid-19 CT Zenodo",
        "description": "Segmentation of left and right lung and infections",
        "reference": "Coronavirus Disease Research Community - Zenodo",
        "licence": "Creative Commons Attribution 4.0 International",
        "release": "1.0 20/04/2020",
        "modality": {
            "0": "CT"
        },
        "labels": {
            "0": "right lung",
            "1": "left lung",
            "2": "infection"
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
    :param image_path: path of the downloaded image files from zenodo
    :param label_path: path of the downloaded labels from zenodo
    """
    cwd = os.path.abspath(inspect.getsourcefile(lambda: 0))
    root = pathlib.PurePath(cwd).parents[4]

    # destination paths
    relative_destination = "data/01_covid19ct_zenodo"
    images_tr_dir = os.path.join(root, relative_destination, "imagesTr")
    images_ts_dir = os.path.join(root, relative_destination, "imagesTs")
    labels_tr_dir = os.path.join(root, relative_destination, "labelsTr")

    # create new directories
    os.makedirs(images_tr_dir)
    os.makedirs(images_ts_dir)
    os.makedirs(labels_tr_dir)

    # move the files to the new destination
    move_files(image_path, images_tr_dir)
    move_files(label_path, labels_tr_dir)

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
