"""
@File           : p3_ransac.py
@Time           : 8/20/2024 7:36 PM
@Author         : Gefei Kong
@Description    : as below
--------------------------------------------------------------

"""
import argparse
import os
import glob
import pandas as pd
import numpy as np
from tqdm import tqdm

from utils import RANSAC_circle_algorithm

def main_ransac(args):
    ########
    # parse args
    ########
    print("[ransac]::args:\n{}".format(args))

    db_dir = args.dbscan_dir
    save_dir = args.rans_save_dir
    max_iter = args.max_iter
    threshold_dis = args.threshold_dis

    # create save_dir is not exist
    os.makedirs(save_dir, exist_ok=True)

    #######
    # load all slice files
    #######
    slice_files = glob.glob(os.path.join(db_dir, '*_01.csv'))
    slice_files = sorted(slice_files)

    ########
    # ransac for each slice
    ########
    for id, f_i in enumerate(slice_files):
        print("[ransac]:: slice {} ({}) is processing...".format(id, f_i))
        ########
        # load dbscan res
        ########
        pcd = pd.read_csv(f_i)
        print('[ransac]:: slice {} || statistic of pcd: max z={}, min z={}, diff={}'.format(id, max(pcd.z), min(pcd.z), (max(pcd.z)-min(pcd.z))))
        # print('columns name: ', pcd.columns.values)

        # rm points not been covered by any clusters.
        pcd = pcd[pcd['dbclass']!=-1]   # -1: points not been covered by any clusters
        group_num = len(set(pcd['dbclass']))
        print('[ransac]:: slice {} || group number: {}'.format(id, group_num))

        # create result dataframe
        res = pd.DataFrame([], columns=['x', 'y', 'z', 'dbclass', 'c_x', 'c_y', 'r', 'class'])

        for i in tqdm(range(group_num), total=group_num, smoothing=0.9):
            pcd_gi = np.array(pcd[pcd['dbclass']==i])
            if pcd_gi.shape[0]<200:
                continue

            # ransac circle
            rans = RANSAC_circle_algorithm.RANSACCircle(pcd_gi, max_iter, threshold_dis, i)
            xyzc_r, best_interior, best_interior_idx, best_circle = rans.RanSac_algthm()

            # add result to pandas
            rans_pd = pd.DataFrame(best_interior, columns=['x', 'y', 'z', 'dbclass'])
            rans_pd.loc[:, 'c_x'] = best_circle[0]
            rans_pd.loc[:, 'c_y'] = best_circle[1]
            rans_pd.loc[:, 'r']   = best_circle[2]
            rans_pd.loc[:, 'err'] = best_circle[3]
            rans_pd.loc[:, 'class'] = i
            res = res.append(rans_pd)

        # save result
        savename = os.path.basename(f_i).replace('.csv', '_res.csv')
        res.to_csv(os.path.join(save_dir, savename), index=False)


def parse_args():
    """paramters"""
    parser = argparse.ArgumentParser("[tree trunk]::ransac to get circles")
    parser.add_argument("--dbscan_dir", type=str, default="./Data/results/numSlice30_zMax20",
                        help="the path for non-ground point clouds")
    parser.add_argument("--rans_save_dir", type=str, default="./Data/results/numSlice30_zMax20_rans",
                        help="the directory for saving slice results.")
    parser.add_argument("--max_iter", type=int, default=50,
                        help="the number of max iteration for RANSAC")
    parser.add_argument("--threshold_dis", type=float, default=0.15,
                        help="threshold_dis of RANSAC")

    return parser.parse_args()

if __name__=="__main__":
    args = parse_args()
    main_ransac(args)
