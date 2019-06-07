""" classify_voxels.py
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

# ---------------------------------------------------------------------------- #
# Import Statements for the Necessary Packages
# ---------------------------------------------------------------------------- #
from sklearn import linear_model
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier, GradientBoostingClassifier, RandomForestClassifier, ExtraTreesClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import NearestCentroid, KNeighborsRegressor, KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.svm import SVC

from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn import metrics
from utilities import *

import matplotlib.pyplot as plt
import numpy as np
from inspect import signature

from joblib import dump, load
import time
import argparse

def error(clf, X, y, ntrials=50, test_size=0.2):
    """
    Computes the classifier error over a random split of the data, averaged over
    ntrials runs.

    Ntrials is Default at 50 Runs
    Train Size is Default at 80% Test 20%
    
    Args:
        clf (Machine Learning Model): Classifier Model
        X (Numpy Array of Shape (n,d)): Features Values
        y (Numpy Array of Shape (n,)): Target Classes
        ntrials (integer): Number of Trials
    Returns:
        (type): Description of return value(s)
        train_error -- float, training error
        test_error  -- float, test error
    """
    # ------------------------------------------------------------------------ #
    # Computes Cross - Validation Error Over N Trials
    # ------------------------------------------------------------------------ #
    train_f1_error = 0
    test_f1_error = 0
    
    train_accuracy = 0
    test_accuracy = 0

    train_precision = 0
    test_precision = 0

    train_recall = 0
    test_recall = 0

    for trial in range(ntrials):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=trial)
        clf.fit(X_train, y_train)
        y_pred_train = clf.predict(X_train)
        y_pred_test = clf.predict(X_test)

        train_f1_error = train_f1_error + round(metrics.f1_score(y_train, y_pred_train), 2)
        test_f1_error = test_f1_error + round(metrics.f1_score(y_test, y_pred_test), 2)

        train_accuracy = train_accuracy + metrics.accuracy_score(y_train, y_pred_train, normalize = True)
        test_accuracy = test_accuracy + metrics.accuracy_score(y_test, y_pred_test, normalize = True)

        train_precision = train_precision + metrics.precision_score(y_train, y_pred_train)
        test_precision = test_precision + metrics.precision_score(y_test, y_pred_test)

        train_recall = train_recall + metrics.recall_score(y_train, y_pred_train)
        test_recall = test_recall + metrics.recall_score(y_test, y_pred_test)

    train_f1_error = train_f1_error/float(ntrials) * 100
    test_f1_error = test_f1_error/float(ntrials) * 100
    train_accuracy = train_accuracy/float(ntrials) * 100
    test_accuracy = test_accuracy/float(ntrials) * 100
    train_precision = train_precision/float(ntrials) * 100
    test_precision = test_precision/float(ntrials) * 100
    train_recall = train_recall/float(ntrials) * 100
    test_recall = test_recall/float(ntrials) * 100

    return train_f1_error, test_f1_error, train_accuracy, test_accuracy, train_precision, test_precision, train_recall, test_recall

def autolabel(ax, rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{0:.2f}%'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),
                    textcoords="offset points",
                    ha=ha[xpos], va='bottom')

def plot_train_test(train_error, test_error, model_names):
    ind = np.arange(len(train_error))
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, train_error, width, label='Train Accuracy')
    rects2 = ax.bar(ind + width/2, test_error, width, label='Test Accuracy')

    model_numbers = range(len(model_names))

    ax.set_ylabel('Accuracy')
    ax.set_title('Training and Testing Accuracy')
    ax.set_xticks(ind)
    ax.set_xticklabels(model_numbers)
    ax.legend()

    autolabel(ax, rects1, "left")
    autolabel(ax, rects2, "right")

    fig.tight_layout()

    plt.show()
    plt.savefig('plot.png')

def plot_roc(clf, X, y, test_size=0.2, n_classes=2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)
    y_score = clf.fit(X_train, y_train).decision_function(X_test) #Need to Get Proper Score Function for the Model. Each Model is Different!

    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = metrics.roc_curve(y_test, y_score)
        roc_auc[i] = metrics.auc(fpr[i], tpr[i])

    fpr["micro"], tpr["micro"], _ = metrics.roc_curve(y_test.ravel(), y_score.ravel())
    roc_auc["micro"] = metrics.auc(fpr["micro"], tpr["micro"])

    plt.figure()
    lw = 2
    plt.plot(fpr[n_classes-1], tpr[n_classes-1], label='ROC curve (area = %0.2f)' % roc_auc[n_classes-1])
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.show()

def plot_prc(clf, X, y, test_size=0.2, n_classes=2):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)
    y_score = clf.fit(X_train, y_train).decision_function(X_test) #Need to Get Proper Score Function for the Model. Each Model is Different!
    
    average_precision = metrics.average_precision_score(y_test, y_score)
    precision, recall, _ = metrics.precision_recall_curve(y_test, y_score)

    step_kwargs = ({'step': 'post'} if 'step' in signature(plt.fill_between).parameters else {})
    plt.step(recall, precision, color='b', alpha=0.2, where='post')
    plt.fill_between(recall, precision, alpha=0.2, color='b', **step_kwargs)

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title(str(n_classes) + 'class Precision-Recall curve: AP={0:0.2f}'.format(average_precision))
    plt.show()

def main():
    # ------------------------------------------------------------------------ #
    # Parse Command Line Arguments
    # ------------------------------------------------------------------------ #
    parser = argparse.ArgumentParser(description="Machine Learning Model Comparisons.")

    parser.add_argument("training_csv", action="store", help="Indicate the path to the csv to train the specified model on.")

    parser.add_argument("prediction_csv", action="store", help="Indicate the path to the csv for the specified model to predict on.")

    parser.add_argument("model_name", action="store", choices=['All', 'BaggingClassifier', 
    'GradientBoostingClassifier', 'LogisticRegression', 'MLPClassifier_ActivationIdentity', 
    'MLPClassifier_ActivationLogistic', 'MLPClassifier_TanH', 'MLPClassifier_Relu', 
    'NearestCentroid','KNeighborsClassifier', 'DecisionTree', 'RandomForest', 'ExtraTreesClassifier',
    'StochasticGradientDescent_Hinge', 'StochasticGradientDescent_Log', 
    'StochasticGradientDescent_Perceptron', 'StochasticGradientDescent_ModifiedHuber',
    'StochasticGradientDescent_SquaredHinge',
    'SupportVectorMachine_RBFKernel',
    'SupportVectorMachine_SigmoidKernel', 'Analyze', 'DeveloperChosen'], help="The identifier to indicate which model to test and train on.")
    
    args = parser.parse_args()

    models = {
        'BaggingClassifier':BaggingClassifier(n_estimators=20),
        'GradientBoostingClassifier':GradientBoostingClassifier(n_estimators=300, max_depth=6, loss='exponential'),
        'LogisticRegression':linear_model.LogisticRegression(solver='lbfgs'),
        'MLPClassifier_ActivationIdentity':MLPClassifier(activation='identity'),
        'MLPClassifier_ActivationLogistic':MLPClassifier(activation='logistic', max_iter=400),
        'MLPClassifier_TanH':MLPClassifier(activation='tanh', max_iter=1000),
        'MLPClassifier_Relu':MLPClassifier(activation='relu', max_iter=1000),
        'NearestCentroid':NearestCentroid(),
        'KNeighborsClassifier':KNeighborsClassifier(n_neighbors=5, weights='distance'),
        'DecisionTree':DecisionTreeClassifier(max_depth=None),
        'RandomForest':RandomForestClassifier(n_estimators=30),
        'ExtraTreesClassifier':ExtraTreesClassifier(n_estimators=30),
        'StochasticGradientDescent_Hinge':linear_model.SGDClassifier(loss='hinge', max_iter=1000, tol=1e-3),
        'StochasticGradientDescent_Log':linear_model.SGDClassifier(loss='log', max_iter=1000, tol=1e-3),
        'StochasticGradientDescent_Perceptron':linear_model.SGDClassifier(loss='perceptron', max_iter=1000, tol=1e-3),
        'StochasticGradientDescent_ModifiedHuber':linear_model.SGDClassifier(loss='modified_huber', max_iter=1000, tol=1e-3),
        'StochasticGradientDescent_SquaredHinge':linear_model.SGDClassifier(loss='squared_hinge', max_iter=1000, tol=1e-3),
        'SupportVectorMachine_RBFKernel':SVC(kernel='rbf', gamma='scale'),
        'SupportVectorMachine_SigmoidKernel':SVC(kernel='sigmoid', gamma='scale')
    }

    # ------------------------------------------------------------------------ #
    # Load Stroke-MRI DataSet
    # ------------------------------------------------------------------------ #
    stroke_train = load_model_data(args.training_csv, header=1, predict_col=0)
    X_train = stroke_train.X;
    X_train_name = stroke_train.Xnames
    y_train = stroke_train.y;
    y_train_name = stroke_train.yname

    n,d = X_train.shape # n = Number of Examples, d = Number of Features

    normalized_X_train = preprocessing.scale(X_train)

    if(args.model_name != 'All'):
        stroke_test = load_model_test(args.prediction_csv, header=1, predict_col=3)
        X_test = stroke_test.X;
        X_test_name = stroke_test.Xnames
        y_test = stroke_test.y;
        y_test_name = stroke_test.yname

        n,d = X_test.shape # n = Number of Examples, d = Number of Features

        normalized_X_test = preprocessing.scale(X_test)

        print("Classifying using Sci-Kit Learn:",args.model_name,"Classifier")
        clf = models[args.model_name]
        clf.fit(normalized_X_train, y_train) #Full Model Training
        y_pred_train = clf.predict(normalized_X_train)
        train_error = metrics.f1_score(y_train, y_pred_train)
        dump(clf, args.model_name + '.joblib')
        print(args.model_name, "Training F1 Score:",str(train_error))

        y_pred_test = clf.predict(normalized_X_test)

        filename = model + ".csv"
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                print("Could Not Remove", filename, "Insufficient Permissions")
                sys.exit(1)
            log = open(filename, "w+")

        for i in range(len(y_test)): #How Many DataPoints
            log.write(str(y_test[i][0])+','+str(y_test[i][1])+','+str(y_test[i][2])+','+str(y_pred_test[i])+'\n')
    else: # Run Through ALL
        # -------------------------------------------------------------------- #
        # Plotting SetUp
        # -------------------------------------------------------------------- #
        train_f1_score = []
        test_f1_score = []
        model_names = []
        #-----------------------------------------------------------------------
        filename = "model_analysis.csv"
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                print("Could Not Remove",filename,"Insufficient Permissions")
                sys.exit(1)
        log = open(filename, "w+")

        print("Testing All Classifiers")
        for key, value in models.items():
            print("Classifying using Sci-Kit Learn:",key,"Classifier")
            log.write("Classifying using Sci-Kit Learn:" + ' ' + key + ' ' + "Classifier\n")
            log.flush()
            clf = value

            start_time = time.time()
            training_f1_error, testing_f1_error, train_accuracy, test_accuracy, train_precision, test_precision, train_recall, test_recall = error(clf, normalized_X_train, y_train)
            print("TOOK", str(time.time() - start_time), "To Train")
            log.write("TOOK " + str(time.time() - start_time) + " " + "To Train" + '\n')
            log.flush()

            print(key, "Training F1 Score:",str(training_f1_error))
            log.write(key + ' ' + "F1 Score:" + ' ' + str(training_f1_error) + '\n')
            log.flush()
            print(key, "Testing F1 Score: " + str(testing_f1_error))
            log.write(key + ' ' + "Testing F1 Score: " + ' ' + str(testing_f1_error) + '\n')
            log.flush()

            print(key, "Training Accuracy:",str(train_accuracy))
            log.write(key + ' ' + "Training Accuracy:" + ' ' + str(train_accuracy) + '\n')
            log.flush()
            print(key, "Testing Accuracy: " + str(test_accuracy))
            log.write(key + ' ' + "Testing Accuracy: " + ' ' + str(test_accuracy) + '\n')
            log.flush()

            print(key, "Training Precision:",str(train_precision))
            log.write(key + ' ' + "Training Precision:" + ' ' + str(train_precision) + '\n')
            log.flush()
            print(key, "Testing Precision: " + str(test_precision))
            log.write(key + ' ' + "Testing Precision: " + ' ' + str(test_precision) + '\n')
            log.flush()

            print(key, "Training Recall:",str(train_recall))
            log.write(key + ' ' + "Training Recall:" + ' ' + str(train_recall) + '\n')
            log.flush()
            print(key, "Testing Recall: " + str(test_recall))
            log.write(key + ' ' + "Testing Recall: " + ' ' + str(test_recall) + '\n')
            log.flush()
                
            print("-----------------------------------------------------------")
            log.write("-----------------------------------------------------------\n")
            log.flush()
            train_f1_score.append(training_f1_error)
            test_f1_score.append(testing_f1_error)
            model_names.append(key)

        plot_train_test(train_f1_error, test_f1_error, model_names)
        plt.savefig('plot.png')

if __name__ == "__main__":
    main()

"""
NOTE
We Only Need Label, Pixel Values for Training/Testing on Cross Validation.
After We Make the Model, We Have New CSVs for All the Pixels in 1 DICOM File.
"""