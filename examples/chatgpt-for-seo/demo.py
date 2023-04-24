from services.openai import get_chat_completion

topic = "Artificial Intelligence"
company = "Tesla"
website = "https://discovery.patsnap.com/"
description = "Tesla Motors specializes in developing a full range of electric vehicles. Tesla Motors was started by a group of Silicon Valley entrepreneurs and strives to create a revolution and accelerate the world’s transition to electric mobility with a full range of increasingly affordable electric cars. Tesla vehicles are EVs (electric vehicles), which are transforming the way people drive and move. Tesla has gone public as of June 29, 2010, and has a market cap of $34.32 billion. Tesla Motors’ goal is to increase the number and variety of EVs through three strategies. The first is to sell its own branded vehicle through its showrooms. The second is to sell premium, high-quality, patented electric components to other automakers. Lastly, it serves as a “catalyst and positive example to other automakers.” There has already been a movement in the EV market with the push of the GM Volt, rumored to have been inspired by the Tesla Roadster."
edit_text = "The Lithium-ion battery top 100 is Discovery PatSnap’ annual ranking of the top 100 Most Patent Filings Lithium-ion battery Key Players in the world. Discovery has identified the top key players, startups & unicorns, fast-growings, news entrants in 2022, ranking from differnt perspectives, including patent filing intensity, academic research capability, news media heat. The company list is generated from various data types."


def get_top_keywords():
    """ 获取顶级关键词 """
    messages = [{"role": "user",
                 "content": f"Identify the top keywords related to company that will drive the most relevant traffic to our website {website} and increase search engine visibility. Gather data on search volume, competition, and related keywords. The keywords should be relevant to our target audience and align with our content marketing strategy."}]
    get_chat_completion(messages)


def get_high_volume_keywords():
    """ 获取高搜索量关键词 """
    messages = [{"role": "user",
                 "content": f"Suppose you’re an SEO lead; suggest some high-volume, low-difficulty keywords for {topic}."}]
    get_chat_completion(messages)


def get_long_tail_keywords():
    """ 获取长尾关键词 """
    messages = [{"role": "user",
                 "content": f"Provide me with long-tail, high-volume, low-difficulty keywords for {topic} as if you’re a content marketer."}]
    get_chat_completion(messages)


def get_top_competitors():
    """ 获取顶级竞争对手 """
    messages = [{"role": "user",
                 "content": f"I need a table of the top competitors for '{company}' and their URLs curated by a keyword strategist."}]
    get_chat_completion(messages)


def get_seo_keywords():
    """ 获取seo关键词 """
    messages = [{"role": "user",
                 "content": f"Act like an SEO expert having accurate and detailed information about keywords and create a list of 5 SEO keywords related to the following description post section {description}."}]
    get_chat_completion(messages)


def get_content_keywords():
    """ 获取seo关键词 """
    messages = [{"role": "user",
                 "content": f"Suppose you’re a keyword researcher, create a list of listicle content keywords for the {topic}."}]
    get_chat_completion(messages)


def get_relevant_keywords():
    """ 获取相关关键词 """
    messages = [{"role": "user",
                 "content": f"You’re an online marketing manager, make a list of broad topics relevant to {topic} and expand each topic with a list of phrases you think your customers use."}]
    get_chat_completion(messages)


def get_company_description():
    """ 获取公司描述 """
    messages = [{"role": "user",
                 "content": f"Assuming you are a content marketer; Create an SEO optimized enterprise detail page outline, compare and compare different products or services related to the keyword {company}, and position consumers with a neutral tone and an expected length of 500-100 words."}]
    get_chat_completion(messages)


def get_edit_text():
    """ 改写文本 """
    messages = [{"role": "user",
                 "content": f"Improve {edit_text} to ensure the content is relevant and informative for the Competitive intelligence Analyst."}]
    get_chat_completion(messages)


def adding_cta_for_text():
    """ 为文本添加CTA内容 """
    messages = [{"role": "user",
                 "content": f"Improve this {description} by adding a call-to-action (CTA) to encourage readers to take a specific action, such as signing up for a newsletter or purchasing a product."}]
    get_chat_completion(messages)


def rewrite_text():
    """ 重写文本 """
    keywords = ["Lithium-ion battery", "Top 100 Key Players companies", "Most Patent Filings in the world in 2022"]
    messages = [{"role": "user", "content": f"Rewrite the text above using {keywords} as SEO keywords"}]
    get_chat_completion(messages)


def get_faq():
    """ 重写文本 """
    prompt = """
    Create the FAQs Page Schema markup for the following questions and answers:
    
    Q: What technical fields has Tesla Co., Ltd. researched?
    A: Tesla Co., Ltd. has researched the technical fields related to NeodymiumNeodymium magnetMagnet
    Q: What is Tesla Co., Ltd.'s total number of patents?
    A: Tesla Co., Ltd. has 15 patents in total.
    Q: What kind of company is Tesla Co., Ltd.?
    A: Tesla Co., Ltd. develops magnetic products such as Neodymium magnets and Samarium magnets. The company was founded on October 22, 2001 and is headquartered...
    Q: Where is Tesla Co., Ltd.'s headquarters?
    A: Tesla Co., Ltd. is located in , South Korea.
    """
    messages = [{"role": "user", "content": prompt}]
    get_chat_completion(messages)


def analysis_website():
    web = "https://discovery.patsnap.com/company/tesla/"

    messages = [{"role": "user",
                 "content": f"Act as an SEO specialist, analyze {web}, and make improvement suggestions regarding technical SEO with the ways to make those improvements listed in a table."}]
    get_chat_completion(messages)


def develop_strategy():
    url = "https://discovery.patsnap.com/ranking/lithium-ion-battery/"
    keywords = ["Lithium-ion battery", "Top 100 Key Players companies", "Most Patent Filings in the world in 2022"]
    messages = [{"role": "user",
                 "content": f"As an SEO expert, I would like you to develop a strategy to improve the search engine ranking of {url} for the keywords: {keywords}"}]
    get_chat_completion(messages)


if __name__ == '__main__':
    get_top_keywords()
    # get_high_volume_keywords()
    # get_long_tail_keywords()
    # get_top_competitors()
    # get_seo_keywords()
    # get_content_keywords()
    # get_relevant_keywords()
    # get_company_description()
    # get_edit_text()
    # adding_cta_for_text()
    # rewrite_text()
    # get_faq()
    # analysis_website()
    # develop_strategy()
