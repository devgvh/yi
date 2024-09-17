import random
'''
关于动爻的断法：
六爻安定的，以本卦卦辞断之。
一爻动，以动爻之爻辞断之。
两爻动者，则取阴爻之爻辞以为断，盖以“阳主过去，阴主未来”故也。如天风姤卦，初六、九五两爻皆动，则以初六爻断之，九五爻为辅助之断，“阳主过去，阴主未来”，其中大有学问。
所动的两爻如果同是阳爻或阴爻，则取上动之爻断之，如既济卦，初九、九五两爻皆动，则以九五爻的爻辞为断。
三爻动者，以所动三爻的中间一爻之爻辞为断，如卦，九二、九四、九五等三爻皆动，则取九四爻的爻辞为断。
四爻动者，以下静之爻辞断之，如火水未济卦，九二、六三、九四、六五四爻皆动，则以初六爻的爻辞断之，如初六、六三、九四、六五等四爻皆动，则取九二爻的爻辞断之。
五爻动者，取静爻的爻辞断之。
六爻皆动的卦，如果是乾坤二卦，以“用九”、“用六”之辞断之，如乾卦六爻皆动，则为群龙无首，吉。
乾坤两卦外其余各卦，如果是六爻皆动，则以变卦的彖辞断之，如天风姤卦六爻皆动，则以乾卦的彖辞断之，因为姤卦是自乾卦变来，姤卦是在八宫卦的乾宫之中。
请帮我实现一个函数，输入从6到9随机的6个数字的列表
如果只有一个数字是6或者9，那就返回那个数字和这个数字在列表中的位置。
如输入[8, 7, 8, 9, 7, 8]，则输出9,4
如果输入中有两个数字是6或者9，当两个数字相同时，取后面那个数字，并返回它的位置，当两个数字不同时，返回数字6和它的位置
如输入[8, 7, 6, 6, 7, 8]，则输出6,4
如输入[8, 7, 6, 9, 7, 8]，则输出6,3
如果输入中有三个数字是6或者9，返回这三个数字中间的那个数，和它的位置
如输入[9, 6, 8, 9, 7, 8]，则输出6,2
bagua_dict = {
    "阳阳阳": "乾",
    "阳阳阴": "兑",
    "阳阴阴": "离",
    "阳阴阳": "震",
    "阴阳阳": "巽",
    "阴阳阴": "坎",
    "阴阴阳": "艮",
    "阴阴阴": "坤"
}'''

bagua_with_elements_dict = {
    "阳阳阳": "天",
    "阳阳阴": "泽",
    "阳阴阳": "火",
    "阳阴阴": "雷",
    "阴阳阳": "风",
    "阴阳阴": "水",
    "阴阴阳": "山",
    "阴阴阴": "地"
}

liu_shi_gua = {
    "天天":"乾",
    "泽天":"夬",
    "火天":"大有",
    "雷天":"大壮",
    "风天":"小畜",
    "水天":"需",
    "山天":"大畜",
    "地天":"泰",
    "天泽":"履",
    "泽泽":"兑",
    "火泽":"睽",
    "雷泽":"归妹",
    "风泽":"中孚",
    "水泽":"节",
    "山泽":"损",
    "地泽":"临",
    "天火":"同人",
    "泽火":"革",
    "火火":"离",
    "雷火":"丰",
    "风火":"家人",
    "水火":"既济",
    "山火":"贲",
    "地火":"明夷",
    "天雷":"无妄",
    "泽雷":"随",
    "火雷":"噬嗑",
    "雷雷":"震",
    "风雷":"益",
    "水雷":"屯",
    "山雷":"颐",
    "地雷":"复",
    "天风":"姤",
    "泽风":"大过",
    "火风":"鼎",
    "雷风":"恒",
    "风风":"巽",
    "水风":"井",
    "山风":"蛊",
    "地风":"升",
    "天水":"讼",
    "泽水":"困",
    "火水":"未济",
    "雷水":"解",
    "风水":"涣",
    "水水":"坎",
    "山水":"蒙",
    "地水":"师",
    "天山":"遁",
    "泽山":"咸",
    "火山":"旅",
    "雷山":"小过",
    "风山":"渐",
    "水山":"蹇",
    "山山":"艮",
    "地山":"谦",
    "天地":"否",
    "泽地":"萃",
    "火地":"晋",
    "雷地":"豫",
    "风地":"观",
    "水地":"比",
    "山地":"剥",
    "地地":"坤"
}



