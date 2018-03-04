'''
Classes that form the basis for syncopython
The rhythm string for each limb will be parsed and joined
to output to drumseq.py as I develop a backend.
'''
import re

class RhythmString:
    '''
    RhythmString object has a MIDI sound #, RhythmString, and label.
    '''

    def __init__(self, patch, rs, label):
        self.patch = patch
        self.rhythm = rs
        self.label = label

    def __str__(self):
        return '{} "{}" {}'.format(self.patch, self.rhythm, self.label)

class Transcription:
    '''
    This class parses a readable stream into RhythmStrings, 
    and parses a collection of RhythmStrings into a string
    to be handled by the backend.
    '''

    def __init__(self, input_stream=None, **kwargs):
        if input_stream:
            print(input_stream) #getting extra positional argument
            self.stack = self.feed(input_stream)

    def feed(new_input): # new_input should be a readable stream (or string)
        '''
        parse new_input and modify internal state accordingly
        modify internal state according to new input
        '''
        stack = []
        for item in new_input.read().split('\n'):
            r = item.split('|')
            stack.append(RhythmString(r[0],r[1],r[2]))

        return stack 

    def output_drumseq(self, stack):
        '''
        TODO
        generates pattern suitable for drumseq.Sequencer
        based on current internal state
        '''
        rv = '# 1...2...3...4... '
        for r in stack: # need \n between RS?
            ds_rhythm = self.drumseq_helper(r.rhythm) 
            rv += '{} {} {} '.format(r.patch,ds_rhythm, r.label) 
        return rv
        
    def drumseq_helper(self, rhythm):
        rv = ''
        for beat in rhythm.split(','):
            rv += self.beat_parse('\d', beat)
            rv += self.beat_parse('e', beat)
            rv += self.beat_parse('&', beat)
            rv += self.beat_parse('a', beat)
        return rv    

    def beat_parse(self, exp, beat):
        return 'x' if re.search(exp, beat) else '.'

if __name__ == "__main__":
     RH = RhythmString(42, '1 &, 2 &, 3 &, 4 &', 'HH')
     LH = RhythmString(38, '   , 2  ,    , 4  ', 'Snare')
     RF = RhythmString(36, '1  ,   &, 3  ,   &', 'Kick')
     LF = RhythmString(42, '   , 2  ,    , 4  ', 'Foot')
