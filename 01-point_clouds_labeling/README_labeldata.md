# Assignment 01: Point Clouds Labeling
Label point clouds by CloudCompare for data preparation for 3D segmentation task.

## Software
1. [CloudCompare](https://www.danielgm.net/cc/)
2. (Optional) [QGIS](https://www.qgis.org/) or [ArcGIS (Pro)](https://www.esri.com/en-us/arcgis/products/arcgis-pro/overview?srsltid=AfmBOor314a-hTZeIX6diXq_sYR3lMnkMjCa82ZZIHWk3zrQvkcig1bd) (through NTNU software center)

## 2. Workflow
### 2.1 Data preparation
1. Find the tile you need to label through the file [data arrangement.xlsx](https://studntnu-my.sharepoint.com/:x:/g/personal/gefeik_ntnu_no/EUogwVPFy1xEm4JadvBxQRABZ8ntcYeu-DoARDvZsycjQA?e=YzK0az)  
   **To protect your person private, the `data_arrangement.xlsx` file is shared through NTNU onedrive and only people in NTNU have access to this file. For the students who can't download this file, get the share from your classmates or send email to Gefei.*
2. Get the corresponding point cloud data for this tile through the following way:
   - Visit [Green room](https://link.mazemap.com/Pah28i1x) neighbored the classroom L11;
   - Find device NTNU00743 & Login to your NTNUaccount;
   - Find the data at the path *F:\3DDigitalModelling2024\A01_datas\data* ; 
   - Copy it to your own devices.  
3. Get the metadata for the point clouds (to idenfity where your tile is):
   - You can find it by the same way of step 2;
   - The path for the metadata is: *F:\3DDigitalModelling2024\A01_datas\metadata* . 

### 2.2 Labeling
The labeling workflow is provided by video tutorials as following links:
#### Public video(s)
1. [Reference video #1 (before 07:10)](https://www.youtube.com/watch?v=B61WNd7R_w4)

#### The video tutorials specifically for TBA4256  
(limited by NTNU settings, their links will expires Sunday, Sep 25, 2024. 
If you miss the download time, just let Gefei know and she will update them.)
1. [Labeling data](https://studntnu-my.sharepoint.com/:v:/g/personal/gefeik_ntnu_no/EXV4PNuUrMZIojDIbr6L38QBurgp2KtLI_qtiaAnyPLc_A?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=WltjLS)
2. [Identify point cloud class with the assistance of orthophotos](https://studntnu-my.sharepoint.com/:v:/g/personal/gefeik_ntnu_no/EaIvGhdVZhNHqdCuc1TSwJ8B1f7d4dqGBdyw6qlqjjRfGg?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=zRCDfy)


#### The attached files mentioned in the video tutorials
1. [Annotation (label) list](./Annotation%20list.txt)
2. [Wms server link for Trondheim orthophotos](https://wms.geonorge.no/skwms1/wms.nib-prosjekter)
3. The way to find metadata that shows tile locations can be found through [2.1 Data preparation](#21-data-preparation)

### 2.3 Submit your result
1. Submit reports in Blackboard/Inspera (will open later, updated on 27th, Sep. 2024).
2. Submit your labelling result to Green room's desktop NTNU00743 (where you get your data).
   1. Submission folder: *F:\3DDigitalModelling2024\A01_datas\label_results*
   2. Detailed filename: the original tilename. e.g. 32-1-510-212-67
   
   E.g. your result should be saved as: F:\3DDigitalModelling2024\A01_datas\label_results\32-1-510-212-67.las(.laz)

#### What should be in your report?
1. The description of the data you’re on duty
2. The description of the workflow labeling data.
3. Qualitative evaluation results: compare orthophoto and your label result, and show several examples.
