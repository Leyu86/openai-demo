import openai

import config


def moderation(text: str, model: str = "text-moderation-001"):
    try:
        openai.api_key = config.OPENAI_API_KEY
        response = openai.Moderation.create(input=text, model=model)
        if response is None:
            return True
        print('### Warning ###')
        result = response.get('results', [])[0]
        if result.get('flagged') is False:
            categories = result.get('categories', {})
            if categories.get('hate', False):
                print(
                    f'输入内容 """{text}""" 包含`基于种族、性别、民族、宗教、国籍、性取向、残疾状况或种姓表达、煽动或促进仇恨的内容`')
            if categories.get('hate/threatening', False):
                print(
                    f'输入内容 """{text}""" 包含`基于种族、性别、民族、宗教、国籍、性取向、残疾状况或种姓表达、煽动或促进仇恨和对目标群体的暴力或严重伤害的内容`')
            if categories.get('self-harm', False):
                print(f'输入内容 """{text}""" 包含`提倡、鼓励或描述自残行为（例如自杀、割伤和饮食失调）的内容`')
            if categories.get('sexual', False):
                print(
                    f'输入内容 """{text}""" 包含`意在引起性兴奋的内容，例如对性活动的描述，或宣传性服务（不包括性教育和健康）的内容`')
            if categories.get('sexual/minors', False):
                print(f'输入内容 """{text}""" 包含`包含 18 岁以下个人的色情内容`')
            if categories.get('violence', False):
                print(f'输入内容 """{text}""" 包含`宣扬或美化暴力或颂扬他人的痛苦或屈辱的内容`')
            if categories.get('violence/graphic', False):
                print(f'输入内容 """{text}""" 包含`以极端的画面细节描绘死亡、暴力或严重身体伤害的暴力内容`')

        return result.get('flagged', True)
    except Exception as e:
        print(e)
        return True
