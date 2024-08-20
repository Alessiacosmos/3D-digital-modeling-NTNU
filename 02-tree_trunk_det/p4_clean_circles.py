"""
@File           : p4_clean_circles.py
@Time           : 8/20/2024 8:00 PM
@Author         : Gefei Kong
@Description    : as below
--------------------------------------------------------------
clean RANSAC results to remove circles that are not trunks but others like fences.
"""
import argparse

import numpy as np
import pandas as pd
import os
import glob

from tqdm import tqdm


def main_clean_ransac(args, need_finding_file:list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
    ########
    # parse args
    ########
    print("[clean_ransac]::args:\n{}".format(args))

    rans_dir = args.ransac_dir
    save_dir = rans_dir

    # create save_dir is not exist
    os.makedirs(save_dir, exist_ok=True)

    # create result dataframe
    all_pcd = pd.DataFrame([], columns=['x', 'y', 'z', 'dbclass', 'c_x', 'c_y', 'r', 'class', 'err'])

    for i, f_idx in tqdm(enumerate(need_finding_file), total=len(need_finding_file), smoothing=0.9):
        ########
        # load ransac res
        ########
        filename = os.path.join(rans_dir, 'slice_{}_db_01_res.csv'.format(f_idx))
        pcd = pd.read_csv(filename)
        # print('columns: ', pcd.columns.values)

        # class_num = len(set(pcd['class'])) # class means the number (index) of potential trunks for each slice
        # print('class number: ', class_num)

        ##############################################################################
        # find tree trunk circle
        ##############################################################################
        # 1: tree trunk circle: radius < 2
        pcd_tt = pcd[pcd['r'] < 2]
        # class_num = len(set(pcd_tt['class']))
        # print('class number new (radius<2): ', class_num)


        # 2. tree trunk class:  point number >500
        pcd_tt_pn = pcd_tt['class'].value_counts()
        pcd_tt_pn = pcd_tt_pn.to_frame()
        thres = 500
        # if f_idx==3 or f_idx==4 or f_idx==5:
        if f_idx <= 5:
            thres = 50
        pcd_tt_pn_idx = pcd_tt_pn[pcd_tt_pn['class'] > thres].index
        pcd_tt = pcd_tt[pcd_tt['class'].isin(pcd_tt_pn_idx)]
        # class_num = len(set(pcd_tt['class']))
        # print('class number new (point number > 500): ', class_num)

        pcd_tt['class'] = pcd_tt['class'] + f_idx*10000
        # print('new class: ', pcd_tt['class'].unique())

        all_pcd = all_pcd.append(pcd_tt)
        # print(pcd_tt.shape, all_pcd.shape)

    all_pcd.to_csv(os.path.join(save_dir, 'slice_all_r2_p50_500.csv'), index=False)


def parse_args():
    """paramters"""
    parser = argparse.ArgumentParser("[tree trunk]::clean ransac circles")
    parser.add_argument("--ransac_dir", type=str, default="./Data/results/numSlice30_zMax20_rans",
                        help="the path for non-ground point clouds")

    return parser.parse_args()

if __name__=="__main__":
    args = parse_args()
    need_finding_file = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    main_clean_ransac(args, need_finding_file)

