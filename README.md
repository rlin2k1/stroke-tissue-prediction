stroke-tissue-prediction
===========================

Stroke Tissue Prediction is a project for UCLA's Spring '19 CS 168 class, taught by Professor Fabien Scalzo. The goal is to use various machine learning techniques to analyze a set of scans of a brain, both pre and post-stroke, and determine the likelihood of developing lesions. Specifically, we want compare the accuracy of various algorithmic approaches.

## Prerequisites

These are needed before running the steps in `Getting Started`.

   - Python 3.7+ [(macOS installation)](https://docs.python-guide.org/starting/install3/osx/) [(Linux installation)](https://docs.python-guide.org/starting/install3/linux/)

## Dependencies

These are installed via the bootstrapping process described in `Getting Started`.

- bz2file 0.98
- cycler 0.10.0
- kiwisolver 1.1.0
- matplotlib 2.2.4
- nibabel 2.4.0
- numpy 1.16.2
- pydicom 1.2.2
- pyparsing 2.4.0
- python-dateutil 2.8.0
- pytz 2019.1
- scikit-learn 0.20.3
- scipy 1.2.1
- six 1.12.0
- subprocess32 3.5.3

## Getting Started

1. Run `./bootstrap.sh` to install necessary dependencies.
   - NOTE: if your default python is managed by anaconda (i.e., `which python` returns something like `/usr/local/anaconda3/bin/python`) you MUST do your initial bootstrap using the anaconda option: `./bootstrap.sh --anaconda`.
2. Run `source build/bin/activate` to get inside the virtualenv.
3. Run `deactivate` to close the virtualenv.

## Usage

#### Co-Registering Raw FLAIR MASK `DICOM`s to Perfusion `DICOM`s
If you wish to do Co-Registration, please install the latest SimpleElastix library: https://simpleelastix.github.io/#download
There should already be folder called 'Patients' containing the Number of each Patient. Within each Patient's Number folder, there is a folder called 'Perfusion' containing Perfusion DiComs and a folder called 'FLAIR' containing Flair DiComs.

From within the virtualenv, at the root of the repo, run `python3 src/register_images.py {path_to_flair_perfusion_mappings}`.

The {path_to_flair_perfusion_mappings} is a CSV file that contains:
PATIENTNUMBER,FIXEDDICOM,MOVINGDICOM

Creates a New Directory called 'RESULT' in the src directory and stores the registered Dicoms inside with file name: 
   result_DICOMFILENAME_AcquitionNumber_AcquitionTime_SliceLocation.dcm

#### Generating `CSV` Files from Raw `DICOM`s

1. From within the virtualenv, at the root of the repo, run `python3 src/generate_csvs.py {directory_with_dicoms} {n_intensity_vals} {n_live} {n_die}`. 
   - For a more verbose description of these options and their utilization, run `python3 src/generate_csvs.py -h`.
2. This will generate a training and a testing `csv` per patient, which can be put through the machine learning models.
   - NOTE: directories must be structured like so:
   ```
   Patients <-- structured_directory_root
        |--- 1 <-- patient number... must be an integer
             |--- FLAIR
             |--- Perfusion
        |--- 2
             |--- FLAIR
             |--- Perfusion
        |--- ...
        |--- N
             |--- FLAIR
             |--- Perfusion
   ```

#### Utilizing `CSV` Files

1. Once the `CSV` files have been generated, you should run `verify-csvs.sh` on them.
   - To do this, all `CSV`'s you wish to affect must be in a single directory.
   - Recommended usage is as follows: `./verify-csvs.sh -n {col_count} -c -f col_label,col_label -i {lines_to_ignore} -br -d {directory_with_csvs}`
      - Essentially, this will combine all patients' `CSV` files into one, normalize column count to `col_count`, add `col_label,col_label` as the first line of the condensed `CSV`, and ignore any intensity rows which contained background values.
      - For further usage details, run `./verify-csvs.sh -u`.
2. With the `CSV` files cleaned and condensed, you should run them through the machine learning process of your choice. See the `Utilizing Machine Learning` section for further details.

#### Utilizing Machine Learning

From within the virtualenv, at the root of the repo run `python3 src/classify_voxels.py {path_to_training_csv} {path_to_predict_csv} {which_model_to_run}`.
  Current Machine Learning Models Supported: <br>
   All - Runs training csv through all below models and outputs F1-Score, Accuracy, Precision, and Recall to a Log File: model_analysis.csv<br>
   {All the Below Options would train on a 100/0 Split on Training, Test on the Predicting CSV, and write the Results to Output:{model_name}.csv}<br>
   - [BaggingClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.BaggingRegressor.html)<br>
   - [GradientBoostingClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html)<br>
   - [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)<br>
   - [MLPClassifier_ActivationIdentity](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)<br>
   - [MLPClassifier_ActivationLogistic](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)<br>
   - [MLPClassifier_TanH](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)<br>
   - [MLPClassifier_Relu](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)<br>
   - [NearestCentroid](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestCentroid.html)<br>
   - [KNeighborsClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)<br>
   - [DecisionTree](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)<br>
   - [RandomForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)<br>
   - [ExtraTreesClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html)<br>
   - [StochasticGradientDescent_Hinge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)<br>
   - [StochasticGradientDescent_Log](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)<br>
   - [StochasticGradientDescent_Perceptron](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)<br>
   - [StochasticGradientDescent_ModifiedHuber](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)<br>
   - [StochasticGradientDescent_SquaredHinge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)<br>
   - [SupportVectorMachine_RBFKernel](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)<br>
   - [SupportVectorMachine_SigmoidKernel](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)<br>
   
    For a more verbose description of these options and their utilization, run `python3 src/classify_voxels.py -h`.
## Cleanup

1. Run `./bootstrap.sh -c` to blow away the virtualenv, and clean its dependent files.

## Extensive Description

#### Tissue Fate Prediction in Acute Stroke based on MRI

Stroke is one of the leading cause of death and a major cause of long term disabilities worldwide. While prevention research identifies factors and specific drugs that may lower the risk of a future stroke, the treatment of ischemic stroke patients aims at maximizing the recovery of brain tissue at risk. It is typically done by recanalization of the occluded blood vessel; either mechanically or using a clot-busting drug. Prediction of tissue outcome is essential to the clinical decision-making process in acute ischemic stroke and would help to refine therapeutic strategies.
 
Recent studies based on Machine Learning have outperformed standard approaches and demonstrated great promise in predicting lesion growth. This project aims at comparing the accuracy of state-of-the-art machine learning methods including Deep Learning architectures, LSTM, Decision Trees, and Kernel Spectral Regression. The input will be based on source perfusion weighted MRI obtained after admission of the stroke patient, and the target output will correspond to the lesion annotated on FLAIR images by a Neurologist 3 days after admission.
