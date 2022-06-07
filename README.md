# Quantify Differences

## Data

### Transform Data into medical decathlon structure
To retrieve the medicaldecathlon structure of a dataset, run the corresponding `make_dataset.py` script in `src/data` directory. You will need to add the paths of the downloaded files as an argument to generate the structure. For instance, run the following command to generate the radiopaedia dataset in the medicaldecathlon structure.
```
python covid19/radipaedia/make_dataset.py --image_path "path/to/images" --label_path "path/to/segmentation_masks"
```

## Features

### Extract features from dataset
To extract the features voxelspacing, resolution and number of connected components, run the following script
```
python src/features/extract_features.py -p path/to/dataset
```

:information_source: Make sure that your path points to the dataset that has already been transformed into the medical decathlon structure.

