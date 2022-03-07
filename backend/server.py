import os
from flask import current_app
from flask import Flask, flash, request, redirect, url_for, session,jsonify
from werkzeug.utils import secure_filename
import flask_cors
import logging
import pvqa_simulate as PVQA
from param import args

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

 

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = '345435243535435'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

model = PVQA.getModel()
label2ans = PVQA.getLable2Ans()
imgid2img = PVQA.loadData()

@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER)
    if not os.path.isdir(target):
        os.mkdir(target)
    
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    destination="/".join([target, "image.jpg"])
    file.save(destination)
    response="Uploaded"
    return response

@app.route('/predict', methods=['POST'])
def predict(): 
    question = request.form['question']
    filename = request.form['filename']
    imagename = filename.strip().split(".")[0]
    answer,score = PVQA.predict(model, label2ans, imagename, question, imgid2img)

    return answer

if __name__ == "__main__":
    if args.run:
        app.run(debug=True,host="0.0.0.0",use_reloader=False)
        
    
    

flask_cors.CORS(app, expose_headers='Authorization')