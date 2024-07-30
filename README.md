# ASD_Visualization
This repository can be used to plot Active Speaker Detections in videos if the detections are in the csv file format (for example, val_orig.csv) of the AVA-ActiveSpeaker dataset.

## Environment
This code has been tested with python 3.8. Please install the conda environment using the following commands

```
conda create -n asd_visualization python=3.8
conda activate asd_visualization
pip install -r requirements.txt --no-cache-dir
conda install conda-forge::ffmpeg
```