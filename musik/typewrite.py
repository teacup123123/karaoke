import clipboard
import pyautogui
import time as time
import re

# pinyin='da hai man shi bo lang bu jian chuan ru gang ta zhan zai ma tou yao wang zhe bei fang qing si fei shang bai shuang xin hai dian zhe ta xin li mei shuo de'
# pinyin='na ju hui da sha sha de gu niang dai yi duo hua deng zhe ta hui lai ya xiao xiao de zui er cang bu zhu hua dou chang cheng qing ge ya qing shan yi jiu sui yue ru chang ye bu jian ta bei shang you qing de ren bie wen ta ni hai yuan yi ma'
# pinyin='deng zhe ta hui lai ya'
# pinyin='xiao xiao de zui er cang bu zhu hua'
# pinyin='sha sha de gu niang dai yi duo hua deng zhe ta hui lai ya xiao xiao de zui er cang bu zhu hua dou chang cheng qing ge ya qing shan yi jiu sui yue ru chang ye bu jian ta bei shang you qing de ren bie wen ta ni hai yuan yi ma'
# pinyin='xiao xiao de zui er cang bu zhu hua dou chang cheng qing ge ya qing shan yi jiu sui yue ru chang ye bu jian ta bei shang you qing de ren bie wen ta ni hai yuan yi ma'
# pinyin = '等無心愛的人猶原一咧人未輸咧夢中醒來總是空伊的批信無來苦苦我咧等待心中毋敢講我的央望你走去卓位予我無望大海總是茫茫夜夜咧等夜夜咧夢人生擱存幾冬心愛的人夢中的人暗夜存我一人有情的人請毋通未記阮的名若有來生請叫阮的名'
# pinyin = '你走去卓位予我無望大海總是茫茫夜夜咧等夜夜咧夢人生擱存幾冬心愛的人夢中的人暗夜存我一人有情的人請毋通未記阮的名若有來生請叫阮的名'
# pinyin = '若有來生請叫阮的名'
# pinyin = '猶原一咧人未輸咧夢中醒來總是空伊的批信無來苦苦我咧等待心中毋敢講我的央望你走去卓位予我無望大海總是茫茫夜夜咧等夜夜咧夢人生擱存幾冬心愛的人夢中的人暗夜存我一人有情的人請毋通未記阮的名'
# pinyin = '我的央望你走去卓位予我無望大海總是茫茫夜夜咧等夜夜咧夢人生擱存幾冬心愛的人夢中的人暗夜存我一人有情的人請毋通未記阮的名'
# pinyin = '一人有情的人請毋通未記阮的名'
#
# pinyin = ' '.join('*{}*'.format(i) for i,c in enumerate(pinyin))
#
# pyautogui.confirm('you have 5 secs')
# time.sleep(5)
#
# pyautogui.typewrite(pinyin)

def autotype(english_str:str,type=0):
    for c in english_str.split():
        x = re.search('[a-z]|[0-9]]', c)

    if type==0:
        pinyin = english_str
    else:
        pinyin = ' '.join('*{}*'.format(i) for i, c in enumerate(english_str))

    pyautogui.confirm('you have 5 secs')
    time.sleep(5)



    pyautogui.typewrite(pinyin)

def autocopy(string:str):

    pyautogui.confirm('you have 5 secs')
    time.sleep(5)

    for c in string:
        if c==' ':
            pyautogui.typewrite(c)
        else:
            clipboard.copy(c)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('right')



if __name__ == '__main__':
    # autotype('hello')
    lyrs = """
    等無心愛的人 猶原一咧人 
未輸咧夢中 醒來總是空 
伊的批信無來 苦苦我咧等待 
心中毋敢講 我的央望 
你走去卓位 予我無望 大海總是茫茫 
夜夜咧等 夜夜咧夢 人生擱存幾冬 
心愛的人 夢中的人 暗夜存我一人 
有情的人 請毋通 未記阮的名

若有來生 請叫阮的名
    """

    autocopy(''.join(lyrs.split()))