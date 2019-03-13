import itertools
import xml.etree.ElementTree as ET

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


if __name__ == '__main__':
    tree = loadxml('score/db.musicxml')
    lyrfile = 'treated/pinyin_bass'
    lyrics = loadLyr(lyrfile)

    root = tree.getroot()

    part:ET.Element = root.find('part')

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

    with open('template.xml',encoding='utf8') as f:
        with open('output.xml','w',encoding='utf8',) as fo:
            everything=f.read(-1)
            partstr=ET.tostring(part,encoding="unicode")
            fo.write(everything.format(part1=partstr))
            pass

