import xml.etree.ElementTree as et
import musik.common as cm
import math

etree = cm.loadxml('../score/0316bad.musicxml')
root: et.Element = etree.getroot()


def getDuration(note:et.Element):
    rest = note.find('rest') is not None
    # debug=et.tostring(note)
    dur: et.Element = note.find('duration')
    return int(dur.text),rest

# typedict = {
#     24:('half',True),
#     18:('half',False),
#     16:('half',False),
#     12:('quarter',True),
#     8:('quarter',False),
#     6:('eighth',True),
#     4:('eighth',False),
#     3:('16th',True),
#     2:('16th',False),
#             }

typedict = {
    24:('half',False,False),
    18:('half',False,True),#TODO
    16:('half',False,True),
    12:('quarter',False,False),
    8:('quarter',False,True),
    6:('eighth',False,False),
    4:('eighth',False,True),
    3:('16th',False,False),
    2:('16th',False,True),
            }


for pi,p in enumerate(root.findall('part')):
    p:et.Element = p

    for mi,m in enumerate(p.findall('measure')):
        m:et.Element = m

        if mi==23:
            for _ in m.findall('attribute'):
                m.remove(_)
            attrib = et.Element('attribute')
            m.insert(0,attrib)
            for _ in attrib:
                attrib.remove(_)
            attrib.insert(0,et.fromstring('<divisions>12</divisions>'))

        if mi>=23:
            durations=list(map(getDuration,m.findall('note')))
            durAndBlockers = []
            for duration,isrest in durations:
                if isrest:
                    durAndBlockers.append(duration)
                else:
                    durAndBlockers.extend([0,duration,0])
            durAndBlockers.append(0)
            linked = []
            _ = []
            for d in durAndBlockers:
                if d ==0:
                    if len(_)>0:
                        linked.append(_)
                    _=[]
                else:
                    _.append(d)


            connex=list(filter(lambda x:len(x)>0,linked))
            connex=list(map(lambda x:sum(x),connex))

            note_reserve = m.findall('note')
            for group in linked:
                #the first one takes it all
                n:et.Element = note_reserve.pop(0)
                n.find('duration').text = str(sum(group))
                if n.find('type') is None:
                    n.insert(0,et.Element('type'))
                n.find('type').text, dotOrNot,trip = typedict[sum(group)]

                if trip:
                    n.insert(0,et.fromstring("""
        <time-modification>
          <actual-notes>3</actual-notes>
          <normal-notes>2</normal-notes>
          </time-modification>"""))

                dt = n.find('dot')
                if dt is None and dotOrNot:
                    n.insert(0,et.fromstring('<dot />'))
                if dt is not None and not dotOrNot:
                    n.remove(dt)
                group.pop(0)
                for _ in group:
                    m.remove(note_reserve.pop(0))


            assert sum(connex)==24
            while len(connex)>=2:
                A=connex.pop()
                B=connex.pop()
                connex.append(math.gcd(A,B))

            gcd = connex[0]

            dividedInto = 24/gcd

            if int(dividedInto)%3==0:
                print('triplet for measure {}'.format(mi+1))
            else:
                #remove all dots
                pass

etree.write('../score/0316.musicxml')

