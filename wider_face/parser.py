import re, os, cv2, json, shutil


def is_image_filename(inputstr):
    r = re.compile('.*\.jpg')
    m = r.match(inputstr)

    if m is not None:
        return True
    else:
        return False


def extract_bbx(inputstr):
    r = re.compile('(\d+)\ (\d+)\ (\d+)\ (\d+)\ (\d+)\ (\d+)\ (\d+)\ (\d+)\ (\d+)\ (\d+)')
    m = r.match(inputstr)

    if m is not None:
        x1 = int(m.group(1))
        y1 = int(m.group(2))
        w = int(m.group(3))
        h = int(m.group(4))

        

        x2 = x1 + w
        y2 = y1 + h
        
    
        return x1,y1,x2,y2
    else:
        raise Exception("bbx re match not found with line={}".format(inputstr))

def parse_one_image_label(fd, filenotfoundlist, outputdir):

    line = fd.readline()

    if line == "":
        return None

    if is_image_filename(line):
        filename = line

        if filename[-1] == '\n':
            filename = filename[:-1]

        # print("filename detected={}".format(filename))

        if not check_file_exists(filename):
            print("{} not found".format(filename))
            filenotfoundlist.append(filename)
            while True:
                line = fd.readline()
                

                if line == "":
                    return None


                if is_image_filename(line):
                    if check_file_exists(line):
                        filename = line
                        break
                    else:
                        filenotfoundlist.append(line)
        # print("found file={}".format(filename))
                    

        imgshape = get_image_size(filename)

        image_w = imgshape[1]
        image_h = imgshape[0]

        number_of_lines = int(fd.readline().strip())

        bbxlist=[]
        
        for i in range(number_of_lines):
            line = fd.readline()
            try:
                bbx = extract_bbx(line)
            except:
                print("error occured while processing filename={}".format(filename))
                raise Exception(filename)

            bbxlist.append(bbx)
        
        # print("filename={}".format(filename))
        # print(bbxlist)

        # crease json object
        jsonobj={}
        jsonobj['w'] = image_w
        jsonobj['h'] = image_h
        jsonobj['imgfile'] = filename
        
        rectlist = []
        for bbx in bbxlist:
            bbxobj = {}
            rectobj = {}
            rectobj['x1'] = bbx[0]
            rectobj['y1'] = bbx[1]
            rectobj['x2'] = bbx[2]
            rectobj['y2'] = bbx[3]
            bbxobj['rect'] = rectobj
            bbxobj['name'] = "face"
            rectlist.append(bbxobj)
        jsonobj['objects'] = rectlist

        # save in file
        filenamesplit = filename.split('/')
        filename = filenamesplit[1]
        labelfilename = "{}-label.json".format(filename)
        with open(labelfilename, 'w') as filew:
            json.dump(jsonobj, filew)
        
        # print("dump done")
        shutil.move(labelfilename,outputdir)


    else:
        raise Exception("expected image filename as input")
    
    return 1 # return anything but None

def get_image_size(filename):

    filedir = "/home/chadrick/Downloads/wider_face_dataset/WIDER_train/images"
    
    filepath = filedir + "/" + filename

    # print("filepath=", filepath)

    if not os.path.exists(filepath):
        raise Exception("cannot find {}".format(filename))
    else:
        img = cv2.imread(filepath)
        # print("img shape=", img.shape)
    
    return img.shape

def check_file_exists(filename):

    filedir = "/home/chadrick/Downloads/wider_face_dataset/WIDER_train/images"
    
    filepath = filedir + "/" + filename


    if os.path.exists(filepath):
        return True
    else:
        return False





def main():
    INPUTFILE = "wider_face_train_bbx_gt.txt"

    outputdir = "train_labels"

    if os.path.exists(outputdir):
        shutil.rmtree(outputdir)
    
    os.makedirs(outputdir)
    
    

    fd = open(INPUTFILE, 'r')

    isTest = False
    filenotfound_list = []
    exception_list=[]

    while True:
        try:
            ret = parse_one_image_label(fd, filenotfound_list, outputdir)
        except Exception as err:
            filename = str(err)
            print("err found in processing {}".format(filename))
            exception_list.append(filename)


        if ret is None:
            break
        
        if isTest:
            break
    
    print("filenotfound case count: {}".format(len(filenotfound_list)))

    print("end of code")





if __name__=="__main__":
    main()