import random
import suan_fa_yj

def yi_bian(dayan):
    left, right = [], []
    for i in dayan:
        hand = random.choice((left, right))
        hand.append(i)

    ren = random.choice(right)
    right.remove(ren)
    # print(ren)

    left_yu = len(left) % 4
    if left_yu == 0:
        left_yu = 4

    right_yu = len(right) % 4
    if right_yu == 0:
        right_yu = 4

    # print(left_yu, right_yu)

    left_xx = random.sample(left, left_yu)
    right_xx = random.sample(right, right_yu)
    # print(left_xx, right_xx, [ren])
    dayan = left + right
    xxx = left_xx + right_xx + [ren]

    dayan = [item for item in dayan if item not in xxx]
    return dayan


def get_yao(dayan):
    dayan = yi_bian(dayan)
    # print(dayan, len(dayan))

    dayan = yi_bian(dayan)
    # print(dayan, len(dayan))

    dayan = yi_bian(dayan)
    # print(dayan, len(dayan))

    return int(len(dayan) / 4)

def dayanshifa():
    dayan = ['chao' + str(i) for i in range(1, 51)]
    yi = random.choice(dayan)
    dayan.remove(yi)

    # 365233 6:23097 6.3%   9:68253 18.7%  7:114500 31.3% 8: 159385 43.6%
    numlist = []
    for i in range(6):
        numlist.append(get_yao(dayan))
        #with open('file.txt', 'a') as file:
        #    file.write(str(get_yao(dayan)) + '\n')
    yin_yang_list = suan_fa_yj.convert_to_yin_yang(numlist)
    ret = suan_fa_yj.get_guaming_dongyao(yin_yang_list, numlist)
    return ret

'''
宋代哲学家、思想家朱熹在其著作《易学启蒙》中总结的断卦方法：
。前十卦主贞，后十卦主悔，前十卦是指初爻不变的十卦，后十卦是指初爻有变的十卦；
④有四爻变，以之卦的两个不变爻为准进行判断，而以下爻为主；
⑤有五爻变，看之卦不变的一爻；
⑥六爻皆变，乾变坤看乾卦用九；坤变乾看坤卦用六。其余各卦看之卦《彖辞》；
⑦六爻皆不变，看本卦《彖辞》，以内卦为贞，外卦为悔。
返回值:卦爻词位置,本卦/之卦,变爻数   如:1, 本卦, 1,   2,之卦,5
0:本卦卦词, 1:初爻词 2:二爻词, 3:三爻词, 4:四爻词, 5:五爻词, 6:六爻词, 7:之卦词
'''
def find_special_number(nums):
    biaoyao_list = []
    jingyao_list = []
    for i, num in enumerate(nums):
        if num == 6 or num == 9:
            biaoyao_list.append((i+1))
        else:
            jingyao_list.append((i+1))
    #print(biaoyao_list, jingyao_list)
    if len(biaoyao_list) == 0:
        return 0, '本卦', len(biaoyao_list)
    elif len(biaoyao_list) == 1:
        return biaoyao_list[0], '本卦', len(biaoyao_list)
    elif len(biaoyao_list) == 2:
        return biaoyao_list[1], '本卦', len(biaoyao_list)
    elif len(biaoyao_list) == 3:
        if biaoyao_list[0] == 1:
            return 0, '之卦', len(biaoyao_list)
        else:
            return 0, '本卦', len(biaoyao_list)
    elif len(biaoyao_list) == 4:
        return jingyao_list[0], '之卦', len(biaoyao_list)
    elif len(biaoyao_list) == 5:
        return jingyao_list[0], '之卦', len(biaoyao_list)
    elif len(biaoyao_list) == 6:
        if sum(nums) == 36:
            return 7, '用六', len(biaoyao_list)
        elif sum(nums) == 54:
            return 7, '用九', len(biaoyao_list)
        else:
            return 0, '之卦', len(biaoyao_list)

if __name__ == '__main__':
    ret = dayanshifa()
    print(ret)
    print(ret[2], find_special_number(ret[2]))
    print("=======================================")

    sss = [
        [7, 7, 8, 8, 8, 7],
        [7, 7, 8, 8, 9, 7],
        [9, 7, 8, 8, 8, 7],
        [7, 6, 8, 8, 9, 7],
        [7,7,9,9,9,7],
        [9,9,9,7,7,7],
        [6, 7, 9, 9, 9, 7],
        [9, 9, 9, 6, 6, 7],
        [9, 9, 9, 6, 6, 6],
        [9,9,9,9,9,9],
        [6,6,6,6,6,6]]
    for s in sss:
        print(s, find_special_number(s))



