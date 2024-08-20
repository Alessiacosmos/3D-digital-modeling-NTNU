"""
@File           : p5_get_trunks_A.py
@Time           : 8/20/2024 8:27 PM
@Author         : Gefei Kong
@Description    : as below
--------------------------------------------------------------
get tree trunk clusters by DBSCAN, to connect the circles belonging to the same trunk across slices.
"""
import argparse

import numpy as np
import pandas as pd
import os
from sklearn.cluster import DBSCAN


def main_get_trunks_A(args):
    ########
    # parse args
    ########
    print("[get trunks (A)]::args:\n{}".format(args))

    rans_dir = args.ransac_dir
    save_dir = rans_dir
    eps = args.eps
    minpts = args.min_pts

    # create save_dir is not exist
    os.makedirs(save_dir, exist_ok=True)

    ########
    # load clean_circle res
    ########
    filename_clean_circles = os.path.join(rans_dir, 'slice_all_r2_p50_500.csv')

    pcd = pd.read_csv(filename_clean_circles)
    class_num = len(set(pcd['class'])) # class means the number (index) of potential trunks for each slice
    print('[get trunks (A)]::trunk number (considering each slice seperately): ', class_num)

    # extract every class's c_x, c_y
    pcd_classXY = pcd.drop_duplicates(subset=['c_x', 'c_y'])

    XY = np.array(pcd_classXY.iloc[:,4:6]) # [n_points, 3] (xyz)

    ##############################################################################
    # Compute DBSCAN across slices
    ##############################################################################
    db = DBSCAN(eps=eps, min_samples=minpts).fit(XY) # input: [n_points,2]
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print('[get trunks (A)]::trunk number (merged all slices): ', n_clusters_)


    ##############################################################################
    # get new class (the index of trunks merged all slices)
    ##############################################################################
    for i, idx in enumerate(set(labels)):
        l_idx = np.where(labels==idx)[0]
        old_class_idx = pcd_classXY.iloc[l_idx, -2]
        old_class = np.array(pcd_classXY.iloc[l_idx,-2])
        pcd.loc[pcd['class'].isin(old_class), 'newclass'] = int(idx)
        # print(idx, pcd[pcd['class'].isin(old_class)])

    pcd.to_csv(filename_clean_circles.replace('.csv', '_newclass.csv'), index=False)



def parse_args():
    """paramters"""
    parser = argparse.ArgumentParser("[tree trunk]::dbscan AGAIN to find trunks")
    parser.add_argument("--ransac_dir", type=str, default="./Data/results/numSlice30_zMax20_rans",
                        help="the path for non-ground point clouds")
    parser.add_argument("--eps", type=float, default=0.3,
                        help="eps of DBSCAN (merge trunk slices)")
    parser.add_argument("--min_pts", type=int, default=2,
                        help="min_pts of DBSCAN (merge trunk slices)")

    return parser.parse_args()

if __name__=="__main__":
    args = parse_args()
    main_get_trunks_A(args)
