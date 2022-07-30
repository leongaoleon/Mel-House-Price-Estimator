import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import mysql.connector as sql
import pickle
from datetime import date

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

# konfigurasi koneksi mySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'blueprint23'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_DB'] = 'melbourne'
app.config['MYSQL_PORT'] = 3306

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JSON_SORT_KEYS'] = False

# object untuk membuat koneksi terhadap mysql
mysql = MySQL(app)

# Preprocessing
def season(x):
    summer = [12,1,2]
    autumn = [3,4,5]
    winter = [6,7,8]
    spring = [9,10,11]
    if x in summer:
        return 'summer'
    elif x in autumn:
        return 'autumn'
    elif x in winter:
        return 'winter'
    elif x in spring:
        return 'spring'
    
def distance(y):
    if 0 < y <= 5:
        return 'very near'
    elif 5 < y <= 10:
        return 'near'
    elif 10 < y <= 15:
        return 'far'
    else:
        return 'very far'

housing = pd.read_csv('Melbourne_housing_FULL.csv')
housing = housing.dropna()
housing['age'] = 2020 - housing['YearBuilt']
housing = housing.drop(['Address', 'SellerG', 'Postcode', 'CouncilArea', 'Lattitude', 'Longtitude', 'Regionname', 'Propertycount', 'Bedroom2', 'YearBuilt'], axis=1)
housing['Date'] = pd.to_datetime(housing['Date'])
housing['month'] = housing['Date'].dt.month
housing['season'] = housing['month'].apply(season)
housing['Distance'] = housing['Distance'].apply(distance)
housing['Suburb'] = [x.lower() for x in housing['Suburb']]
housing.drop(['Method', 'Date'],axis=1, inplace=True)
r = housing[['Bathroom', 'Rooms', 'Type', 'Car', 'Suburb']]
housing = housing[r.replace(r.stack().value_counts()).gt(10).all(1)]


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    return render_template('index.html')


@app.route('/result', methods=['POST', 'GET'])
def result():   
        
    def season(x):
        summer = [12,1,2]
        autumn = [3,4,5]
        winter = [6,7,8]
        spring = [9,10,11]
        if x in summer:
            return 'summer'
        elif x in autumn:
            return 'autumn'
        elif x in winter:
            return 'winter'
        elif x in spring:
            return 'spring'


    def distance(suburb):

        near = housing[housing['Distance']=='near'].groupby('Suburb').count().index
        very_near = housing[housing['Distance']=='very near'].groupby('Suburb').count().index
        far = housing[housing['Distance']=='far'].groupby('Suburb').count().index
        very_far = housing[housing['Distance']=='very far'].groupby('Suburb').count().index

        if suburb in near:
            return 'near'
        elif suburb in very_near:
            return 'very near'
        elif suburb in far:
            return 'far'
        else:
            return 'very far'

    if request.method=='POST':
        input = request.form
        data = pd.DataFrame({
            'Suburb': [input['Suburb'].lower()],
            'Rooms': [input['Rooms']],
            'Type': [input['Type']],
            'Distance': [distance(str(input['Suburb']))],
            'Bathroom': [input['Bathroom']],
            'Car': [input['Car']],
            'Landsize': [input['Landsize']],
            'BuildingArea': [input['BuildingArea']],
            'age': [input['age']],
            'month': [input['month']],
            'season': [season(int(input['month']))],
    })

        if str(request.form.get('Suburb')).lower() in housing['Suburb'].values:
            prediction = model.predict(data)
            output = round(prediction[0],2)
            return render_template('index.html', prediction_text='Price should be $ {}'.format(output))
        else:
            return render_template('index.html', prediction_text='No Data of the suburb')

@app.route('/input_data', methods=['POST', 'GET'])
def input_data():
    if request.method == 'POST':

        form = request.form
        sql = f"INSERT INTO housing (`id`, `Suburb`, `Address`, `Rooms`, `Type`, `Price`, `Method`, `SellerG`, `Date`, `Distance`, `Postcode`, `Bedroom2`, `Bathroom`, `Car`, `Landsize`, `BuildingArea`, `YearBuilt`, `CouncilArea`, `Lattitude`, `Longtitude`, `Regionname`, `Propertycount`) VALUES (NULL, '{str(form['Suburb'])}', '{str(form['Address'])}', {str(form['Rooms'])}, '{str(form['Type'])}',  {str(form['Price'])}, '{str(form['Method'])}', '{str(form['SellerG'])}', '{str(form['Date'])}',{str(form['Distance'])}, {str(form['Postcode'])},{str(form['Bedroom2'])},{str(form['Bathroom'])},{str(form['Car'])},{str(form['Landsize'])},{str(form['BuildingArea'])}, {str(form['YearBuilt'])},'{str(form['CouncilArea'])}',{str(form['Lattitude'])},{str(form['Longtitude'])},'{str(form['Regionname'])}',{str(form['Propertycount'])})"
        cur = mysql.connection.cursor()
        cur.execute(sql)
        mysql.connection.commit()
        cur.close()
        return render_template('input_data.html', text='input data success')

    return render_template('input_data.html')

@app.route('/visualization', methods=['POST', 'GET'])
def visualization():
    return render_template('visual.html')

@app.route('/table', methods=['POST', 'GET'])
def table():
    connection = sql.connect(
        host = "localhost",
        port = "3306",
        user = "root",
        password = "blueprint23",
        database = "melbourne"
        )
    c = connection.cursor(buffered=True)
    query = 'select * from housing order by id desc limit 10;'
    c.execute(query)
    data = c.fetchall()
    return render_template('data.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)