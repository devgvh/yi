import SparkApi
import time
#以下密钥信息从控制台获取
appid = "46b1176e"     #填写控制台中获取的 APPID 信息
api_secret = "N2JiODE0MWQxZWQ1MjYzOGJlNTI*****"   #填写控制台中获取的 APISecret 信息
api_key ="05e2cdbb9d19105d2e2d5c5fd86****"    #填写控制台中获取的 APIKey 信息

#用于配置大模型版本，默认“general/generalv2”
domain = "generalv3.5"   # v1.5版本
#domain = "generalv2"    # v2.0版本
#云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v3.5/chat"  # v1.5环境的地址
#Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
#text =[]
def getText(role,content):
    text = []
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text

def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length

def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text
    
test_dongyao = \
       "请按以下鼎卦的格式，给出履卦和九四爻的介绍，控制在200字以内，注意要严格按下面的格式，不要有多余的解释\n\
        鼎：打破惯性，破旧立新\n\
        卦词：鼎，元吉，亨\n\
        象征：它的结构由下巽上离组成，象征着燃木煮食的过程，以及由此引发的化生为熟、除旧布新的变化，鼎作为重要的礼器，也代表了权力和地位的象征\n\
        动爻：九二爻，鼎黄耳金铉，利贞”，这里的“黄耳金铉”指是装饰和提手，黄色和金色都是吉祥的颜色，象征尊贵和坚固。意义在于持正则吉，处于领导地位的人应当坚守正道，才能获得吉祥和成功。\n\
        总体建议：鼎卦强调了稳定与变革，而九五爻则是提醒我们在变革中应当坚守正道，这样才能取得最终的成功"

test_wudongyao = "请按以下鼎卦的格式，给出随卦的介绍，控制在200字以内，注意要严格按下面的格式，不要有多余的解释\n\
        鼎：打破惯性，破旧立新\n\
        卦词：鼎，元吉，亨\n\
        象征：它的结构由下巽上离组成，象征着燃木煮食的过程，以及由此引发的化生为熟、除旧布新的变化，鼎作为重要的礼器，也代表了权力和地位的象征\n\
        彖辞：元吉，亨,表达了这一卦象极为吉祥且通畅的特点。彖辞中的“元”指的是始，表示事物的开始和发展；“吉”意味着吉祥；“亨”则代表顺利无阻。因此，鼎卦的彖辞整体上预示着事物发展的吉祥和顺利。\n\
        总体建议：鼎卦强调了稳定与变革的重要性，鼎卦也提醒我们在生活和工作中要懂得适时地进行必要的改变和创新，这样才能保持活力和进步"

#鼎，九五（空代表无动爻）， xxxx, xxxxx
def get_question(gua, yao, test_dongyao, test_wudongyao):
    prompt = ""
    if len(yao) == 0:
        prompt = test_wudongyao[:12] + gua + test_wudongyao[13:]
    else: #17,18
        prompt = test_dongyao[:12] + gua + test_dongyao[13:15] + yao + test_dongyao[17:]
    return prompt

def ai_jiegua(gua, yao):
    question = checklen(getText("user", get_question(gua, yao, test_dongyao, test_wudongyao)))
    print("大模型输入：", gua, yao, question)
    #question = get_question("鼎", "", test_dongyao, test_wudongyao)
    SparkApi.answer = ""
    SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    time.sleep(3)
    return SparkApi.answer

