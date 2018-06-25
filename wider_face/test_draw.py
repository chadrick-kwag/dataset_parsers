import os, cv2, random, json

def main():
    labeldir = "train_labels"
    imagedir = "/home/chadrick/Downloads/wider_face_dataset/WIDER_train/images"

    if not os.path.exists(labeldir):
        raise Exception("{} not found".format(labeldir))

    fileslist = os.listdir(labeldir)

    random.shuffle(fileslist)

    select_file = fileslist[0]
    select_filepath = os.path.join(labeldir, select_file)

    jsonobj = json.load(open(select_filepath, 'r'))

    imgfile = jsonobj['imgfile']

    imgfilepath = imagedir + "/" + imgfile
    
    if not os.path.exists(imgfilepath):
        print(imgfilepath)
        raise Exception("{} not found".format(imgfile))
    
    raw_img = cv2.imread(imgfilepath)

    objlist = jsonobj['objects']

    for obj in objlist:
        rect = obj['rect']

        x1 = rect['x1']
        y1 = rect['y1']
        x2 = rect['x2']
        y2 = rect['y2']

        cv2.rectangle(raw_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
    
    print("test draw: {}".format(select_file))
    cv2.imwrite("test_draw.png", raw_img)
    
    print("end of code")

        


    



if __name__ == "__main__":
    main()