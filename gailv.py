import numpy as np
import suan_fa_yj
import imgGen_local3

imgGen_local3.read_guaming(imgGen_local3.guaming_miaoshu_map)
imgGen_local3.read_yijing(imgGen_local3.yi_zhengwen_map)

def get_bian_gua(numlist):
    biangua_numlist = []
    for i, num in enumerate(numlist):
        if numlist[i] == 6:
            biangua_numlist.append(7)
        elif numlist[i] == 9:
            biangua_numlist.append(8)
        else:
            biangua_numlist.append(numlist[i])

    yin_yang_list = suan_fa_yj.convert_to_yin_yang(biangua_numlist)
    #print(yin_yang_list)
    xiang_2 = suan_fa_yj.get_bagua(yin_yang_list)
    gua_ming = xiang_2 + suan_fa_yj.liu_shi_gua[xiang_2]
    #print(gua_ming)
    return gua_ming, biangua_numlist

for i in range(4096):
    s = np.base_repr(i, base=4, padding=6)
    s = s[-6:]
    numlist = [int(x)+6 for x in s]

    dayan_dict = {6:1, 7:5, 8:7, 9:3}
    #dayan_dict = {6: 1, 7: 3, 8: 3, 9: 1}

    gailv_ret = dayan_dict[numlist[0]] * dayan_dict[numlist[1]] * dayan_dict[numlist[2]] * dayan_dict[numlist[3]] * dayan_dict[numlist[4]] * dayan_dict[numlist[5]]

    #print(s, numlist)
    yin_yang_list = suan_fa_yj.convert_to_yin_yang(numlist)
    #print(yin_yang_list)
    xiang_2 = suan_fa_yj.get_bagua(yin_yang_list)
    gua_ming = xiang_2 + suan_fa_yj.liu_shi_gua[xiang_2]

    gua, yao, _ = suan_fa_yj.get_guaming_dongyao(yin_yang_list, numlist)

    qu_gua, qu_yao = gua_ming[2:], yao
    if yao == '六爻变':
        qu_gua = biangua_ming[2:]
        qu_yao = ''
    weizhi = suan_fa_yj.get_dongyao_weizhi(qu_yao)
    gua_yao_ci = imgGen_local3.yi_zhengwen_map[qu_gua][weizhi]
    biangua_ming, biangua_numlist = get_bian_gua(numlist)

    if len(yao) == 0:
        yao = '无动爻'
    print(gua_ming[2:]+'之'+biangua_ming[2:], ''.join(map(str, numlist)), yin_yang_list, gua_ming, yao, gailv_ret, biangua_ming, ''.join(map(str, biangua_numlist)), gua_yao_ci)