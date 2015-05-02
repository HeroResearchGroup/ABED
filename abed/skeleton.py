"""
Functions for creating a skeleton config file

"""

from abed.utils import info, mkdir

def init_config():
    txt = """
###############################################################################
#                                General Settings                             #
###############################################################################
PROJECT_NAME = ''
TASK_FILE = './abed_tasks.txt'
RESULT_DIR = '/path/to/local/results/'
MAX_FILES_DIR = 1000

###############################################################################
#                          Server parameters and settings                     #
###############################################################################
REMOTE_NEEDS_INIT = True
REMOTE_USER = 'username'
REMOTE_HOST = 'address.of.host'
REMOTE_PATH = '/home/%s/projects/project_name' % REMOTE_USER
REMOTE_PORT = 22
REMOTE_SCRATCH = None
REMOTE_SCRATCH_ENV = 'TMPDIR'

###############################################################################
#                      Settings for Master/Worker program                     #
###############################################################################
MW_SENDATONCE = 100 # number of tasks (hashes!) to send at once
MW_COPY_SLEEP = 120

###############################################################################
#                      Experiment parameters and settings                     #
###############################################################################
TYPE = 'ASSESS'
DATADIR = 'datasets'
EXECDIR = 'execs'
DATASETS = ['dataset_1', 'dataset_2']
METHODS = ['method_1', 'method_2']
PARAMS = {
        'method_1': {
            'param_1': [val_1, val_2],
            'param_2': [val_3, val_4],
            'param_3': [val_5, val_6]
            },
        'method_2': {
            'param_1': [val_1, val_2, val_3],
            },
        }

COMMANDS = {
        'method_1': ("{execdir}/method_1 {datadir}/{dataset} {param_1} "
            "{param_2} {param_3}"),
        'method_2': "{execdir}/method_2 {datadir}/{dataset} {param_1}"
        }

METRICS = {
        'NAME_1': {
            'metric': metric_function_1,
            'higher_better': True
            },
        'NAME_2': {
            'metric': metric_function_2,
            'higher_better': False
            }
        }

###############################################################################
#                                PBS Settings                                 #
###############################################################################
PBS_NODES = 1
PBS_WALLTIME = 360
PBS_CPUTYPE = None
PBS_CORETYPE = None
PBS_PPN = None
PBS_MODULES = ['mpicopy', 'python/2.7.9']
PBS_EXPORTS = ['PATH=$PATH:/home/%s/.local/bin/abed' % REMOTE_USER]
PBS_MPICOPY = [DATADIR, EXECDIR, TASK_FILE]
PBS_TIME_REDUCE = 600

"""
    configfile = './abed_conf.py'
    with open(configfile, 'w') as fid:
        fid.write(txt)
    info("Wrote initial config to %s." % configfile)
    mkdir('datasets')
    mkdir('execs')
    info("Created 'datasets' and 'execs' directories")