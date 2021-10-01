#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import gzip
import re
import shutil
import pandas as pd


def unzip_list(path, names):
    '''
    Descomprime todos los .gz del directorio especificado
    Parameters
    ----------
    path : str
        path donde se encuentran los archivos a descomprimir
    names: list
        lista con los files que se deben descomprimir
    
    Returns
    ---------
    bool
    '''
    for name in names:
        name = name.rsplit('/', 1)[-1]
        dir_ = path+name

        with gzip.open(dir_, 'rb') as f_in:
            size = 100000
            count = 0
            print('Descomprimiendo: ', dir_)
            for chunk in pd.read_csv(f_in, chunksize=size, low_memory=False):
                count = count + 1
                chunk.to_csv(dir_[:-7]+'_'+str(count)+'.csv', index=False)

        os.remove(dir_)
    
    return True


def create_paths():
    '''
    Renueva el directorio donde se descargan los files.
    Parameters
    ----------
    
    Returns
    ---------
    str
    '''
    folder = '../jsonReport/'
    try:
        shutil.rmtree(folder)
    except:
        pass
    if not os.path.exists(folder):
        os.makedirs(folder)

    return folder