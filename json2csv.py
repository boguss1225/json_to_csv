import pandas as pd
import json
import glob

TARGET_PATH = "label/float_bbox/TL1"

def convert_json_to_csv(filename, out):
    s = json.load(open(filename, 'r'))
    
    filename_base = s['imagePath']
    w = s['imageWidth']
    h = s['imageHeight']

    for ann in s['shapes']:
        label = ann['label']
        xmin = ann['points'][0][0]
        ymin = ann['points'][0][1]
        xmax = ann['points'][1][0]
        ymax = ann['points'][1][1]

        out.write('{},{},{},{},{},{},{},{}\n'.format(
            filename_base, w, h, label, xmin, ymin, xmax, ymax))

if __name__ == "__main__":
    # define save csv file
    out_file = TARGET_PATH + '.csv'
    out = open(out_file, 'w')
    out.write('filename,width,height,class,xmin,ymin,xmax,ymax\n')

    # convert json to csv
    for filename in glob.glob(TARGET_PATH+"/*.json"):
        convert_json_to_csv(filename, out)

    out.close()
    print("done")
