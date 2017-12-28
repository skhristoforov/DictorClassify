import pycurl
import numpy as np
import pyglet
import urllib.parse as parse
import urllib.request as urllib2
import pyaudio
import wave
import xmltodict
from collections import OrderedDict
import certifi
from api import API_KEY

class User:
    def __init__(self, name='default'):
        self.id_length = 32
        self.id = ''.join(np.random.choice(np.array(list('0123456789abccdef')), size=32).tolist())
        self.name = name

    def __repr__(self):
        return self.name + '_' + self.id

default_user = User()

class Recognizer:
    def __init__(self):
        self.WAVE_OUTPUT_FILENAME = "replica.wav"

    def get_senses(self, user=default_user):
        def recognize(wav_data, user):
            sets = {
                'uuid': user.id,
                'key': API_KEY,
                'topic': 'queries',
                'lang': 'ru-RU'
            }
            req = urllib2.Request("https://asr.yandex.net/asr_xml?" + parse.urlencode(sets), data=wav_data)
            req.add_header('Content-Length', '%d' % len(wav_data))
            req.add_header('Content-Type', 'audio/x-wav')
            req.add_header('Host', 'asr.yandex.net')
            res = urllib2.urlopen(req)
            return res.read().decode('utf-8')

        def parse_sense(input_sting):
            root = xmltodict.parse(input_sting)
            if root['recognitionResults']['@success'] == '1':
                if type(root['recognitionResults']['variant']) is list:
                    return root['recognitionResults']['variant']
                elif type(root['recognitionResults']['variant']) is OrderedDict:
                    return [root['recognitionResults']['variant']]
                else:
                    raise RuntimeError('Error in parsing XML')
            else:
                return list()

        data = open(self.WAVE_OUTPUT_FILENAME, 'rb').read()
        output = recognize(data, user)
        senses = parse_sense(output)
        #return senses
        if len(senses):
            best_sense = sorted(senses, key=lambda x: float(x['@confidence']))[-1]['#text']
        else:
            best_sense = ''
        return best_sense
        


