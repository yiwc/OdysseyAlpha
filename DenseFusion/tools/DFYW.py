from PIL import Image
import os
import sys
if __name__=="__main__":
    sys.path.append("../")
import numpy as np
from lib.network import PoseNet, PoseRefineNet
import torch
import numpy.ma as ma
import scipy.io as scio
import YWTools
import torchvision.transforms as transforms
from torch.autograd import Variable
from lib.transformations import euler_matrix, quaternion_matrix, quaternion_from_matrix,euler_from_quaternion
import copy
from matplotlib import pyplot as plt
import matplotlib.patches as patches

vector_ploter=YWTools.plot3d_vector_tool()
vector_ploter.add_origin() #增加原点向量
# vector_ploter.show()
# Parameters

num_points = 1000 #？？？
num_obj = 21 # ycb 已经训练好了，含有21个类，不能改。
border_list = [-1, 40, 80, 120, 160, 200, 240, 280, 320, 360, 400, 440, 480, 520, 560, 600, 640, 680] #???
img_width = 480 #输入图片尺寸
img_length = 640
xmap = np.array([[j for i in range(640)] for j in range(480)]) #[0000...,1111...,222] 480,640
ymap = np.array([[i for i in range(640)] for j in range(480)]) #[0 1 2 3..., 0 1 2 3 ..., 0 1 2 3 ...] 480,640
norm = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) #???
bs=1 # batch size
iteration = 2 #???


    #camera paras
cam_cx = 312.9869 #???
cam_cy = 241.3109 #???
cam_fx = 1066.778 #x方向焦距，水平
cam_fy = 1067.487 #y方向焦距，垂直
cam_scale = 10000.0 # scale


banana_dataset_dir="../datasets/yw_test/rgbd-dataset/banana/banana_1"
test_image_file=os.path.join(banana_dataset_dir,"banana_1_1_1.png")
test_depth_file=os.path.join(banana_dataset_dir,"banana_1_1_1_depth.png")
test_label_file=os.path.join(banana_dataset_dir,"banana_1_1_1_mask.png")
test_bbox_file=os.path.join(banana_dataset_dir,"banana_1_1_1_loc.txt")
banana_bbox=[227,245,150,60]

esti_model_file="../trained_checkpoints/ycb/pose_model_26_0.012863246640872631.pth"
refine_model_file="../trained_checkpoints/ycb/pose_refine_model_69_0.009449292959118935.pth"

# rgbd dataset - banana # http://rgbd-dataset.cs.washington.edu/dataset/rgbd-dataset/


img = Image.open(test_image_file)
depth = np.array(Image.open(test_depth_file))
label_banana=np.array(Image.open(test_label_file))

## load Estimator Net
estimator = PoseNet(num_points = num_points, num_obj = num_obj)
estimator.cuda()
estimator.load_state_dict(torch.load(esti_model_file))
estimator.eval()
refiner = PoseRefineNet(num_points = num_points, num_obj = num_obj)
refiner.cuda()
refiner.load_state_dict(torch.load(refine_model_file))
refiner.eval()

## Prediction

posecnn_meta = scio.loadmat("test/000003.mat")
label = np.array(posecnn_meta['labels']) #segmentation label 0/1， 有物体画1，无物体画0
posecnn_rois = np.array(posecnn_meta['rois']) #rois 是用来获得bounding box的
#rois
#行数，物体的个数
#第0列，
#第1列，物体id
#第3,5列，rowmin rowmax
#第2,4列，colmin colmax
# lst = posecnn_rois[:, 1:2].flatten() #[  1.  20.  14.   6.  19.]#说明里面有5个物体，
lst = [1] # assume only banana
my_result_wo_refine = [] #???
my_result = []



