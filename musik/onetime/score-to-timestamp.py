import pygame, time
import pygame.locals as locs
import numpy as np

now = time.time()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Pygame Keyboard Test')
pygame.mouse.set_visible(0)

singleton ='前奏小提2.txt'
for track in [singleton]:#'前奏小提歌詞.txt']:#'saxophone 歌詞.txt']:#'歌詞.txt',
    treated = 'treated/treat_{}'.format(track)
    timed = 'treated/timed_{}'.format(track)

    with open(treated, 'r', encoding='utf-8') as f:
        linez = f.readlines()

        print('treating {}'.format(track))

        timestampeds = []

        responsible = {i:None for i in [257,258,259]}

        while True:
            event = pygame.event.wait()
            if event.type == 2 and event.dict['key'] in [257,258,259]:
                l=linez.pop(0)
                responsible[event.dict['key']]=l
                timestamped = '{}:{}'.format(time.time() - now, l)
                print(timestamped)
                timestampeds.append(timestamped)
            if event.type == 3 and event.dict['key'] in [257,258,259]:
                l,responsible[event.dict['key']] = responsible[event.dict['key']],None
                timestamped = '{}:{}'.format(time.time() - now, l)
                timestampeds.append(timestamped)
            if all(responsible[i]==None for i in [257,258,259]) and len(linez)==0:
                break

        with open(timed, 'w+', encoding='utf-8') as f:
            f.writelines(timestampeds)
