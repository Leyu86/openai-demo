from component.openai import openai

template = """
{organization.display_name} is a {organization.normalized_entity_type_en} headquartered in {organization.original_address.city}, {organization.original_address.state}, {organization.original_address.country}. The company was founded on {organization.founded_date} and currently employs {organization.employee_number} people.

In terms of patents, {organization.display_name} has {patent_count} patents with a total value of {snapshot.patent.total_value} and an average amount of {snapshot.patent.avg_amount}. Additionally, {organization.display_name} has {snapshot.patent_with_out_collapse.total} patents without collapse, with a total value of {snapshot.patent_with_out_collapse.total_value} and an average amount of {snapshot.patent_with_out_collapse.avg_amount}. 

{organization.display_name} has received {snapshot.research_funding.total} rounds of research funding, with a total amount of {snapshot.research_funding.total_amount}. {organization.display_name} has published a total of {snapshot.paper.total} papers, with a total citation count of {snapshot.paper.total_citation}.

As of {snapshot.financial.date}, {organization.display_name} had a revenue of {snapshot.financial.revenue} {snapshot.financial.currency}. 

{organization.display_name} has made {snapshot.acquisition.total} acquisitions, with a total amount of {snapshot.acquisition.total_amount}. {organization.display_name} has also made {snapshot.investment.total} investments, with a total amount of {snapshot.investment.total_amount}. Finally, {organization.display_name} has received {snapshot.grant.total} grants, with a total amount of {snapshot.grant.total_amount}.

{organization.display_name} has {organization.subsidiaries} subsidiaries and is a subsidiary of {organization.sub_sidiary_of.normalized_name}. 

The company's social media presence includes a {organization.social_medias[0].type} account with the URL {organization.social_medias[0].url}, a {organization.social_medias[1].type} account with the URL {organization.social_medias[1].url}, and a {organization.social_medias[2].type} account with the URL {organization.social_medias[2].url}. 

The company's industry includes {organization.offset_info.normalized_industry[0].name} and {organization.offset_info.normalized_industry[1].name}.

"""


def get_template(json) -> str:
    prompt = '''
    Please generate an enterprise information description string template based on JSON data for attribute filling. Variable usage {variable}. requirement:

        -Fully analyze the significance of each attribute for the enterprise and describe it

        -Interpreting the content of data snapshots showcases the strength of enterprises

        -The template information is enriched and the sentences are smooth
        
        -Rich content
    '''

    messages = [{"role": "system", "content": prompt},
                {"role": "system", "name": "example_user", "content": '{"organiztion:"{"description":"Apple is ...","display_name":"Apple, Inc.","employee_number":164000,"original_address":{"country":"United States","state":"California","country_en":"United States","country_code":"US"},"id":"56f905e632e18c87e0afe588e2c1f34a","entity_id":"56f905e632e18c87e0afe588e2c1f34a","name":"Apple, Inc.", "founded_date": "19870915"},"data_snapshot:{"patent":{"total":262423,"total_value":17822687700,"avg_amount":234272},"patent_with_out_collapse":{"total":389318,"total_value":17822687700,"avg_amount":234272},"research_funding":{"total":4,"total_amount":23054147},"paper":{"total":10717,"total_citation":127193},"funding":{"total":1,"total_amount":0},"financial":{"date":1293753600000,"revenue":185176000000,"currency":"CNY"},"news":{"total":73351},"acquisition":{"total":10,"total_amount":658094797},"investment":{"total":10,"total_amount":195759485},"grant":{"total":5,"total_amount":742954}}"}'},
                {"role": "system", "name": "example_assistant",  "content": 'The company is called {name}. {name} is headquartered in {original_address.state}, {original_address.country}. The company was founded on {founded_date} and currently employs {employee_number} people.\n\nIn terms of data snapshot, {name} has {patent.total} patents with a total value of {patent.total_value} and an average amount of {patent.avg_amount}. {name} also has {patent_with_out_collapse.total} patents without collapse, with a total value of {patent_with_out_collapse.total_value} and an average amount of {patent_with_out_collapse.avg_amount}. Additionally, {name} has received {research_funding.total} rounds of research funding, with a total amount of {research_funding.total_amount}.\n\nIn terms of papers, {name} has published a total of {paper.total} papers, with a total citation count of {paper.total_citation}. {name} has received {funding.total} rounds of funding, with a total amount of {funding.total_amount}.\n\nAs of {financial.date}, {name} had a revenue of {financial.revenue} {financial.currency}.\n\n{acquisition.total} acquisitions have been made by {name}, with a total amount of {acquisition.total_amount}. {name} has also made {investment.total} investments, with a total amount of {investment.total_amount}. Finally, {name} has received {grant.total} grants, with a total amount of {grant.total_amount}.'},
                {"role": "user", "content": json}]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.5
    )

    print(response)


