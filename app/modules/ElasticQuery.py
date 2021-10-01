#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import json
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch.helpers import bulk


def client():
    '''
    Configuracion del cliente para la cuenta Elastic
    Parameters
    ----------

    Returns
    ---------
    dict
    '''
    try:
        proes = Elasticsearch(
            host=["rgioddbprd57455.dtvpan.com","rgioddbprd57456.dtvpan.com","rgioddbprd57457.dtvpan.com"],
            port=9200,
            http_auth=("logstash", "logstash"),
            use_ssl=True
        )
    except:
        proes = None

    try:
        deves = Elasticsearch(
        host="localhost",
        port=9200,
        http_auth=None,
        use_ssl=False
        )
    except:
        deves = None

    _dict = {'pro': proes, 'dev': deves}

    return _dict


def lastupdate(client, index):
    '''
    Configuracion del cliente para la cuenta Elastic
    Parameters
    ----------
    client : elasticsearch obj
        obj con la configuracion de elasticsearch
    index: str
        indice elastic desde donde consumir los datos

    Returns
    ---------
    str
    '''
    try:
        s = Search(using=client, index=index) \
        .sort({ "Date": "desc"}) \
        .extra(size=1)

        response = s.execute()
        for hit in response:
            filename = hit.filename
    except:
        filename = None

    return filename


def insert(path, client, index):
    '''
    Funcion para desarrollo ....
    Bulk insert elastic
    
    Parameters
    ----------

    Returns
    ---------
    bool
    '''
    files = glob.glob(path+'*.json')
    files = sorted(files)

    for file in files:
        print('\n Elastic insert desde: ', file)
        df = pd.read_json(file, lines=True)
        df = df[['filename', 'lineItem/intervalUsageEnd', 'product/service']]
        df = json.loads(df.to_json(orient='records'))
        print('Numero de registros que se trataran de insertar en', index, ':',len(df))

        actions = [
            {
                "_index": index,
                "_source":i,
            }
                for i in df
            ]

        bulk(client, actions)

    return True