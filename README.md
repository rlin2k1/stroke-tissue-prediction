stroke-tissue-prediction
===========================

Stroke Tissue Prediction is a project for UCLA's Spring '19 CS 168 class, taught by Professor Fabien Scalzo. The goal is to use various machine learning techniques to analyze a set of scans of a brain, both pre and post-stroke, and determine the likelihood of developing lesions. Specifically, we want compare the accuracy of various algorithmic approaches.

## Prerequisites

These are needed before running the steps in `Getting Started`.

   - Python 3.7+ [(macOS installation)](https://docs.python-guide.org/starting/install3/osx/) [(Linux installation)](https://docs.python-guide.org/starting/install3/linux/)

## Dependencies

These are installed via the bootstrapping process described in `Getting Started`.

   - nibabel 2.4.0
   - numpy 1.16.2
   - pydicom 1.2.2
   - scikit-learn 0.20.3
   - scipy 1.2.1
   - six 1.12.0

## Getting Started

1. Run `./bootstrap.sh` to install necessary dependencies.
2. Run `source build/bin/activate` to get inside the virtualenv.
3. Run `deactivate` to close the virtualenv.

## Usage

1. TODO: work on this.

## Cleanup

1. Run `./bootstrap.sh -c` to blow away the virtualenv, and clean its dependent files.

## Extensive Description

#### Tissue Fate Prediction in Acute Stroke based on MRI

Stroke is one of the leading cause of death and a major cause of long term disabilities worldwide. While prevention research identifies factors and specific drugs that may lower the risk of a future stroke, the treatment of ischemic stroke patients aims at maximizing the recovery of brain tissue at risk. It is typically done by recanalization of the occluded blood vessel; either mechanically or using a clot-busting drug. Prediction of tissue outcome is essential to the clinical decision-making process in acute ischemic stroke and would help to refine therapeutic strategies.
 
Recent studies based on Machine Learning have outperformed standard approaches and demonstrated great promise in predicting lesion growth. This project aims at comparing the accuracy of state-of-the-art machine learning methods including Deep Learning architectures, LSTM, Decision Trees, and Kernel Spectral Regression. The input will be based on source perfusion weighted MRI obtained after admission of the stroke patient, and the target output will correspond to the lesion annotated on FLAIR images by a Neurologist 3 days after admission.
