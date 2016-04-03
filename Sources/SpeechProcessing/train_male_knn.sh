#!/bin/bash

mkdir -p RAVDESS/models

python pyAudioAnalysis/audioAnalysis.py trainClassifier -i RAVDESS/male/train_set/neutral/ RAVDESS/male/train_set/calm/ RAVDESS/male/train_set/happy/ RAVDESS/male/train_set/sad/ RAVDESS/male/train_set/angry/ --method knn -o RAVDESS/models/male_emotions_knn