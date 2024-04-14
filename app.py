from flask import Flask , render_template, request, make_response, redirect, session, jsonify , url_for
import pickle 
import numpy as np
import pandas as pd

# Create an instance of the Flask class
app = Flask(__name__)
app.secret_key="MYMACHINELEARNINGPROJECT"
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)
    
features = ['Logical quotient rating', 'coding skills rating', 'hackathons', 'public speaking points',
            'self-learning capability?', 'Extra-courses did', 'Taken inputs from seniors or elders',
            'worked in teams ever?', 'Introvert', 'reading and writing skills', 'memory capability score']

# Define a route and a function to handle requests to that route
@app.route('/', methods = ['GET','POST'])
def index():
    if 'name' in session:
        name = session['name']
        return redirect(url_for('careerPrediction', Name=name))
        
    
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        contact = request.form.get('contact')
        print("Details :: ",name, email, contact, sep=" ")

        # Set a cookie with the data
        session["name"] = name
        session["email"] = email 
        session["contact"] = contact
        return redirect(url_for('careerPrediction', Name=name))
    return render_template("index.html")


@app.route('/careerPrediction', methods = ['GET','POST'])
def careerPrediction():
    # Step 1: Grab the data from the cookies and check whether it is empty or not
    # If it is empty, return to 
    name = session["name"]
    print("Name := ",name)
    if name is None :
         response = make_response("Name is empty, please fill out the personal details first!")
         return redirect("/",Response=response)
         
    # Step 2: Get the data from the form as we did in index.html page
    if request.method == "POST":
        form_data = request.form
        print("FORM: ",form_data)
        input_data = pd.DataFrame({feature: [form_data[feature]] for feature in features})
        
        # Convert categorical inputs (yes/no, poor/medium/excellent) to numerical encodings
        input_data['self-learning capability?'] = input_data['self-learning capability?'].map({'yes': 1, 'no': 0})
        input_data['Extra-courses did'] = input_data['Extra-courses did'].map({'yes': 1, 'no': 0})
        input_data['Taken inputs from seniors or elders'] = input_data['Taken inputs from seniors or elders'].map({'yes': 1, 'no': 0})
        input_data['worked in teams ever?'] = input_data['worked in teams ever?'].map({'yes': 1, 'no': 0})
        input_data['Introvert'] = input_data['Introvert'].map({'yes': 1, 'no': 0})
        input_data['reading and writing skills'] = input_data['reading and writing skills'].map({'poor': 0, 'medium': 1, 'excellent': 2})
        input_data['memory capability score'] = input_data['memory capability score'].map({'poor': 0, 'medium': 1, 'excellent': 2})
        
        prediction = model.predict(input_data)
        return render_template("career_prediction.html" , pred=prediction[0])    
    
    # Step 4: Render the template using the data and search for jinja template tagging, otherwise ask me!
    return render_template("career_prediction.html",Name=name)


@app.route('/logout',methods=["POST"])
def logout():
     for key in list(session.keys()):
        session.pop(key)
     return redirect(url_for('index'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
