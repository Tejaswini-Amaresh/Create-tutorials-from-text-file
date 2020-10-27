from flask import Flask, render_template,request,send_file,jsonify
from werkzeug.utils import secure_filename
import os
import summary_gen as sg
import question as ques
import create_video as cv
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = 'static/uploads'
app = Flask(__name__)
CORS(app, expose_headers=["x-suggested-filename"])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(80), unique=True,primary_key=True)
    password = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(80), nullable=False)

db.create_all()

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)

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
    x = sg.pptgen(text,summary,mapping,fname)
    ppt_path=x['ppt_path']
    pdf_path=x['pdf_path']
    print("xxxxxxx    ",pdf_path,"      xxxxxxx")
    cv.PPTtoPDF(ppt_path,pdf_path)
    return {'ppt_path':ppt_path, 'pdf_path':pdf_path}

@app.route('/return-files',methods=["GET"])
def return_files_tut():
    pptname=request.args.get("pptpath")
    result = send_file(pptname, as_attachment=True,conditional=False)
    return result

@app.route('/return-files1',methods=["GET"])
def return_files_tut1():
    pptname=request.args.get("pptpath")
    result = send_file(pptname,conditional=False)
    return result

@app.route('/users/register', methods=['POST'])
def register():
    username = request.get_json()['username']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    newuser= User()
    setattr(newuser,'username',username)
    setattr(newuser,'email',email)
    setattr(newuser,'password',password)
    db.session.add(newuser)
    db.session.commit()
    result = {
		'username' : username,
		'email' : email,
		'password' : password
	}

    return jsonify({'result' : result})
	

@app.route('/users/login', methods=['POST'])
def login():
    username = request.get_json()['username']
    password = request.get_json()['password']
    x=User.query.get(username)
    if x:
        if bcrypt.check_password_hash(x.password, password):
            access_token = create_access_token(identity = {'username': username,'email': x.email})
            result = access_token
        else:
            result = jsonify({"error":"Invalid username and password"})
    
    return result

@app.route('/assessments', methods=['POST'])
def assessments():
    print(request.get_json())
    text=request.get_json()['data']
    questions=ques.sentensify(text)
    return {'data':questions}

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
    

if __name__ == "__main__":
  app.run(debug=True)