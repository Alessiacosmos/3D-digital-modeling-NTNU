"""
@File           : main_wholeworkflow.py
@Time           : 8/20/2024 6:58 PM
@Author         : Gefei Kong
@Description    : as below
--------------------------------------------------------------

"""
import argparse

from utils import configs

from p1_slice_data import main_slice
from p2_dbscan import main_dbscan
from p3_ransac import main_ransac
from p4_clean_circles import main_clean_ransac
from p5_get_trunks_A import main_get_trunks_A
from p6_get_trunks_B import main_get_trunks_B



def get_args_each_step(cfg):
    save_dirs = cfg.save_dirs

    args_perstep = {
        '1': {'cloud_path': cfg.cloud_path, 'save_dir':save_dirs['s1_slice']},
        '2': {'slice_dir': save_dirs['s1_slice'], 'db_save_dir': save_dirs['s2_dbscan']},
        '3': {'dbscan_dir': save_dirs['s2_dbscan'], 'rans_save_dir': save_dirs['s3-6_ransac']},
        '4': {'ransac_dir': save_dirs['s3-6_ransac']},
        '5': {'ransac_dir': save_dirs['s3-6_ransac']},
        '6': {'ransac_dir': save_dirs['s3-6_ransac']}
    }

    args_perstep['1'].update(cfg['param_slice'])
    args_perstep['2'].update(cfg['param_dbscan'])
    args_perstep['3'].update(cfg['param_ransac'])
    args_perstep['4'].update(cfg['param_clean'])
    args_perstep['5'].update(cfg['param_dbscan_step5'])

    args_perstep = configs.DotDict(args_perstep)

    return args_perstep

def main(args):
    #########
    # load config
    #########
    cfg = configs.load_config(args.config_path)
    print(f"{cfg.save_root_dir = }")

    # #########
    # # get_args_each_step
    # #########
    args_perstep = get_args_each_step(cfg)
    print(F"{args_perstep = }")

    #########
    # get tree trunks by running workflow step-by-step
    #########
    # step 1: slice data by z values
    main_slice(args_perstep['1'])

    # step 2: DBSCAN to group points
    main_dbscan(args_perstep['2'])

    # step 3: RANSAC to get circles in each slice
    main_ransac(args_perstep['3'])

    # step 4: clean circles from RANSAC
    main_clean_ransac(args_perstep['4'], args_perstep['4']['need_finding_file'])

    # step 5: DBSCAN again to get the cluster of tree trunks
    main_get_trunks_A(args_perstep['5'])

    # step 6: get ultimate trunks by expanding the 3D bbox of preliminary trunks
    main_get_trunks_B(args_perstep['6'])

    print("done.")



def parse_args_mainw():
    """paramters"""
    parser = argparse.ArgumentParser("[tree trunk]::slice point cloud")
    parser.add_argument("--config_path", type=str, default="./configs/cfg_trunkdet.yml",
                        help="the path for config file")

    return parser.parse_args()

if __name__=="__main__":
    args = parse_args_mainw()
    main(args)