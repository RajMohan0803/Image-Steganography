from flask import Flask,request,redirect,url_for,flash,render_template,send_from_directory
import uuid
import os
import stegano
IMAGES = os.path.join(os.getcwd(), "images")
HIDDEN = os.path.join(os.getcwd(), "hidden")


app = Flask(__name__)
@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method == "POST":
        file = request.files['file']
        secret = request.form['secret']
        password = request.form['pass']
        filename = str(uuid.uuid4()).replace("-",'')[:10]+"."+file.filename.split(".")[-1]
        srcPath = os.path.join(IMAGES,filename)
        file.save(srcPath)
        dstPath = str(uuid.uuid4()).replace("-",'')[:10]+"."+file.filename.split(".")[-1]
        stegano.hide(encryptionKey=password,secretMsg=secret,srcImgFile=srcPath,dstImgFile=os.path.join(HIDDEN,dstPath))
        return render_template('index.html',url=url_for('download_file',name=dstPath))
        return send_from_directory(os.getcwd(),dstPath,as_attachment=True)
    return render_template("index.html")

@app.route('/output/<name>')
def download_file(name):
    return send_from_directory(HIDDEN, name)

@app.route("/decode",methods=['GET','POST'])
def decode():
    if request.method == "POST":
        file = request.files['file']
        password = request.form['pass']
        filename = str(uuid.uuid4())+"."+file.filename.split(".")[-1]
        srcPath = os.path.join(IMAGES,filename)
        file.save(srcPath)
        test = stegano.find(decryptionKey=password,srcImgFile=srcPath)
        return render_template('decode.html',text=test)

    return render_template('decode.html')
if __name__ == "__main__":
    app.run(
        debug= True,
        port = 8080
    )
