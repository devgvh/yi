#详细说明见博客，程序不复杂，一个后台多个前台。
https://mp.weixin.qq.com/s/cG9tw3-d0gGYWl69ZuZe3A

AI用的阿里的大模型，还有一个星火大模型备用。
主程序跑在华为云上，主程序算命结果可在车，手机、电脑等浏览器直接显示。
同时做了一个微信小程序优化体验。还做了一个嵌入设备入口。

调用AI大模型主要是提供一个样例，同时给出要算的卦象，让大模型生成解卦。

样例如下：
"请按以下鼎卦的格式，给出履卦和九四爻的介绍，控制在150字以内，注意要严格按下面的格式，不要有多余的解释\n\
        鼎：打破惯性，破旧立新\n\
        卦词：鼎，元吉，亨\n\
        象征：它的结构由下巽上离组成，象征着燃木煮食的过程，以及由此引发的化生为熟、除旧布新的变化，鼎作为重要的礼器，也代表了权力和地位的象征\n\
        动爻：九二爻，鼎黄耳金铉，利贞”，这里的“黄耳金铉”指是装饰和提手，黄色和金色都是吉祥的颜色，象征尊贵和坚固。意义在于持正则吉。\n\
        总体建议：鼎卦强调了稳定与变革，而九五爻则是提醒我们在变革中应当坚守正道，这样才能取得最终的成功"

算卦用：大衍蓍法（周易自带的算卦方法），模拟50根蓍草的18变
原文 ：“大衍之数五十，其用四十有九。分而为二以象两，挂一以象三，揲之以 四以象四时，归奇于扐以象闰，五岁再闰，故再扐而后挂。
同时代码也备了金钱卦的算法。两个算卦方法概率不一致。

解卦是让AI大模型参考用朱熹《易学启蒙》里的方法来解。

①有一爻变，用本卦变爻爻辞占断；

②有两爻变，用本卦两变爻爻辞判断，而以上爻爻辞为主；

③有三爻变，以本卦和之卦的《彖辞》判断。以本卦为贞（体），变卦为悔（用）

。。。。。。
同时也备了南怀谨的解卦算法
