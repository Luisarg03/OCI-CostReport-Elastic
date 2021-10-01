#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.client import get_client
from modules.ElasticQuery import client, lastupdate
from modules.Unzip import create_paths, unzip_list
from modules.request import getfiles, RequestDownload
from modules.PandasProcess import PreProcess

from modules.ElasticQuery import insert ### Dev funtion


### Configuracion cliente OCI
config = '../OciConfig/config.prod'
account = 'NC'
ociclient = get_client(config, account)


### Configuracion cliente elastic
esclient = client()
print('\n clientes elastic: ', esclient)


### Variables para desarrollo
index = "oci-dev"
esclient = esclient['dev']


### Variables productivas
# index = "oci-nc"
# esclient = esclient['pro']


if __name__ == '__main__':
    ### Directorio de descargas
    path = create_paths()

    ### Obtengo la ultima actualizacion de los indices
    '''
    start -> str: Nombre de file desde donde empezar la descarga. ej: 1000000692115
    end -> str: Nombre de file donde terminar la descarga. ej: 1000000692115

    En ambos casos, los files que se especifiquen se excluyen de la lista de descarga.
    '''
    prefix = "reports/cost-csv"
    start_after = lastupdate(esclient, index)
    print('\n Ultimo file en Elastic: ', index, start_after)

    ### Obtengo el nombre completo del file desde donde iniciar la descarga...
    start_after = getfiles(ociclient['client'], ociclient['bucket'], start_after)
    print('\n Nombre del files en bucket:', 'start ->',start_after)

    ##############################
    ### Variables de reproceso ###
    # filename = '1000000692115.csv.gz'
    # prefix = getfiles(ociclient['client'], ociclient['bucket'], filename)
    # start_after = None
    # print('\n Reprocesado de files en bucket:', 'file ->',prefix)
    ##############################


    ## Descarga de los nuevos files
    list_files = RequestDownload(
        ociclient['client'],
        ociclient['bucket'],
        prefix,
        start_after,
        path
        )


    unzip_list(path, list_files)
    PreProcess(path, list_files)

    ### Desa funcion
    insert(path, esclient, index)
