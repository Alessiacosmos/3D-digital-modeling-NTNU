'''
Author: Gefei
Date:   2022
'''

import numpy as np
import random


class RANSACCircle:
    """
    RANSAC algorithm
        INPUT:
            pcdxy:          np.array()     # point clouds data (only xy),  [N,2]
            MAX_Iteration:  int            # the number you want for max iterations
            Thres_dis:      int            # distance threshold to
        OUTPUT:
            self.pcd
            best_interior:      np.array()
            best_interior_idx:  list
            best_plane:         list
    """
    def __init__(self, pcdxyzc, MAX_Iteration, Thres_dis, class_number):
        self.xyzc = pcdxyzc  # n_points * 3
        self.xyzc_count = self.xyzc.shape[0]
        # print('point clouds size: ', self.xyzc.shape)
        self.Max_Iter = MAX_Iteration
        self.thres_dis = Thres_dis
        self.class_i = class_number
        self.best_err = 999999999


    def RanSac_algthm(self):
        """
        INPUT: self.pcd;    self.Max_Iter;  self.thres_dis
        :return: self.pcd, best_interior, best_interior_idx, best_circle
        """
        best_interior = np.array([])
        best_interior_idx = np.array([])
        best_circle = []

        for i in range(self.Max_Iter):
            # print('iteration no. ', i, '=======================')
            # Step 1: add 3 random points
            random.seed()
            start_points_idx = random.sample(range(self.xyzc_count), 3)
            # start_points_idx = [random.randint(0, self.xyzc_count-1) for i_l in range(3)] # start_points = np.random.randint(0, self.point_count, size=3)
            # print('start_points_idx: ', start_points_idx)
            p1 = [self.xyzc[start_points_idx[0], 0], self.xyzc[start_points_idx[0], 1]]
            p2 = [self.xyzc[start_points_idx[1], 0], self.xyzc[start_points_idx[1], 1]]
            p3 = [self.xyzc[start_points_idx[2], 0], self.xyzc[start_points_idx[2], 1]]
            # print('3 random points:\np1: {}\np2: {}\np3: {}\n'.format(p1, p2, p3))

            # Step 2: Calculate circle contains p1, p2 and p3
            # Circle equation: (x-a)^2 + (y-b)^2 = r^2
            # p1: x1, y1
            # p2: x2, y2
            # p3: x3, y3
            A = np.array([[p2[0] - p1[0], p2[1] - p1[1]], [p3[0] - p2[0], p3[1] - p2[1]]])
            B = np.array([[p2[0] ** 2 - p1[0] ** 2 + p2[1] ** 2 - p1[1] ** 2],
                          [p3[0] ** 2 - p2[0] ** 2 + p3[1] ** 2 - p2[1] ** 2]])
            try:
                inv_A = np.linalg.inv(A)
            except:
                row, col = np.diag_indices_from(A)
                A[row, col] += 1e-6
                inv_A = np.linalg.inv(A)

            c_x, c_y = np.dot(inv_A, B) / 2
            c_x, c_y = c_x[0], c_y[0]
            r = np.sqrt((c_x - p1[0]) ** 2 + (c_y - p1[1]) ** 2)

            # Step 3: add points into interior points
            # Skip points have be chosen as seed
            # pcd_p_search = np.delete(self.pcd_p, start_points_idx, axis=0)

            #  Calculate distance between the point and the plane
            #  (now all point are in calculating, including 3 samples)
            dist = np.sqrt(np.square((self.xyzc[:,0]-c_x)) + np.square((self.xyzc[:,1]-c_y)))
            dist_diff = np.abs(dist - r)
            # print(dist_diff[0], dist_diff[start_points_idx[0]], dist_diff[start_points_idx[1]], dist_diff[start_points_idx[2]])
            # print('distance_diff from every point to this circle: ', dist_diff)

            # Add points in distance threshold as interior points
            # threshold:
            interior_idx = np.where((dist_diff <= self.thres_dis))[0]
            # print('interior max dist: {} : {}, min dist: {} : {}; interior_num = {}'.format(
            #     max(dist), max(dist[interior_idx]), min(dist[interior_idx]), min(dist), interior_idx.shape))
            pcd_p_interior = self.xyzc[interior_idx, :]

            # update the best model
            if i == 0:
                 best_circle = [c_x, c_y, r]

            # calculate MSE
            err = np.sum(dist_diff) / len(dist_diff)
            if err < self.best_err: # and (pcd_p_interior.shape[0]< self.point_count/2 * 1.15):
                # print('[RANSAC_circle]::{} || updating..., best_err={}'.format(i, self.best_err))
                # if i!=0:
                #     self.xyzc[best_interior_idx, -1] = 0
                best_interior = pcd_p_interior
                best_interior_idx = interior_idx
                best_circle = [c_x, c_y, r, err]
                # self.xyzc[interior_idx, -1] = self.class_i
                self.best_err = err


        return self.xyzc, best_interior, best_interior_idx, best_circle






