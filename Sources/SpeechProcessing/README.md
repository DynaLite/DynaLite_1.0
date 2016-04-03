Train Emotion Classifier
------------------------  
1. **Setup data**  
   *Download from source and format*
  - Download RAVDESS speech database from this link: http://smartlaboratory.org/ravdess/download/  
  - Download speech only, no music, all actors.
  - Create a folder named `RAVDESS` here, and extract all the speech files into it.  
  - Run the script `format_wavs.sh` to format all the wav files correctly. Note: all the files will be moved into the folder `RAVDESS/all` with this script.
  - Run the script `setup_for_training.sh` to orginize the .wav files into folders for training the classifiers.  
  
   *Or, download pre-formatted dataset*  
  - Here's a link to an already formated dataset:   
2.  **Download pyAudioAnalysis**  
  - Download a zip of pyAudioAnalysis: https://github.com/tyiannak/pyAudioAnalysis/archive/master.zip
  - Extract and store `pyAudioAnalysis` folder here.
  - I'll figure out the best way to include other repos soon.
3.  **Train classifiers** 
  - Run any of the training scripts to train a specific classifier. The classifiers will be stored in `RAVDESS/models`.  