def generate_and_sum():
    num1 = random.choice([2, 3])
    num2 = random.choice([2, 3])
    num3 = random.choice([2, 3])
    total = num1 + num2 + num3
    return total

def call_six_times():
    results = []
    for i in range(6):
        result = generate_and_sum()
        results.append(result)
    return results

def convert_to_yin_yang(numbers):
    result = ''
    for num in numbers:
        if num % 2 == 0:
            result += '阴'
        else:
            result += '阳'
    return result


def get_bagua(text):
    first_three = text[:3]
    last_three = text[3:]
    nei_gua = bagua_with_elements_dict[first_three]
    wai_gua = bagua_with_elements_dict[last_three]

    return wai_gua + nei_gua


# ret 返回主动爻和它的位置（从1~6），如6，2代表主动爻为第二爻，值为6
# 特殊情况：0,0 ：无变爻，6，0：6变爻全为6， 9，0：6变爻全为9， 0,-1：6个变爻
def find_special_number(nums):
    count_6 = 0
    count_9 = 0
    list_6 = []
    list_9 = []

    for i, num in enumerate(nums):
        if num == 6:
            count_6 += 1
            list_6.append(i + 1)
        elif num == 9:
            count_9 += 1
            list_9.append(i + 1)

    if count_6 + count_9 == 0:
        return 0, 0
    elif count_6 + count_9 == 6:
        if count_6 == 6:
            return 6, 0
        elif count_9 == 6:
            return 9, 0
        else:
            return 0, -1
    elif count_6 + count_9 == 1:
        return (6 if count_6 == 1 else 9), (list_6[0] if count_6 == 1 else list_9[0])
    elif count_6 + count_9 == 2:
        if count_6 == 2:
            return 6, list_6[1]
        elif count_9 == 2:
            return 9, list_9[1]
        else:
            return 6, list_6[0]
    elif count_6 + count_9 == 3:
        combined = list_6 + list_9
        combined.sort()
        return nums[combined[1] - 1], combined[1]
    elif count_6 + count_9 == 4:
        given_list = [1, 2, 3, 4, 5, 6]
        combined = list_6 + list_9
        missing_numbers = list(set(given_list) - set(combined))
        return nums[min(missing_numbers) - 1], min(missing_numbers)
    elif count_6 + count_9 == 5:
        given_list = [1, 2, 3, 4, 5, 6]
        combined = list_6 + list_9
        missing_numbers = list(set(given_list) - set(combined))
        return nums[missing_numbers[0] - 1], missing_numbers[0]

def reverse_yin_yang(s):
    result = ""
    for char in s:
        if char == "阴":
            result += "阳"
        elif char == "阳":
            result += "阴"
        else:
            result += char
    return result
# ret 返回主动爻和它的位置（从1~6），如6，2代表主动爻为第二爻，值为6
# 特殊情况：0,0 ：无变爻，6，0：6变爻全为6， 9，0：6变爻全为9， 0,-1：6个变爻
weizhi_list = ['初', '二', '三', '四', '五', '上', '用']
def get_dongyao_weizhi(yao):
    if yao == '':
        return 0
    for i, wz in enumerate(weizhi_list):
        if wz in yao:
            return i + 1

