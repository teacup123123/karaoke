fp = 'treated/timed_前奏小提2.txt'
offset = -20

with open(fp,encoding='utf8') as f:
    linez = f.readlines()
    newlines = []
    for l in linez:
        t, r = l.split(':')
        t=float(t)+offset
        nl = '{}:{}'.format(t,r)
        newlines.append(nl)
    print(''.join(newlines))
