import mido
import copy
import os
import shutil

## Module 1: extracting the upper line with mido:

def get_note(msg):
    dict = msg.dict()
    if 'note' not in dict.keys():
        return -999
    else:
        return dict['note']

def break_track_into_moments(track):
    moments = []
    temp_list = []
    for msg in track:
        time_incr = msg.dict()['time']
        if time_incr == 0:
            temp_list.append(msg)
        else:
            moments.append(temp_list)
            temp_list = []
            temp_list.append(msg)
    return moments

def single_track_upper_melody(track):
    temp_time_to_add = 0
    new_list = []

    for msg in track:
        dict = msg.dict()
        if 'channel' in dict.keys() and dict['channel'] != 0:
            time_to_add = dict['time']
            temp_time_to_add = temp_time_to_add + time_to_add
        else:
            msg.time = msg.time + temp_time_to_add
            temp_time_to_add = 0
            new_list.append(msg)

    moments = break_track_into_moments(new_list)
    watchlist = []
    result_list = []

    temp_time_to_add = 0
    for m in moments:
        tmp_block_list = []
        highest_note_value = max([get_note(x) for x in m])
        for msg in m:
            # not top voice begin:
            if msg.type == 'note_on' and msg.dict()['note'] < highest_note_value and msg.dict()['velocity'] > 0:
                note = msg.dict()['note']
                watchlist.append(note)
                temp_time_to_add = temp_time_to_add + msg.dict()['time']
            # not top voice end:
            elif msg.type == 'note_on' and  msg.dict()['velocity'] == 0 and msg.dict()['note'] in watchlist:
                note = msg.dict()['note']
                watchlist.remove(note)
                temp_time_to_add = temp_time_to_add + msg.dict()['time']
            # top voice:
            else:
                msg.time = msg.dict()['time'] + temp_time_to_add
                temp_time_to_add = 0
                tmp_block_list.append(msg)
        result_list.extend(tmp_block_list)

    result_track = copy.deepcopy(track)
    result_track.clear()
    # result_track = mido.MidiTrack()
    result_track.extend(result_list)
    return result_track

def midi_file_melody_only(midi_file_path):
    midi_file = mido.MidiFile(midi_file_path, clip=True)
    track = midi_file.tracks[0]
    resulted_track = single_track_upper_melody(track)

    midi_file.tracks[0] = resulted_track

    return midi_file

## Module 2: Starting the output:

### 2.1: MIDI file -> MIDI file (melody only):
def process(input_file_path,output_path):
    result = midi_file_melody_only(input_file_path)
    input_name = result.filename
    output_name = 'melody_only_'+ input_name
    result.save(output_path + output_name)

### 2.2: Folder of MIDI files -> Folder of MIDI files (melody only):
def find_name(string):
    index = string.rfind('/')
    return string[index + 1:]

def batch_process(input_folder_path, output_path):
    output_folder_name = 'melody_only_' + find_name(input_folder_path)
    output_folder_path = output_path + output_folder_name

    if os.path.exists(output_folder_path + '/'):
        shutil.rmtree(output_folder_path + '/')
    os.makedirs(output_folder_path + '/')

    for files in os.listdir(input_folder_path):
        input_file_path = input_folder_path + '/' + files
        input_file_name = find_name(input_file_path)
        result = midi_file_melody_only(input_file_path)
        result.filename = 'melody_only_' + input_file_name
        result.save(output_folder_path + '/' + result.filename)


## Module 3: Run this script

if __name__ == '__main__':
    input_folder_path = 'sample_MIDIs'
    output_path = './'
    batch_process(input_folder_path, output_path)
    print('Finished processing!')

