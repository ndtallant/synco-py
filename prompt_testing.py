#!/usr/bin/env python3
'''
Nick Tallant
This file is the main user interaction.
'''
# Shell Functionality
from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter

# Project Specific
from src.transcription import Transcription 
from src.transcription import RhythmString 
from src.user_messages import load_screen, get_help
from src.synco_2 import MidiOut

inst_list = ['Hi-Hat', 'Snare', 'Kick']
inst_completer= WordCompleter(inst_list, ignore_case=True)


command_completer = WordCompleter(['Add Instrument',
                                   'Change Instrument',
                                   'Delete Instrument',
                                   'See Drumkit',
                                   'help', 'exit', 'play'],
                                   ignore_case=True)

def prompt_inst(no_rhythm=False):
    '''
    This function prompts the user for an instrument,
    and then prompts for a new rhythm.
    '''
    r = RhythmString()
    
    while True:    
        
        inst_entry = prompt("   Instrument > ", completer=inst_completer) #pass history in here or nah?
        
        if no_rhythm:
            break 
        
        if inst_entry in inst_list:
            rhy = prompt_rhythm()       
            break
        
        else:
            print('   Enter Hi-Hat, Snare, or Kick')

    r.label = inst_entry
    r.rhythm = rhy
    r.set_patch()
    print(r) 
    return r 
    
def prompt_rhythm():
    '''
    Prompts the user for a rhythm
    put error handling here maybe????
    '''
    return prompt("     Rhythm > ") #pass history in here or nah?
     
def change_inst(rm_inst=False):
    '''
    Will update the transcription stack and overwrite an instrument.
    Most funtionality is contained in prompt_inst, the difference here
    being the output to the transcription stack.
    
    Rather than having a seperate function, this one 'deletes'
    an instrument by the boolen kwarg rm_inst. It just sets
    the instrument to all rests.
    '''
    action = 'remove' if rm_inst else 'change' 
    print('What instrument to you want to {}?'.format(action)) 
    if rm_inst:
        inst = prompt_inst(no_rhythm=True)
        print('Removed {}'.format(inst)) 
    else:
        prompt_inst() 

def prompt_command(t, action):
    '''Interface for user to enter commands in command completer.'''
    
    command = prompt("> ", completer=command_completer) 

    if command in ('Add Instrument', 'Add Drumkit'):
        t.stack.append(prompt_inst())
        print(t.stack) 
    if command == 'Change Instrument':
        t = change_inst()
    if command == 'Delete Instrument':
        t = change_inst(rm_inst=True)
    if command in {'play', 'exit', 'help'}:
        action = command 
    if command == 'See Drumkit':
        try: 
            print(t.stack)
            if len(t.stack) == 0:
                print('I can\'t see a drumset right now :( ')
        except: # I know...
            print('I can\'t see a drumset right now')
            print('Dev-note: no Transcription stack')

    return t, action

if __name__ == '__main__':
    
    load_screen()
    history = InMemoryHistory()
    t = Transcription() 
    while True:
        try:
            action = None 
            t, action = prompt_command(t, action)    
            
            if action == 'help':
                get_help()
            
            if action == 'play':
                print(t.output_drumseq()) 
                with MidiOut(t=t, user_port='1') as out:
                    out.play()
            
            if action == 'exit':
                break 
        
        except EOFError:
            break  # Control-D pressed.
    
    print('\nSweet Beats!\n')
