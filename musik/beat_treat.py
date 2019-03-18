from scipy.io import wavfile as wav
import numpy as np
import matplotlib.pyplot as pl
import xml.etree.ElementTree as ET
import musik.common as cm
from scipy import interpolate
import json


def adjustPartTempo(part, tempos):
    for mi,measure in enumerate(part):
        measure: ET.Element = measure

        direction: ET.Element = measure.find('direction')
        if direction is not None:
            measure.remove(direction)
        # if direction is None:
        #     direction = ET.SubElement(measure, 'direction')

        toadd=\
        '''<direction placement="above">
        <direction-type>
          <metronome parentheses="no" default-x="-30.12" relative-y="20.00">
            <beat-unit>quarter</beat-unit>
            <per-minute>{tempo}</per-minute>
            </metronome>
          </direction-type>
        <staff>1</staff>
        <sound tempo="{tempo}"/>
        </direction>'''.format(tempo = float(tempos[mi])) if mi<np.size(tempos) else tempos[-1]

        measure.insert(0,ET.fromstring(toadd))

        # sound: ET.Element = direction.find('sound')
        # if sound is None:
        #     sound = ET.SubElement(direction, 'sound')

        # sound.attrib['tempo'] = '{0:.3f}'

if __name__ == '__main__':

    ## load data
    etree = cm.loadxml('../score/0316.xml')
    root: ET.Element = etree.getroot()
    beat_lines, vocal_lines, part_list, measureBeats = cm.findParts(root)
    rate, data = wav.read('../treated/corrected0314/beat.wav')
    batchname = 'portOjisan'

    # left = data[:, 0]
    # right = data[:, 1]
    # data = left + right
    data = abs(data)
    # assert all(x>=0 for x in data)

    window = 0.005  # 5ms = 200Hz
    window *= rate  # now in sample numbers
    window = int(window)
    print('window = int(window) = {}'.format(window))

    # pl.plot(data[window:4*window])
    # pl.show()

    nbwindow = len(data) // window
    print('nbwindow = len(data)={}//window'.format(nbwindow))
    data: np.ndarray = data[:nbwindow * window]
    data = data.reshape((nbwindow, window))
    downsample = data.sum(axis=1)
    ts = np.arange(len(downsample)) * window / rate * 1000  # ms

    # upwards = np.sign(np.diff(downsample))==1
    thresh = np.max(downsample) * 0.4
    bigger = downsample >= thresh
    smaller = downsample < thresh
    bigger = np.roll(bigger, 1)
    crossing = np.logical_and(bigger, smaller)
    beats = np.logical_and(downsample > thresh, crossing)

    # pl.plot(ts,crossing)
    # pl.show()

    _ = np.nonzero(crossing)
    ts = ts[_]

    _ = zip([b[0] for b in beat_lines], ts)
    beat, beatInMs = zip(*_)
    beat = np.insert(beat,0,0)
    beatInMs = np.insert(beatInMs,0,0)

    f2 = interpolate.interp1d(beat, beatInMs, kind='cubic')


    def beat2timemono(beatnum):
        assert type(beatnum) in [int, float, np.int32, np.int64]
        if beatnum >= beat[-1]:
            endingSlope = (beatInMs[-1] - beatInMs[-2]) / (beat[-1] - beat[-2])
            return (beatnum - beat[-1]) * endingSlope + beatInMs[-1]
        else:
            _ = f2(beatnum)
            if type(_) == np.ndarray and np.size(_) == 1:
                _ = float(_)
            return _


    def beat2time(beatnums):
        if type(beatnums) == int or type(beatnums) == float:
            return beat2timemono(beatnums)
        else:
            return np.array([beat2timemono(bn) for bn in beatnums])


    # referencePitch = cm.pitchFromXmlNotation('0 C ')
    for vli, l in enumerate(vocal_lines):
        notesForJson = []
        for start, end, pitch, lyr in l:
            startms, endms = beat2time(start), beat2time(end)
            note = {'start': int(startms), 'end': int(endms), 'pitch': int(pitch), 'lyric': lyr}
            notesForJson.append(note)
        minPitchi = int(np.argmin([entry['pitch'] for entry in notesForJson]))
        maxPitchi = int(np.argmax([entry['pitch'] for entry in notesForJson]))
        maxPitch = notesForJson[maxPitchi]['pitch']
        minPitch = notesForJson[minPitchi]['pitch']

        #beat fusion
        for start, end, pitch, lyr in beat_lines:
            startms, endms = beat2time(start), beat2time(end)
            note = {'start': int(startms), 'end': int(endms), 'pitch': -1, 'lyric': lyr}
            notesForJson.append(note)
        notesForJson.sort(key=lambda x:x['start'])


        ref = 12 * np.floor(minPitch / 12.)
        content = {'notes': notesForJson, 'referencePitch': int(ref),
                   'range': maxPitch - ref + 4, 'vocalmin': minPitch, 'vocalmax': maxPitch}
        content = json.dumps(content,ensure_ascii=False)
        with open('../docs/json/{}{}.json'.format(batchname, vli), 'w', encoding='utf') as f:
            f.write(content)

    measureBeats = np.array(measureBeats)
    measureTimes = beat2time(measureBeats)
    qnpms=np.diff(measureBeats)/np.diff(measureTimes)
    bpm = qnpms*1000*60/8
    adjustPartTempo(part_list[0], bpm)
    etree.write('../docs/xml/{}.xml'.format(batchname))

    part_listnew = [ET.fromstring(ET.tostring(x)) for x in part_list]
    part_listDeclnew = [ET.fromstring(ET.tostring(x)) for x in root.find('part-list')]

    for parti, (part, partDec) in enumerate(zip(part_listnew, part_listDeclnew)):
        part: ET.Element = part

        pldec = root.find('part-list')
        for x in pldec.findall('score-part'):
            pldec.remove(x)

        for p in root.findall('part'):
            if p.tag == 'part':
                root.remove(p)

        adjustPartTempo(part, bpm)

        pldec.insert(0, partDec)
        root.insert(5, part)
        etree.write('../docs/xml/{}{}.xml'.format(batchname, parti))
