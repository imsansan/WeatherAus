import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder 
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import roc_curve as ROC
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score
import warnings
warnings.filterwarnings("ignore")


def dataWash(city, path: str):
    weather = pd.read_csv(path)
    
    X = weather.iloc[:,:-1]
    Y = weather.loc[:,("Location","RainTomorrow")]
    X = X.loc[X.loc[:,"Location"] == city]
    Y = Y.loc[Y.loc[:,"Location"] == city]
    Y =Y.drop(['Location'], axis=1)
    X =X.drop(['Location'], axis=1)
    
    #get month
    X["Date"] = X["Date"].apply(lambda x:int(x.split("/")[1])) 
    X = X.rename(columns={"Date":"Month"})

    #fill Null object-data up with most frequent value
    cate = X.columns[X.dtypes == "object"].tolist()
    si = SimpleImputer(missing_values=np.nan,strategy="most_frequent")
    si.fit(X.loc[:,cate])
    X.loc[:,cate] = si.transform(X.loc[:,cate])

    #encode object data
    oe = OrdinalEncoder()
    oe = oe.fit(X.loc[:,cate])
    X.loc[:,cate] = oe.transform(X.loc[:,cate])
    
    oe = oe.fit(Y.loc[:,:])
    Y.loc[:,:] = oe.transform(Y.loc[:,:])


    #fill float data up with mean value.
    col = X.columns[X.dtypes == "float64"].tolist()
    impmean = SimpleImputer(missing_values=np.nan,strategy = "mean")
    impmean = impmean.fit(X.loc[:,col])
    X.loc[:,col] = impmean.transform(X.loc[:,col])
    
    return X, Y
    


def Solution(city, Xt, Yt):

    Xtrain, Xtest, Ytrain, Ytest = train_test_split(Xt,Yt,test_size=0.3)
    
    Xreal, Yreal = dataWash(city, '%s.csv' % (city))
    print(Xreal)
    print(Yreal)
    
    for i in [Xtrain,Xtest,Ytrain,Ytest]: 
        i.index = range(i.shape[0])
    
    clf = LogisticRegression()
    clf.fit(Xtrain, Ytrain.values.ravel())

    result = clf.predict(Xtest)
    score = clf.score(Xtest,Ytest.values.ravel())
    recall = recall_score(Ytest.values.ravel(), result)
    auc = roc_auc_score(Ytest.values.ravel(),clf.decision_function(Xtest))
    #print("LR's testing accuracy %f, recall is %f, auc is %f" % (score,recall,auc))
    
    #print(clf.predict(Xreal))
    #print(clf.score(Xtrain, Ytrain.values.ravel()))
    '''
    #draw ROC curve
    FPR, Recall, thresholds = ROC(Ytest,clf.decision_function(Xtest),pos_label=1)
    area = roc_auc_score(Ytest,clf.decision_function(Xtest))
    plt.figure()
    plt.plot(FPR, Recall, color='red',
             label='ROC curve (area = %0.2f)' % area)
    plt.plot([0, 1], [0, 1], color='black', linestyle='--')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('Recall')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()
    '''
    #report
    #print(classification_report(Ytest.values.ravel(), result))
    


