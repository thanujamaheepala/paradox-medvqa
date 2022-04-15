# coding=utf-8

import base64
import pandas as pd
import pickle
import numpy as np
import torch
import json

#from tasks.pvqa_model import PVQAModel

baseUrl = 'D:/UoM/__Sem7/fyp/Project/PVQA0/'

generatedDataUrl = 'D:/1Projects/paradox-medvqa/backend/fasterrcnn/data/pvqa/val3.csv'

model_dir ="D:/UoM/__Sem7/fyp/Models/model_logit_fc_improved"

qaDataPath = 'D:/UoM/__Sem7/fyp/Project/PVQA/PathVQA/baselines/method1/saved/lxmert/'


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

def getDevData(split, imageName):
    jsonFile = qaDataPath+'pvqa_%s.json' % (split)
    results = []
    f = open(jsonFile)
    data = json.load(f)
    for datum in data:
        if(datum["img_id"]==imageName):
            for i in range(len(datum["sentf"]["pvqa"])):
                result ={}
                result['q'] = datum["sentf"]["pvqa"][i]
                result['a'] = list(datum["labelf"]["pvqa"][i].keys())[0]
                results.append(result)
            break
    f.close()
    return results

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
        newBoxes = temp.reshape(datum['num_boxes'], -1)
        newBoxes = newBoxes.copy()
        newBoxes[:, (0, 2)] /= datum['img_w']
        newBoxes[:, (1, 3)] /= datum['img_h']
        datum['boxes'] = newBoxes

        features = df['features'][i]
        buf = base64.b64decode(features[1:])
        temp = np.frombuffer(buf, dtype=np.float32)
        datum['features'] = temp.reshape(datum['num_boxes'], -1)

        data.append(datum)

    return data

def getDatum(imageName):
    [split,i] = imageName.split("_")
    i = int(i)
    tsv_file = baseUrl+'data/pvqa/images/%s%s.csv' % (split, '1')
    df = pd.read_csv(tsv_file, delimiter='\t', names=FIELDNAMES)
    result ={}
    w = df['image_w'][i]
    h = df['image_h'][i]
    result['num_boxes'] = df['num_boxes'][i]
    boxes = df['boxes'][i]
    buf = base64.b64decode(boxes[1:])
    temp = np.frombuffer(buf, dtype=np.float64).astype(np.float32)
    newBoxes = temp.reshape(result['num_boxes'], -1)
    newBoxes = newBoxes.copy()
    newBoxes[:, (0, 2)] /= w
    newBoxes[:, (1, 3)] /= h
    result['boxes'] = newBoxes
    features = df['features'][i]
    buf = base64.b64decode(features[1:])
    temp = np.frombuffer(buf, dtype=np.float32)
    result['features'] = temp.reshape(result['num_boxes'], -1)
    print(split,i)
    return result

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
        image_fet = getDatum(imageName)
        #image_fet = imgid2img[img_id]
        feats = torch.tensor([image_fet['features']])
        boxes = torch.tensor([image_fet['boxes']])
        #x=[[0.42870745062828064, 0.8027528524398804, 0.5035841464996338, 0.8730128407478333], [0.5356519222259521, 0.3737952709197998, 0.619545042514801, 0.45575541257858276], [0.30980637669563293, 0.043671395629644394, 0.4400382339954376, 0.16920115053653717], [0.3398924767971039, 0.3686801791191101, 0.4383499026298523, 0.44426628947257996], [0.7550418376922607, 0.29634469747543335, 0.8526651263237, 0.38381078839302063], [0.7719050049781799, 0.7284417748451233, 0.8532600402832031, 0.8178581595420837], [0.19592757523059845, 0.5504931211471558, 0.25883254408836365, 0.6280836462974548], [0.4356710910797119, 0.3120732605457306, 0.5300268530845642, 0.3757137358188629], [0.1113203838467598, 0.6665712594985962, 0.15926416218280792, 0.7191407680511475], [0.912814199924469, 0.2462512105703354, 0.9892672300338745, 0.3156096339225769], [0.6942574381828308, 0.21822653710842133, 0.7687147855758667, 0.292035311460495], [0.10931017249822617, 0.10623438656330109, 0.17678630352020264, 0.1899186074733734], [0.4338819086551666, 0.5172147750854492, 0.5089320540428162, 0.5907399654388428], [0.06269052624702454, 0.016377247869968414, 0.9640729427337646, 0.912826418876648], [0.2391432672739029, 0.5432127714157104, 0.40321192145347595, 0.7679009437561035], [0.890274167060852, 0.8614845275878906, 0.9514532089233398, 0.9411722421646118], [0.1722627729177475, 0.6330573558807373, 0.23883773386478424, 0.7000097036361694], [0.6518767476081848, 0.8496911525726318, 0.7371088862419128, 0.9227791428565979], [0.500993013381958, 0.6266785264015198, 0.7273868918418884, 0.8361244797706604], [0.05356789752840996, 0.040531061589717865, 0.4729466140270233, 0.37414878606796265], [0.6640874147415161, 0.34379300475120544, 0.7328667044639587, 0.41217008233070374], [0.34844955801963806, 0.5035748481750488, 0.4231318533420563, 0.580455482006073], [0.2372569739818573, 0.175831139087677, 0.4534211754798889, 0.35268038511276245], [0.25889211893081665, 0.5392387509346008, 0.40508562326431274, 0.7644274830818176], [0.019167887046933174, 0.05262110382318497, 0.9720558524131775, 0.9353787302970886], [0.46531063318252563, 0.49700215458869934, 0.8204541206359863, 0.8769106268882751], [0.8959102630615234, 0.7224257588386536, 0.9753996133804321, 0.7968845963478088], [0.0, 0.004591057077050209, 0.9983332753181458, 0.7180605530738831], [0.25561192631721497, 0.7017958760261536, 0.3072853088378906, 0.75636225938797], [0.7607050538063049, 0.0028635391499847174, 0.9853459596633911, 0.18142957985401154], [0.18968896567821503, 0.5473822951316833, 0.26221221685409546, 0.6309423446655273], [0.6487547159194946, 0.2764231562614441, 0.869713306427002, 0.4395729899406433], [0.12047036737203598, 0.03029019385576248, 0.9785342216491699, 0.8662253618240356], [0.04626569151878357, 0.45675861835479736, 0.4567093551158905, 0.9134964346885681], [0.16367946565151215, 0.6265455484390259, 0.25080451369285583, 0.7038748860359192], [0.30757471919059753, 0.8417203426361084, 0.36942169070243835, 0.9097743630409241]]
        # boxes=torch.tensor(x)
        # a = feats.tolist()
        #b = boxes.tolist()
        # with open('feats.txt', 'w') as f:
        #     f.write(str(a))
        # with open('boxes.txt', 'w') as f:
        #     f.write(str(b))
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
    # print(logit)
    # print(logit2)
    # print(label)
    # print(score)
    # print(label2)
    # print(score2)
    return answer,round(score2.item(), 4) 

def getLable2Ans():
    label2ans = pickle.load(
        open(baseUrl+'data/pvqa/qas/trainval_label2ans.pkl', 'rb'))
    #print(label2ans)
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
