#!/bin/bash

mkdir -p RAVDESS/models

# male_emotions_svm
python pyAudioAnalysis/audioAnalysis.py trainClassifier -i RAVDESS/male/train_set/neutral/ RAVDESS/male/train_set/calm/ RAVDESS/male/train_set/happy/ RAVDESS/male/train_set/sad/ RAVDESS/male/train_set/angry/ --method svm -o RAVDESS/models/male_emotions_svm

# male_emotions_knn
python pyAudioAnalysis/audioAnalysis.py trainClassifier -i RAVDESS/male/train_set/neutral/ RAVDESS/male/train_set/calm/ RAVDESS/male/train_set/happy/ RAVDESS/male/train_set/sad/ RAVDESS/male/train_set/angry/ --method knn -o RAVDESS/models/male_emotions_knn

# female_emotions_svm
python pyAudioAnalysis/audioAnalysis.py trainClassifier -i RAVDESS/female/train_set/neutral/ RAVDESS/female/train_set/calm/ RAVDESS/female/train_set/happy/ RAVDESS/female/train_set/sad/ RAVDESS/female/train_set/angry/ --method svm -o RAVDESS/models/female_emotions_svm

# female_emotions_knn
python pyAudioAnalysis/audioAnalysis.py trainClassifier -i RAVDESS/female/train_set/neutral/ RAVDESS/female/train_set/calm/ RAVDESS/female/train_set/happy/ RAVDESS/female/train_set/sad/ RAVDESS/female/train_set/angry/ --method knn -o RAVDESS/models/female_emotions_knn

# both_genders_emotions_svm
python pyAudioAnalysis/audioAnalysis.py trainClassifier -i RAVDESS/both_genders/train_set/neutral/ RAVDESS/both_genders/train_set/calm/ RAVDESS/both_genders/train_set/happy/ RAVDESS/both_genders/train_set/sad/ RAVDESS/both_genders/train_set/angry/ --method svm -o RAVDESS/models/both_genders_emotions_svm

# both_genders_emotions_knn
python pyAudioAnalysis/audioAnalysis.py trainClassifier -i RAVDESS/both_genders/train_set/neutral/ RAVDESS/both_genders/train_set/calm/ RAVDESS/both_genders/train_set/happy/ RAVDESS/both_genders/train_set/sad/ RAVDESS/both_genders/train_set/angry/ --method knn -o RAVDESS/models/both_genders_emotions_knn

# male_emotions_regression


# female_emotions_regression


# both_genders_emotions_regression

# python pyAudioAnalysis/audioAnalysis.py trainRegression -i speechEmotion/ --method svm -o svmSpeechEmotion