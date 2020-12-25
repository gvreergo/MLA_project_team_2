from PIL import Image
from PIL import ImageOps
import os
from skimage.transform import resize
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_pic_from_directory(DB ,path , label , im_size ):
    """ DB : pandas.DataFrame
        path : str
        label : str
        im_size : np.array[int]
        _ _ _ _ _ _ _ _ _
        returns DB
    get every pictures from "path" directory, grayscale,  resize to "im_size" and add them to DB with label "label" """
    dirs = os.listdir(path)
    dirs = dirs[:1] # limited in order to speed up testing

    for filename in dirs :
        temp_path = path+'\\'+filename
        #img treatment
        im=Image.open(temp_path , mode = 'r')
        #formatting
        im = ImageOps.grayscale(im) #to grayscale
        im = np.array (im) #to np.array
        im = resize(im, (im_size[0] , im_size[1]), anti_aliasing=True) #resize to size 256*256
        #print(im.shape)
        # data normalisation
        #im /= 255.0
        new_row = pd.DataFrame ([filename ,  label ,  im ]).transpose()
        #print (new_row)
        DB = pd.concat([DB , new_row ], ignore_index = True , axis = 0  )
    print(path + " done")

    return DB

def create_DB(path ,  label , save_path ,im_size):
    """
    path : array[string]
    label : array[string]
    save_path : str
    im_size : array[int]
    returns a dataframe of every picture in the repository given in "path" labelled as "label"
    /!\/!\/!\/!\/!\/!\data in path[i] wil be labelled with label[i]/!\/!\/!\/!\ """
    #init values
    DB = pd.DataFrame()
    length = len(path)
    for i in range(length):
        DB = get_pic_from_directory( DB = DB , path = path[i] , label = label[i] , im_size = im_size )
    DB.to_csv( path_or_buf = save_path )#, index=True , index_label = [label_1 , label_2] )
    DB.columns = ['filename' , 'label' , 'xray']
    print(DB)
    return DB



if __name__ == "__main__" :
    path_1 , label_1 = "..\database\covid" , "covided"  # covid-much
    path_2 , label_2 = "..\database\\normal" , "healthy"   # covid-free
    path = [path_1 , path_2]
    label = [label_1 , label_2]
    save_path =  "DB.csv"
    im_size = [256,256]
    DB = create_DB(path , label , save_path , im_size )
    #del DB[0]
    #print(DB.keys())
    #print(DB.xray[:])
