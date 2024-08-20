"""
@File           : configs.py
@Time           : 8/20/2024 6:32 PM
@Author         : Gefei Kong
@Description    : as below
--------------------------------------------------------------
global configs
"""
import os
import yaml


class DotDict(dict):
    """Dictionary subclass that allows for dot notation access."""
    def __init__(self, *args, **kwargs):
        super(DotDict, self).__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = DotDict(value)

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{attr}'")

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, attr):
        try:
            del self[attr]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{attr}'")


def load_config(config_path:str):
    with open(config_path, "r+") as cfgf:
        cfg = yaml.safe_load(cfgf)

    # set result folders
    cfg = create_result_folders(cfg)
    cfg = DotDict(cfg)

    return cfg

def create_result_folders(cfg:dict):
    save_root_dir = cfg['save_root_dir']

    ############
    # set names of save_dirs of each step
    ############
    save_dirs = {}
    # step 1: slice
    save_dirs['s1_slice']  = os.path.join(save_root_dir,'slice')
    # step 2: DBSCAN
    slice_num, tree_max_height = cfg['param_slice']['slice_num'], cfg['param_slice']['tree_max_height']
    save_dirs['s2_dbscan'] = os.path.join(save_root_dir, "results",
                                   "numSlice{}_zMax{}".format(slice_num, tree_max_height))
    # step 3: RANSAC
    save_dirs['s3-6_ransac'] = save_dirs['s2_dbscan'] + "rans"
    # create save_dir for step 4:

    ############
    # create related dirs
    ############
    for k, v_dir in save_dirs.items():
        os.makedirs(v_dir, exist_ok=True)

    ############
    # add save_dirs to cfg
    ############
    cfg['save_dirs'] = save_dirs

    return cfg
