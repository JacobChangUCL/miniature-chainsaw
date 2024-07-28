
import torch
from torchvision import models
import numpy as np
import cv2
import os
#这段代码使用了I-FGM算法生成对抗样本。首先定义优化目标。目标是什么？有两种情况。如果是Non-target的情况，那么假设正确
#标签是[1,0,0],那么我们就要minimum第一个标签的概率。如果是target的情况，那么我们就要maximum目标标签的概率。
#可以直接用第一个标签的值为优化目标，但是这样做的话，性能会比较差。这里我们用信息论的交叉熵来定义优化目标。这种方式的
#优点是我们将优化目标改为了模型所拥有的信息。以信息来度量是更合理的方式。这里我们用pytorch的交叉熵函数来定义优化目标。
#我们不需要训练一个新的模型，只需要用原来的模型来生成梯度，并利用梯度更新图片。
#对梯度取符号是FGSM。对梯度取反是I-FGM。

#技巧：通过conda安装包时，最好不要使用vpn，否则会出现各种问题。
#获取计算设备 默认是CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
#在这里我需要一个原始图像集
#图像加载以及预处理
for i in ['elephant','chair','cup','laptop']: #, we want to generate 4 classes of adversarial captchas
    if not os.path.exists(f"./captcha/{i}"):
        os.mkdir(f"./captcha/{i}")
    for j in range(1,10):

        image_path=f"data/caltech101/101-small/{i}/image_00{j:02}.jpg"
        orig = cv2.imread(image_path)[..., ::-1]
        orig = cv2.resize(orig, (224, 224))
        img = orig.copy().astype(np.float32)

        #load the class label
        with open('./data/imagenet_classes.txt', 'r') as f:
            labels_name_array = [line.strip() for line in f.readlines()]

        #preprocess method,follow the value of imagenet
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
        img /= 255.0
        img = (img - mean) / std
        img = img.transpose(2, 0, 1)#HWC->CHW

        img=np.expand_dims(img, axis=0)#add batch dim
        img=torch.from_numpy(img).float()
        img.requires_grad = True#图像数据梯度可以获取
        img.to(device)

        #使用预测模式 固定droupout和BN层的行为
        model = models.alexnet(pretrained=True).to(device).eval()
        original_label=np.argmax(model(img).data.cpu().numpy())

        # #设置为不保存梯度值 自然也无法修改
        # for param in model.parameters():
        #     param.requires_grad = False
        # 这两段不保存除了img之外的梯度值，因为我们不需要修改模型，只需要修改图片

        optimizer = torch.optim.SGD([img], lr=0.1)
        optimizer2 = torch.optim.Adam([img], lr=0.1)
        loss_func = torch.nn.CrossEntropyLoss()

        epochs = 30
        loss_gap = 10  # 在cross entropy中，loss_gap越大,正确标签被选择到的概率越小。这个数值越大
        second_stage_loss_gap = 0.2
        # 优化第一阶段的时间就

        for epoch in range(epochs):
            # 梯度清零
            optimizer.zero_grad()

            # forward + backward
            output = model(img)
            # 在这里output就是logits层的值
            original_label_array = np.zeros(output.shape)
            original_label_array[0][original_label] = 1

            loss = -1 * loss_func(output, torch.from_numpy(original_label_array).to(device))
            label = np.argmax(output.data.cpu().numpy())

            print("epoch={} loss={} label={}".format(epoch, -1 * loss, label))
            if loss * -1 > loss_gap:
                print("first stage attack success,now turn to the second stage")
                second_stage_target = label
                break
            # 如果定向攻击成功
            # if label == target:
            #     break
            if epoch == epochs - 1:
                second_stage_target = label
            loss.backward()
            optimizer.step()

        for epoch in range(epochs):
            # 梯度清零
            optimizer2.zero_grad()

            # forward + backward
            output = model(img)
            # 在这里output就是logits层的值
            target_label_array = np.zeros(output.shape)
            target_label_array[0][second_stage_target] = 1

            # in this stage,we need to minimize the error between target label and output
            loss = loss_func(output, torch.from_numpy(target_label_array).to(device))
            label = np.argmax(output.data.cpu().numpy())

            print("epoch={} loss={} label={}".format(epoch, loss, label))
            if loss < second_stage_loss_gap:
                print("second stage attack success")
                second_stage_target = label
                break
            # 如果定向攻击成功
            # if label == target:
            #     break
            loss.backward()
            optimizer2.step()

        adv = img.data.cpu().numpy()[0]
        adv = adv.transpose(1, 2, 0)
        adv = (adv * std) + mean
        adv = adv * 255.0
        # adv = adv[..., ::-1]  # RGB to BGR
        adv = np.clip(adv, 0, 255).astype(np.uint8)

        cv2.imwrite(f"./captcha/{i}/image_00{j:02}.jpg", adv)
        print(f"save image to ./captcha/{i}/image_00{j:02}.jpg")