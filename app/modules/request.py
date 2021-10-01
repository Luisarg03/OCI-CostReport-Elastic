#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd


def getfiles(client, bucket, file):
    last = None
    list_data = []

    try:

        while True:
            namespace = 'bling'
            prefix = "reports/cost-csv"
            report_bucket_objects = client.list_objects(namespace_name=namespace,
                                                        bucket_name=bucket,
                                                        prefix=prefix,
                                                        start_after=last)

            for o in report_bucket_objects.data.objects:
                list_data.append({'name': o.name, 'size': o.size, 'time_created': o.time_created})

            if len(report_bucket_objects.data.objects) == 0:
                break
            else:
                df = pd.DataFrame(list_data)
                last = df.name.tail(1).values[0]

        if file is not None:
            matching = [s for s in df.name if file in s]
            value = df.loc[df.name == matching[0]]
            value = value.name
            for i in value:
                value = i
        else:
            value = None

    except:
        value = None

    return value


def RequestDownload(client, bucket, prefix, start_after, path):
    '''
    Descarga los files de costos desde OCI 
    Parameters
    ----------
    client : oci obj
        obj con la configuracion de OCI
    bucket: str
        nombre del bucket
    start: str
        nombre de file desde donde empezar las descargas (excluye)
    end: str
        nombre de file donde finalizar las descargas (excluye)
    path: str
        directorio donde se guardaran las descargas
    Returns
    ---------
    list
    '''
    namespace = 'bling'
    report_bucket_objects = client.list_objects(namespace_name=namespace,
                                                bucket_name=bucket,
                                                prefix=prefix,
                                                start_after=start_after)

    list_name = []
    for i in report_bucket_objects.data.objects:
        filename = i.name
        object_details = client.get_object(namespace_name=namespace,
                                           bucket_name=bucket,
                                           object_name=i.name)

        print('Descargando desde: ', filename)
        with open(path+filename.rsplit('/', 1)[-1], 'wb') as f:
            for chunk in object_details.data.raw.stream(2048 ** 2, decode_content=False):
                f.write(chunk)
        
        list_name.append(filename)

    return list_name