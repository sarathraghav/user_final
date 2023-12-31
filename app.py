from flask import Flask, render_template, request, app, jsonify, url_for, redirect
import pickle
import numpy as np

app = Flask(__name__)

clf0 = pickle.load(open("lrclfmodel.pkl","rb"))
clf1 = pickle.load(open("nbclfmodel.pkl","rb"))
clf2 = pickle.load(open("svmclfmodel.pkl","rb"))
clf3 = pickle.load(open("knnclfmodel.pkl","rb"))
clf4 = pickle.load(open("dtclfmodel.pkl","rb"))
clf5 = pickle.load(open("rfclfmodel.pkl","rb"))

reg0 = pickle.load(open("life_insurance_predictionlr.pkl","rb"))
reg1 = pickle.load(open("life_insurance_predictionsvm.pkl","rb"))
reg2 = pickle.load(open("life_insurance_predictionrf.pkl","rb"))
reg3 = pickle.load(open("life_insurance_predictiongr.pkl","rb"))


users = {'buvan':'buvan','sarath':'sarath','chaitanya':'chaitanya'}

# signup route
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # create new user
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        # redirect to login page
        return redirect(url_for('login'))
    # render signup form
    return render_template('signup.html')

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # check if user exists and password is correct
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            # redirect to welcome page
            return redirect(url_for('welcome', username=username))
        # if login fails, render login form with error message
        error = 'Invalid username or password'
        return render_template('login.html', error=error)
    # render login form
    return render_template('login.html')

# welcome route
@app.route('/welcome/<username>')
def welcome(username):
    # render welcome page with username
    return render_template('main.html', username=username)


@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':

        age = int(request.form['age'])
        sex = request.form.get('sex')
        cp = request.form.get('cp')
        trestbps = int(request.form['trestbps'])
        chol = int(request.form['chol'])
        fbs = request.form.get('fbs')
        restecg = int(request.form['restecg'])
        thalach = int(request.form['thalach'])
        exang = request.form.get('exang')
        oldpeak = float(request.form['oldpeak'])
        slope = request.form.get('slope')
        ca = int(request.form['ca'])
        thal = request.form.get('thal')
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = request.form.get('smoker')
        region = request.form.get('region')
        mobile = request.form.get('mobile')
        model1 = request.form.get('model1')
        model2 = request.form.get('model2')
        
        
        data1 = np.array([[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])
        data2 = np.array([[age,sex,bmi,children,smoker,region]]).reshape(1,-1)
        m1 = 0
        m2 = 0

        if m1==0:
             my_prediction1 = clf4.predict(data1)
        
        if m2==0:
             my_prediction2 = reg3.predict(data2)[0]
             my_prediction3 = "(Accuarcy:87.8%)"
             
         
        from twilio.rest import Client
  
        # Your Account Sid and Auth Token from twilio.com / console
        account_sid = 'ACab5818a9b3b8af6f717b6c4ee2e948f8'
        auth_token = '8937a62fcb5aaab42bc1bdb97b68f0b8'
        if(my_prediction1==1):
  
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                                from_='+15077040615',
                                body ='You have chances of heart disease.Please consult a doctor at the earliest',
                                to =mobile
                            )
            
        elif(my_prediction1==0):
  
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                                from_='+15077040615',
                                body ='Congratulations You do not have major chances of heart disease',
                                to =mobile
                            )
        return render_template('result.html', prediction1=my_prediction1,prediction3=my_prediction3,prediction_text = "The cost of health insurance per year is {}").format(my_prediction2)
        
        

        
@app.route('/clickhere')
def clickhere():
     return render_template('k.html')

@app.route('/algorithms')
def algorithms():
     return render_template('algorithms.html')


@app.route('/details')
def index():
    return render_template('k.html')





@app.route('/back')
def back():
     return render_template('main.html')

@app.route('/Back')
def Back():
     return render_template('k.html')

@app.route('/logout')
def logout():
     return render_template('thank.html')
if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')