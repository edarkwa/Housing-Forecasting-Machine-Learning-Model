# -*- coding: utf-8 -*-
"""Fitting a machine learning model using scikitlearn .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Il0rOrHQHiZbD1xCAV5RHLhB5SkiZ3ug

#BUDT 737 Big Data and AI for Business- Spring 2022
Darkwa_Emma

references https://scikit-learn.org/stable/

Load the _house_price_regression.csv

Exploratory Data Analysis (EDA)
"""

import seaborn as sns 
import matplotlib 
import matplotlib.pyplot as plt
import sklearn
import pandas as pd
import io
from sklearn import preprocessing

from google.colab import files
uploaded = files.upload()

#dfHP=pd.read_csv(io.BytesIO(uploaded['HW1_house_price_regression.csv']))
#print(dfHP)

dfHP=pd.read_csv('HW1_house_price_regression.csv')
dfHP

"""# **Data Cleaning**


"""

# check for missing values in columns
total = dfHP.isnull().sum().sort_values(ascending=False)
total

"""Missing data"""

pct_null = dfHP.isnull().sum() / len(dfHP)
missing_features = pct_null[pct_null > 0.95].index
dfHP.drop(missing_features, axis=1, inplace=True)
dfHP
#in this code i'm asking for the variable with the most missing features which is above 0.95 to be dropped.

#reference
#https://stackoverflow.com/questions/45515031/how-to-remove-columns-with-too-many-missing-values-in-python

# display type and keys of dict
print("Type of %s dataset: %s" % ("dfHP", type(dfHP)))
print("Keys: %s" % dfHP.keys)
print("Keys: %s" % dfHP.keys())

"""Correlation"""

#Apply pandas.DataFrame.corr to analyze pairwise correlations of columns.
pd.set_option("display.max_columns", 0) 
pd.set_option("display.max_rows", 0) 
corr_matrix = dfHP.corr()
#  Print the pairwise correlations.
print(corr_matrix)
# Show pairwise correlations in colormap with colorbar.
plt.figure(figsize=(30,30))
sns.heatmap(corr_matrix,annot=True,cmap=plt.cm.CMRmap_r)
plt.title("Column Correlations")
plt.show()
#using correlation to know which features correlate with the target feature the most

# report data types of columns
dfHP.dtypes

#report descriptive statistics
dfHP.describe()

"""Analyzing the target

"""

dfHP.SalePrice.describe()

plt.figure(figsize=(10, 6))
sns.histplot(dfHP.SalePrice, kde=True, alpha=0.9)
#we can see the sale price is right skewed which means that the mean is 
#above the median, hence the distribution of sale price is postitivly skewed

print(f'Skewness: {dfHP.SalePrice.skew():.3f}')
print(f'Kurtosis: {dfHP.SalePrice.kurtosis():.3f}')

"""Handling categorical variables"""

#%pip install category_encoders
#import category_encoders as ce
#df2=dfHP.copy()
#encoder = ce.BinaryEncoder(cols=df2.columns)
#dfHP2=encoder.fit_transform(df2)
#print(dfHP2)

#reference 
#https://www.geeksforgeeks.org/conve

dfHP = pd.get_dummies(dfHP)
dfHP

dfHP.dropna(inplace=True)
dfHP

"""Clustering"""

import numpy as np
data=np.array(dfHP[["SalePrice","GrLivArea"]],dtype='f')

from scipy.cluster.vq import kmeans, vq
# compute k-means with k = 4 (4 clusters)
centroids,_ = kmeans(data,4)

index,_ = vq(data,centroids)

from matplotlib.pyplot import plot, show,title

plot(data[index==0,0],data[index==0,1], 'or',markersize=5) 
plot(data[index==1,0],data[index==1,1], 'ob',markersize=5) 
plot(data[index==2,0],data[index==2,1], 'om',markersize=5) 
plot(data[index==3,0],data[index==3,1], 'oy',markersize=5) 
plot(data[index==4,0],data[index==4,1], 'oc',markersize=5) 
plot(centroids[:,0],centroids[:,1],     'sg',markersize=8) 

