### DFYW 5
#it is DFYW4 version and based in the main root folder

### DFYW 4
# combined with ZED depth and 2d img
# copy this file with folder<src> and <posecnn>
### DFYW 3
# combined with maskcnn

### DFYW 2


from PIL import Image
import os
import numpy as np
import sys
if __name__=="__main__":
    sys.path.append("../")
from DenseFusion_lib.network import PoseNet, PoseRefineNet
import torch
import numpy.ma as ma
import scipy.io as scio
# import YWTools
import torchvision.transforms as transforms
from torch.autograd import Variable
from DenseFusion_lib.transformations import euler_matrix, quaternion_matrix, quaternion_from_matrix, euler_from_quaternion
import copy
# from matplotlib import pyplot as plt
# import matplotlib.patches as patches
# from posecnn.YW_poseCNN import MASKCNN
# import torchvision.transforms.functional as TF
# import math
import torch
import torchvision
import os
from torchvision.datasets.folder import default_loader
import torchvision.transforms.functional as TF
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import matplotlib.patches as patches
import random

class mask_cnn_segmentor(object):
    """
    Ref:https://pytorch.org/docs/stable/torchvision/models.html#semantic-segmentation
    Input: is the img
    Output: is the segmentation and croped img
    """

    def __init__(self):

        root_path_test_use_only=os.path.join(os.getcwd(),"DenseFusion_src")#You may change this to any folder as you have a test datasets like this dataset.

        self.imgs_dir=os.path.join(root_path_test_use_only,"datasets","imgs")
        self.imgs_and_depth_dir=os.path.join(root_path_test_use_only,"datasets","imgs_and_depth")
        self.model=model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
        self.COCO_INSTANCE_CATEGORY_NAMES = [
            '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
            'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
            'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
            'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
            'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
            'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
            'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
            'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
            'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
            'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
            'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
            'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]


    def eval(self,img_input):
        self.model.eval()
        x =[img_input]
        predictions=self.model(x)
        return predictions

    def get_highest_eval_res(self,img_input):
        # [0] ["boxes"][0]
        # [0]img sequence in the img_input
        # [boxes] boxes,
        # [0] first results in maybe 23 results.
        predictions=self.eval(img_input)
        box=predictions[0]["boxes"][0].detach().numpy()
        label=predictions[0]["labels"][0].detach().numpy()
        mask=predictions[0]["masks"][0].detach().numpy()
        score=predictions[0]["scores"][0].detach().numpy()
        name=self.COCO_INSTANCE_CATEGORY_NAMES[int(label)]
        dict={"box":box,"label":label,"mask":mask,"score":score,"name":name}
        return dict

    def get_eval_res_by_name(self,img_input,name_target):
        predictions=self.eval(img_input)

        objects_len=len(predictions[0]["labels"])
        for i in range(objects_len):

            label = predictions[0]["labels"][i].detach().numpy()
            name = self.COCO_INSTANCE_CATEGORY_NAMES[int(label)]
            if(name == name_target):
                box = predictions[0]["boxes"][i].detach().numpy()
                label = predictions[0]["labels"][i].detach().numpy()
                mask = predictions[0]["masks"][i].detach().numpy()
                score = predictions[0]["scores"][i].detach().numpy()
                name = self.COCO_INSTANCE_CATEGORY_NAMES[int(label)]
                dict = {"box": box, "label": label, "mask": mask, "score": score, "name": name}
                return dict
        return None



    def get_box_rcwh(self,box):
        x1,y1,x2,y2=box
        r=y1
        c=x1
        w=abs(x2-x1)
        h=abs(y2-y1)
        return r,c,w,h

    def show(self,img_raw,box,mask):
        w = 10
        h = 10
        # fig = plt.figure()

        # img_mat=img_raw.cpu().numpy()[0,:,:]
        img_mat=img_raw.cpu().numpy().transpose([1,2,0])

        fig,ax=plt.subplots(2, 2, sharex='col')
        img = img_raw
        # fig.add_subplot(2, 2, 1)
        ax[0,0].imshow(img_mat)


        # plt.imshow(box)
        print(box)
        r,c,w,h=self.get_box_rcwh(box)
        rect = patches.Rectangle((c, r), w,h, linewidth=3, edgecolor='r', facecolor='none')
        # rect = patches.Rectangle((0.5, 0.5), 3, 3, linewidth=1, edgecolor='r', facecolor='none')
        ax[0,1].imshow(img_mat)
        ax[0,1].add_patch(rect)

        img_masked=img_mat[:]
        img_masked[:,:,0]=img_masked[:,:,0]+mask.transpose([1,2,0])[:,:,0]
        img_masked[:,:,1]=img_masked[:,:,1]-mask.transpose([1,2,0])[:,:,0]
        img_masked[:,:,2]=img_masked[:,:,2]-mask.transpose([1,2,0])[:,:,0]

        # img_masked[:,:,0]=img_masked[:,:,0]+1

        # img_masked=img_masked-mask.transpose([1,2,0])*0.5
        ax[1,1].imshow(np.squeeze(mask))
        ax[1,0].imshow(np.squeeze(img_masked))



        crpped_img=img_raw





        plt.show()


    # for experiments
    def get_an_test_img(self, id):
        # for img in os.listdir(self.imgs_dir):
        img_name = os.listdir(self.imgs_dir)[id]
        img_path = os.path.join(self.imgs_dir, img_name)
        img = default_loader(img_path)
        return img

    def get_an_test_img_tensor(self, id):
        return TF.to_tensor(self.get_an_test_img(id))

    def get_an_test_img_and_depth(self):
        # img_name="banana_1_1_19.png"
        # depth_name="banana_1_1_19_depth.png"
        # img_name="banana_1_4_268.png"
        # depth_name="banana_1_4_268_depth.png"
        # ia=random.choice([1,2,4])
        ia=random.choice([4])
        ib=random.choice(range(1,220))
        img_name="banana_1_"+str(ia)+"_"+str(ib)+".png"
        depth_name="banana_1_"+str(ia)+"_"+str(ib)+"_depth.png"
        print("img_name",img_name)
        print("depth_name",depth_name)
        # # Good Test Im
        # img_name="banana_1_4_157.png"
        # depth_name="banana_1_4_157_depth.png"

        # img_name = os.listdir(self.imgs_and_depth_dir)[id]
        img_path = os.path.join(self.imgs_and_depth_dir, img_name)
        depth_path = os.path.join(self.imgs_and_depth_dir, depth_name)
        return default_loader(img_path),default_loader(depth_path)
class DenseFusion_YW(object):
    def __init__(self,posecnn):
        # posecnn
        self.posecnn= posecnn

        # df
            #camera paras
        self.cam_cx = 312.9869 #???
        self.cam_cy = 241.3109 #???
        self.cam_fx = 1066.778 #x方向焦距，水平
        self.cam_fy = 1067.487 #y方向焦距，垂直
        self.cam_scale = 10000.0 # scale ????
            #main
        self.num_points=200 # default 1000
        self.num_obj = 21  # ycb 已经训练好了，含有21个类，不能改。
        # self.xmap = np.array([[j for i in range(640)] for j in range(480)])  # [0000...,1111...,222] 480,640
        # self.ymap = np.array([[i for i in range(640)] for j in range(480)])  # [0 1 2 3..., 0 1 2 3 ..., 0 1 2 3 ...] 480,640
        self.xmap = np.array([[j for i in range(1280)] for j in range(720)])  # [0000...,1111...,222] 480,640
        self.ymap = np.array([[i for i in range(1280)] for j in range(720)])  # [0 1 2 3..., 0 1 2 3 ..., 0 1 2 3 ...] 480,640
        self.norm = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) # For img transform in the df
        self.bs=1
        self.iteration=2
        self.esti_model_file="DenseFusion_src/pose_model_26_0.012863246640872631.pth"
        self.refine_model_file="DenseFusion_src/pose_refine_model_69_0.009449292959118935.pth"
        self.estimator = PoseNet(num_points=self.num_points, num_obj=self.num_obj)
        self.estimator.cuda()
        self.estimator.load_state_dict(torch.load(self.esti_model_file))
        self.estimator.eval()
        self.refiner = PoseRefineNet(num_points=self.num_points, num_obj=self.num_obj)
        self.refiner.cuda()
        self.refiner.load_state_dict(torch.load(self.refine_model_file))
        self.refiner.eval()
        self.lst = [1]  # assume only banana. This is designed for multi-label task, if multi label detected in one img,
                        #they may allocated with different id, id==1.it means the label is 1, id==2, it means the label is 2; so with known the
                        #label, we can know label1 is banana ,label2 is apple like this.
        self.my_result_wo_refine = []  # ???
        self.my_result = []

    def DenseFusion(self,img,depth,posecnn_res):
        my_result_wo_refine=[]

        itemid=1 # this is simplified for single label decttion, if multi-label used, check DFYW3.py for more

        depth=np.array(depth)
        # img = img

        seg_res = posecnn_res

        x1, y1, x2, y2 = seg_res["box"]
        banana_bbox_draw = self.posecnn.get_box_rcwh(seg_res["box"])
        rmin, rmax, cmin, cmax = int(y1), int(y2), int(x1), int(x2)
        try:
            depth = depth[:, :, 1] # because depth has 3 dimensions RGB but they are the all the same with each other
        except:
            # depth=depth
            pass
        depth=np.nan_to_num(depth)#DIY
        mask_depth = ma.getmaskarray(ma.masked_not_equal(depth, 0))  # ok
        mask_depth_nonzeros = mask_depth[:].nonzero()
        label_banana = np.squeeze(seg_res["mask"])
        label_banana = ma.getmaskarray(ma.masked_greater(label_banana, 0.5))
        label_banana_nonzeros = label_banana.flatten().nonzero()

        mask_label = ma.getmaskarray(ma.masked_equal(label_banana, itemid))  # label from banana label
        mask_label_nonzeros = mask_label[:].nonzero()

        mask = mask_label * mask_depth

        mask_nonzeros = mask[:].flatten().nonzero()
        mask_target=mask[rmin:rmax, cmin:cmax]
        choose = mask[rmin:rmax, cmin:cmax].flatten().nonzero()[0]
        res_len_choose=len(choose)
        if len(choose) > self.num_points:
            c_mask = np.zeros(len(choose), dtype=int)
            c_mask[:self.num_points] = 1
            np.random.shuffle(c_mask)
            choose = choose[c_mask.nonzero()]
        else:
            # print("(?)len of choose is 0, check error")
            print("Info, DenseFusion: len(choose)=",len(choose))
            # return "ERROR, img broken (?)"
            # choose = np.pad(choose, (0, self.num_points - len(choose)), 'wrap')
            return None

        depth_masked = depth[rmin:rmax, cmin:cmax].flatten()[choose][:, np.newaxis].astype(np.float32)
        xmap_masked = self.xmap[rmin:rmax, cmin:cmax].flatten()[choose][:, np.newaxis].astype(np.float32)
        ymap_masked = self.ymap[rmin:rmax, cmin:cmax].flatten()[choose][:, np.newaxis].astype(np.float32)
        choose = np.array([choose])
        pt2 = depth_masked / self.cam_scale
        pt0 = (ymap_masked - self.cam_cx) * pt2 / self.cam_fx
        pt1 = (xmap_masked - self.cam_cy) * pt2 / self.cam_fy
        cloud = np.concatenate((pt0, pt1, pt2), axis=1)

        img_masked = np.array(img)[:, :, :3]
        img_masked = np.transpose(img_masked, (2, 0, 1))
        img_masked = img_masked[:, rmin:rmax, cmin:cmax]

        cloud = torch.from_numpy(cloud.astype(np.float32))
        choose = torch.LongTensor(choose.astype(np.int32))
        img_masked = self.norm(torch.from_numpy(img_masked.astype(np.float32)))
        index = torch.LongTensor([itemid - 1])

        cloud = Variable(cloud).cuda()
        choose = Variable(choose).cuda()
        img_masked = Variable(img_masked).cuda()
        index = Variable(index).cuda()


        cloud = cloud.view(1, self.num_points, 3)
        img_masked = img_masked.view(1, 3, img_masked.size()[1], img_masked.size()[2])

        pred_r, pred_t, pred_c, emb = self.estimator(img_masked, cloud, choose, index)
        pred_r = pred_r / torch.norm(pred_r, dim=2).view(1, self.num_points, 1)

        pred_c = pred_c.view(self.bs, self.num_points)
        how_max, which_max = torch.max(pred_c, 1)
        pred_t = pred_t.view(self.bs * self.num_points, 1, 3)
        points = cloud.view(self.bs * self.num_points, 1, 3)

        my_r = pred_r[0][which_max[0]].view(-1).cpu().data.numpy()
        my_t = (points + pred_t)[which_max[0]].view(-1).cpu().data.numpy()
        my_pred = np.append(my_r, my_t)
        my_result_wo_refine.append(my_pred.tolist())

        my_result=[]
        for ite in range(0, self.iteration):
            T = Variable(torch.from_numpy(my_t.astype(np.float32))).cuda().view(1, 3).repeat(self.num_points,
                                                                                             1).contiguous().view(1,
                                                                                                                  self.num_points,
                                                                                                                  3)
            my_mat = quaternion_matrix(my_r)
            R = Variable(torch.from_numpy(my_mat[:3, :3].astype(np.float32))).cuda().view(1, 3, 3)
            my_mat[0:3, 3] = my_t

            new_cloud = torch.bmm((cloud - T), R).contiguous()
            pred_r, pred_t = self.refiner(new_cloud, emb, index)
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
            my_result.append(my_pred.tolist())
        my_result_np = np.array(my_result)
        my_result_mean = np.mean(my_result, axis=0)
        my_r = my_result_mean[:4]
        my_t = my_result_mean[4:]
        my_r_quaternion=my_r
        return my_r_quaternion,my_t
        # my_euler_form_r=euler_from_quaternion(my_r)
        # print("my_euler_form_r",my_euler_form_r)

        # #my_euler_form_r <class 'tuple'>: (0.9198490563735781, -0.007832527911272334, -0.47081842893943104)
        # my_euler_yaw=list(my_euler_form_r)[2]
        # my_rotation_matrix_from_euler=euler_matrix(my_euler_form_r[0],my_euler_form_r[1],my_euler_form_r[2])
                # [[0.90679773  0.18969227 - 0.37647672  0.]
                #  [-0.41995766  0.48440958 - 0.76745223  0.]
                # [0.03678917 0.85402822 0.51892423 0.]
                # [0.          0.          0.          1.]]
        # x=np.dot(my_rotation_matrix_from_euler,np.array([[1,0,0,1]]).transpose()).flatten()
        # y=np.dot(my_rotation_matrix_from_euler,np.array([[0,1,0,1]]).transpose()).flatten()
        # z=np.dot(my_rotation_matrix_from_euler,np.array([[0,0,1,1]]).transpose()).flatten()
        # newvs=[]
        # grasp_vector=[math.cos(my_euler_yaw),math.sin(my_euler_yaw),0]
        #
        # mx=my_rotation_matrix_from_euler[0,0:3]
        # my=my_rotation_matrix_from_euler[1,0:3]
        # mz=my_rotation_matrix_from_euler[2,0:3]
        # newvs.append([0,0,0,mx[0],mx[1],mx[2]])
        # newvs.append([0,0,0,my[0],my[1],my[2]])
        # newvs.append([0,0,0,mz[0],mz[1],mz[2]])
        # vector_ploter.addvs(newvs)
if __name__ == "__main__":
    posecnn=mask_cnn_segmentor()
    dfyw = DenseFusion_YW(posecnn=posecnn)

    #Notice: Change this to zed
    test_one_img, test_one_depth = dfyw.posecnn.get_an_test_img_and_depth()

    seg_res=posecnn.get_eval_res_by_name(TF.to_tensor(test_one_img), "banana")
    # pred_r,pred_t=dfyw.DenseFusion(img=test_one_img,depth=test_one_depth,posecnn_res=seg_res)
    pred_r,pred_t=dfyw.DenseFusion(img=test_one_img,depth=test_one_depth,posecnn_res=seg_res)
    pred_r_matrix=quaternion_matrix(pred_r)
    print(pred_t,pred_r)
