#!/bin/bash

# Place this file inside the unzipped folder
# containing all the RAVDESS wav files

cd RAVDESS

mkdir -p all

for file in *.wav; do
	sox "$file" -r 16000 all/"$file"
done

rm *.wav

cd ..