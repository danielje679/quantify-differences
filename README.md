# Quantify Differences of Datasets

## Data

### Overview of Medical Decathlon Structure

To make sure each dataset is structured in the same way and can be accessed easily, we have decided to adapt the structure of Medical Decathlon (http://medicaldecathlon.com/). Here the structure for each dataset is as follows:

```
dataset_1
│   dataset.json  
│
└───imagesTr
│      img1.nii.gz
│      img2.nii.gz 
│      ...
└───imagesTs
│      img1.nii.gz
│      img2.nii.gz 
│      ...  
└───labelsTr
       label1.nii.gz
       label2.nii.gz 
       ... 
```   

There is one ``dataset.json`` file with some information about the dataset, description, license, release data. It also contains information about the training and test data such as number of Samples, labels, as well as a list of image and label pairs.

The ``imagesTr``, ``imagesTs`` and ``labelsTr`` contain all training images, testing images and labels. Every image or label file is in the standard  NIFTI format (.nii.gz ending). In our conversions scripts, the sample images will get converted into NIFTI if the original dataset is not in NIFTI. The ``imagesTs`` directory can be empty, if the dataset does not provide any testing images.

### Transforming Datasets into Medical Decathlon Structure

To retrieve the medicaldecathlon structure of a dataset, run the corresponding `make_dataset.py` script in `src/data` directory. You will need to add the paths of the downloaded files as an argument to generate the structure. For instance, run the following command to generate the radiopaedia dataset in the medicaldecathlon structure.
Depending on the dataset, the ``--image_path`` option might not be needed. 

**1. Zenodo dataset**

This can be downloaded here: https://zenodo.org/record/3757476#.Xpz8OcgzZPY
```
python covid19/covid19ct_zenodo/make_dataset.py --image_path "path/to/images" --label_path "path/to/segmentation_masks"
```

**2. Radiopaedia**

This can be downloaded here: https://medicalsegmentation.com/covid19/.
Use the "Segmentation dataset no. 2 (13. April)", as the first dataset does not contain any full volumes.
```
python covid19/radiopaedia/make_dataset.py --image_path "path/to/images" --label_path "path/to/segmentation_masks"
```
**3. MosMed**

This can be downloaded here: https://mosmed.ai/en/datasets/covid191110/
```
python covid19/mosmed/make_dataset.py --image_path "path/to/images" --label_path "path/to/segmentation_masks"
```
**4. ImagEngLab**

This can be downloaded here: https://www.imagenglab.com/newsite/covid-19/. You need to download all of the 81 cases.

For this dataset, you do not need to specify the ``--image_path``option, as the labels can be downloaded together with the CT files.
```
python covid19/imagenglab/make_dataset.py --image_path "path/to/images"
```

## Features

### Extract features from dataset
To extract the features voxelspacing, resolution and number of connected components, run the following script

```
python src/features/extract_features.py -p path/to/dataset
```

This will print out the mean and standard deviation over all samples of the given dataset for each of the corresponding features.

:information_source: Make sure that your path points to the dataset that has already been transformed into the medical decathlon structure.

