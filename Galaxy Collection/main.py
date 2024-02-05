from flask import *
from sklearn import *
from werkzeug.utils import secure_filename
import joblib
import matplotlib.pyplot as plt
clf = joblib.load('model.pkl') 
import numpy as np

host = "0.0.0.0"
app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

  
###
#@app.route('/uploader', methods = ['GET', 'POST'])
#def upload_file():
#   if request.method == 'POST':
#      f = request.files['file']
#      f.save(secure_filename(f.filename))
#      return 'file uploaded successfully'
###


# Load first 15 of each type
  
f = open('json_data.json')
galaxyData = json.load(f)

galaxyTypes = [];
galaxiesToDisplay = [];
count = 0;

for i in range(len(galaxyData)):
  if(galaxyData[i] not in galaxyTypes):
    galaxyTypes.append(galaxyData[i])
    count = 0
    galaxiesToDisplay.append({"galaxy":galaxyData[i],"index":i})
  else:
    if (count < 10):
      galaxiesToDisplay.append({"galaxy":galaxyData[i],"index":i})
      count+=1

#-------------------
#  HTML Insert for Galaxy Pictures
#-------------------
dataFilters = ""
imagesList = ""

for i in range(len(galaxyTypes)):
  dataFilters+=f'<li class="list" data-filter="{galaxyTypes[i]}">{galaxyTypes[i]}</li>'
  
for i in range(len(galaxiesToDisplay)):
  imagesList+=f'<div class="itemBox" data-item="{galaxiesToDisplay[i]["galaxy"]}"><img src="/images/{galaxiesToDisplay[i]["index"]}.jpeg" onclick="openPopup(this)>"</img></div>'
#-------------------

#-------------------
# Model Predictions Precalculated
#-------------------
"""
predicitons = [];

for i in range(len(galaxiesToDisplay)):
  pltImg = np.array([plt.imread(f'images/{galaxiesToDisplay[i]["index"]}.jpeg')])
  pltImg = pltImg.reshape((pltImg.shape[0], -1))
  prediction = clf.predict_proba(pltImg)[0]
  top_3_index = np.flip(np.argsort(prediction)[-3:])
  top_3_proba = prediction[top_3_index]
  labels = [];
  for k in range(3):
    labels.append(text_labels[top_3_index[k]])
  predicitons.append({"probabilities":top_3_proba,"labels":labels,"index":galaxiesToDisplay[i]["index"]})
  
#-------------------
"""

@app.route("/")
def main():
    return render_template('upload.html', dataFil = dataFilters,imgList=imagesList)

@app.route('/images/<path:filename>')
def serve_static(filename):
    return send_from_directory('images', filename)

app.run(host, debug=False)