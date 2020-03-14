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

    def __init__(self,root_path_test_use_only):
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


if __name__=="__main__":

    sgmentor=mask_cnn_segmentor(os.getcwd())

    for i in range(len(os.listdir(sgmentor.imgs_dir))):
        img=sgmentor.get_an_test_img_tensor(i)
        # res=sgmentor.get_highest_eval_res(img)
        res=sgmentor.get_eval_res_by_name(img,"banana")
        # res=sgmentor.get_eval_res_by_name(img,"apple")
        # dict={"box":box,"label":label,"mask":mask,"score":score,"name":name}

        sgmentor.show(img,res["box"],res["mask"])
        # break

    # img=sgmentor.get_an_test_img_tensor(3)
    # print(sgmentor.eval(img))

    # model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)
    # model.eval()
    # # x = [torch.rand(3, 300, 400), torch.rand(3, 500, 400)]
    # # x = [TF.to_tensor(sgmentor.get_an_test_img(0))]
    # # x = [sgmentor.get_an_test_img_tensor(i) for i in range(4)]
    # x = [sgmentor.get_an_test_img_tensor(1)]
    # predictions = model(x)
    # print(predictions)
    # # plt.imshow(x[1][1,:])
    # plt.imshow(torch.squeeze(predictions[0]["masks"][0]).detach().numpy())
    # plt.show()
    # # plt.imshow(torch.squeeze(predictions[1]["masks"][0]).detach().numpy())
    # # plt.show()
    # # plt.imshow(torch.squeeze(predictions[2]["masks"][0]).detach().numpy())
    # # plt.show()
    # # plt.imshow(torch.squeeze(predictions[3]["masks"][0]).detach().numpy())
    # # plt.show()
    # print(len(sgmentor.COCO_INSTANCE_CATEGORY_NAMES))