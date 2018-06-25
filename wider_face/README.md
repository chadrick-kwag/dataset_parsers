# converter for wider face dataset

## usage
1. place the python files to the dir where the user has unzipped annotations zip file.
2. adjust the paths to wider face image dirs and target label file to parse and convert in `parser.py` file

## check conversion
`test_draw.py` is to check if the converted files actually correspond to ground truth bounding boxes. It will randomly select a converted `.json` file and draw the bbx info inside the json file to the actual image and save this image output.

Please adjust the image dir and `.json` file stored directory before use.


