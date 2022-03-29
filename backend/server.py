import os
from flask import current_app
from flask import Flask, flash, request, redirect, url_for, session,jsonify
from werkzeug.utils import secure_filename
import flask_cors
import logging
import pvqa_simulate as PVQA
from param import args
import shutil

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

 

UPLOAD_FOLDER = 'uploads'
UPLOAD_FOLDER_RCNN = 'fasterrcnn/data/pvqa/val'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = '345435243535435'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = PVQA.getModel()
label2ans = PVQA.getLable2Ans()
imgid2img = PVQA.loadData()
dataType = "pvqa"

@app.route('/upload', methods=['POST'])
def fileUpload():
    global dataType
    target=os.path.join(UPLOAD_FOLDER)
    target2=os.path.join(UPLOAD_FOLDER_RCNN)
    if not os.path.isdir(target):
        os.mkdir(target)
    
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    destination="/".join([target, "image.jpg"])
    destination2="/".join([target2, "val_0000.jpg"])
    file.save(destination)
    shutil.copyfile(destination, destination2)

    imageName = filename.strip().split(".")[0]
    try:
        (split, id) = imageName.strip().split('_')

        if((split in ["val","train","test"]) and (len(id)==4)):
            dataType = "pvqa"
        else:
            dataType="other"
    except ValueError:
        dataType="other"

    if(dataType!="pvqa"):
        os.chdir('fasterrcnn')
        cmd = "bash run_bccd2.sh"
        returned_value = os.system(cmd)
        os.chdir('../')

    response="Uploaded"
    return response

@app.route('/predict', methods=['POST'])
def predict():
    global dataType
    question = request.form['question']
    filename = request.form['filename']
    imagename = filename.strip().split(".")[0]
    answer,score = PVQA.predict(model, label2ans, imagename, question, imgid2img, dataType)

    return answer+" ---> "+str(score)+"%"

if __name__ == "__main__":
    if args.run:
        app.run(debug=True,host="0.0.0.0",use_reloader=False)
        
    
    

flask_cors.CORS(app, expose_headers='Authorization')