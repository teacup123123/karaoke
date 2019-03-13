import re

file = 'bass.txt'

caught = ''
with open(file,encoding='utf8') as f:
    ls=f.readlines()
    ls = ''.join(ls)
    for c in ls:
        o=re.search('[a-z]|[A-Z]',c)
        if o is None:
            caught +=c

print(caught)
