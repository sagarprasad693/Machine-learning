#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


dataset = pd.read_csv('https://raw.githubusercontent.com/edyoda/data-science-complete-tutorial/master/Data/HR_comma_sep.csv.txt')


# In[4]:


dataset.head()


# In[5]:


X = dataset.drop(columns=['left'])
y = dataset.left


# In[6]:


float_data = X.select_dtypes(include=['float'])
int_data = X.select_dtypes(include=['int64'])
obj_data = X.select_dtypes(include=['object'])


# In[7]:


from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OrdinalEncoder, MinMaxScaler, OneHotEncoder
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestClassifier


# In[8]:


int_pipeline = make_pipeline(MinMaxScaler(),SelectKBest(k=4, score_func=f_classif))
obj1_pipeline = make_pipeline(OneHotEncoder())
obj2_pipeline = make_pipeline(OrdinalEncoder())


# In[10]:



preprocessor = make_column_transformer(
                (int_pipeline, int_data.columns),
                (obj1_pipeline, ['sales']),
                (obj2_pipeline, ['salary']),                
                 remainder = 'passthrough'
                )


# In[11]:


master_pipeline = make_pipeline(preprocessor, RandomForestClassifier(n_estimators = 100))


# In[12]:



from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)


# In[13]:


master_pipeline.fit(X_train, y_train)

y_pred = master_pipeline.predict(X_test)
print(master_pipeline.score(X_test, y_test))

print(master_pipeline.steps[0][1].transformers)


# In[ ]:


from sklearn.model_selection import GridSearchCV
params = {'columntransformer__pipeline-1__selectkbest__k': [2, 3, 4],
          'randomforestclassifier__n_estimators': [100, 120, 140]}
gs = GridSearchCV(master_pipeline, param_grid = params, cv = 4)
gs.fit(X_train, y_train)


# In[ ]:


print(gs.best_params_)
print(gs.score(X_test, y_test))


# In[ ]:




