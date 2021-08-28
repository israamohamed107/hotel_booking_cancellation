from flask import Flask,render_template ,request
import joblib

model = joblib.load('model.pkl')
scaler= joblib.load('scaler.pkl')

lst=[]

app = Flask(__name__)


@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict',methods=['GET'])
def predict():
    lst.append(int(request.args.get('lead_time')))
    lst.append(int(request.args.get('arrival_date_week_number')))
    lst.append(int(request.args.get('arrival_date_day_of_month')))
    lst.append(int(request.args.get('stays_in_week_nights')))
    lst.append(int(request.args.get('previous_cancellations')))
    lst.append(float(request.args.get('adr')))
    lst.append(int(request.args.get('required_car_parking_spaces')))
    lst.append(int(request.args.get('total_of_special_requests')))
    lst.append(int(request.args.get('reservation_status_day')))
    lst.append(int(request.args.get('reservation_status_month')))
    
    market_segment=request.args.get('market segment')
    if market_segment=='Groups':
        lst.append(1)
    else:
        lst.append(0)
    deposit_type=request.args.get('deposit_type')

    if deposit_type=='Non Refund':
        lst.append(1)
    else:
        lst.append(0)

    prediction=model.predict(scaler.transform([lst]))[0]

    if prediction:
        return render_template('index.html', pred='This Guest will cancel the reservation')
    else:
        return render_template('index.html', pred='This Guest will not cancel the reservation')


if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1')

