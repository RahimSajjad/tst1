import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from data_preprocess import*
app = Flask(__name__)

model = pickle.load(open('finalized_model_neigh', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')
######################predict
#route for predict data
@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [x for x in request.form.values()]
    print(f"User Input features values :{int_features}")#
    try:
        heatId = int(int_features[0])
        print(f"User heatId[0] values :{heatId}")
        mat_list = int_features[1] #119--4545.9
        print(f"User mat_list[1] code values :{mat_list}")


    ##matcode,weight=mat_list.split('--')
    #print(f"matcode:{matcode}")
    #print(f"Weight:{weight}")
    #print(f"heatId:{heatId}")

        final_features = testing_data(heatId, mat_list, recp)   #making the input feature according to the feed of model
        print(f"heatId:{heatId}")
        print(f"mat_list: {mat_list}")
        print(f"Recp: {recp} \n")
        print(f"Final_features by def testing_data(heatId, mat_list, recp) :{final_features} \n")

        #f=[np.array(final_features)]
        #final=np.array(final_features)
        #readyforpred=np.delete(final,-1,1)
        #prediction = model.predict(readyforpred)

        prediction = model.predict(final_features)
        print(f"Prediction by model.predict(final_features) :{prediction}")#

        #output = get_result(heatId,prediction[0])

        #print(output)
        #print(recp)
        #output = get_result(prediction[0], heatId, temp_data)
        #print(output)
        #outputss = get_result(prediction[0], heatId, temp_data)

        return render_template('index.html', prediction_text='Defect type for the given input is {}'.format(prediction))
    except:
        return render_template('index.html', prediction_text='Error')
###################API
@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls through request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)
if __name__ == "__main__":
    app.run(debug=True)
