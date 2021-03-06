"""
Functions for managing tasks

"""

import os
import sys
import random

from itertools import izip, product

from abed.conf import settings
from abed.exceptions import (AbedHashCollissionException, 
        AbedExperimentTypeException)
from abed.results.walk import walk_hashes
from abed.utils import error

def cartesian(params):
    return (dict(izip(params, x)) for x in product(*params.itervalues()))

def check_size():
    if not sys.maxsize == 9223372036854775807:
        error("Running on a non 64-bit system. This may cause problems with "
                "hashes.")
        raise SystemExit

def task_hash(task):
    """
    This yields a hash of a list by combining the hashes of all list elements.
    """
    hsh = hash(frozenset(task.items()))
    hsh %= ((sys.maxsize + 1) * 2)
    return hsh

def init_tasks():
    if settings.TYPE == 'ASSESS':
        return init_tasks_assess()
    elif settings.TYPE == 'CV_TT':
        return init_tasks_cv_tt()
    elif settings.TYPE == 'RAW':
        return init_tasks_raw()
    raise AbedExperimentTypeException

def init_tasks_assess():
    out = {}
    for dset in settings.DATASETS:
        for method in settings.METHODS:
            for prmset in cartesian(settings.PARAMS[method]):
                task = {key: value for key, value in prmset.iteritems()}
                task['dataset'] = dset
                task['method'] = method
                hsh = task_hash(task)
                if hsh in out:
                    raise AbedHashCollissionException
                out[hsh] = task
    return out

def init_tasks_cv_tt():
    out = {}
    rng = random.Random(x=settings.CV_BASESEED)
    for train, test in settings.DATASETS:
        seed = rng.randint(0, 2**31-1)
        for method in settings.METHODS:
            for prmset in cartesian(settings.PARAMS[method]):
                task = {key: value for key, value in prmset.iteritems()}
                task['train_dataset'] = train
                task['test_dataset'] = test
                task['method'] = method
                task['cv_seed'] = seed
                hsh = task_hash(task)
                if hsh in out:
                    raise AbedHashCollissionException
                out[hsh] = task
    return out

def init_tasks_raw():
    out = {}
    with open(settings.RAW_CMD_FILE, 'r') as fid:
        tasks = [x.strip() for x in fid.readlines()]
    for txttask in tasks:
        hsh = hash(txttask)
        hsh %= ((sys.maxsize + 1) * 2)
        if hsh in out:
            raise AbedHashCollissionException
        out[hsh] = txttask
    return out

def read_tasks():
    with open(settings.TASK_FILE, 'r') as fid:
        tasks = fid.readlines()
    tasks = [x.strip() for x in tasks]
    tasks = map(int, tasks)
    grid = init_tasks()
    out = {}
    for key in tasks:
        out[key] = grid[key]
    return out

def update_tasks(tasks):
    delcnt = 0
    if not os.path.exists(settings.RESULT_DIR):
        return 0
    for hsh in walk_hashes():
        try:
            del tasks[int(hsh)]
            delcnt += 1
        except KeyError:
            pass
    return delcnt

def explain_tasks(all_tasks):
    for task in sorted(all_tasks.keys()):
        if settings.TYPE == 'RAW':
            cmd = all_tasks[task]
        else:
            d = {k:v for k, v in all_tasks[task].iteritems()}
            command = settings.COMMANDS[d['method']]
            d['datadir'] = '{datadir}'
            d['execdir'] = '{execdir}'
            cmd = command.format(**d)
        print('%s : %s' % (task, cmd))
