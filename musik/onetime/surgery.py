import musik as ms
import xml.etree.ElementTree as et

tree = ms.loadxml('../../score/0323_Tikai.musicxml')
root = tree.getroot()

lyr = ''.join("""
有情的人 別問她 你還願意嗎
""".split())
lyr = [c for c in lyr]

for meas in root.findall('part')[2]:
    measnum = int(meas.attrib['number'])
    if measnum>=92 and measnum<=95:
        for note in meas.findall('note'):
            if len(lyr)==0:
                break
            old = note.find('lyric')
            if old is not None:
                note.remove(old)

            _=note.find('notations')
            if _ is not None:
                _ = _.find('tied')
                if _ is not None:
                    if _.attrib['type']=='stop':
                        continue


            if note.find('rest') is None:
                insertee = lyr.pop(0)
                note:et.Element
                note.insert(0,et.fromstring("""<lyric number="1" default-x="6.58" default-y="-70.00" relative-y="-24.40">
          <syllabic>single</syllabic>
          <text>{}</text>
          </lyric>""".format(insertee)))

tree.write('../../score/0323_Tikai.musicxml',encoding='utf8')