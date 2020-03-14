from DFYW5 import mask_cnn_segmentor
from DFYW5 import DenseFusion_YW
import torchvision.transforms.functional as TF
import time
import sys
import os
import numpy as np
import cv2
from DenseFusion_lib.transformations import euler_matrix, quaternion_matrix, quaternion_from_matrix, euler_from_quaternion
from inspect import currentframe, getframeinfo
from scipy.spatial import KDTree
sys.path.append(os.path.join(os.getcwd(),"DenseFusion","tools"))
sys.path.append(os.path.join(os.getcwd(),"DenseFusion"))
def main(db):
    db=db
    posecnn=mask_cnn_segmentor()
    dfyw = DenseFusion_YW(posecnn=posecnn)


    while(1):



        if(db.DF_sensor_able):
            pass
            time.sleep(1)
        else:
            continue
        # try:

        #Notice: Change this to zed
        # test_one_img, test_one_depth = dfyw.posecnn.get_an_test_img_and_depth()
        img,depth=db.cam_image,db.cam_depth
        if(img.size==0):
            time.sleep(1)
            print("DF sensor waiting for image")
            continue
        # print("img==", img)
        # print("depth==", depth)
        #img resize
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = cv2.resize(img, (640, 480), interpolation=cv2.INTER_LINEAR)

        depth = cv2.cvtColor(depth, cv2.COLOR_BGR2RGB)
        depth = depth[:,:,0]

        # x, y = np.mgrid[0:depth.shape[0], 0:depth.shape[1]]
        # xygood = np.array((x[~depth.mask], y[~depth.mask])).T
        # xybad = np.array((x[depth.mask], y[depth.mask])).T
        # depth[depth.mask] = depth[~depth.mask][KDTree(xygood).query(xybad)[1]]


        # depth = cv2.resize(depth, (640, 480), interpolation=cv2.INTER_LINEAR)
        depth_nans=depth[np.isnan(depth)]
        depth_infs=depth[np.isinf(depth)]
        #depth shape=(720,1280,4)
        # z = depth[i, j, 2]
        # x = depth[i, j, 0])
        # y = depth[i, j, 1]
        #img shape=(720,1280,4)
        seg_res=posecnn.get_eval_res_by_name(TF.to_tensor(img), "banana")
        if(seg_res==None):
            time.sleep(1)
            print("info:Posecnn has no detection")
            continue

        db.publish_posecnn_banana_mask(seg_res["mask"])
        db.publish_posecnn_banana_box(posecnn.get_box_rcwh(seg_res["box"]))

        # continue
        DF_res=dfyw.DenseFusion(img=img,depth=depth,posecnn_res=seg_res)
        if(DF_res==None):
            print("Info, Dense Fusion Return None")
            continue
        pred_r,pred_t=DF_res[0],DF_res[1]
        pred_r_matrix=quaternion_matrix(pred_r)
        print(pred_r,pred_t)
        print(pred_r_matrix)
        db.DF_pred_matrix=pred_r_matrix

        # print()

        # except Exception as err:
        #
        #     print("\n\nerror, ZED_DF_Sensor.py. def main()")
        #     print(err)
        #     frameinfo = getframeinfo(currentframe())
        #     print(frameinfo.filename, frameinfo.lineno)
        #     print("\n\n")
        time.sleep(1)
    pass

if __name__ == "__main__":
    # pass
    main()