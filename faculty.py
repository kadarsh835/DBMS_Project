from flask import *
import os
app = Flask(__name__)
 
@app.route('/')  
def home():

    # Set template directory to main_app's Template Folder
    template_dir = os.path.join(os.path.dirname(__file__), 'main_app\\templates\\')
    app.template_folder = template_dir

    #Set styles directory to main_app's Static Folder
    static_dir = os.path.join(os.path.dirname(__file__), 'main_app\\static\\')
    app.static_folder = static_dir
    
    #return
    return render_template('home.html')

if __name__ == '__main__':  
   app.run(debug = True)