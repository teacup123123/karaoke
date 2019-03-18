import xml.etree.ElementTree as et
import musik.common as cm
import math

etree = cm.loadxml('../score/0316bad.musicxml')
root: et.Element = etree.getroot()

for pi,p in enumerate(root.findall('part')):
    p:et.Element = p

    for mi,m in enumerate(p.findall('measure')):
        m:et.Element = m

        notes = m.findall('note')
        for ni,n in enumerate(notes):
            # n:et.Element
            if 'print-object' in n.attrib:
                m.remove(n)
            #     lastnoteDuration = notes[ni-1].find('duration')
            #     lastnoteDuration.text = str(int(lastnoteDuration.text)+int(n.find('duration').text))
            # n.find('duration').text = str(int(float(n.find('duration').text)))
        direction = m.find('direction')
        if direction is not None:
            direction = direction.find('direction-type')
            if direction is not None:
                for x in direction.findall('words'):
                    direction.remove(x)


etree.write('../score/0316bad.musicxml')

