import json

song = {}
song['src'] = 'score/mix.mp3'
song['notes'] = []



note = {}
note['start'] = 0
note['end'] = 1000
note['pitch'] = -1
note['lyric'] = 'miaou'
song['notes'].append(note)


jsonstr = json.dumps(song)
with open('../json/test.json','w') as f:
    f.write(jsonstr)
