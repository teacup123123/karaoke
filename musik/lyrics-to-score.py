##
relativescales = list('zxcvbnmasdfghjqwertyu')
relativescales_sharp = [c.capitalize() for c in relativescales]

mapping = dict((c, i % 7 + 1) for i, c in enumerate(relativescales))
numbermap = dict((c, i // 7 - 1) for i, c in enumerate(relativescales))

for source in ['bass.txt']:#'歌詞.txt', 'saxophone 歌詞.txt','前奏小提歌詞.txt']:

    with open(source, encoding='utf8') as f:
        caught = f.readlines()

    caught = ''.join(caught)
    caught = ''.join(caught.split())  # removes whitespaces

    lyrics = []
    tones = []
    for c in caught:
        if c in relativescales or c in relativescales_sharp:
            tones.append(c)
        else:
            lyrics.append(c)

    relativetones = ['{}{}{}'.format(mapping[t.lower()], '' if t.islower() else '#' ,
                                     '' if numbermap[t.lower()] == 0 else
                                     '+' if numbermap[t.lower()] == 1 else
                                     '-') for t in
                     tones]
    assert len(lyrics) == len(tones)

    with open('treated\\treat_' + source, 'w+', encoding='utf-8') as f:
        for l, t in zip(lyrics, relativetones):
            f.write('{}{}\n'.format(l, t))
