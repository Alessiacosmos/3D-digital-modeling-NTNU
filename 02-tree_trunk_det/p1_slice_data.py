"""
@File           : p1_slice_data.py
@Time           : 8/20/2024 5:53 PM
@Author         : Gefei Kong
@Description    : as below
--------------------------------------------------------------

"""
import os
import argparse

import open3d as o3d
import numpy as np
import pandas as pd

from pyntcloud import PyntCloud
from tqdm import tqdm


def main_slice(args):
    ########
    # parse args
    ########
    print("[slice_data]::args:\n{}".format(args))

    pcd_name        = args.cloud_path
    tree_max_height = args.tree_max_height
    slice_num       = args.slice_num
    save_dir        = args.save_dir

    # create save_dir is not exist
    os.makedirs(save_dir, exist_ok=True)


    ########
    # 1. read data
    ########
    pcd = o3d.io.read_point_cloud(pcd_name)
    point_pcd = np.asarray(pcd.points)
    print('[slice_data]::cloud shape:=================', point_pcd.shape)

    ########
    # 2. convert to pyntcloud -> pandas.dataframe
    ########
    """x       y       z  red  green  blue"""
    pcd_pynt = PyntCloud.from_instance('open3d', pcd)
    # print(pcd_pynt.points.head())

    # sort
    pcd_pynt_sort = pcd_pynt.points.sort_values(by=['z'])
    print("[slice_data]::the example of input clouds:=================\n",pcd_pynt_sort.head())

    ########
    # 3. rm the points with extreme z values
    # the points whose z values >=200 or <=-200 are removed.
    ########
    pcd_pynt_sort_2 = pcd_pynt_sort[(pcd_pynt_sort['z']<330)&(pcd_pynt_sort['y']>-200)]
    print('[slice_data]:: z  min and z max (after filtering): ', pcd_pynt_sort_2['z'].min(), pcd_pynt_sort_2['z'].max())

    ########
    # slice them based on z value
    ########
    print('[slice_data]::slicing...=================')
    ## 1. limite the point clouds to the range [min_z, tree_max_height], where tree_max_height is defined by users.
    pcd_pynt_sort_2 = pcd_pynt_sort_2[pcd_pynt_sort_2['z']<tree_max_height]
    ## 2. get every slice's ranges
    z_diff = (pcd_pynt_sort_2['z'].max() - pcd_pynt_sort_2['z'].min()) / slice_num
    slice_lim = [pcd_pynt_sort_2['z'].min() + z_diff*i for i in range(slice_num+1)] # np.arange(pcd_pynt_sort['z'].min(), pcd)
    slice_lim[-1] +=0.1
    print('[slice_data]:: final z max: {}; z min: {}; slice_num: {}\n slice: {}'.format(
        pcd_pynt_sort_2['z'].max() , pcd_pynt_sort_2['z'].min(), slice_num, slice_lim))

    ## 3. slice
    for si in tqdm(range(slice_num), total=slice_num, smoothing=0.9):
        # if si>0:
        #     break
        slice_i = pcd_pynt_sort_2[(pcd_pynt_sort_2['z']>=slice_lim[si]) & (pcd_pynt_sort_2['z']<slice_lim[si+1])]
        save_path = os.path.join(save_dir, 'slice_{}.csv'.format(si))
        slice_i.to_csv(save_path, index=False)


def parse_args():
    """paramters"""
    parser = argparse.ArgumentParser("[tree trunk]::slice point cloud")
    parser.add_argument("--cloud_path", type=str, default="./Data/off-ground points.pcd",
                        help="the path for non-ground point clouds")
    parser.add_argument("--save_dir", type=str, default="./Data/slice",
                        help="the directory for saving slice results.")
    parser.add_argument("--tree_max_height", type=float, default=20.,
                        help="the max height of trees will be detected, default=20.0")
    parser.add_argument("--slice_num", type=int, default=30,
                        help="the expected number of slices, default=30")

    return parser.parse_args()

if __name__=="__main__":
    args = parse_args()
    main_slice(args)