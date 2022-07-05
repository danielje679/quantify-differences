import SimpleITK as sitk
import os


def move_files(source_path, destination_path, only_nifti_files=True):
    """Moves files from one directory to another.
    :param source_path: source directory from which to move files
    :param destination_path: destination directory to move the files
    :param only_nifti_files: (default=True) if only .nii.gz files should be moved
    :param limit:
    """
    for filename in os.listdir(source_path):
        if only_nifti_files and not filename.endswith(".nii.gz"):
            continue

        source_file = os.path.join(source_path, filename)
        destination_file = os.path.join(destination_path, filename)

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
    img = sitk.ReadImage(img_path)
    sitk.WriteImage(img, new_img_path)
