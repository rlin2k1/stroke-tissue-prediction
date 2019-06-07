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

## Data
Data for this project comes from a series of MRI scans for eighteen patients who had been treated for ischemic stroke at UCLA’s Ronald Reagan Medical Center. Each patient had two sets of MRI images: perfusion, and FLAIR, represented in the international standard DICOM image format, which is essentially a standard image appended with a load of metadata, such as patient name, brain slice location (slice meaning vertical location, relative to the patient’s eyes, moving up or down), and image capture time. The data will not be released as it contains privileged information of patients.

## Usage

#### Co-Registering Raw FLAIR MASK `DICOM`s to Perfusion `DICOM`s

If you wish to do Co-registration, please install the latest [SimpleElastix library](https://simpleelastix.github.io/#download).

There should already be folder called `Patients` containing the number (an integer) of each Patient. Within each Patient's Number folder, there is a folder called `Perfusion` containing Perfusion `DICOM`s and a folder called `FLAIR`, containing FLAIR `DICOM`s.

From within the virtualenv, at the root of the repo, run `python3 src/register_images.py {path_to_flair_perfusion_mappings}`.

The `{path_to_flair_perfusion_mappings}` is a CSV file that contains rows of format:

   PATIENTNUMBER,FIXEDDICOM,MOVINGDICOM

This will create a new directory called `RESULT` in the `src` directory, and store the co-registered `DICOM`s inside with file name: 

   ```bash
   result_DICOMFILENAME_AcquitionNumber_AcquitionTime_SliceLocation.dcm
   ```

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

From within the virtualenv, at the root of the repo, run:

   ```bash
   python3 src/classify_voxels.py {path_to_training_csv} {path_to_input_csv} {which_model_to_run}
   ```

##### Current Machine Learning Models Supported

   - `All` - Put this in place of `{which_model_to_run}` to use all the models list below, and output their individual F1-Score, Accuracy, Precision, and Recall. This will output to a single `CSV`, `model_analysis.csv`. 
   - Use any of the below options to train on a 100/0 Split of Training, Test, in place of the `{which_model_to_run}` option. This will output to a single `CSV`, named `{which_model_to_run}.csv`.

      - [BaggingClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.BaggingRegressor.html)
      - [GradientBoostingClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html)
      - [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
      - [MLPClassifier_ActivationIdentity](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
      - [MLPClassifier_ActivationLogistic](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
      - [MLPClassifier_TanH](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
      - [MLPClassifier_Relu](https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html)
      - [NearestCentroid](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestCentroid.html)
      - [KNeighborsClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html)
      - [DecisionTree](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)
      - [RandomForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
      - [ExtraTreesClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html)
      - [StochasticGradientDescent_Hinge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)
      - [StochasticGradientDescent_Log](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)
      - [StochasticGradientDescent_Perceptron](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)
      - [StochasticGradientDescent_ModifiedHuber](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)
      - [StochasticGradientDescent_SquaredHinge](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html)
      - [SupportVectorMachine_RBFKernel](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)
      - [SupportVectorMachine_SigmoidKernel](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html)
   
For a more verbose description of these options and their utilization, run `python3 src/classify_voxels.py -h`.

## Cleanup

1. Run `./bootstrap.sh -c` to blow away the virtualenv, and clean its dependent files.

## Extensive Description

#### Tissue Fate Prediction in Acute Stroke based on MRI

Stroke is one of the leading cause of death and a major cause of long term disabilities worldwide. While prevention research identifies factors and specific drugs that may lower the risk of a future stroke, the treatment of ischemic stroke patients aims at maximizing the recovery of brain tissue at risk. It is typically done by recanalization of the occluded blood vessel; either mechanically or using a clot-busting drug. Prediction of tissue outcome is essential to the clinical decision-making process in acute ischemic stroke and would help to refine therapeutic strategies.
 
Recent studies based on Machine Learning have outperformed standard approaches and demonstrated great promise in predicting lesion growth. This project aims at comparing the accuracy of state-of-the-art machine learning methods including Deep Learning architectures, LSTM, Decision Trees, and Kernel Spectral Regression. The input will be based on source perfusion weighted MRI obtained after admission of the stroke patient, and the target output will correspond to the lesion annotated on FLAIR images by a Neurologist 3 days after admission.
