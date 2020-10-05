from flask import Flask, render_template,request,send_file
from werkzeug.utils import secure_filename
import os
import summary_gen as sg
from flask_cors import CORS, cross_origin

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
CORS(app, expose_headers=["x-suggested-filename"])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def readfile(filename):
    f=open(filename,'r')
    x=f.read()
    return x
 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("upload.html")
  
@app.route("/submit",methods=["POST"])
def summary_gen():
    #return "Hello"
    upload_file=request.files["Upload"]
    filename = secure_filename(upload_file.filename)
    if upload_file and allowed_file(upload_file.filename):
        upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        fname=filename.split(".")[0]+"_summary.pptx"
        vname=filename.split(".")[0]+"_summary.mp4"
        filename=app.config['UPLOAD_FOLDER']+"/"+filename
        text=readfile(filename)
        summary,mapping = sg.processing(text)
        return {'text':text,'summary':summary,'mapping':mapping,'fname':fname} #render_template("hello.html",context={"filename":fname,"Videoname":vname})
    else:
        return render_template("wrong_response.html")

@app.route("/ppt",methods=["POST"])
def pptgen():
    print(request)
    data=request.get_json()
    print(data)
    text=data['text1']
    summary=data['summary1']
    mapping=data['mapping']
    fname=data['fname']
    ppt_path = sg.pptgen(text,summary,mapping,fname)
    return {'ppt_path':ppt_path}

@app.route('/return-files',methods=["GET"])
def return_files_tut():
    pptname=request.args.get("pptpath")
    result = send_file(pptname, as_attachment=True,conditional=False)
    return result
    

if __name__ == "__main__":
  app.run(debug=True)