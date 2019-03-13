from musik.common import translate_timed, absolute_notation

sample = '''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 2.0 Partwise//EN"
                                "http://www.musicxml.org/dtds/partwise.dtd">
<score-partwise version="2.0">
  <identification>
    <encoding>
      <software>Finale 2011 for Windows</software>
      <software>Dolet Light for Finale 2011</software>
      <encoding-date>2015-11-24</encoding-date>
      <supports attribute="new-system" element="print" type="yes" value="yes"/>
      <supports attribute="new-page" element="print" type="yes" value="yes"/>
    </encoding>
  </identification>
  <defaults>
    <scaling>
      <millimeters>6.9674</millimeters>
      <tenths>40</tenths>
    </scaling>
    <page-layout>
      <page-height>1705</page-height>
      <page-width>1206</page-width>
      <page-margins type="both">
        <left-margin>86</left-margin>
        <right-margin>86</right-margin>
        <top-margin>86</top-margin>
        <bottom-margin>86</bottom-margin>
      </page-margins>
    </page-layout>
    <system-layout>
      <system-margins>
        <left-margin>0</left-margin>
        <right-margin>0</right-margin>
      </system-margins>
      <system-distance>146</system-distance>
      <top-system-distance>97</top-system-distance>
    </system-layout>
    <appearance>
      <line-width type="stem">1.0417</line-width>
      <line-width type="beam">5</line-width>
      <line-width type="staff">0.944</line-width>
      <line-width type="light barline">1.4583</line-width>
      <line-width type="heavy barline">5</line-width>
      <line-width type="leger">1.4583</line-width>
      <line-width type="ending">1.0417</line-width>
      <line-width type="wedge">1.25</line-width>
      <line-width type="enclosure">0.944</line-width>
      <line-width type="tuplet bracket">1.25</line-width>
      <note-size type="grace">75</note-size>
      <note-size type="cue">75</note-size>
    </appearance>
    <music-font font-family="Kousaku" font-size="19.75"/>
    <word-font font-family="ＭＳ ゴシック" font-size="9.9"/>
    <lyric-font font-family="ＭＳ ゴシック" font-size="9.9"/>
  </defaults>
  <part-list>
    <score-part id="P1">
      <part-name print-object="no">MusicXML Part</part-name>
      <score-instrument id="P1-I1">
        <instrument-name>Grand Piano</instrument-name>
      </score-instrument>
      <midi-instrument id="P1-I1">
        <midi-channel>1</midi-channel>
        <midi-program>1</midi-program>
        <volume>80</volume>
        <pan>0</pan>
      </midi-instrument>
    </score-part>
  </part-list>
  <!--=========================================================-->
  <part id="P1">
    <measure number="1" width="427">
      <print>
        <system-layout>
          <system-margins>
            <left-margin>57</left-margin>
            <right-margin>0</right-margin>
          </system-margins>
          <top-system-distance>230</top-system-distance>
        </system-layout>
        <measure-numbering>system</measure-numbering>
      </print>
      <attributes>
        <divisions>2</divisions>
        <key>
          <fifths>0</fifths>
          <mode>major</mode>
        </key>
        <time symbol="common">
          <beats>{tot8thNum}</beats>
          <beat-type>8</beat-type>
        </time>
        <clef>
          <sign>C</sign>
          <line>2</line>
        </clef>
      </attributes>
      <sound tempo="{tempo}"/>
      <sound tempo="{tempo}"/>
      {notes}
      <barline location="right">
        <bar-style>light-heavy</bar-style>
      </barline>
    </measure>
  </part>
  <!--=========================================================-->
</score-partwise>
'''

tab = '  '

tempo = 240 * 2  # quarter notes per minute
# 60qn/min = 1qn/s
# 120qn/min = 2qn/s
# 240qn/min = 4qn/s
# 480qn/min = 8qn/s V
# 1 qn = 0.125s
# 1 eighth = 0.0625s

# suppose that the human year is sensitive to rounding to 0.125s

unit = '8th'

rest = \
    '''<note default-x="252">
        <rest/>
        <duration>{duration}</duration>
        <voice>1</voice>
        <type>{unit}</type>
    </note>'''.replace('\t', tab)

note = \
    '''<note default-x="329">
        <pitch>
            <step>{step}</step>{alter}
            <octave>{octave}</octave>
        </pitch>
        <duration>{duration}</duration>
        <voice>1</voice>
        <type>{unit}</type>
        <dot/>
        <stem default-y="10">up</stem>
        <beam number="1">begin</beam>
        <lyric default-y="-80" number="1">
            <syllabic>single</syllabic>
            <text font-size="9.9">{hatsuon}</text>
        </lyric>
    </note>'''.replace('\t', tab)


def translate(fileo='test.xml', timed='treated/timed_歌詞.txt', lyrics='treated/pinyin_歌詞', refPitch=0):
    with open(timed, encoding='utf8') as f:
        subs = f.readlines()
        with open(lyrics, encoding='utf8') as f:
            pronounciation = f.readlines()
            pronounciation = ''.join(pronounciation)
            pronounciation = pronounciation.split()

            pressed = set()
            singing = None
            notes = []
            totalDuration = 0
            t_now = 0

            for entry in subs:
                tinS, lyric, pitch = translate_timed(entry)
                t = int(round(tinS * 8 * 2))
                pitch += refPitch

                FIN = False
                nextSinging = None
                if len(pressed) == 0:
                    # starting new note, patch the rest
                    if t > t_now:
                        notes.append(rest.format(unit=unit, duration=t - t_now))
                        totalDuration += t - t_now
                    singing = pitch
                elif singing == pitch:
                    FIN = True  # stopped correctly
                    nextSinging = None
                elif pitch not in pressed:
                    FIN = True
                    nextSinging = pitch

                if FIN:
                    assert singing is not None
                    # finish what was started
                    word = pronounciation.pop(0) + '1'

                    alter = ''
                    notation, octave = absolute_notation(singing)
                    if notation[-1] == '#':
                        alter = '<alter>1</alter>'
                    elif notation[-1] == 'b':
                        alter = '<alter>-1</alter>'
                    step = notation[0]

                    notes.append(
                        note.format(step=step, octave=octave + 4, duration=t - t_now, unit=unit, hatsuon=word,
                                    alter=alter)
                    )
                    totalDuration += t - t_now
                    singing = nextSinging

                t_now = t
                if pitch in pressed:
                    pressed.remove(pitch)
                else:
                    pressed.add(pitch)

            assert len(pressed) == 0
            notes = '\n'.join(notes)
            xml = sample.format(tempo=tempo, tot8thNum=totalDuration, notes=notes)
            with open(fileo, 'w', encoding='utf8') as f:
                f.write(xml)


if __name__ == '__main__':
    base = -3 # or -8 for E, -3 for A
    # translate(refPitch=base)
    # translate(refPitch=base,timed='treated/timed_前奏小提歌詞.txt',lyrics='treated/pinyin_小提1')
    translate(refPitch=base,timed='treated/timed_前奏小提2.txt',lyrics='treated/pinyin_小提2')
    # translate(refPitch=base,timed='treated/timed_bass.txt',lyrics='treated/pinyin_bass')