def get_company_info_desc(data) -> str:
    return template.format(data)


if __name__ == '__main__':
    s = '{"patent_count":"410959","organization":{"description":"Huawei Technologies is ...","display_name":"Huawei Technologies Co., Ltd.","employee_number":10001,"original_address":{"country":"China","state":"Guangdong Sheng","city":"Shenzhen","country_en":"China","country_code":"CN"},"id":"f254495135e355974c3390b08a879344","entity_id":"f254495135e355974c3390b08a879344","discovery_info":{"entity_id":"f254495135e355974c3390b08a879344","last_funding_date":20130101,"last_funding_type":"Seed","num_funding_rounds":1,"rank":1459,"startup":false,"unicorn":false},"logo_s3_path":"COMPANY/MASTER/LOGO/f254/4951/35e3/5597/4c33/90b0/8a87/9344/b96def2a7442119f.png","name":"Huawei Technologies Co., Ltd.","normalized_last_funding_type":"Seed","normalized_last_funding_time":{"time_ts":1356998400000},"normalized_entity_status":"ACTIVE","normalized_entity_type_en":"Company","offset_info":{"entity_id":"f254495135e355974c3390b08a879344","ownership_type":["Subsidiary"],"normalized_topic":[{"normalized_display_name":"Wireless","normalized_id":"1415eb2b-b23d-494c-8628-e4f389197f62"},{"normalized_display_name":"Software","normalized_id":"50707e39-02a9-4699-9254-683fc6345321"}],"normalized_industry":[{"confidence":2.9844364523887634,"code":"51121","name":"Software Publishers","hits":3,"level":5,"source":["DISCOVERY"]},{"confidence":1.894602882862091,"code":"33422","name":"Radio and Television Broadcasting and Wireless Communications Equipment Manufacturing","hits":3,"level":5,"source":["FACTSET","DISCOVERY"]}]},"patent_info":{"average_value":234271.69446744747,"total_patents":262423,"total_patent_value":17822687700},"seo_name":"huawei-technologies","social_medias":[{"type":"TWITTER","url":"https://twitter.com/Huawei"},{"type":"FACEBOOK","url":"http://www.facebook.com/huaweidevice"},{"type":"LINKEDIN","url":"https://www.linkedin.com/company/huawei/"}],"founded_date":19870915,"sub_sidiary_of":{"normalized_id":"403671e7bcb29ca8f98e41ee2f8109c9","normalized_name":"Shenzhen Huawei Technologies Investment Holding Co. Ltd.","normalized_display_name":"Shenzhen Huawei Technologies Investment Holding Co. Ltd.","is_startup":false,"is_unicorn":false,"seo_name":"shenzhen-huawei-technologies-investment-holding-co-ltd","id":"403671e7bcb29ca8f98e41ee2f8109c9"},"subsidiaries":190,"website":"https://www.huawei.com","finance_factset_id":"05L112-E"},"snapshot":{"patent":{"total":262423,"total_value":17822687700,"avg_amount":234272},"patent_with_out_collapse":{"total":389318,"total_value":17822687700,"avg_amount":234272},"research_funding":{"total":4,"total_amount":23054147},"paper":{"total":10717,"total_citation":127193},"funding":{"total":1,"total_amount":0},"financial":{"date":1293753600000,"revenue":185176000000,"currency":"CNY"},"news":{"total":73351},"acquisition":{"total":10,"total_amount":658094797},"investment":{"total":10,"total_amount":195759485},"grant":{"total":5,"total_amount":742954}}}'
    get_template(s)
