import SimpleITK as sitk
import os


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
