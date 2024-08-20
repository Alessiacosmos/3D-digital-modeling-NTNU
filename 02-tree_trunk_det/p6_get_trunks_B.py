"""
@File           : p6_get_trunks_B.py
@Time           : 8/20/2024 8:40 PM
@Author         : Gefei Kong
@Description    : as below
--------------------------------------------------------------
get final trunks by expanding the 3D bbox to [min_z, max_z]
"""
import argparse

import numpy as np
import pandas as pd
import os



def main_get_trunks_B(args):
    ########
    # parse args
    ########
    print("[get trunks (B)]::args:\n{}".format(args))

    rans_dir = args.ransac_dir
    save_dir = rans_dir

    # create save_dir is not exist
    os.makedirs(save_dir, exist_ok=True)

    ########
    # load clean_circle res
    ########
    filename = os.path.join(rans_dir, 'slice_all_r2_p50_500_newclass.csv')

    pcd = pd.read_csv(filename)
    class_num = len(set(pcd['newclass']))
    print('[get trunks (B)]::trunk number: ', class_num)

    ########
    # expand the 3D bbox of each trunk to [min_z, max_z]
    ########
    # get 3D bbox
    # get the center_x, center_y. height and width of every new class
    pcd_group = pcd.groupby('newclass')
    g_x = pcd_group['x'].agg(['max', 'min'])
    g_y = pcd_group['y'].agg(['max', 'min'])
    g_z = pcd_group['z'].agg(['max', 'min'])

    new_col = list(pcd.columns.values)
    new_col = new_col.append('finclass')
    pcd_output = pd.DataFrame([], columns=new_col)

    g_z_new = [g_z['max'].max(), g_z['min'].min()]
    for idx in range(0, class_num-1):
        x_gi = [g_x.loc[idx, 'max']+0.2, g_x.loc[idx, 'min']-0.2]
        y_gi = [g_y.loc[idx, 'max']+0.2, g_y.loc[idx, 'min']-0.2]

        # xy_ratio = (np.abs(y_gi[0]-y_gi[1]) / np.abs(x_gi[0]-x_gi[1]) )
        # print(xy_ratio)
        # if xy_ratio<1:
        #     continue
        pcd_gi = pcd[(pcd['x']<=x_gi[0])&(pcd['x']>=x_gi[1])&
                     (pcd['y']<=y_gi[0])&(pcd['y']>=y_gi[1])&
                     (pcd['z']<=g_z_new[0])&(pcd['z']>=g_z_new[1])]

        pcd_gi.loc[:,'finclass'] = idx
        pcd_output = pcd_output.append(pcd_gi)


    pcd_output.to_csv(filename.replace('.csv', '_finclass.csv'), index=False)


def parse_args():
    """paramters"""
    parser = argparse.ArgumentParser("[tree trunk]::dbscan AGAIN to find trunks")
    parser.add_argument("--ransac_dir", type=str, default="./Data/results/numSlice30_zMax20_rans",
                        help="the path for non-ground point clouds")

    return parser.parse_args()

if __name__=="__main__":
    args = parse_args()
    main_get_trunks_B(args)

