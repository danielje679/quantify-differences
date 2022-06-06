# for generating features such as mean resolution, number of connected components per label, ..
from skimage.measure import label, regionprops
import numpy as np
import argparse
import SimpleITK as sitk
import os

# TODO reform functions with paths


def voxel_spacing(x_sitk):
    """Voxel spacing
    Parameters:
    x_sitk (SimpleITK.SimpleITK.Image): image
    Returns:
    lst(int): spacing
    """
    return [round(x_sp, 2) for x_sp in x_sitk.GetSpacing()]


def resolution(x):
    """Image resolution. The order is different depending on input type.
    Parameters:
    x_sitk (SimpleITK.SimpleITK.Image or numpy.ndarray): image
    Returns:
    tuple(int): resolution
    """
    if isinstance(x, np.ndarray):
        return np.shape(x)
    else:
        return x.GetSize()


def connected_components(y, connectivity=2):
    """Calculate the connected components of a label map.
    Parameters:
    y (numpy.ndarray): label map
    connectivity (int): maximum number of orthogonal hops to consider a
        pixel/voxel a neighbor (the smaller the 'connectivity' attribute, the
        more connected components).
    Returns:
    (numpy.ndarray, int): an array where each component is assigned a new label,
        ant the number of connected components
    """
    labeled_image, nr_components = label(y, return_num=True, connectivity=1)
    return labeled_image, nr_components

def main():
    # ARGUMENT PARSING
    parser = argparse.ArgumentParser(description='Retrieve statistics about the dataset')

    parser.add_argument('-p', '--path', type=str, help='path to the data', required=True)
    parser.add_argument('-v', '--voxel_spacing', type=bool, help='voxel spacing of the image')
    parser.add_argument('-r', '--resolution', type=bool, help='Image resolution of the image')
    parser.add_argument('-cc', '--conn_comp', type=bool, help='Connected components of the label map')

    args = parser.parse_args()

    image_path = args.path + "/imagesTr"
    label_path = args.path + "/labelsTr"

    # iterate over files and labels
    for filename in zip(os.listdir(image_path), os.listdir(label_path)):
        image_file = os.path.join(image_path, filename[0])
        label_file = os.path.join(label_path, filename[1])

        sitk_img = sitk.ReadImage(image_file)
        sitk_labels = sitk.ReadImage(label_file)
        labels = sitk.GetArrayFromImage(sitk_labels)

        print('Voxel Spacing: ', voxel_spacing(sitk_img), '\nResolution: ', resolution(sitk_img), '\nConnected Components: ', connected_components(labels))


if __name__ == '__main__':
    main()