# for generating features such as mean resolution, number of connected components per label, ..
from skimage.measure import label, regionprops
import numpy as np
import argparse
import SimpleITK as sitk
import os


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

    # TODO these arguments are currently not implemented
    parser.add_argument('-v', '--voxel_spacing', type=bool, help='voxel spacing of the image')
    parser.add_argument('-r', '--resolution', type=bool, help='Image resolution of the image')
    parser.add_argument('-cc', '--conn_comp', type=bool, help='Connected components of the label map')

    args = parser.parse_args()

    image_path = args.path + "/imagesTr"
    label_path = args.path + "/labelsTr"

    # iterate over files and labels
    ctr = 1
    voxel_spacing_list = []
    resolution_list = []
    connected_components_list = []
    for filename in zip(os.listdir(image_path), os.listdir(label_path)):
        if filename[0].endswith(".nii.gz"):
            print('Volume ', ctr)
            ctr += 1

            image_file = os.path.join(image_path, filename[0])
            label_file = os.path.join(label_path, filename[1])

            sitk_img = sitk.ReadImage(image_file)
            sitk_labels = sitk.ReadImage(label_file)
            labels = sitk.GetArrayFromImage(sitk_labels)

            voxel_spacing_list.append(voxel_spacing(sitk_img))
            resolution_list.append(resolution(sitk_img))
            connected_components_list.append(connected_components(labels)[1])

    voxel_spacing_mean, voxel_spacing_std = np.mean(voxel_spacing_list, axis=0), np.std(voxel_spacing_list, axis=0)
    resolution_mean, resolution_std = np.mean(resolution_list, axis=0), np.std(resolution_list, axis=0)
    connected_components_mean, connected_components_std = np.mean(connected_components_list), np.std(connected_components_list)
    print("Voxel Spacing - mean: ", voxel_spacing_mean, " - std: ", voxel_spacing_std)
    print("Resolution - mean: ", resolution_mean, " - std: ", resolution_std)
    print("Number of Connected Components - mean: ", connected_components_mean, " - std: ", connected_components_std)


if __name__ == '__main__':
    main()
