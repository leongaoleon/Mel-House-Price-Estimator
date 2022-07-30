import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
import pickle

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

# model
gb = GradientBoostingRegressor(learning_rate=0.25, max_depth=8, min_samples_leaf=5, min_samples_split=10)
scaler = StandardScaler()

onehot_pipeline = Pipeline([
    ('onehot', OneHotEncoder(drop='first'))
])

ordinal_pipeline = Pipeline([
    ('onehot', OrdinalEncoder())
])

scaler_pipeline = Pipeline([
    ('scaler', scaler)
])

transformer = ColumnTransformer([
    ('scaler', scaler_pipeline, ['Landsize', 'BuildingArea', 'age']),
    ('one_hot', onehot_pipeline, ['Type', 'Suburb', 'season']),
    ('ordinal', ordinal_pipeline, ['Distance'])
    
])
new_pipeline_gb = Pipeline([
    ('transformer', transformer),
    ('clf', gb)
])

X = housing.drop('Price', axis=1)
y = housing['Price']

new_pipeline_gb.fit(X, y)

pickle.dump(new_pipeline_gb, open('model.pkl','wb'))
model = pickle.load(open('model.pkl','rb'))