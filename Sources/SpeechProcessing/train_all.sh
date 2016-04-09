#!/bin/bash

mkdir -p DATA/models

# # low_vs_high_arousal
# python pyAudioAnalysis/audioAnalysis.py trainClassifier -i DATA/both_genders/train_set/low_arousal/ DATA/both_genders/train_set/high_arousal/ --method svm -o DATA/both_genders/models/low_vs_high_arousal

# # low_arousal__low_valence_vs_high_valence
# python pyAudioAnalysis/audioAnalysis.py trainClassifier -i DATA/both_genders/train_set/low_arousal__low_valence/ DATA/both_genders/train_set/low_arousal__high_valence/ --method svm -o DATA/both_genders/models/low_arousal__low_valence_vs_high_valence

# # high_arousal__low_valence_vs_high_valence
python pyAudioAnalysis/audioAnalysis.py trainClassifier -i DATA/both_genders/train_set/high_arousal__low_valence/ DATA/both_genders/train_set/high_arousal__high_valence/ --method svm -o DATA/both_genders/models/high_arousal__low_valence_vs_high_valence

# # neutaral vs calm
# TODO: the following has errors????
# python pyAudioAnalysis/audioAnalysis.py trainClassifier -i DATA/both_genders/train_set/neutaral/ DATA/both_genders/train_set/calm/ --method svm -o DATA/both_genders/models/neutaral_vs_calm


# angry vs fear
# python pyAudioAnalysis/audioAnalysis.py trainClassifier -i DATA/both_genders/train_set/angry/ DATA/both_genders/train_set/fear/ --method svm -o DATA/both_genders/models/angry_vs_fear
