import shutil
import glob, os
import random

list_folder = ['Form', 'Email', 'Memo', 'News', 'Note', 'Report', 'Resume', 'ADVE', 'Scientific', 'Letter']
for path_name in list_folder:
    print('currently in '+path_name)
    if not glob.glob("./" + path_name +"/*.jpg"):
        print('converting files...\n')
        # doesn't actually matter where I exec as long as correct path name
        # is passed into argv[1]
        os.system('python3 ./Form/convert.py '+path_name)
    print('does it get here??')
    if not os.path.isdir("./" + path_name +"/training"):
            print('creating testing and training directories...')
            os.mkdir("./" + path_name +"/training")
            os.mkdir("./" + path_name +"/testing")
    print('spliting training and testing data...')
    print(glob.glob("./" + path_name +"/*.jpg"))
    for filepath in glob.glob("./" + path_name +"/*.jpg"):
        val = random.random()
        if val >= 0.7:
            try:
                shutil.move(filepath, "./"+path_name+"/testing")
            except:
                continue
        else:
            try:
                shutil.move(filepath, "./"+path_name+"/training")
            except:
                continue
        


