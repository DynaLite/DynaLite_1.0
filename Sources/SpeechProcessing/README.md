Train Emotion Classifier
------------------------  
1. **Setup data** (_download from source and format, can skip step #2 if you do this_)
  - Download RAVDESS speech database from this link: http://smartlaboratory.org/ravdess/download/  
  - Download speech only, no music, all actors.
  - Create a folder named `RAVDESS` here, and extract all the speech files into it.  
  - Run the script `format_wavs.sh` to format all the wav files correctly. Note: all the files will be moved into the folder `RAVDESS/all` with this script.
  - Run the script `setup_for_training.sh` to orginize the .wav files into folders for training the classifiers.  
2.  **Setup data** (_or, download pre-formatted dataset_, **_don't do if you did step #1_**)
  - Here's a link to an already formated dataset:   
3.  **Download pyAudioAnalysis**  
  - Download a zip of pyAudioAnalysis: https://github.com/tyiannak/pyAudioAnalysis/archive/master.zip
  - Extract and store `pyAudioAnalysis` folder here.
  - I'll figure out the best way to include other repos soon.
4.  **Train classifiers** 
  - Run any of the training scripts to train a specific classifier. The classifiers will be stored in `RAVDESS/models`.  
