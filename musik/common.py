import itertools
import xml.etree.ElementTree as ET
import numpy as np

simple_map = {1: 0,
              2: 2,
              3: 4,
              4: 5,
              5: 7,
              6: 9,
              7: 11}


def translate_timed(start):
    timeInSecs, remain = start.split(':')
    lyric = remain[0]
    remain: str = remain[1:]
    sharp = '#' in remain
    pitch = simple_map[int(remain[0])]
    while '+' in remain:
        remain = remain.replace('+', '', 1)
        pitch += 12
    while '-' in remain:
        remain = remain.replace('-', '', 1)
        pitch -= 12
    pitch += sharp
    # print(float(timeInSecs))
    return float(timeInSecs), lyric, pitch


keys = 'C,C#,D,D#,E,F,F#,G,G#,A,A#,B'.split(',')


def absolute_notation(pitch):
    octave = pitch // 12
    pitch = pitch % 12

    return keys[pitch], octave


def loadxml(path):
    tree = ET.parse(path)
    return tree


def loadLyr(file):
    with open(file, encoding='utf8') as f:
        pronounciation = f.readlines()
        pronounciation = ''.join(pronounciation)
        pronounciation = pronounciation.split()
        return pronounciation


def fifthdict(fifthnum: int):
    pitchModulos = np.array([0,2,4,5,7,9,11],dtype=int)
    pitchModulos = np.mod(pitchModulos + 7 * fifthnum,12)
    pitchModulos = np.sort(pitchModulos)
    if np.sign(fifthnum)<0 and pitchModulos[0]==1:
        pitchModulos = np.roll(pitchModulos,1)
        pitchModulos[0]-=12

    items = zip('CDEFGAB',pitchModulos)
    return dict(items)


def pitchFromXmlNotation(pitchstr: str,natural=False):
    '''
    returns 0 for C2
    half tone = 1
    -1 used as drumbeat, whose lyrics change keys

    :param pitchstr:
    :return:
    '''

    strlist = pitchstr.split()
    if strlist[0] == 'drum':
        return -1

    if natural:
        fifth = fifthdict(0)
    else:
        fifth = fifthdict(int(strlist[0]))
    note = fifth[strlist[1]]+ int(strlist[2])*12
    alteration = int(strlist[3]) if len(strlist)==4 else 0

    return note + alteration


def findParts(root: ET.Element):
    part_liste: ET.Element = root.find('part-list')
    part_list = part_liste.findall('score-part')
    found_beat_part_num = None
    for score_part in part_list:
        score_part: ET.Element
        instrument_name: ET.Element = score_part.find('part-name')
        if instrument_name.text == 'Finger Snap':
            print('found Finger Snap, using as beat')
            found_beat_part_num = score_part.attrib['id']

            #delete this part from the xml tree since finger snap is not good
            part_liste.remove(score_part)

    vocal_lines = []
    beat_lines = []
    measureBeats = []
    part_list = root.findall('part')
    for part in part_list:
        part: ET.Element  # containing many measures
        vocal_lines_in_part = dict()

        meas_list = part.findall('measure')
        globaltime = 0
        keySig = 'x'
        for measi, meas in enumerate(meas_list):
            measureBeats.append(globaltime)
            meas: ET.Element
            for _ in meas.findall('direction'):
                meas.remove(_)
            attr: ET.Element = meas.find('attributes')
            if attr is not None:
                key: ET.Element = attr.find('key')
                if key is not None:
                    fifth: ET.Element = key.find('fifths')
                    keySig = fifth.text

            localTime = 0

            for elt in meas:
                elt: ET.Element
                if elt.tag in ['note', 'backup']:
                    if elt.tag == 'backup':
                        localTime = 0
                    else:
                        assert elt.tag == 'note'
                        voice: ET.Element = elt.find('voice')
                        vocal_lines_in_part[voice.text] = vocal_lines_in_part.get(voice.text, [])
                        rest = elt.find(
                            'rest')
                        dur = int(elt.find('duration').text)
                        notations: ET.Element = elt.find('notations')
                        tied: ET.Element = notations.find('tied') if notations is not None else None
                        if rest is not None:
                            localTime += dur
                        else:
                            start = globaltime + localTime
                            lyr: ET.Element = elt.find('lyric')
                            lyr: ET.Element = lyr.find('text') if lyr is not None else None
                            pitch: ET.Element = elt.find('pitch')
                            if pitch is not None:
                                step: ET.Element = pitch.find('step')
                                octave: ET.Element = pitch.find('octave')
                                alter: ET.Element = pitch.find('alter')
                                altertext = '' if alter is None else alter.text
                                pitch = ' '.join([keySig, step.text, octave.text, altertext])  # TODO
                            else:
                                pitch = 'drum'

                            if lyr is not None:
                                lyr = lyr.text
                            else:
                                lyr = ''
                            note = (start,
                                    start + dur,
                                    pitchFromXmlNotation(pitch,True),
                                    lyr,
                                    True if tied is not None and tied.attrib['type'] == 'start' else False)
                            vocal_lines_in_part[voice.text].append(note)
                            localTime += dur

            globaltime += localTime
            # print('meas {} of part {}'.format(measi,part.attrib['id']))

            # print(elt.tag)
            # pass
            # i=meas.iter()

        for key in vocal_lines_in_part.keys():
            # link up
            def iterator():
                start0, end0, lyr0 = None, None, ''
                for start, end, pitch, lyr, accumulate in vocal_lines_in_part[key]:
                    if start0 == None:  # first
                        start0 = start
                    end0 = end
                    lyr0 += lyr

                    if not accumulate:
                        # save
                        yield start0, end0, pitch, lyr0
                        # reset
                        start0, end0, lyr0 = None, None, ''

            vocal_lines_in_part[key] = [x for x in iterator()]

            print('{}: {}'.format(key, vocal_lines_in_part[key]))
        vocal_lines_in_part = [v for k, v in vocal_lines_in_part.items()]
        if part.attrib['id'] == found_beat_part_num:
            beat_lines = vocal_lines_in_part[0]

            #delete this part from the xml tree since finger snap is not good
            root.remove(part)
        else:
            vocal_lines.extend(vocal_lines_in_part)
    print('plucked all info from sheet')
    return beat_lines, vocal_lines,part_list, measureBeats


if __name__ == '__main__':
    tree = loadxml('score/db.musicxml')
    lyrfile = 'treated/pinyin_bass'
    lyrics = loadLyr(lyrfile)

    root = tree.getroot()

    part: ET.Element = root.find('part')

    measures = part.findall('measure')
    notes = [[note for note in m.findall('note')] for m in measures]
    notes = list(itertools.chain.from_iterable(notes))
    # assert len(notes)==len(lyrics)

    count = 0
    for n in notes:
        n: ET.Element = n
        withLyric = True
        for tag in n:
            if tag.tag == 'rest':
                withLyric = False

            if tag.tag == 'notations':
                tied: ET.Element = tag.find('tied')
                if tied.attrib['type'] == 'stop':
                    withLyric = False

            if tag.tag == 'lyric':
                n.remove(tag)

        if withLyric:
            lyric = ET.SubElement(n, 'lyric')
            text = ET.SubElement(lyric, 'text')
            syllabic = ET.SubElement(lyric, 'syllabic')
            text.text = lyrics.pop(0) + '1'
            syllabic.text = 'single'
            count += 1

    with open('template.xml', encoding='utf8') as f:
        with open('output.xml', 'w', encoding='utf8', ) as fo:
            everything = f.read(-1)
            partstr = ET.tostring(part, encoding="unicode")
            fo.write(everything.format(part1=partstr))
            pass