#label axes and figure title
plt.title("4-means clustering between Ground Living Area  and Sale Price")
plt.xlabel("Sale Price($)")
plt.ylabel("Gr Living Area")
show()

"""# **Visualization**

Showing the distributions that were positively correlated with the target
"""

fig, ax = plt.subplots(5, 4, figsize=(20, 24))

sns.histplot(dfHP.SalePrice,       kde=True, alpha=0.9, ax=ax[0][0])
sns.countplot(dfHP.OverallQual,        palette='crest', ax=ax[0][1])
sns.histplot(dfHP.GrLivArea,       kde=True, alpha=0.9, ax=ax[0][2])
sns.countplot(dfHP.GarageCars,         palette='crest', ax=ax[0][3])

sns.histplot(dfHP.GarageArea,      kde=True, alpha=0.9, ax=ax[1][0])
sns.histplot(dfHP.TotalBsmtSF,     kde=True, alpha=0.9, ax=ax[1][1])
sns.histplot(dfHP ['1stFlrSF'],     kde=True, alpha=0.9, ax=ax[1][2])
sns.countplot(dfHP.FullBath,           palette='crest', ax=ax[1][3])

sns.countplot(dfHP.TotRmsAbvGrd,       palette='crest', ax=ax[2][0])
sns.histplot(dfHP.YearBuilt,       kde=True, alpha=0.9, ax=ax[2][1])
sns.histplot(dfHP.YearRemodAdd,    kde=True, alpha=0.9, ax=ax[2][2]) 
sns.countplot(dfHP.Fireplaces,         palette='crest', ax=ax[2][3])

sns.histplot(dfHP.BsmtFinSF1,      kde=True, alpha=0.9, ax=ax[3][0])
sns.histplot(dfHP.WoodDeckSF,      kde=True, alpha=0.9, ax=ax[3][1])
sns.histplot(dfHP['2ndFlrSF'],     kde=True, alpha=0.9, ax=ax[3][2])
sns.histplot(dfHP.OpenPorchSF,     kde=True, alpha=0.9, ax=ax[3][3])

sns.countplot(dfHP.HalfBath,           palette='crest', ax=ax[4][0])
sns.histplot(dfHP.LotArea,         kde=True, alpha=0.9, ax=ax[4][1])
sns.countplot(dfHP.BsmtFullBath,       palette='crest', ax=ax[4][2])
sns.histplot(dfHP.BsmtUnfSF,       kde=True, alpha=0.9, ax=ax[4][3])

#reference/citation
#https://dev.to/thalesbruno/subplotting-with-matplotlib-and-seaborn-5ei8

"""# Create training and Validation sets"""

#separate the predicting attribute into Y for model training 
y = dfHP.SalePrice
#separate the other attributes from the predicting attribute
x = dfHP.drop(['SalePrice'],axis=1)

#importing train_test_split from sklearn
from sklearn.model_selection import train_test_split
# split the data and target into training and validation sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 123)
# verify sizes
print("After:\nTraining Data = %s\nValidation Data = %s" % (y_train.shape, y_test.shape))
print("Training Target = %s\nValidation Target = %s" % (x_train.shape, x_test.shape))

"""# ML Modeling
Applying the model

Multiple Linear Regression (MLR)
"""

from sklearn.linear_model import LinearRegression
# create mlr model
mlr = LinearRegression()
# fit the training data
mlr.fit (x_train, y_train)
y_pred = mlr.predict(x_test)
y_pred_train = mlr.predict(x_test)

"""LinearRegression()

"""

# importing scaler to help normalize data
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.preprocessing import StandardScaler


scaler = StandardScaler()

x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

#reporting the RMSE and MSE
import math
pred=mlr.predict(x_train)
tr=(y_train)

MSE = mean_squared_error(tr,pred)
print("Mean Square Error for train:\n")
print (MSE)

RMSE = math.sqrt(MSE)
print("RMSE for train:\n")
print(RMSE)

#Reporting the coefficent, rs for both the training and validation data.
print("Coefficients = %s" % mlr.coef_)
print("Intercept = %f" % mlr.intercept_)
print("R2 for training = %.5f" % mlr.score(x_train, y_train))
print("R2 for validation = %.5f" % mlr.score(x_train, y_train))