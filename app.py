# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
import pandas as pd
from wsgiref import simple_server

app = Flask(__name__)  # initializing a flask app


@app.route('/',methods=['GET','POST'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/predict',methods=['POST'])  # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the userx
            gender = request.form['gender']

            if gender == 'Male':
                gender = 0
            else:
                gender= 1
            company_type= request.form['company_type']

            if company_type == 'Service':
                company_type =1
            else:
                company_type =0
            wfh_setup_avail =request.form['wfh_setup_avail']

            if wfh_setup_avail == 'Yes':
                wfh_setup_avail = 1
            else:
                wfh_setup_avail = 0
            Designation = int(request.form['Designation'])

            if Designation==0:
                Designation_0 = 1
                Designation_1 = 0
                Designation_2 = 0
                Designation_3 = 0
                Designation_4 = 0
                Designation_5 = 0
            elif Designation==1:
                Designation_0 = 0
                Designation_1 = 1
                Designation_2 = 0
                Designation_3 = 0
                Designation_4 = 0
                Designation_5 = 0
            elif Designation==2:
                Designation_0 = 0
                Designation_1 = 0
                Designation_2 = 1
                Designation_3 = 0
                Designation_4 = 0
                Designation_5 = 0
            elif Designation==3:
                Designation_0 = 0
                Designation_1 = 0
                Designation_2 = 0
                Designation_3 = 1
                Designation_4 = 0
                Designation_5 = 0
            elif Designation==4:
                Designation_0 = 0
                Designation_1 = 0
                Designation_2 = 0
                Designation_3 = 0
                Designation_4 = 1
                Designation_5 = 0
            else:
                Designation_0 = 0
                Designation_1 = 0
                Designation_2 = 0
                Designation_3 = 0
                Designation_4 = 0
                Designation_5 = 1

            Quarter = int(request.form['Quarter'])

            if Quarter==1:
                Quarter_1=1
                Quarter_2=0
                Quarter_3=0
                Quarter_4=0
            elif Quarter==2:
                Quarter_1 = 0
                Quarter_2 = 1
                Quarter_3 = 0
                Quarter_4 = 0
            elif Quarter==3:
                Quarter_1 = 0
                Quarter_2 = 0
                Quarter_3 = 1
                Quarter_4 = 0
            else:
                Quarter_1 = 0
                Quarter_2 = 0
                Quarter_3 = 0
                Quarter_4 = 1
            Season = request.form['Season']
            if Season=='Autumn':
                Season_Autumn=1
                Season_Spring=0
                Season_Summer=0
                Season_Winter=0
            elif Season=='Spring':
                Season_Autumn = 0
                Season_Spring = 1
                Season_Summer = 0
                Season_Winter = 0
            elif Season == 'Summer':
                Season_Autumn = 0
                Season_Spring = 0
                Season_Summer = 1
                Season_Winter = 0
            else:
                Season_Autumn = 0
                Season_Spring = 0
                Season_Summer = 0
                Season_Winter = 1
            mon_of_join=int(request.form['mon_of_join'])
            men_fatigue_score=float(request.form['men_fatigue_score'])
            res_al=int(request.form['res_al'])
            dict_pred={
                'gender': gender,
                'company_type': company_type,
                'wfh_setup_avail': wfh_setup_avail,
                'Designation': Designation,
                'res_al': res_al,
                'men_fatigue_score': men_fatigue_score,
                'mon_of_join': mon_of_join,
                'Designation_0': Designation_0,
                'Designation_1': Designation_1,
                'Designation_2': Designation_2,
                'Designation_3': Designation_3,
                'Designation_4': Designation_4,
                'Designation_5': Designation_5,
                'Quarter_1': Quarter_1,
                'Quarter_2': Quarter_2,
                'Quarter_3': Quarter_3,
                'Quarter_4': Quarter_4,
                'Season_Autumn': Season_Autumn,
                'Season_Spring': Season_Spring,
                'Season_Summer': Season_Summer,
                'Season_Winter': Season_Winter
                }
            with open("standardScalar.sav", 'rb') as f:
                scalar = pickle.load(f)
            with open("modelForPrediction.sav", 'rb') as f:
                model = pickle.load(f)
                data_df = pd.DataFrame(dict_pred, index=[1, ])
                predict_text = model.predict(data_df)
                output=round(predict_text[0]*100, 2)
                if output >80:
                    text= "Your Burnout Score = "+str(output)+ " ----VERY BAD"
                    return render_template('result.html', prediction_text=text)
                elif (output>50) and (output<80):
                    text= "Your Burnout Score = "+str(output)+ " ----FAIR"
                    return render_template('result.html', prediction_text=text)
                elif (output>20) and (output<50):
                    text= "Your Burnout Score = "+str(output)+" ----GOOD"
                    return render_template('result.html', prediction_text=text)
                else:
                    text = "Your Burnout Score = " + str(output) + " ----EXCELLENT"
                    return render_template('result.html', prediction_text=text)

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)