for idx in range(len(lst)):
    itemid = lst[idx]
    try:
        rmin, rmax, cmin, cmax = YWTools.get_bbox(posecnn_rois,border_list,img_width,img_length,idx)

        mask_depth = ma.getmaskarray(ma.masked_not_equal(depth, 0)) #ok
        # mask_label = ma.getmaskarray(ma.masked_equal(label, itemid))  #label from 000003.mat
        mask_label = ma.getmaskarray(ma.masked_equal(label_banana, itemid))  #label from banana label
        mask = mask_label * mask_depth

        # Add the patch to the Axes
        # fig, ax = plt.subplots(1)
        # ax.imshow(depth)
        # plt.show()

        # plt.imshow(mask)
        # plt.show()
        # plt.imshow(mask_depth)
        # plt.show()
        # plt.imshow(mask_label)
        # plt.show()
        # plt.imshow(mask)
        # plt.show()

        choose = mask[rmin:rmax, cmin:cmax].flatten().nonzero()[0]
        if len(choose) > num_points:
            c_mask = np.zeros(len(choose), dtype=int)
            c_mask[:num_points] = 1
            np.random.shuffle(c_mask)
            choose = choose[c_mask.nonzero()]
        else:
            choose = np.pad(choose, (0, num_points - len(choose)), 'wrap')

        depth_masked = depth[rmin:rmax, cmin:cmax].flatten()[choose][:, np.newaxis].astype(np.float32)
        xmap_masked = xmap[rmin:rmax, cmin:cmax].flatten()[choose][:, np.newaxis].astype(np.float32)
        ymap_masked = ymap[rmin:rmax, cmin:cmax].flatten()[choose][:, np.newaxis].astype(np.float32)
        choose = np.array([choose])

        pt2 = depth_masked / cam_scale
        pt0 = (ymap_masked - cam_cx) * pt2 / cam_fx
        pt1 = (xmap_masked - cam_cy) * pt2 / cam_fy
        cloud = np.concatenate((pt0, pt1, pt2), axis=1)

        img_masked = np.array(img)[:, :, :3]
        img_masked = np.transpose(img_masked, (2, 0, 1))
        img_masked = img_masked[:, rmin:rmax, cmin:cmax]

        cloud = torch.from_numpy(cloud.astype(np.float32))
        choose = torch.LongTensor(choose.astype(np.int32))
        img_masked = norm(torch.from_numpy(img_masked.astype(np.float32)))
        index = torch.LongTensor([itemid - 1])

        cloud = Variable(cloud).cuda()
        choose = Variable(choose).cuda()
        img_masked = Variable(img_masked).cuda()
        index = Variable(index).cuda()

        cloud = cloud.view(1, num_points, 3)
        img_masked = img_masked.view(1, 3, img_masked.size()[1], img_masked.size()[2])

        pred_r, pred_t, pred_c, emb = estimator(img_masked, cloud, choose, index)
        pred_r = pred_r / torch.norm(pred_r, dim=2).view(1, num_points, 1)

        pred_c = pred_c.view(bs, num_points)
        how_max, which_max = torch.max(pred_c, 1)
        pred_t = pred_t.view(bs * num_points, 1, 3)
        points = cloud.view(bs * num_points, 1, 3)

        my_r = pred_r[0][which_max[0]].view(-1).cpu().data.numpy()
        my_t = (points + pred_t)[which_max[0]].view(-1).cpu().data.numpy()
        my_pred = np.append(my_r, my_t)
        my_result_wo_refine.append(my_pred.tolist())

        for ite in range(0, iteration):
            T = Variable(torch.from_numpy(my_t.astype(np.float32))).cuda().view(1, 3).repeat(num_points,
                                                                                             1).contiguous().view(1,
                                                                                                                  num_points,
                                                                                                                  3)
            my_mat = quaternion_matrix(my_r)
            R = Variable(torch.from_numpy(my_mat[:3, :3].astype(np.float32))).cuda().view(1, 3, 3)
            my_mat[0:3, 3] = my_t

            new_cloud = torch.bmm((cloud - T), R).contiguous()
            pred_r, pred_t = refiner(new_cloud, emb, index)
            pred_r = pred_r.view(1, 1, -1)
            pred_r = pred_r / (torch.norm(pred_r, dim=2).view(1, 1, 1))
            my_r_2 = pred_r.view(-1).cpu().data.numpy()
            my_t_2 = pred_t.view(-1).cpu().data.numpy()
            my_mat_2 = quaternion_matrix(my_r_2)
            my_mat_2[0:3, 3] = my_t_2
            my_mat_final = np.dot(my_mat, my_mat_2)
            my_r_final = copy.deepcopy(my_mat_final)
            my_r_final[0:3, 3] = 0
            my_r_final = quaternion_from_matrix(my_r_final, True)
            my_t_final = np.array([my_mat_final[0][3], my_mat_final[1][3], my_mat_final[2][3]])
            my_pred = np.append(my_r_final, my_t_final)
            my_r = my_r_final
            my_t = my_t_final
            my_euler_form_r=euler_from_quaternion(my_r)
            # <class 'tuple'>: (0.9198490563735781, -0.007832527911272334, -0.47081842893943104)
            my_rotation_matrix_from_euler=euler_matrix(my_euler_form_r[0],my_euler_form_r[1],my_euler_form_r[2])
                    # [[0.90679773  0.18969227 - 0.37647672  0.]
                    #  [-0.41995766  0.48440958 - 0.76745223  0.]
                    # [0.03678917 0.85402822 0.51892423 0.]
                    # [0.          0.          0.          1.]]
            x=np.dot(my_rotation_matrix_from_euler,np.array([[1,0,0,1]]).transpose()).flatten()
            y=np.dot(my_rotation_matrix_from_euler,np.array([[0,1,0,1]]).transpose()).flatten()
            z=np.dot(my_rotation_matrix_from_euler,np.array([[0,0,1,1]]).transpose()).flatten()
            newvs=[]
            # newvs.append([0,0,0,x[0],x[1],x[2]])
            # newvs.append([0,0,0,y[0],y[1],y[2]])
            newvs.append([0,0,0,z[0],z[1],z[2]])
            vector_ploter.addvs(newvs)
        # Here 'my_pred' is the final pose estimation result after refinement ('my_r': quaternion, 'my_t': translation)

        my_result.append(my_pred.tolist())

        #plot mask
        maskfig = plt.figure("mask plot")
        ax = maskfig.add_subplot(111)
        rect = patches.Rectangle((banana_bbox[0],banana_bbox[1]), banana_bbox[2], banana_bbox[3], linewidth=5, edgecolor='w', facecolor='none')
        ax.imshow(mask)
        ax.add_patch(rect)
        # plt.show()

    except ZeroDivisionError:
        print("PoseCNN Detector Lost {0} at No.{1} keyframe".format(itemid, now))
        my_result_wo_refine.append([0.0 for i in range(7)])
        my_result.append([0.0 for i in range(7)])

print("my_result,",my_result)
vector_ploter.show()