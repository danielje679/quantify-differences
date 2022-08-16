# Generate the dataset /data/covid19/04_imagenglab in medical decathlon format

import argparse
import os
import pathlib
import json
import inspect
import numpy as np
import SimpleITK as sitk
#import data as utils



def move_images(img_paths, destination_path):
    """
    :param img_paths: list of exact paths of the images to be moved
    :param destination_path: the destination dir
    :return:
    """
    idx = 1
    for source_file in img_paths:
        filename = os.path.basename(source_file)

        # new name with id
        split_1 = os.path.splitext(filename)
        split_2 = os.path.splitext(split_1[0])
        new_name = split_2[0] + str(idx) + split_2[1] + split_1[1]
        idx += 1

        destination_file = os.path.join(destination_path, new_name)
        os.replace(source_file, destination_file)

def nrrd_to_nifti(img_path, dest=None):
    """ Converts a nrrd file to a nifti file and stores it in the same location or destination location if specified
    :param img_path: path to the image
    :param dest:  path where the file should be stored. If not given, this is the same is the given image path
    :return:
    """
    new_img_path = os.path.splitext(img_path)[0] + ".nii.gz"
    if dest is not None:
        new_img_path = dest
    print(new_img_path)
    print(img_path)
    img = sitk.ReadImage(img_path)
    sitk.WriteImage(img, new_img_path)


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
        "name": "ImagEngLab",
        "description": "Automatically segmentated  Covid19 regions of interest",
        "reference": "Zaffino, Paolo and Marzullo, Aldo and Moccia, Sara and Calimeri, Francesco and De Momi, Elena and Bertucci, Bernardo and Arcuri, Pier Paolo and Spadea, Maria Francesca, An Open-Source COVID-19 CT Dataset with Automatic Lung Tissue Classification for Radiomics ",
        "licence": "CC BY-NC 4.0",
        "release": "14/09/2021",
        "modality": {
            "0": "CT"
        },
        "labels": {
            "0": "air",
            "1": "healthy lung",
            "2": "ground glass opacities",
            "3": "consolidition",
            "4": "other dense tissue"
        },
        "numTraining": num_tr,
        "numTest": num_ts,
        "training": tr_label_paths,
        "test": ts_paths
    }

    #  store the json file
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)


def create_medical_decathlon_structure(image_path):
    """
    :param image_path: path of the downloaded image files from mosmed
    :param label_path: path of the downloaded labels from mosmed
    """
    cwd = os.path.abspath(inspect.getsourcefile(lambda: 0))
    root = pathlib.PurePath(cwd).parents[4]

    # destination paths
    relative_destination = "data/04_imagenglab"
    images_tr_dir = os.path.join(root, relative_destination, "imagesTr")
    images_ts_dir = os.path.join(root, relative_destination, "imagesTs")
    labels_tr_dir = os.path.join(root, relative_destination, "labelsTr")

    # create new directories
    os.makedirs(images_tr_dir)
    os.makedirs(images_ts_dir)
    os.makedirs(labels_tr_dir)

    img_paths = []
    label_paths = []
    nifti_img_paths = []
    nifti_label_paths = []

    # move the files to the new destination
    for i in range(11, 82, 10):
        patient_ids = np.arange(i - 10, i)
        if i > 80:
            patient_ids = np.arange(i - 10, i+1)
        dir_1 = "patients_" + str(patient_ids[0]) + "-" + str(patient_ids[-1])
        for patient_id in patient_ids:
            dir_2 = str(patient_id)
            filename = "CT.nrrd"
            nifti_filename = "CT.nii.gz"
            labelname = "GMM_LABELS.nrrd"
            nifti_labelname = "GMM_LABELS.nii.gz"

            file_path = os.path.join(image_path, dir_1, dir_2, filename)
            label_path = os.path.join(image_path, dir_1, dir_2, labelname)
            nifti_file_path = os.path.join(image_path, dir_1, dir_2, nifti_filename)
            nifti_label_path = os.path.join(image_path, dir_1, dir_2, nifti_labelname)

            img_paths.append(file_path)
            label_paths.append(label_path)
            nifti_img_paths.append(nifti_file_path)
            nifti_label_paths.append(nifti_label_path)

    # conversion to nifti
    for i in img_paths:
        nrrd_to_nifti(i)

    for l in label_paths:
        nrrd_to_nifti(l)

    move_images(nifti_img_paths, images_tr_dir)
    move_images(nifti_label_paths, labels_tr_dir)

    # create the dataset.json file
    create_json(os.path.join(root, relative_destination))


def main():
    # ARGUMENT PARSING
    parser = argparse.ArgumentParser(description='Retrieve statistics about the dataset')

    parser.add_argument('-ip', '--image_path', type=str, help='path to the image data', required=True)

    args = parser.parse_args()

    create_medical_decathlon_structure(args.image_path)


if __name__ == '__main__':
    main()
