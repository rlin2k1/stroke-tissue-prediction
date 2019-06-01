""" sci-kit-template.py
This module is a template for the sci-kit learn library.

Models to Make:
- Linear Regression
- Logistic Regression
- K-Nearest Neighbors
- SVM
- Perceptron

Author(s):
    Roy Lin

Date Created:
    May 30th, 2019
"""
from sklearn import linear_model
from sklearn.tree import DecisionTreeClassifier # Decision Tree Model
from sklearn.ensemble import BaggingClassifier, GradientBoostingClassifier, RandomForestClassifier, ExtraTreesClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import NearestCentroid, KNeighborsRegressor, KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split # Split Data
from sklearn import preprocessing # Normalize the Data
from sklearn import metrics
from util import *

import argparse

def error(clf, X, y, ntrials=100, test_size=0.2) :
    """
    Computes the classifier error over a random split of the data,
    averaged over ntrials runs.

    Ntrials is Default at 100 Runs
    Train Size 80% Test 20%
    
    Args:
        clf (type): classifier
        X           -- numpy array of shape (n,d), features values
        y           -- numpy array of shape (n,), target classes
        ntrials     -- integer, number of trials
    Returns:
        (type): Description of return value(s)
        train_error -- float, training error
        test_error  -- float, test error
    """
    # ------------------------------------------------------------------------ #
    # Computes Cross - Validation Error Over N Trials
    # ------------------------------------------------------------------------ #
    train_error = 0
    test_error = 0
    for trial in range(ntrials):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=trial)
        clf.fit(X_train, y_train)
        y_pred_train = clf.predict(X_train)
        y_pred_test = clf.predict(X_test)
        train_error = train_error + metrics.accuracy_score(y_train, y_pred_train, normalize=True)
        test_error = test_error + metrics.accuracy_score(y_test, y_pred_test, normalize=True)
        
    train_error = train_error/float(ntrials)
    test_error = test_error/float(ntrials)

    return train_error, test_error


def write_predictions(y_pred, filename, yname=None) :
    """Write out predictions to csv file."""
    out = open(filename, 'wb')
    f = csv.writer(out)
    if yname :
        f.writerow([yname])
    f.writerows(zip(y_pred))
    out.close()

def main():
    # ---------------------------------------------------------------------------- #
    # Parse Command Line Arguments
    # ---------------------------------------------------------------------------- #
    parser = argparse.ArgumentParser(description="Machine Learning Model Comparisons.")

    parser.add_argument("request_descriptor", action="store", choices=['All', 'BaggingClassifier', 
    'GradientBoostingClassifier', 'LogisticRegression', 'MLPClassifier_ActivationIdentity', 
    'MLPClassifier_ActivationLogistic', 'MLPClassifier_TanH', 'MLPClassifier_Relu', 
    'NearestCentroid', 'KNeighborsRegressor', 'KNeighborsClassifier',
    'RadiusNeighborsClassifier', 'DecisionTree', 'RandomForest', 'ExtraTreesClassifier',
    'StochasticGradientDescent_Hinge', 'StochasticGradientDescent_Log', 
    'StochasticGradientDescent_Perceptron', 'StochasticGradientDescent_ModifiedHuber',
    'StochasticGradientDescent_SquaredHinge', 'SupportVectorMachine_LinearKernel',
    'SupportVectorMachine_RBFKernel', 'SupportVectorMachine_PolynomialKernel',
    'SupportVectorMachine_SigmoidKernel'], help="The identifier to indicate which model to test and train on.")
    args = parser.parse_args()
    # ------------------------------------------------------------------------ #
    # Load Stroke-MRI DataSet
    # ------------------------------------------------------------------------ #
    stroke = load_model_data("stroke_train.csv", header=1, predict_col=0)
    X = stroke.X; 
    Xname = stroke.Xnames
    y = stroke.y; 
    yname = stroke.yname

    n,d = X.shape # n = number of examples, d =  number of features

    normalized_X = preprocessing.scale(X)

    models = {
        'BaggingClassifier':BaggingClassifier(n_estimators=20),
        'GradientBoostingClassifier':GradientBoostingClassifier(n_estimators=300, max_depth=6, loss='exponential'),
        'LogisticRegression':linear_model.LogisticRegression(),
        'MLPClassifier_ActivationIdentity':MLPClassifier(activation='identity'),
        'MLPClassifier_ActivationLogistic':MLPClassifier(activation='logistic'),
        'MLPClassifier_TanH':MLPClassifier(activation='tanh'),
        'MLPClassifier_Relu':MLPClassifier(activation='relu'),
        'NearestCentroid':NearestCentroid(),
        'KNeighborsRegressor':KNeighborsRegressor(n_neighbors=5),
        'KNeighborsClassifier':KNeighborsClassifier(n_neighbors=5, weights='distance'),
        'RadiusNeighborsClassifier':RadiusNeighborsClassifier(radius=8, outlier_label=0, weights='uniform'),
        'DecisionTree':DecisionTreeClassifier(max_depth=None),
        'RandomForest':RandomForestClassifier(n_estimators=30),
        'ExtraTreesClassifier':ExtraTreesClassifier(n_estimators=30),
        'StochasticGradientDescent_Hinge':linear_model.SGDClassifier(loss='hinge'),
        'StochasticGradientDescent_Log':linear_model.SGDClassifier(loss='log'),
        'StochasticGradientDescent_Perceptron':linear_model.SGDClassifier(loss='perceptron'),
        'StochasticGradientDescent_ModifiedHuber':linear_model.SGDClassifier(loss='modified_huber'),
        'StochasticGradientDescent_SquaredHinge':linear_model.SGDClassifier(loss='squared_hinge'),
        'SupportVectorMachine_LinearKernel':SVC(kernel='linear'),
        'SupportVectorMachine_RBFKernel':SVC(kernel='rbf'),
        'SupportVectorMachine_PolynomialKernel':SVC(kernel='poly'),
        'SupportVectorMachine_SigmoidKernel':SVC(kernel='sigmoid'),
    }

    if(args.request_descriptor != 'All'):
        print("Classifying using Sci-Kit Learn",args.request_descriptor,"Classifier")
        dtc = models[args.request_descriptor]
        training_error_decision, testing_error_decision = error(dtc, normalized_X, y)
        print(args.request_descriptor, "Training Error:",str(training_error_decision))
        print(args.request_descriptor, "Testing Error: " + str(testing_error_decision))
    else:
        print("Testing All Classifiers")
        for key, value in models.items():
            print("Classifying using Sci-Kit Learn",key,"Classifier")
            dtc = value
            training_error_decision, testing_error_decision = error(dtc, normalized_X, y)
            print(args.request_descriptor, "Training Error:",str(training_error_decision))
            print(args.request_descriptor, "Testing Error: " + str(testing_error_decision))
            print("-----------------------------------------------------------")

if __name__ == "__main__":
    main()

"""
NOTE
We Only Need Label, Pixel Values for Training/Testing on Cross Validation.
After We Make the Model, Then We Have New CSVs for All the Pixels in 1 DICOM
File.
"""