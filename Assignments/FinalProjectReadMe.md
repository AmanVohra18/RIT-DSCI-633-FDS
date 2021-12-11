# Problem Statement

## Creating a classifier to identify if a job posting is fraudulent.

# Project Working


1. Data Cleaning.
2. Data Exploration.
3. Model Building
4. Evaluation by means of appropriate metrics.
5. Model Comparison.



# Data

The data for this project was taken from Kaggle. The original size is 17880 rows by 18 columns.

# Dependencies

 re

 time

 numpy

 pandas

 nltk

 sklearn

# Modeling 

I chose four different models to test out:
1. Naive Bayes
2. K-Nearest Neighbor
3. Passive Aggressive Classifier
Each model was hyperparameter tuned using GridSearchCV and a 5 fold cross validation.

Data was Resampled using SmoteTomek then a model was trained again. 
4. Random Forest Classifier

# Result


The performance of all the models were all quite good. KNN and PAC performed similarly, Naive Bayes performed very well too. When treated with resampled data, Random Forest turned out to be the best performing model. 






                    Naive Bayes      PAC       KNN     Random 
                                                       Forest

      Accuracy         0.98      0.99      0.98      1.0      
       
       Precision        0.89      0.88      0.82      1.0
  
      Recall           0.58      0.76      0.80      0.99



# Future Work

For Future work, I would like to work on making this project from being machine learning based to deep learning based.I would like to further work on the imbalance of data. I would like to work on training models like XGBoost and the Decision Tree Classifier. Also, instead of using TF-IDF for preprocessing, I would like to explore word embedding techniques with tools like Word2Vec.


```python

```
