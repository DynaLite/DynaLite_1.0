#!/bin/bash

mkdir -p RAVDESS/models

python pyAudioAnalysis/audioAnalysis.py trainClassifier -i RAVDESS/both_genders/train_set/neutral/ RAVDESS/both_genders/train_set/calm/ RAVDESS/both_genders/train_set/happy/ RAVDESS/both_genders/train_set/sad/ RAVDESS/both_genders/train_set/angry/ --method svm -o RAVDESS/models/both_genders_emotions_svm