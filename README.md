# Global Database of Basin Morphology

This project aims to perform an analysis of global rivers using the SRTM 30 dataset and the LSDTopoTools package. The code presented here could be adapted to other projects which require the bulk downloading and processing of SRTM data based on polygon areas of interest.

This workflow has been designed to run on the QMUL Apocrita supercomputer (which uses Univa Grid Engine as its scheduler) so some modification of the scripts will most likely be needed if this is to be run in a different environment.

## Requirements

- Python modules required to run scripts can be found within `requirements.txt`
- Data is accessed using the AWS CLI (v2), installation details can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- Topographic analysis is done using a [2018 release of LSDTopoTools](https://zenodo.org/record/1291889), patched with the files found in `LSD_code/`.
- The code uses the following modules on the QMUL HPC system:
  - gdal 2.3.1
  - gcc 6.3.0
  - python 3.6.3
  - proj 5.2.0

## Directory Structure

This section provides an overview of the files contained within this repository and how to use them.

#### `climate_zones/`

The files within this directory are generated using some of the preprocessing scripts. The initial input data, taken from [this paper](https://www.hydrol-earth-syst-sci.net/11/1633/2007/hess-11-1633-2007.html) is provided as a `geotiff`. This raster is split into a series shapefiles, which are subdivided until each climate sub zone is small enough to be processed in a sane amount of time and with a sane amount of memory. The final files which should be used are contained within `singlepart_files_split/`, the other folders contain intermediate data which is preserved for debugging purposes.

An additional folder, `singlepart_files_split_original/`, contains the climate zones prior to the lake processing step.

Full code is for these preprocessing steps can be found in https://zenodo.org/record/3257656.

#### `preprocessing/`

`srtm_filenames.lst` is the list of every SRTM 30 tile stored on the OpenTopography servers.

`parse_srtm_filenames.py` This script processes the list of SRTM tiles into a json file, `srtm_coords.json`, which stores the corner coordinates of each SRTM tile, keyed with the filename of the tile on the OpenTopography server.

`get_bbox.py` This script identifies the bounding box coordinates, the UTM zone and if the bottom left corner of the bounding box is in the Northern or Southern hemisphere for each shapefile generated using `quadpoly.py`. The results are stored in `../processing/bboxes.json`.

`get_dl_list.py` The final preprocessing script, this loads the bounding box of each shapefile from `../processing/bboxes.json` and calculates all of the SRTM tiles which intersect this bounding box. From this intersection a json containing a list of download urls, keyed by the climate sub zone name is written to `../processing/download_links.json`.

#### `processing/`

`get_urls.py` Simple command line script to return a list of the download urls for a given input climate sub zone filename.

`runner.sh` Main script which handles the download, merging, clipping and reprojection of the SRTM tiles, runs the file through the LSD code and postprocesses the outputs. Takes six input arguments:

```
$1 - shapefile name without .shp
$2 - utm zone
$3 - north or south
$4 - drainage threshold in pixels
$5 - min basin size in pixels
$6 - max basin size in pixels
```

`res_runner.sh` Script used to get the resolution data for each tile prior to the full analysis being run. Takes three input arguments:

```
$1 - shapefile name without .shp
$2 - utm zone
$3 - north or south
```

`build_array_params.py` Use this script to generate a file containing the matrix of parameters needed to deploy an array job. Takes 2 input arguments, the minimum and maximum number of SRTM tiles to be included in the job. This allows multiple array jobs to be created with different memory requirements.

`Array_{1..4}.sh` Example UGE job scripts used to deploy array job composed of multiple instances of `runner.sh`.

`Array_res.sh` Example UGE job script used to deploy array job to get the resolution data. Calls `res_runner.sh`.

`array_params_*.txt` Output parameter files generated by `build_array_params.py`.

`SRTM.driver` parameter file for the LSD code. Most other parameters can be ignored, as they are not used in this analysis.

`bboxes.json` JSON containing the bounding boxes of each climate zone tile.

`download_links.json` JSON containing the download links needed to build the topographic data for each climate zone tile.

`threshold_areas.json` JSON containing the basin min and max areas, and the channel extraction threshold for each climate zone tile, ensuring a consistent channel extraction threshold across all of the analysis.

#### `LSD_code/`

This project lightly modifies the LSDTopoTools `chi_mapping_tool.cpp` and `LSDChiTools.cpp` files to generate the required output data from the clipped SRTM tiles. These patches should be applied to this [2018 release of LSDTopoTools](https://zenodo.org/record/1291889), by copying these 2 files into the appropriate folders in the LSDTopoTools installation and making the driver file with the command: `make -f chi_mapping_tool.make`.

If you need guidance on getting started with LSDTopoTools, see [this user guide](http://lsdtopotools.github.io/LSDTT_book/).

#### `postprocessing/`

Following the execution of the LSD code, `export_rivers.py` is used to identify the longest river in each drainage basin and export it to its own `csv` file.

`secondary_analysis.py` Can be run with two command line arguments, to generate secondary statistics, including NCI for a folder full of river data files:

```
$ python secondary_analysis.py <output_filename> <path to folder of river files>
```

This file will contain the NCI value for each river, alongside its relief, flow length, overall gradient, Aridity index statistics, a straightness metric and a pit fill metric.

#### `lakes/`

We have used the [Global Lakes and Wetlands Database](https://www.worldwildlife.org/pages/global-lakes-and-wetlands-database) to clip out lakes from our topographic data, to ensure we are only analysing real channels. A paper describing the data can be found [here](https://www.sciencedirect.com/science/article/pii/S0022169404001404). We are only using the level 1 data, as the level 2 data is not at an appropriate resolution for this global study, details of this process can be seen in [this issue](https://github.com/sgrieve/gdbm/issues/2).

`clipper.py` is the code used to process the data downloaded from the above links into the appropriate format

#### `summary_figure/` and `zone_figure/`

Files used to generate some figures.

## Workflow

This section outlines the steps required to go from the Koppen climate zone raster to the final processed files, via a series of preprocessing steps, an automated processing workflow and some postprocessing.


#### 1. Climate Zone Processing

1. Download [Koppen Climate Zone dataset](https://www.hydrol-earth-syst-sci.net/11/1633/2007/hess-11-1633-2007.html)
1. `reclassify.py`
1. Use QGIS to convert reclassified raster to polygon
1. `multi_to_single.py`
1. `quadpoly.py`

#### 2. SRTM Tile Processing

1. Download SRTM filenames from OpenTopography: `aws s3 ls s3://raster/SRTM_GL1/ --recursive --endpoint-url https://opentopography.s3.sdsc.edu --no-sign-request`
1. `parse_srtm_filenames.py`
1. `get_bbox.py`
1. `get_dl_list.py`

#### 3. Resolution Adjustments

We need to get the data resolution for each climate zone tile, so that we can set a globally consistent set of channel extraction parameters.

1. Generate resolution job parameter file: `build_array_params_resolution.py`
1. Write job scripts for your HPC environment, reading in the parameter files generated by `build_array_params_resolution.py`. See the example for UGE: `array_res.sh`.
1. Dump all the JSON files generated in the previous step into a single directory, and run `area_thresholds.py` to generate the final JSON file needed to run the main HPC processing steps.

#### 4. HPC Processing

1. Generate job parameter file: `build_array_params.py`
1. Write job scripts for your HPC environment, reading in the parameter files generated by `build_array_params.py`. See the examples for UGE: `array_{1..4}.sh`.

#### 5. Postprocessing

1. Generate the summary statistics for each climate zone via `secondary_analysis.py`, which can be run as an HPC job using `secondary_job.sh`


## Naming Conventions

The Koppen climate zones are described by letter codes in the original paper. We have merged some of the similar zones to allow us to identify more general trends in the data to emerge.

This table contains the mappings between the letter codes used in the paper and our numerical codes.

|Letter Code| Classification | Code (original range)|
| --- | --- |---|
| Af | Tropical-Rainforest | 1 |
| Am | Tropical-Monsoon | 2 |
| Aw | Tropical-Savannah | 3 |
| BWh | Arid-Desert-Hot | 4 |
| BWk | Arid-Desert-Cold | 5 |
| BSh | Arid-Steppe-Hot | 6 |
| BSk | Arid-Steppe-Cold | 7 |
| Cs | Temperate-Dry summer | 8 (8, 9)|
| Cw | Temperate-Dry winter | 11 (11, 12, 13) |
| Cf | Temperate-Without dry season | 14 (14, 15, 16) |
| Ds | Cold-Dry summer | 17 (17, 18, 19, 20)|
| Dw | Cold-Dry Winter | 21 (21, 22, 23, 24) |
| Df | Cold-Without dry season | 25 (25, 26, 27, 28) |

As the climate zones are not contiguous, we need to be able to split each climate zone into a series of individual polygons, to achieve this, a sub zone ID is added to each climate zone so that the 5th polygon of zone 4 would be referred to as `4_5`. Note that no information is contained within these sub zone IDs, we cannot assume any spatial relationship between sub zones based on their numerical value.

In some cases the sub zones are still too big to be processed efficiently. These are further divided using a quadtree-like algorithm. In order to ensure files are never overwritten whilst running this recursive algorithm, the output subsets of a given climate sub zone are given an additional unique id: `4_5_a6a60415_78a8_4ed7_8f74_f9fbfceb09f5`. Again, these additional IDs confer no other information and serve solely to ensure the uniqueness of each climate sub zone.

## Raw data headers

```
row,col,lat,long,elevation,flow length,drainage area,basin key,flowdir,aridity index,pit flag
```
