import pandas as pd
import json
import os
import glob
import cv2

BASE_PATH = "/media/hemyo/New Volume/huon_am100/cropped_fish/tuna_whole(done)/"
TARGET_PATH = BASE_PATH + "json/"
IMAGE_PATH = BASE_PATH + "images/"
LABEL_LIST = ["nose", "tail"]

def convert_json_to_csv(filename, out):
    s = json.load(open(filename, 'r'))

    filename_base = s['imagePath']
    filepath = os.path.join(IMAGE_PATH,filename_base)
    im = cv2.imread(filepath)
    h,w,c = im.shape
    # write: fname, class, bbox_x1, bbox_y1, bbox_x2, bbox_y2
    out.write(f'{filename_base},0,0,0,{w},{h}')
        
    for ann in s['shapes']:
        label = str(ann['label'])
        x = int(ann['points'][0][0])
        y = int(ann['points'][0][1])

        if not label in LABEL_LIST : 
            print("the label isn't valid", label)
            return True
        if label == "nose": 
            nose_x = x
            nose_y = y
        if label == "tail":
            tail_x = x
            tail_y = y
        
    out.write(',{},{},1,{},{},1'.format(nose_x, nose_y, tail_x, tail_y))
    out.write('\n')

    return 0

if __name__ == "__main__":
    # define save csv file
    out_file = BASE_PATH + 'salmon_kpt_v1.csv'
    out = open(out_file, 'w')
    out.write('fname,class,bbox_x1,bbox_y1,bbox_x2,bbox_y2,nose_x,nose_y,nose_visibility,tail_x,tail_y,tail_visibility\n')

    json_list = glob.glob(TARGET_PATH+"/*.json")
    print(len(json_list), "json files are globbed")

    # convert json to csv
    for filename in json_list:
        has_label_error = convert_json_to_csv(filename, out)
        if has_label_error : break

    out.close()
    print("[done] saved at:",out_file)
