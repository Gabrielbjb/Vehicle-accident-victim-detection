from flask import * 
import os
from proses_image import proses_deteksi_kecelakaan

app = Flask(__name__ , static_folder='static')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static', 'uploads')

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/selesai',methods=['GET','POST'])   
def success():   
    if request.method == 'POST':  
        f = request.files['new-image'] 
        if f.filename == '': 
            f = request.files['new-image-button'] 
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(filepath)
        return redirect(url_for('display_image', filename=f.filename))

@app.route('/selesai/<filename>')
def display_image(filename):
    lokasi = f"{os.getcwd()}/static/uploads/{filename}"
    hasil = proses_deteksi_kecelakaan(lokasi.replace("\\","/"))
    print(filename)
    print("===================================================================")
    return render_template('selesai.html', filename=filename, judul=hasil[0], desk=hasil[1])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