def get_numlist(gua, yao):
    guaxiang = ''
    yinyang_list = ''
    for key, value in liu_shi_gua.items():
        if value == gua:
            guaxiang = key
    print(guaxiang)
    for k, v in bagua_with_elements_dict.items():
        if v == guaxiang[0]:
            yinyang_list = k[::-1] + yinyang_list
        if v == guaxiang[1]:
            yinyang_list = yinyang_list + k[::-1]

    yinyang_list = yinyang_list[::-1]
    dongyao_num = get_dongyao_weizhi(yao)
    numlist = []
    for x in yinyang_list:
        if x == '阴':
            numlist.append(8)
        else:
            numlist.append(7)
    if yao != '':
        numlist[dongyao_num-1] = 9 if numlist[dongyao_num-1] == 7 else 6

    return numlist





def get_guaming_dongyao(yin_yang_list, num_list):
    ret = find_special_number(num_list)
    #if ret == (0, -1):
    #    yin_yang_list = reverse_yin_yang(yin_yang_list)
    #    print("reverse", yin_yang_list)

    xiang_2 = get_bagua(yin_yang_list)
    gua_ming = xiang_2 + liu_shi_gua[xiang_2]
    #print(gua_ming)
    dong_yao = ""

    if ret == (0, 0):
        dong_yao = ""
    elif  ret == (0, -1):
        dong_yao = '六爻变'
    elif ret == (6, 0):
        dong_yao = "用六"
    elif ret == (9, 0):
        dong_yao = "用九"
    else:
        weizhi = weizhi_list[ret[1] - 1]
        yao = ''
        if ret[0] == 7 or ret[0] == 9:
            yao = '九' #阳为九
        elif ret[0] == 6 or ret[0] == 8:
            yao = '六' #阴为六

        if weizhi == '初' or weizhi == '上':
            dong_yao = weizhi + yao
        else:
            dong_yao = yao + weizhi

    return gua_ming, dong_yao, num_list

def suan_yi_gua():
    num_list = call_six_times()
    #print(num_list)
    yin_yang_list = convert_to_yin_yang(num_list)
    #print(yin_yang_list)
    return get_guaming_dongyao(yin_yang_list, num_list)

#gua, yao, numlist = suan_yi_gua()
#print(gua, yao, numlist)
#print(get_numlist(gua[2:], yao))

#print(suan_yi_gua())
'''
ret = suan_yi_gua("阳阳阳阳阳阳", [9,9,9,9,9,9])
ret = suan_yi_gua("阴阴阴阴阴阴", [6,6,6,6,6,6])
ret = suan_yi_gua("阴阴阳阴阴阴", [6,6,9,6,6,6])
ret = suan_yi_gua("阴阳阳阳阳阴", [6,9,9,9,9,6])
'''

# 测试用例
'''
print("-----测试------")
print(find_special_number([8, 7, 8, 9, 7, 8]))  # 输出：(9, 4)
print(find_special_number([8, 7, 8, 8, 7, 6]))  # 输出：(6, 6)
print(find_special_number([8, 7, 6, 6, 7, 8]))  # 输出：(6, 4)
print(find_special_number([9, 9, 8, 8, 7, 8]))  # 输出：(9, 2)
print(find_special_number([8, 7, 6, 9, 7, 8]))  # 输出：(6, 3)
print(find_special_number([9, 8, 8, 7, 7, 6]))  # 输出：(6, 6)
print(find_special_number([6, 9, 8, 7, 7, 6]))  # 输出：(6, 3)
print(find_special_number([9, 9, 8, 6, 7, 7]))  # 输出：(6, 3)
print(find_special_number([8, 9, 6, 7, 9, 7]))  # 输出：(6, 3)
print(find_special_number([9, 9, 8, 6, 6, 7]))  # 输出：(6, 3)
print(find_special_number([6, 9, 6, 7, 9, 7]))  # 输出：(6, 3)
print(find_special_number([9, 9, 6, 6, 6, 8]))  # 输出：(6, 3)
print(find_special_number([6, 9, 9, 7, 9, 9]))  # 输出：(6, 3)
'''