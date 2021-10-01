#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import os
import glob
import json


def PreProcess(path, filename):
    '''
    Lee todos los .csv del directorio y los convierte a .json
    Parameters
    ----------
    path : str
        path donde se encuentran los files descargados
    filename: list
        lista de path de files descargados

    Returns
    ---------
    bool
    '''
    paths = glob.glob(path+'*.csv')

    for file in paths:
        print('conviertiendo: ', file)
        matching = [s for s in filename if file[18:-6] in s]
        print(path, matching[0])
            
        df = pd.read_csv(file, low_memory=False)
        df = df.fillna('null')

        # #### ADD FOR DEV
        df['Date'] = df['lineItem/intervalUsageEnd']
        df['filename'] = matching[0]
        # ### REMOVE

        dic = df.to_dict(orient='records')
        id = file[18:-4]

        # Crea el .json donde se guarda la data particionada
        jsonfile = open(path+id+'.json', 'w')
        for row in dic:
            json.dump(row, jsonfile)
            jsonfile.write('\n')
    
        del df
        del dic
        os.remove(file)

    return True
