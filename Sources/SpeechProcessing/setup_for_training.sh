#!/bin/bash

# Need to have all files formatted correctly located in
# a folder named "all"

rm -rf RAVDESS/female RAVDESS/male RAVDESS/both_genders

# ~~~ REMOVE UNWANTED FILES ~~~~~~

rm RAVDESS/all/03-01-06*
rm RAVDESS/all/03-01-07*
rm RAVDESS/all/03-01-08*

# ~~~ MAKE DIRS ~~~~~~

mkdir RAVDESS/female RAVDESS/male RAVDESS/both_genders

mkdir RAVDESS/female/train_set RAVDESS/female/validation_set
mkdir RAVDESS/male/train_set RAVDESS/male/validation_set
mkdir RAVDESS/both_genders/train_set RAVDESS/both_genders/validation_set

# Training set folders
mkdir RAVDESS/male/train_set/neutral
mkdir RAVDESS/male/train_set/calm
mkdir RAVDESS/male/train_set/happy
mkdir RAVDESS/male/train_set/sad
mkdir RAVDESS/male/train_set/angry
mkdir RAVDESS/male/train_set/regression

mkdir RAVDESS/female/train_set/neutral
mkdir RAVDESS/female/train_set/calm
mkdir RAVDESS/female/train_set/happy
mkdir RAVDESS/female/train_set/sad
mkdir RAVDESS/female/train_set/angry
mkdir RAVDESS/female/train_set/regression

mkdir RAVDESS/both_genders/train_set/neutral
mkdir RAVDESS/both_genders/train_set/calm
mkdir RAVDESS/both_genders/train_set/happy
mkdir RAVDESS/both_genders/train_set/sad
mkdir RAVDESS/both_genders/train_set/angry
mkdir RAVDESS/both_genders/train_set/regression

# Validation set folders
mkdir RAVDESS/male/validation_set/neutral
mkdir RAVDESS/male/validation_set/calm
mkdir RAVDESS/male/validation_set/happy
mkdir RAVDESS/male/validation_set/sad
mkdir RAVDESS/male/validation_set/angry

mkdir RAVDESS/female/validation_set/neutral
mkdir RAVDESS/female/validation_set/calm
mkdir RAVDESS/female/validation_set/happy
mkdir RAVDESS/female/validation_set/sad
mkdir RAVDESS/female/validation_set/angry

mkdir RAVDESS/both_genders/validation_set/neutral
mkdir RAVDESS/both_genders/validation_set/calm
mkdir RAVDESS/both_genders/validation_set/happy
mkdir RAVDESS/both_genders/validation_set/sad
mkdir RAVDESS/both_genders/validation_set/angry

# ~~~ COPY FILES TO TRAINING SETS ~~~~~~

