"""
@File           : p2_dbscan.py
@Time           : 8/20/2024 6:21 PM
@Author         : Gefei Kong
@Description    : as below
--------------------------------------------------------------

"""
import argparse
import glob
import os
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from tqdm import tqdm


def main_dbscan(args):
    ########
    # parse args
    ########
    print("[dbscan]::args:\n{}".format(args))

    slice_dir = args.slice_dir
    save_dir  = args.db_save_dir
    eps       = args.eps
    minpts    = args.min_pts


    # create save_dir is not exist
    os.makedirs(save_dir, exist_ok=True)

    #######
    # load all slice files
    #######
    slice_files = glob.glob(os.path.join(slice_dir, '*.csv'))
    slice_files = sorted(slice_files)

    for sid, s_i in tqdm(enumerate(slice_files), total=len(slice_files), smoothing=0.9):
        #######
        # read data
        #######
        # read as pd.Dataframe
        basename = os.path.basename(s_i) # e.g. 'Data/slice_4.csv'
        savename = os.path.join(save_dir, basename.replace('.csv', '_db_01.csv'))
        df = pd.read_csv(s_i)
        # get (x,y) coordinates of all points
        arr = np.array(df.iloc[:,:3]) # shape: [n_points, 3] (xyz)
        XY  = arr[:,:2]

        ##############################################################################
        # Compute DBSCAN
        ##############################################################################
        db = DBSCAN(eps=eps, min_samples=minpts).fit(XY) # input: [n_points,2]
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_

        # # Number of clusters in labels, ignoring noise if present.
        # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        # print('cluster number: ', n_clusters_)


        ##############################################################################
        # save as csv point cloud
        ##############################################################################
        pcd_dbclass = np.concatenate((arr, np.array([labels]).T), axis=1)
        pcd_dbclass_df = pd.DataFrame(pcd_dbclass, columns=['x','y','z','dbclass'])
        pcd_dbclass_df.to_csv(savename, index=False)


def parse_args():
    """paramters"""
    parser = argparse.ArgumentParser("[tree trunk]::dbscan to group points")
    parser.add_argument("--slice_dir", type=str, default="./Data/slice",
                        help="the path for non-ground point clouds")
    parser.add_argument("--db_save_dir", type=str, default="./Data/results/numSlice30_zMax20",
                        help="the directory for saving slice results.")
    parser.add_argument("--eps", type=float, default=0.1,
                        help="eps of DBSCAN")
    parser.add_argument("--min_pts", type=int, default=5,
                        help="min_pts of DBSCAN")


    return parser.parse_args()

if __name__=="__main__":
    args = parse_args()
    main_dbscan(args)

