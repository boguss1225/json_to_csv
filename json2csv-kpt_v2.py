import pandas as pd
import json
import glob

TARGET_PATH = "/home/hemyo/Downloads/OneDrive_2024-04-17/01_EU-MLT-0017-MFF (done)"

def convert_json_to_csv(filename, out):
    s = json.load(open(filename, 'r'))

    filename_base = s['imagePath']

    # write: fname, class, bbox_x1, bbox_y1, bbox_x2, bbox_y2
    out.write('{},0, 0, 0, 999, 999'.format(filename_base))
    
    for ann in s['shapes']:
        label = ann['label']
        x = ann['points'][0][0]
        y = ann['points'][0][1]
        out.write(',{},{},1'.format(int(x), int(y)))
    out.write('\n')

if __name__ == "__main__":
    # define save csv file
    out_file = TARGET_PATH + '.csv'
    out = open(out_file, 'w')
    
    csv_head = 'fname,class,bbox_x1,bbox_y1,bbox_x2,bbox_y2,\
                nose_x,nose_y,nose_visibility,\
                eye_x,eye_y,eye_visibility,\
                midfin_x,midfin_y,midfin_visibility,\
                bellyfin_x,bellyfin_y,bellyfin_visibility,\
                backfin_x,backfin_y,backfin_visibility,\
                tailtip_x,tailtip_y,tailtip_visibility,\
                tailtip_x,tailtip_y,tailtip_visibility,\
                tail_x,tail_y,tail_visibility'
    out.write(csv_head)

    json_list = glob.glob(TARGET_PATH+"/*.json")
    print(len(json_list), "json files are globbed")

    # convert json to csv
    for filename in json_list:
        convert_json_to_csv(filename, out)

    out.close()
    print("done")
