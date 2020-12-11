# MIDI Melody Extraction

This repository contains the code for extracting the melodic line from the MIDI files of polyphonic music. 

Refer to the Jupyter Notebook `MIDI_MelodyExtractionTutorial.ipynb` for usage tutorial. 
The tutorial contains codes and instructions for single and batch extraction. 

#### Library dependency: 
- mido
- numpy

### Notes:
1. The python script assumes the melody is contained in the first channel of the 
first track of the MIDI file.

2. Current melody extraction criterion: 
    - When two notes happen at the same time, only the top one will remain. 
    
3. It works well with **quantized** midi. 

