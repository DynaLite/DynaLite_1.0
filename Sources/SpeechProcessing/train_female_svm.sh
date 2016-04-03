#!/bin/bash

mkdir -p RAVDESS/models

python pyAudioAnalysis/audioAnalysis.py trainClassifier -i RAVDESS/female/train_set/neutral/ RAVDESS/female/train_set/calm/ RAVDESS/female/train_set/happy/ RAVDESS/female/train_set/sad/ RAVDESS/female/train_set/angry/ --method svm -o RAVDESS/models/female_emotions_svm