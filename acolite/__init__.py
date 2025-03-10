from acolite import landsat
from acolite import sentinel2
from acolite import sentinel3
from acolite import planet
from acolite import pleiades
from acolite import worldview
from acolite import venus

from acolite import chris
from acolite import prisma
from acolite import hico
from acolite import hyperion
from acolite import desis

from acolite import gf
from acolite import amazonia
from acolite import formosat
from acolite import ecostress

from acolite import ac
from acolite import aerlut
from acolite import output
from acolite import shared
from acolite import dem
from acolite import ged

from acolite import tact
from acolite import acolite
from acolite import adjacency

from acolite import gem
from acolite import parameters

## ignore numpy errors
import numpy as np
olderr = np.seterr(all='ignore')

import os, datetime
code_path = os.path.dirname(os.path.abspath(__file__))
path = os.path.dirname(code_path)

## find config file
if not os.path.exists('{}{}config'.format(path, os.path.sep)):
    ## check if binary distribution
    if '{}dist{}acolite'.format(os.path.sep,os.path.sep) in path:
        ## two levels for this file
        for i in range(2): path = os.path.split(path)[0]

cfile='{}{}config{}config.txt'.format(path,os.path.sep,os.path.sep)
config = shared.import_config(cfile)
config['code_path'] = code_path
config['path'] = path

## update version info
if 'version' in config:
    version = 'Generic Version {}'.format(config['version'])
else:
    version = 'Generic GitHub Clone'

    gitdir = '{}/.git'.format(path)
    gd = {}
    if os.path.exists(gitdir):
        gitfiles = os.listdir(gitdir)

        for f in ['ORIG_HEAD', 'FETCH_HEAD', 'HEAD']:
            gf = '{}/{}'.format(gitdir, f)
            if not os.path.exists(gf): continue
            st = os.stat(gf)
            dt = datetime.datetime.fromtimestamp(st.st_mtime)
            gd[f] = dt.isoformat()[0:19]

        version_long = ''
        if 'HEAD' in gd:
            version_long+='clone {}'.format(gd['HEAD'])
            version = 'Generic GitHub Clone c{}'.format(gd['HEAD'])
        if 'FETCH_HEAD' in gd:
            version_long+=' pull {}'.format(gd['FETCH_HEAD'])
            version = 'Generic GitHub Clone p{}'.format(gd['FETCH_HEAD'])

## run through config data
for t in config:
    ## set EARTHDATA credentials
    if t in ['EARTHDATA_u', 'EARTHDATA_p']:
        if (t not in os.environ) & (len(config[t]) > 0): os.environ[t] = config[t]
        continue
    ## split lists (currently only sensors)
    if ',' in config[t]:
        config[t] = config[t].split(',')
        continue

    ## test paths
    ## replace $ACDIR in config by ac.path
    if '$ACDIR' == config[t][0:6]:
        # os.path.join did not give the intended result on Windows
        config[t] = path + '/' + config[t].replace('$ACDIR', '')
        config[t] = config[t].replace('/', os.sep)

        ## make acolite dirs if they do not exist
        if not (os.path.exists(config[t])):
            os.makedirs(config[t])

    if (os.path.exists(config[t])):
        config[t] = os.path.abspath(config[t])

if 'verbosity' not in config: config['verbosity'] = 5

## read parameter scaling and settings
param = {'scaling':acolite.parameter_scaling()}
import json
with open(config['parameter_cf_attributes'], 'r', encoding='utf-8') as f:
    param['attributes'] = json.load(f)
