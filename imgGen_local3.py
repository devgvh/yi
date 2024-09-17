import random
import logging
from gevent import monkey
# 下面这句不加也能启动服务，但是你会发现Flask还是阻塞式单线程，在一个请求未返回时，
# 其他请求也会阻塞，所以请添加这句变成协程异步操作，可以单线程同时处理多个请求
monkey.patch_all()


from gevent.pywsgi import WSGIServer
from PIL import Image, ImageDraw, ImageFont
import textwrap
import suan_fa_yj
import test_dayan
import qianwen_api_test
import time
from flask import Flask, request, jsonify, send_file
# 示例用法
fontname = 'data/simsun.ttc'
guaming_miaoshu_map = {key: [] for key in suan_fa_yj.liu_shi_gua.values()}
yi_zhengwen_map = {key: [] for key in suan_fa_yj.liu_shi_gua.values()}
yi_xiang_map = {key: [] for key in suan_fa_yj.liu_shi_gua.values()}
tuan_map = {key: '' for key in suan_fa_yj.liu_shi_gua.values()}
guaxu_map = {key: 0 for key in suan_fa_yj.liu_shi_gua.values()}


def auto_print(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} before...")
        result = func(*args, **kwargs)
        print(f"Calling {func.__name__} after...")
        return result
    return wrapper

# 计算文本所需空间的宽度和高度
def get_text_size(draw, text, font):
    # 使用textbbox方法获取文本的尺寸
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height

def get_max_len(text, length):
    if len(text) <= length:
        return text
    else:
        return text[:length-1] + "\u2026"

def draw_gua_ming2(draw, text, fontsize, start_y, mid_width, f='black'):
    # 添加卦名到图片上
    font_l = ImageFont.truetype(fontname, fontsize)
    text_width, text_height = get_text_size(draw, text.strip(), font_l)
    x = mid_width - text_width // 2
    draw.text((x, start_y), text.strip(), fill=f, font=font_l)
    return start_y + fontsize

#不超过1行，24个字
def draw_gua_chi2(draw, text, line_words, font_size, start_x, start_y):
    font = ImageFont.truetype(fontname, font_size)
    text = get_max_len(text.strip(), line_words)
    draw.text((start_x, start_y), text, fill='black', font=font)
    return start_y + font_size

def draw_info(draw, font_size, start_x, starty):
    font = ImageFont.truetype(fontname, font_size)
    text = "起:大衍筮法 断:ning@通义千问max"
    draw.text((start_x + 2*font_size, starty), text, font=font, fill='black')

#不超过4行，96个字
def draw_xiang2(draw, text, line_words, font_size, start_x, start_y, max_lines, f='black'):
    font = ImageFont.truetype(fontname, font_size)
    text = get_max_len(text.strip(), line_words * max_lines)
    lines = textwrap.wrap(text, width=line_words)
    start_line = 0
    for line in lines:
        draw.text((start_x, start_y + start_line*(font_size)), line, font=font, fill=f)
        start_line += 1
    return start_y + (start_line) * (font_size)


def draw_yinyao(draw, x, y, col, w, bianyao_flag, fontsize):
    draw.line((x, y, x+4*fontsize,y),fill=col,width=w,joint=None)
    draw.line((x+5*fontsize, y, x+9*fontsize,y),fill=col,width=w,joint=None)
    if(bianyao_flag):
        #draw.text((x,y), 'X', fill='white', font=font_s)
        circle_center = (x + 9*fontsize - fontsize, y)
        draw.ellipse((circle_center[0] - fontsize/2, circle_center[1] - fontsize/2,
                      circle_center[0] + fontsize/2, circle_center[1] + fontsize/2), fill='white')
def draw_yangyao(draw, x, y, col, w, bianyao_flag, fontsize):
    draw.line((x,y,x+9*fontsize,y),fill=col,width=w,joint=None)
    if(bianyao_flag):
        #draw.text((x,y-fontsize/4), 'X', fill=col, font=font_s)
        circle_center = (x + 9*fontsize - fontsize, y)
        draw.ellipse((circle_center[0] - fontsize/2, circle_center[1] - fontsize/2,
                      circle_center[0] + fontsize/2, circle_center[1] + fontsize/2), fill='white')
def get_bianyao_num(dongyao):
    xuhao_list = ['上', '五', '四', '三', '二', '初']
    for i, item in enumerate(xuhao_list):
        if item in dongyao:
            return i


