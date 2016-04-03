Train Emotion Classifier
------------------------  
1. Setup data
  - Download RAVDESS speech database from this link: http://smartlaboratory.org/ravdess/download/  
  - Download speech only, no music, all actors.
  - Create a folder named `RAVDESS` here, and extract all the speech files into it.  
  - Run the script `format_wavs.sh` to format all the wav files correctly. Note: all the files will be moved into the folder `RAVDESS/all` with this script.
  - Run the script `setup_for_training.sh` to orginize the .wav files into folders for training the classifiers.
2.  Train classifiers 
  - Run any of the training scripts to train a specific classifier. The classifiers will be stored in `RAVDESS/models`.  
