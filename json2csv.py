import pandas as pd
import json
import os
import glob

TARGET_PATH = "/run/user/1000/gvfs/smb-share:server=10.50.1.4,share=datalakev1/04_RV_workspace/01_Tuna/testset_task/testset_v1/"

def convert_json_to_csv(filename, out):
    s = json.load(open(filename, 'r'))
    
    filename_base = s['imagePath']
    w = s['imageWidth']
    h = s['imageHeight']
    # w = 1360
    # h = 1024

    for ann in s['shapes']:
        label = ann['label']
        xmin = ann['points'][0][0]
        ymin = ann['points'][0][1]
        xmax = ann['points'][1][0]
        ymax = ann['points'][1][1]

        # reversed value check
        if(xmin>xmax): xmin,xmax=swap(xmin,xmax)
        if(ymin>ymax): ymin,ymax=swap(ymin,ymax)

        # check value validity
        if(xmax > w): 
            print(filename, "] out of bound xmax:",xmax)
            xmax = w
            # quit()
        if(ymax > h): 
            print(filename, "] out of bound ymax:",ymax) 
            ymax = h
            # quit()
        if(xmin < 0): 
            print(filename, "] out of bound xmin:",xmin)
            xmin = 0
            # quit()
        if(ymin < 0): 
            print(filename, "] out of bound ymin:",ymin) 
            ymin = 0
            # quit()

        out.write('{},{},{},{},{},{},{},{}\n'.format(
            filename_base, int(w), int(h), label, int(xmin), int(ymin), int(xmax), int(ymax)))

def swap(x,y):
    temp = x
    x = y
    y = temp
    return x, y

if __name__ == "__main__":
    # define save csv file
    out_file = TARGET_PATH + os.path.basename(os.path.normpath(TARGET_PATH))+ '.csv'
    out = open(out_file, 'w')
    out.write('filename,width,height,class,xmin,ymin,xmax,ymax\n')

    json_list = glob.glob(TARGET_PATH+"/*.json")
    print(len(json_list), "json files are globbed")

    # convert json to csv
    for filename in json_list:
        convert_json_to_csv(filename, out)

    out.close()
    print("done")
