import pyautogui
import time
from musik.common import translate_timed

fin = 'treated/timed_saxophone 歌詞.txt'
double = True
# coord_upOctave = (972, 373)
# coord_downOctave = (974, 404)
ref = -3  # this is our tonality
offset = -15
refOctave = 0
currentOctave = -1

midicity_keyboard = 'awsedftgyhuj'




pyautogui.confirm('Do-Re-Mi-Fa-So-La-Si-CONFIRM')
pressed = set()

with open(fin, encoding='utf8') as f:
    pyautogui.keyDown('a')
    time.sleep(1)
    pyautogui.keyUp('a')
    genesis = time.time()+offset


    notes = f.readlines()
    while len(notes)>0:
        event = notes.pop(0)
        t, lyric, pitch = translate_timed(event)
        pitch += ref


        toPress = midicity_keyboard[pitch % 12]
        destOctave = pitch // 12

        if destOctave!=currentOctave:
            continue #ignore other octaves

        key = (lyric, pitch)  #TODO 疊詞無法

        wait = (genesis + t) - time.time()
        if wait > 0:
            time.sleep(wait)

        if key in pressed:
            pressed.remove(key)
            pyautogui.keyUp(toPress)
            # print('up: {}'.format(toPress))
        else:
            pressed.add(key)
            pyautogui.keyDown(toPress)
            # print('down: {}'.format(toPress))


        # while currentOctave != destOctave:
        #     diff = destOctave - currentOctave
        #     if diff > 0 :
        #         pyautogui.moveTo(coord_upOctave[0],coord_upOctave[1])
        #         pyautogui.click()
        #         currentOctave+=1
        #     else:
        #         pyautogui.moveTo(coord_downOctave[0],coord_downOctave[1])
        #         pyautogui.click()
        #         currentOctave-=1


pyautogui.confirm('finished')