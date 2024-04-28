import pandas as pd
from flask import Flask, render_template, request
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
import pickle
import random

app = Flask(__name__)

# Load the regression model
with open('model4.pkl', 'rb') as f:
    model = pickle.load(f)

# Load the scaler
with open('smallscaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the form inputs
        sponsor_name = request.form['sponsor_name']
        package_cost = float(request.form['package_cost'])
        branding = "branding" if('Branding' in request.form.getlist('records')) else ""
        advertising = "Advertising" if('Advertising' in request.form.getlist('records')) else ""
        hospitality = "Hospitality" if('Hospitality' in request.form.getlist('records')) else ""
        workshops = "Workshops" if('Workshops' in request.form.getlist('records')) else ""
        sales_lift = float(request.form['sales_lift'])
            
        sales_package_benefits = " ".join([branding, advertising, hospitality, workshops])
        df = pd.DataFrame([[sponsor_name, package_cost, sales_package_benefits, sales_lift]], columns=['sponsor_name', 'package_cost', 'sales_package_benefits', 'sales_lift'])
        for feature in ['sponsor_name', 'package_cost', 'sales_package_benefits', 'sales_lift']:
            labels_ordered=df[feature].value_counts().index
            labels_ordered={k:i for i,k in enumerate(labels_ordered,0)}
            df[feature]=df[feature].map(labels_ordered)
        # Preprocess the inputs
        # Scale the input
        scaled_input = scaler.transform(df.iloc[0].values.reshape(1, -1))
        X = pd.DataFrame(scaled_input).T
        # Make the prediction
        prediction = model.predict(X)[0]
        return render_template('index.html', prediction=prediction)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)