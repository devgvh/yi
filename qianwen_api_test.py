import dashscope
import threading
import suan_fa_yj
import os

api_key=os.getenv("DASHSCOPE_API_KEY")
#export DASHSCOPE_API_KEY=YOUR_API_KEY
dashscope.api_key = "sk-HZ7lMsU5bu"
test_dongyao = "请按以下鼎卦的格式，给出履卦和九四爻的介绍，控制在150字以内，注意要严格按下面的格式，不要有多余的解释\n\
        鼎：打破惯性，破旧立新\n\
        卦词：鼎，元吉，亨\n\
        象征：它的结构由下巽上离组成，象征着燃木煮食的过程，以及由此引发的化生为熟、除旧布新的变化，鼎作为重要的礼器，也代表了权力和地位的象征\n\
        动爻：九二爻，鼎黄耳金铉，利贞”，这里的“黄耳金铉”指是装饰和提手，黄色和金色都是吉祥的颜色，象征尊贵和坚固。意义在于持正则吉。\n\
        总体建议：鼎卦强调了稳定与变革，而九五爻则是提醒我们在变革中应当坚守正道，这样才能取得最终的成功"

test_wudongyao = "请按以下鼎卦的格式，给出随卦的介绍，控制在200字以内，注意要严格按下面的格式，不要有多余的解释\n\
        鼎：打破惯性，破旧立新\n\
        卦词：鼎，元吉，亨\n\
        象征：它的结构由下巽上离组成，象征着燃木煮食的过程，以及由此引发的化生为熟、除旧布新的变化，鼎作为重要的礼器，也代表了权力和地位的象征\n\
        彖辞：元吉，亨。鼎卦的彖辞整体上预示着事物发展的吉祥和顺利。\n\
        总体建议：鼎卦强调了稳定与变革的重要性，鼎卦也提醒我们在生活和工作中要懂得适时地进行必要的改变和创新，这样才能保持活力和进步"


class Call_qianwen:
    def call_qianwen(self, yangli):
        response = dashscope.Generation.call(model=dashscope.Generation.Models.qwen_max, prompt=yangli)
        return response.output['text']

    # 鼎，九五（空代表无动爻）， xxxx, xxxxx
    def get_question(self, gua, yao, dongyao=test_dongyao, wudongyao=test_wudongyao):
        prompt = ""
        if len(yao) == 0:
            prompt = wudongyao[:12] + gua + wudongyao[13:]
        else:  # 17,18
            prompt = dongyao[:12] + gua + dongyao[13:15] + yao + dongyao[17:]
        return self.call_qianwen(prompt)

    def get_ai_jie_gua(self, gua, yao):
        text = self.get_question(gua, yao)
        # print("大模型输出：", text)
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

def worker(num):
    """线程工作函数"""
    print(f"Thread {num} starting.")
    ret = suan_fa_yj.suan_yi_gua()
    qianwen = Call_qianwen()
    ret2 = qianwen.get_ai_jie_gua(ret[0],ret[1])
    print(ret2)
    print(f"Thread {num} finished.")


if __name__ == '__main__':
    threads = []
    for i in range(3):  # 创建并启动3个线程
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()  # 等待所有线程完成