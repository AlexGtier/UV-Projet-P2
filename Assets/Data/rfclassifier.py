# -*- coding: utf-8 -*-
"""RFClassifier.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1G2-ErRElBtSth4162tG5OwsVC4GdoJUL
"""

!pip install ipympl

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 

# %matplotlib widget

#inspired by https://towardsdatascience.com/hyperparameter-tuning-the-random-forest-in-python-using-scikit-learn-28d2aa77dd74

"""data = pd.read_excel('data.xlsx')
data.head()

X = data.iloc[:, 0:212].values #features
y = data.iloc[:, 212].values   #labels

np.save('X', X)
np.save('y', y)
"""

data = pd.read_excel('data.xlsx') 

X = data.iloc[:, 0:212].values #features 
y = data.iloc[:, 212].values #labels

np.save('X', X) 
np.save('y', y)

"""### Load Data + Analysis"""

X = np.load('X.npy')
y = np.load('y.npy')

fig = plt.figure()
_ = plt.hist(y)
plt.xlabel('Decision')
plt.ylabel('# Occurence')
plt.suptitle('Histogram of Decision')
plt.show()

## On vérifie que la distribution est "logique" 
# et ça se vérifie car plus grande distribution en 0 (donc ne rien faire) ok mais attention

#on peut normalizer les données ici

X[:,0] = (X[:,0]-X[:,0].min())/np.max(X[:,0] - X[:,0].min()) #position en x [0,1]
X[:,1] = (X[:,1]-X[:,1].min())/np.max(X[:,1] - X[:,1].min()) #position en y [0,1]
X[:,2] = X[:,2]/360 #degre -> [0 1]

d_max = np.max(X[:, 4::4]) #on prend tous les éléments de l'array qui correspondent à la distance et on calcule la distance max
X[:, 4::4] = X[:, 4::4]/d_max #distance entre [0 1]

# Ici on va vérifier qu'on ait pas des lignes totatement vide (donc non pertinentes pour un algo ML)
id_sup = []
fig = plt.figure()
for i in range(X.shape[1]):
    if X[:,i].min() == X[:,i].max(): #si max = min => pas de variation
        plt.plot(X[:,i], label='ligne : '+str(i))
        id_sup.append(i)
plt.show()
print("Il y a {} lignes vides sur les {}.".format(len(id_sup), i+1)) #aïe aïe

X = np.delete(X, id_sup, axis=1)

X.shape

"""### Random Forest"""

# import
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
cf = RandomForestClassifier(n_jobs=-1)

# Number of trees in random forest
n_estimators = [10, 100, 1000]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [10, 100]
max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 10]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Create the random grid
params_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

grid_search = GridSearchCV(estimator=cf, param_grid=params_grid, cv=5)
grid_search.fit(X, y)

"""## Save Model"""

import pickle

# Save to file in the current working directory
pkl_filename = "pickle_model.pkl"

with open(pkl_filename, 'wb') as file:
    pickle.dump(grid_search, file)