# coding=utf-8

import base64
import pandas as pd
import pickle
import numpy as np
import torch

#from tasks.pvqa_model import PVQAModel

baseUrl = 'D:/UoM/__Sem7/fyp/Project/PVQA0/'

generatedDataUrl = 'D:/1Projects/paradox-medvqa/backend/fasterrcnn/data/pvqa/val3.csv'

model_dir ="D:/UoM/__Sem7/fyp/Models/model_logit_fc_improved"


FIELDNAMES = ['image_id', 'image_w', 'image_h',
              'num_boxes', 'boxes', 'features']

def getModel():
    # model = PVQAModel(4092)
    # state_dict = torch.load("%s.pth" % model_dir, map_location=lambda storage, loc: storage)
    # model.load_state_dict(state_dict["model_state_dict"])
    # model = model.cpu()
    model = torch.load("%s.pth" % model_dir, map_location=lambda storage, loc: storage)['saved_full_model'] 
    model = model.cpu() 
    return model

def load_tsv(split: str, dataType="pvqa"):
    if(dataType=="pvqa"):
        tsv_file = baseUrl+'data/pvqa/images/%s%s.csv' % (split, '1')
    else:
        tsv_file = generatedDataUrl
    df = pd.read_csv(tsv_file, delimiter='\t', names=FIELDNAMES)

    data = []
    for i in range(df.shape[0]):
        datum = {}
        datum['img_id'] = '%s_%04d' % (split, df['image_id'][i])
        datum['img_w'] = df['image_w'][i]
        datum['img_h'] = df['image_h'][i]
        datum['num_boxes'] = df['num_boxes'][i]

        boxes = df['boxes'][i]
        buf = base64.b64decode(boxes[1:])
        temp = np.frombuffer(buf, dtype=np.float64).astype(np.float32)
        datum['boxes'] = temp.reshape(datum['num_boxes'], -1)

        features = df['features'][i]
        buf = base64.b64decode(features[1:])
        temp = np.frombuffer(buf, dtype=np.float32)
        datum['features'] = temp.reshape(datum['num_boxes'], -1)

        data.append(datum)

    return data

# def getDatum(imageName):
#     [split,i] = imageName.split("_")
#     i = int(i)
#     tsv_file = baseUrl+'data/pvqa/images/%s%s.csv' % (split, '1')
#     df = pd.read_csv(tsv_file, delimiter='\t', names=FIELDNAMES)
#     result ={}
#     result['num_boxes'] = df['num_boxes'][i]
#     boxes = df['boxes'][i]
#     buf = base64.b64decode(boxes[1:])
#     temp = np.frombuffer(buf, dtype=np.float64).astype(np.float32)
#     result['boxes'] = temp.reshape(result['num_boxes'], -1)
#     features = df['features'][i]
#     buf = base64.b64decode(features[1:])
#     temp = np.frombuffer(buf, dtype=np.float32)
#     result['features'] = temp.reshape(result['num_boxes'], -1)
#     print(split,i)
#     return result

def loadData():
    splits = ['train', 'test', 'val']
    # loading dtection features to img_data
    imgid2img = {}
    for split in splits:
        data = load_tsv(split)

        for datum in data:
            imgid2img[datum['img_id']] = datum
    return imgid2img 

def predict(model, label2ans, imageName, question, imgid2img, dataType="pvqa"):
    if(dataType=="pvqa"):
        img_id = imageName.strip()
        image_fet = imgid2img[img_id]
        feats = torch.tensor([image_fet['features']])
        boxes = torch.tensor([image_fet['boxes']])
    else:
        img_id = "val_0000"
        imgid2img2 = {}
        data1 = load_tsv("val","other")
        for datum in data1:
            imgid2img2[datum['img_id']] = datum
        image_fet = imgid2img2[img_id]
        feats = torch.tensor([image_fet['features']])
        boxes = torch.tensor([image_fet['boxes']])
    
    # Datum = getDatum(imageName)
    answer = ""
    # feats = torch.tensor([Datum['features']])
    # boxes = torch.tensor([Datum['boxes']])
    # predict and print max 5
    model.eval()
    with torch.no_grad():
        feats, boxes = feats.cpu(), boxes.cpu()
        sents = [question]
        targets = ['']
        logit = model(feats, boxes, sents, targets)
        m = torch.nn.Softmax(dim=1)
        logit2 = m(logit)
        score, label = logit.max(1)
        score2, label2 = logit2.max(1)
        label = int(label[0])
    answer = label2ans[label]
    #answer2 = label2ans[label2]
    print(logit)
    print(logit2)
    print(label)
    print(score)
    print(label2)
    print(score2)
    return answer,round(score2.item()*100, 3) 

def getLable2Ans():
    label2ans = pickle.load(
        open(baseUrl+'data/pvqa/qas/trainval_label2ans.pkl', 'rb'))
    print(label2ans)
    return label2ans


# def load_tsv(split: str):
#     tsv_file = baseUrl+'data/pvqa/images/%s%s.csv' % (split, 1)
#     df = pd.read_csv(tsv_file, delimiter='\t', names=FIELDNAMES)

#     data = []
#     for i in range(df.shape[0]):
#         datum = {}
#         datum['img_id'] = '%s_%04d' % (split, df['image_id'][i])
#         datum['img_w'] = df['image_w'][i]
#         datum['img_h'] = df['image_h'][i]
#         datum['num_boxes'] = df['num_boxes'][i]

#         boxes = df['boxes'][i]
#         buf = base64.b64decode(boxes[1:])
#         temp = np.frombuffer(buf, dtype=np.float64).astype(np.float32)
#         datum['boxes'] = temp.reshape(datum['num_boxes'], -1)

#         features = df['features'][i]
#         buf = base64.b64decode(features[1:])
#         temp = np.frombuffer(buf, dtype=np.float32)
#         datum['features'] = temp.reshape(datum['num_boxes'], -1)

#         data.append(datum)

#     return data


# if __name__ == '__main__':

#     splits = ['test']
#     # loading detection features to img_data
#     imgid2img = {}
#     for split in splits:
#         data = load_tsv(split)

#         for datum in data:
#             imgid2img[datum['img_id']] = datum

#     label2ans = pickle.load(
#         open(baseUrl+'data/pvqa/qas/trainval_label2ans.pkl', 'rb'))

#     model = PVQAModel(4092)
#     state_dict = torch.load("%s.pth" % model_dir)
#     model.load_state_dict(state_dict["model_state_dict"])
#     model = model.cpu()

#     while True:
#         filePath = 'E:/UoM/__Sem7/fyp/Project/PVQA0/data/pvqa/images/test/'
#         print('Enter image name (ex:- test_0001):')
#         img_id = input().strip()
#         imgnameParts=img_id.split("_")
#         if(imgnameParts[0]!="test"):
#             if(len(imgnameParts[1])!=4):
#                 print('Wrong image name..')

#         filePath+=img_id+".jpg"

#         image_fet = imgid2img[img_id]
#         feats = torch.tensor([image_fet['features']])
#         boxes = torch.tensor([image_fet['boxes']])

#         x = 'y'

#         while (x in ['y', 'Y']):
#             print('Enter a question:')
#             q = input().strip()

#             # predict and print max 5
#             with torch.no_grad():
                
#                 feats, boxes = feats.cpu(), boxes.cpu()

#                 sents = [q]
#                 targets = ['yes']

#                 logit = model(feats, boxes, sents, targets)
#                 score, label = logit.max(1)

#             print(label2ans[label])

#             print('Question about previous image? (y/n)')
#             x = input().strip()