def draw_gua_hua2(draw, start_x, starty, fontsize, yao, numlist, f='red'):
    numlist = numlist[::-1] #卦画是从下往上画，所以需要倒置
    dongyao_weizhi = get_bianyao_num(yao)
    for i, num in enumerate(numlist):
        bianyao_flag = False
        if dongyao_weizhi != None and dongyao_weizhi == i:
            bianyao_flag = True
        if num == 6 or num == 9:
            col = f
        else:
            col = 'black'
        if num % 2 == 0:
            draw_yinyao(draw, start_x, starty + (fontsize + fontsize*3/4)*i, col, fontsize, bianyao_flag, fontsize)
        else:
            draw_yangyao(draw, start_x, starty + (fontsize + fontsize*3/4)*i, col, fontsize, bianyao_flag, fontsize)

    return start_x + 9*fontsize, starty + 6* fontsize + 5*fontsize*3/4


def get_ai_jie_gua(gua, yao):
    qianwen = qianwen_api_test.Call_qianwen()
    text = qianwen.get_question(gua, yao)
    #print("大模型输出：", text)
    result = text.split("\n")
    result2 = [s for s in result if s != ""]
    if len(result2) == 0:
        result2.append('解卦失败~~~')
    if len(result2) < 5:
        for i in range(5 - len(result2)):
            result2.append('')
    with open("ai_jiagua.log", "a") as f:
        f.write('|'.join(result2) + '\n')
    return result2
def txt_get():
    ret = test_dayan.dayanshifa()
    gua, yao, numlist = ret[0], ret[1], ret[2]
    result = get_ai_jie_gua(gua, yao)

    return result


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
@auto_print
def local_draw(w, h, f_size, guahua_base, large_size):
    # 加载字体样式
    image = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(image)

    ret = test_dayan.dayanshifa()
    print(ret)
    gua, yao, numlist = ret[0], ret[1], ret[2]
    yao_weizhi = suan_fa_yj.get_dongyao_weizhi(yao)
    print('yaoweizhi:', yao, yao_weizhi)


    miaoshu = random.choice(guaming_miaoshu_map[gua[2:]]).split()
    print(miaoshu)
    start_x , start_y = f_size / 3, f_size/3
    next_y = draw_gua_ming2(draw, yi_xiang_map[gua[2:]][0], large_size, start_y, w/4)
    next_y = draw_gua_ming2(draw, gua[2:], large_size, start_y, w/2)
    next_y = draw_gua_ming2(draw, ''.join(miaoshu), large_size, next_y+f_size/4, w*3/8, 'red')
    #next_y = draw_gua_ming2(draw, yi_xiang_map[gua[2:]][0], 16, next_y, w / 2)
    dongyao_y = next_y
    dongyao_x, next_y = draw_gua_hua2(draw, start_x, next_y + 1*f_size, guahua_base, yao, numlist)

    next_y = draw_xiang2(draw, '[象]' + yi_xiang_map[gua[2:]][1], 14, 17, start_x, next_y+f_size/4, 2, 'red')

    draw_xiang2(draw, '[卦词]' + yi_zhengwen_map[gua[2:]][0], 20, 13, start_x, next_y + f_size/6, 3)
    #next_y = draw_gua_ming2(draw, miaoshu[1], f_size, next_y, 5 * guahua_base)
    #next_y = draw_gua_ming2(draw, '之', large_size, start_y, w/2)

    gua_ming, numlist = get_bian_gua(numlist)
    #miaoshu = random.choice(gua_map[gua_ming[2:]]).split()
    #print(miaoshu)


    #next_y = draw_gua_ming2(draw, miaoshu[0], f_size, next_y + f_size/4, w - 5 * guahua_base)
    #next_y = draw_gua_ming2(draw, miaoshu[1], f_size, next_y, w - 5 * guahua_base)

    dongyao_miaoshu = ''
    if yao_weizhi == 0:
        dongyao_miaoshu = tuan_map[gua[2:]]
    else:
        dongyao_miaoshu = yi_zhengwen_map[gua[2:]][yao_weizhi]

    next_y = draw_xiang2(draw, dongyao_miaoshu, 8, 16, dongyao_x+f_size/4, dongyao_y+f_size/2, 7)

    if yao_weizhi != 0:
        next_y = draw_xiang2(draw, '[象]' + yi_xiang_map[gua[2:]][yao_weizhi+1], 8, 16, dongyao_x + f_size / 4, next_y + f_size, 3)

    if yao_weizhi != 0:
        guahua_base = 3
        draw_gua_hua2(draw, w - 10*guahua_base, guahua_base, guahua_base, '', numlist)
        draw_gua_ming2(draw, '之'+gua_ming[2:], 16,  guahua_base, w*3/4)
    #image.show()
    image.save("output_s.jpg")

