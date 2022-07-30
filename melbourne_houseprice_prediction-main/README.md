# Melbourne House Price Prediction
This final project is one of the requirements for graduating from Job Connector Data Science and Machine Learning Purwadhika Start-up and Coding School

<p align="center"  color="rgb(0, 90, 71)">
<h2>Problem Statement</h2>
</p>
<br>
We're gonna look into Melbourne House Price dataset available at <a href="https://www.kaggle.com/anthonypino/melbourne-housing-market" style="color:rgb(0, 90, 71) ;"><b>Kaggle</b></a> to see if there's spike in price as year passed. I place myself as Data Scientist working at startup company to help people looking for homes of their dreams by building end-to-end project to determine the price of house with certain characteristic such as Suburb area, Land Area, building Area, Distance from Centar Bussiness District, etc.
<br>
<h2> EDA </h2>
First we're gonna ask some question regarding house price in melbourne.
<br>
  - Does price of housing really goes as year passed?
 <br>
  - What factors most influence property prices in Melbourne?
  <br>
  - Does the time of year make any difference to the house price?
  <br>
  - Does distance of the house to the CBD affecting the selling and sales price of the house?
 <br>
<h2> Step of Work <h2>
<h3> 1. Preprocessing </h3>
We're not gonna use any of the Nan values rows because apparently there's many Nan values in BuildingArea and Yearbuilt column. BuildingArea and YearBuilt column definitely gonna affect the price of the house so we need to get rid of the Nan values and using only rows with valid values.
<br>
The column we will use for modelling is Suburb, Rooms, Type of building, Distance, Bathroom, Car, Landsize, BuildingArea and Date.
<h3> 2. Feature engineering </h3>
 I wil try add column that might be useful for predicting which is month and season from Date column and age from Yearbuilt. And after doing visualization based on price it is confirmed that our new column is indeed affecting the housing price in our data.
<h3> 3. Modelling </h3>
I started modelling with Linear model and do Gauss-Markov analysis of residual data to determine if linear model is applicable for our dataset. Turned out based on Gauss-Markov analysis, residual data does not meet our assumption, thus linear model is not applicable for our data.
 <br>
 <br> 
Second model is Random Forest, which is decision tree based ensemble algorithm and not affected by multicolinearity. Although we get faily acceptable test result of r2 with 0,75 but using training result, we get r2 point by 0,96 which is too much difference and i afraid that the model is overfitting. 
 <br>
 <br>
Third model i use is Gradient Boosting, which is also decision tree based ensemble algorithm and not affected by multicolinearity. And after training the data and hyperparameter tuning we get fairly good result by 0,80 and training score by 0,92.
<br>
<br>
<h3> 4. Performance evaluation </h3>
for performance evaluation, i use RMSE and r2 for metric performance. With, RMSE we get result of 294918.04, it means our predicted value can range within RMSE value. For example, if we get predicted value $ 1,000,000 the actual value may be range within $ 1,000,000 + $ 294,918 and $ 1,000,000 - $ 294,918. By using r2 it means how much of model can explained variance of the data. The perfect score would be 1, but as long as we get as close to 1 and by comparing different model we should get the best result.
<h3> 5. Validation Model </h3>
Doing validation model is very usefull to check the stability of the model that has made. I use KFold with 5 fold. And the result gives good stability for each fold. The following below is the result from validation model :
  
```
 R2 Scores : [0.78653393 0.7270442  0.78919657 0.73249267 0.77987211]
 ```
<br>

--------------------------------------------------------------------

<p align="center"  color="rgb(0, 90, 71)">
<h2>Dashboard</h2>
</p>
<br>

### Home Page :
<br>
<center><img src="https://github.com/baguszulfikar/melbourne_houseprice_prediction/blob/main/dashboard%20image/home.png" alt="" width="950" height="450"></center>
<br>

### Prediction Page :
<br>
<center><img src="https://github.com/baguszulfikar/melbourne_houseprice_prediction/blob/main/dashboard%20image/prediction.jpg" alt="" width="950" height="450"></center>
<br>

### Input raw data Page :
<br>
<center><img src="https://github.com/baguszulfikar/melbourne_houseprice_prediction/blob/main/dashboard%20image/input%20raw.jpg" alt="" width="950" height="450"></center>
<br>

### Visualization Page :
<br>
<center><img src="https://github.com/baguszulfikar/melbourne_houseprice_prediction/blob/main/dashboard%20image/visual.jpg" alt="" width="950" height="450"></center>
<br>

### Database Page :
<br>
<center><img src="https://github.com/baguszulfikar/melbourne_houseprice_prediction/blob/main/dashboard%20image/table.jpg" alt="" width="950" height="450"></center>
<br>
