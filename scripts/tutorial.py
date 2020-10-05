from flask import Flask, render_template,request
from werkzeug.utils import secure_filename
import os
import summary_gen as sg

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
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
def pptgen():
    #return "Hello"
    upload_file=request.files["Upload"]
    filename = secure_filename(upload_file.filename)
    if upload_file and allowed_file(upload_file.filename):
        upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        fname=filename.split(".")[0]+"_summary.pptx"
        vname=filename.split(".")[0]+"_summary.mp4"
        filename=app.config['UPLOAD_FOLDER']+"/"+filename
        text=readfile(filename)
        sg.processing(text,fname)
        return render_template("hello.html",context={"filename":fname,"Videoname":vname})
    else:
        return render_template("wrong_response.html")

if __name__ == "__main__":
  app.run(debug=True)