def read_guaming(gua_miaoshu_map):
    with open('data/guaming_miaoshu.dat', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip('\n')
            guaming, miaoshu = line.split(',')
            tmplist = gua_miaoshu_map.get(guaming, [])
            tmplist.append(miaoshu)

def read_tuanci(tuan_map, guaxu_map):
    with open('data/tuan_ci.dat', 'r', encoding='utf-8') as f:
        while True:
            guaming = f.readline()
            tuanci = f.readline()
            if guaming == '' or tuanci == '':
                break
            guaming = guaming.strip()
            tuanci = tuanci.strip('。\n')
            guaxu, guaming = guaming.split(' ')
            tuan_map[guaming] = tuanci
            guaxu_map[guaming] = guaxu
            #print(guaxu, guaming, tuanci)
def read_yijing(yijing_zhengwen):
    with open('data/yi_zhengwen.dat', 'r', encoding='utf-8') as f:
        textlist = f.readlines()
        tmp_guaming = ''
        for i, line in enumerate(textlist):
            line = line.strip('\n\xa0。')
            if i % 7 == 0:
                guaming, guaci = line.split('：')
                tmp_guaming = guaming
            yi_zhengwen_map[tmp_guaming].append(line)
            #print(line)

    with open('data/yong_69.dat', 'r', encoding='utf-8') as f:
        textlist = f.readlines()
        yong_9 = textlist[0].strip('\n\xa0。')
        yong_6 = textlist[1].strip('\n\xa0。')
        yi_zhengwen_map['乾'].append(yong_9)
        yi_zhengwen_map['坤'].append(yong_6)
def read_xiang(yijing_xiang):
    with open('data/xiao_xiang.dat', 'r', encoding='utf-8') as f:
        textlist = f.readlines()
        for i, line in enumerate(textlist):
            tmp_guaming = ''
            xianglist = []
            line = line.strip('\n?？')
            xianglist = line.split(',')
            yijing_xiang[xianglist[1]] = xianglist
            #print(xianglist[1], len(xianglist), yijing_xiang[xianglist[1]])
            yijing_xiang[xianglist[1]].pop(1)

def local_jie_gua(gua, yao):
    yao_weizhi = suan_fa_yj.get_dongyao_weizhi(yao)
    miaoshu = random.choice(guaming_miaoshu_map[gua[2:]])
    guaci = '[卦词]' + yi_zhengwen_map[gua[2:]][0]
    tuan = '[彖]' + tuan_map[gua[2:]]
    da_xiang = '[象]' + yi_xiang_map[gua[2:]][0] + ',' + gua[2:] + ',' + yi_xiang_map[gua[2:]][1]
    yaoci = yi_zhengwen_map[gua[2:]][yao_weizhi]
    xiao_xiang = ''
    if yao_weizhi < 7:
        xiao_xiang = '[象]' + yi_xiang_map[gua[2:]][yao_weizhi+1]
    result = [miaoshu, guaci, tuan, da_xiang, yaoci, xiao_xiang]
    return result

def get_yijing_info(gua):
    miaoshu = random.choice(guaming_miaoshu_map[gua])
    guaci = '[卦词]' + yi_zhengwen_map[gua][0]
    tuan = '[彖]' + tuan_map[gua]
    da_xiang = '[象]' + yi_xiang_map[gua][0] + ',' + gua + ',' + yi_xiang_map[gua][1]
    yao_info = []
    yaonum = 7
    if (gua in '乾坤'):
        yaonum = 8
    for weizhi in range(1, yaonum):
        yaoci = '[' + gua + ']' + yi_zhengwen_map[gua][weizhi]
        xiao_xiang = ''
        if yaonum < 8:
            xiao_xiang = '[象]' + yi_xiang_map[gua][weizhi + 1]
        yao_info.append((yaoci, xiao_xiang))
    return (gua +':'+miaoshu, guaci, tuan, da_xiang, yao_info)


app = Flask(__name__)
@app.route('/api', methods=['GET'])
def api():
    return jsonify(txt_get())

@app.route('/')
def test():
    return 'ningzhiqiang test'


@app.route('/gua')
def get_gua():
    gua, yao, numlist = test_dayan.dayanshifa()
    if yao == '':
        yao = ' '
    str_numlist = ''.join(map(str, numlist))
    return jsonify(gua[2:], yao, str_numlist)

'''
@app.route('/yijing/<param1>/<param2>/<param3>')
def yijing_zhengwen(param1, param2, param3):
    draw_gua(480, 480, 20, param1, param2, param3)
    return send_file("output.jpg", mimetype='image/jpeg', as_attachment=False)
'''

@app.route('/guaimg/<param1>/<param2>/<param3>')
def some_endpoint(param1, param2, param3):
    filename = 'guaimg' + param1 + param2 + "output.jpg"
    draw_gua_sim(filename, 480, 480, 20, param1, param2, param3)
    return send_file(filename, mimetype='image/jpeg', as_attachment=False)

@app.route('/jiegua/<param1>/<param2>/<param3>')
def some_endpoint2(param1, param2, param3):
    filename = 'jiegua' + param1 + param2 + "output.jpg"
    draw_gua_ai(filename,480, 480, 20, param1, param2, param3)
    return send_file(filename, mimetype='image/jpeg', as_attachment=False)



@app.route('/local', methods=['GET'])
def local_draw_api():
    local_draw(240, 240, 16, 11, 20)
    return send_file("output_s.jpg", mimetype='image/jpeg', as_attachment=False)

@app.route('/small')
def get_image():
    small_draw(240, 240, 13, 8, 16)
    return send_file("output_s.jpg", mimetype='image/jpeg', as_attachment=False)

@app.route('/image')
def get_image2():
    test_draw(480, 480, 20)
    return send_file("output.jpg", mimetype='image/jpeg', as_attachment=False)



def draw_gua_sim(filename, w, h, f_size, in_gua, in_yao, in_numlist):
    # 加载字体样式
    line_words = int((w - f_size) // f_size)
    half_line_words = (int)((w - f_size * 11) / f_size)

    image = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(image)

    gua, yao, numlist = in_gua, '', [int(num) for num in in_numlist]   #yao = '' #不解卦，不确定动爻
    print(numlist)
    miaoshu = random.choice(guaming_miaoshu_map[gua])
    start_x , start_y = f_size / 2, f_size / 2
    next_y = draw_gua_ming2(draw, gua+'卦', (int)(f_size*4), start_y, w/2)
    next_y = draw_gua_ming2(draw, miaoshu, (int)(f_size * 2), next_y+f_size/2, w / 2)
    dongyao_x, zongjie_y = draw_gua_hua2(draw, w/2 - (9*f_size*1.2)/2, next_y + f_size, (int)(f_size*1.2), yao, numlist)

    next_y = draw_gua_ming2(draw, '[象]' + yi_xiang_map[gua][1], f_size*0.8, zongjie_y, w / 2, f='blue')
    draw_info(draw, (int)(f_size*0.9), f_size, h - f_size)

    bian_gua_ming, bian_numlist = get_bian_gua(numlist)
    if in_yao != '':
        guahua_base = 5
        draw_gua_hua2(draw, w - 10*guahua_base, h - 10*guahua_base, guahua_base, '', bian_numlist)
        draw_gua_ming2(draw, bian_gua_ming[2:], f_size*0.8,  h-f_size- 10*guahua_base, w-5*guahua_base)

    #image.show()
    image.save(filename)


def draw_gua_ai(filename, w, h, f_size, in_gua, in_yao, in_numlist):
    # 加载字体样式
    line_words = int((w - f_size) // f_size)
    half_line_words = (int)((w - f_size * 11) / f_size)

    image = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(image)

    gua, yao, numlist = in_gua, in_yao, [int(num) for num in in_numlist]
    if yao == ' ':
        yao = ''
        print('无动爻')
    print(numlist)
    jiegua = get_ai_jie_gua(gua, yao)

    start_x , start_y = f_size / 2, f_size / 2
    next_y = draw_gua_ming2(draw, jiegua[0], (int)(f_size*1.5), start_y, w/2)
    next_y = draw_gua_chi2(draw, jiegua[1], line_words, f_size, start_x, next_y + f_size/2)
    next_y = draw_xiang2(draw, jiegua[2], line_words, f_size
                               , start_x, next_y + f_size/2, 4)

    dongyao_x, zongjie_y = draw_gua_hua2(draw, start_x, next_y + f_size, f_size, yao, numlist)
    draw_xiang2(draw, jiegua[3], half_line_words, f_size,
                  dongyao_x + f_size, next_y + f_size/2, 10)
    draw_xiang2(draw, jiegua[4], line_words, f_size
                               , start_x, zongjie_y, 4)
    draw_info(draw, (int)(f_size*0.9), f_size, h - f_size)
    #image.show()
    image.save(filename)

def test_draw(w, h, f_size):
    # 加载字体样式
    line_words = int((w - f_size) // f_size)
    half_line_words = (int)((w - f_size * 11) / f_size)

    image = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(image)

    ret = test_dayan.dayanshifa()
    gua, yao, numlist = ret[0], ret[1], ret[2]
    jiegua = get_ai_jie_gua(gua, yao)

    start_x , start_y = f_size / 2, f_size / 2
    next_y = draw_gua_ming2(draw, jiegua[0], (int)(f_size*1.5), start_y, w/2)
    next_y = draw_gua_chi2(draw, jiegua[1], line_words, f_size, start_x, next_y + f_size/2)
    next_y = draw_xiang2(draw, jiegua[2], line_words, f_size
                               , start_x, next_y + f_size/2, 4)

    dongyao_x, zongjie_y = draw_gua_hua2(draw, start_x, next_y + f_size, f_size, yao, numlist)
    draw_xiang2(draw, jiegua[3], half_line_words, f_size,
                  dongyao_x + f_size, next_y + f_size/2, 10)
    draw_xiang2(draw, jiegua[4], line_words, f_size
                               , start_x, zongjie_y, 4)
    draw_info(draw, (int)(f_size*0.9), f_size, h - f_size)
    #image.show()
    image.save("output.jpg")

def small_draw(w, h, f_size, guahua_base, large_size):
    # 加载字体样式
    line_words = int((w - f_size) // f_size)
    half_line_words = (int)((w - guahua_base * 11) / f_size)
    line_blank = (int) (f_size / 4)

    image = Image.new('RGB', (w, h), 'white')
    draw = ImageDraw.Draw(image)

    ret = test_dayan.dayanshifa()
    gua, yao, numlist = ret[0], ret[1], ret[2]
    jiegua = get_ai_jie_gua(gua, yao)

    start_x , start_y = f_size / 2, f_size / 2
    next_y = draw_gua_ming2(draw, jiegua[0], large_size, start_y, w/2)
    next_y = draw_gua_chi2(draw, jiegua[1], line_words, f_size, start_x, next_y + line_blank*2)
    next_y = draw_xiang2(draw, jiegua[2], line_words, f_size, start_x, next_y + line_blank, 4)
    dongyao_x, zongjie_y = draw_gua_hua2(draw, start_x, next_y + f_size, guahua_base, yao, numlist)
    draw_xiang2(draw, jiegua[3], half_line_words, f_size, dongyao_x + f_size, next_y + line_blank*2, 7)
    draw_xiang2(draw, jiegua[4], line_words, f_size, start_x, zongjie_y+ line_blank*4, 3)
    #image.show()
    image.save("output_s.jpg")


if __name__ == '__main__':
    #img_gen2()
    #test_draw(480, 480, 20)
    # 创建画布并设置大小为300x200像素
    #yijing_gailv()
    read_guaming(guaming_miaoshu_map)
    read_yijing(yi_zhengwen_map)
    read_xiang(yi_xiang_map)
    #print(gua_map)
    #print(yi_zhengwen_map)

    read_tuanci(tuan_map, guaxu_map)
    #print(tuan_map)
    #for key in tuan_map.keys():
    #    print(guaxu_map[key], key, len(tuan_map[key]), tuan_map[key])
    #print(len(tuan_map), len(guaxu_map))
    #local_draw(240, 240, 16, 11, 20)
    context = ('ssl/scs1713669251078_www.jinqiangua.cn_server.crt', 'ssl/scs1713669251078_www.jinqiangua.cn_server.key')

    gua, yao, numlist = suan_fa_yj.suan_yi_gua()
    ret = local_jie_gua(gua, yao)
    print(ret)

    print(guaxu_map)
    guaxu = {int(v): k for k, v in guaxu_map.items()}
    print(guaxu)
    for i in range(1, 65):
        guaming = guaxu[i]
        ret = get_yijing_info(guaming)
        print(str(i) + '，' + ret[0])
        for i in ret[1:4]:
            print(i)
        for i in ret[4]:
            print(i[0], i[1])


    #draw_gua_sim(480, 480, 20, gua[2:], ' ', str_numlist)
    #draw_gua_ai(480, 480, 20, '坤', '', '888888')
    #app.run(host='0.0.0.0', debug=True, port=443, ssl_context = context)
    #server = WSGIServer(('0.0.0.0',443), app, keyfile='ssl/scs1713669251078_www.jinqiangua.cn_server.key', certfile='ssl/scs1713669251078_www.jinqiangua.cn_server.crt')
    #server.serve_forever()