# Copy all male files into their training set
cp RAVDESS/all/03-01-01*[13579].wav 	 RAVDESS/male/train_set/neutral
cp RAVDESS/all/03-01-02*[13579].wav 	 RAVDESS/male/train_set/calm
cp RAVDESS/all/03-01-03*[13579].wav 	 RAVDESS/male/train_set/happy
cp RAVDESS/all/03-01-04*[13579].wav 	 RAVDESS/male/train_set/sad
cp RAVDESS/all/03-01-05*[13579].wav 	 RAVDESS/male/train_set/angry
# All emotions go to regression set
cp RAVDESS/all/*[13579].wav RAVDESS/male/train_set/regression

# Copy all female files into their training set
cp RAVDESS/all/03-01-01*[02468].wav 	RAVDESS/female/train_set/neutral
cp RAVDESS/all/03-01-02*[02468].wav 	RAVDESS/female/train_set/calm
cp RAVDESS/all/03-01-03*[02468].wav 	RAVDESS/female/train_set/happy
cp RAVDESS/all/03-01-04*[02468].wav 	RAVDESS/female/train_set/sad
cp RAVDESS/all/03-01-05*[02468].wav 	RAVDESS/female/train_set/angry
# All emotions go to regression set
cp RAVDESS/all/*[02468].wav RAVDESS/female/train_set/regression

# Copy all non-gender specific files into training set
cp RAVDESS/all/03-01-01*.wav 	RAVDESS/both_genders/train_set/neutral
cp RAVDESS/all/03-01-02*.wav 	RAVDESS/both_genders/train_set/calm
cp RAVDESS/all/03-01-03*.wav 	RAVDESS/both_genders/train_set/happy
cp RAVDESS/all/03-01-04*.wav 	RAVDESS/both_genders/train_set/sad
cp RAVDESS/all/03-01-05*.wav 	RAVDESS/both_genders/train_set/angry
# All emotions go to regression set
cp RAVDESS/all/*.wav RAVDESS/both_genders/train_set/regression

# ~~~ MOVE LAST SPEAKER(s) FROM EACH TRAINING SET TO VALIDATION SET ~~~~~~

# Move last male speaker to validation set
mv RAVDESS/male/train_set/neutral/*23.wav 		 RAVDESS/male/validation_set/neutral/
mv RAVDESS/male/train_set/calm/*23.wav 	  		 RAVDESS/male/validation_set/calm/
mv RAVDESS/male/train_set/happy/*23.wav   		 RAVDESS/male/validation_set/happy/
mv RAVDESS/male/train_set/sad/*23.wav 	  		 RAVDESS/male/validation_set/sad/
mv RAVDESS/male/train_set/angry/*23.wav   		 RAVDESS/male/validation_set/angry/
# Remove last speaker from regression set
rm RAVDESS/male/train_set/regression/*23.wav

# Move last female speaker to validation set
mv RAVDESS/female/train_set/neutral/*24.wav 	RAVDESS/female/validation_set/neutral/
mv RAVDESS/female/train_set/calm/*24.wav 		RAVDESS/female/validation_set/calm/
mv RAVDESS/female/train_set/happy/*24.wav 		RAVDESS/female/validation_set/happy/
mv RAVDESS/female/train_set/sad/*24.wav 		RAVDESS/female/validation_set/sad/
mv RAVDESS/female/train_set/angry/*24.wav 		RAVDESS/female/validation_set/angry/
# Remove last female speaker from regression set
rm RAVDESS/female/train_set/regression/*24.wav

# Move last male speaker to non-gender specific validation set
mv RAVDESS/both_genders/train_set/neutral/*23.wav	RAVDESS/both_genders/validation_set/neutral/
mv RAVDESS/both_genders/train_set/calm/*23.wav 	 	RAVDESS/both_genders/validation_set/calm/
mv RAVDESS/both_genders/train_set/happy/*23.wav   	RAVDESS/both_genders/validation_set/happy/
mv RAVDESS/both_genders/train_set/sad/*23.wav 	 	RAVDESS/both_genders/validation_set/sad/
mv RAVDESS/both_genders/train_set/angry/*23.wav  	RAVDESS/both_genders/validation_set/angry/

# Move last female speaker to non-gender specific validation set
mv RAVDESS/both_genders/train_set/neutral/*24.wav 	RAVDESS/both_genders/validation_set/neutral/
mv RAVDESS/both_genders/train_set/calm/*24.wav 	  	RAVDESS/both_genders/validation_set/calm/
mv RAVDESS/both_genders/train_set/happy/*24.wav   	RAVDESS/both_genders/validation_set/happy/
mv RAVDESS/both_genders/train_set/sad/*24.wav 	  	RAVDESS/both_genders/validation_set/sad/
mv RAVDESS/both_genders/train_set/angry/*24.wav   	RAVDESS/both_genders/validation_set/angry/

# Remove last male speaker from regression set
rm RAVDESS/both_genders/train_set/regression/*23.wav 
# Remove last female speaker from regression set
rm RAVDESS/both_genders/train_set/regression/*24.wav
