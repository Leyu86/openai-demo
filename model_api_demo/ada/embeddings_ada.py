from openai.embeddings_utils import get_embedding
from util.tiktoken_util import chunked_tokens
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_not_exception_type
import numpy as np

from component.openai import openai

EMBEDDING_MODEL = 'text-embedding-ada-002'
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = 'cl100k_base'


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6),
       retry=retry_if_not_exception_type(openai.InvalidRequestError))
def get_embedding(text, model=EMBEDDING_MODEL):
    if isinstance(text, str):
        text = text.replace("\n", " ")

    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def len_safe_get_embedding(text, model=EMBEDDING_MODEL, max_tokens=EMBEDDING_CTX_LENGTH,
                           encoding_name=EMBEDDING_ENCODING, average=True):
    chunk_embeddings = []
    chunk_lens = []
    for chunk in chunked_tokens(text, encoding_name=encoding_name, chunk_length=max_tokens):
        chunk_embeddings.append(get_embedding(chunk, model=model))
        chunk_lens.append(len(chunk))

    if average:
        chunk_embeddings = np.average(chunk_embeddings, axis=0, weights=chunk_lens)
        chunk_embeddings = chunk_embeddings / np.linalg.norm(chunk_embeddings)  # normalizes length to 1
        chunk_embeddings = chunk_embeddings.tolist()
    return chunk_embeddings


if __name__ == '__main__':
    s = '{"entity_id":"08324673176ff8c6b97f1d4b0313fb7d","name_cn":"三星电子株式会社","name_en":"Samsung Electronics Co., ' \
        'Ltd.","normalized_entity_type_en":"Company","original_address":{"country":"韩国","country_en":"South Korea",' \
        '"country_code":"KR"},"country_id":"52d1b118-b540-37ba-9cb2-f5aff686bb10","employee_number":10001,' \
        '"employee_number_interval":"10000人以上","website":"http://www.samsung.com","short_description_en":"Samsung ' \
        'Electronics is an electronics company engaged in consumer electronics, IT and mobile communications, ' \
        'and device solutions.","long_description_en":"Samsung Electronics is a global technology company ' \
        'headquartered in South Korea that operates in various areas of the electronics industry, including consumer ' \
        'electronics, information technology, mobile communications, and device solutions. The company is involved in ' \
        'the development, manufacturing, and sale of a wide range of consumer products, such as mobile phones, ' \
        'tablets, TVs, home theater systems, digital cameras, and home appliances like refrigerators, ' \
        'air conditioners, washing machines, and ovens. \n\nAdditionally, it offers PCs, peripherals, printers, ' \
        'memory and storage products, healthcare and medical equipment, telecommunications infrastructures, ' \
        'and LED lighting solutions. The company is also involved in semiconductor manufacturing, cyber game match ' \
        'hosting, venture capital investments, sponsoring sports teams and games, credit management, and logistics ' \
        'services. \n\nSamsung Electronics operates in various regions worldwide, including Korea, China, ' \
        'North and Latin America, Europe, the Asia Pacific, and Africa. The company also provides repair services and ' \
        'consultation for electronic devices and communication systems.","entity_status":"ACTIVE",' \
        '"normalized_entity_status_cn":"其他","normalized_entity_type_cn":"其他","founded_date":19690212,' \
        '"logo":"https://data-npd-attachment-prod-cn-1251949819.cos.ap-shanghai.myqcloud.com/COMPANY/MASTER/LOGO/0832' \
        '/4673/176f/f8c6/b97f/1d4b/0313/fb7d/18c5a30a8a901b7a.jpeg?sign=q-sign-algorithm%3Dsha1%26q-ak' \
        '%3DAKIDfBZljSVKuGOIxNZWFjzPaXJsGQL2UhgW%26q-sign-time%3D1681653562%3B1681826362%26q-key-time%3D1681653562' \
        '%3B1681826362%26q-header-list%3Dhost%26q-url-param-list%3D%26q-signature' \
        '%3D7c4c3d1c2119595bdcdc30ba646d0f8fc935a025",' \
        '"logo_s3_path":"COMPANY/MASTER/LOGO/0832/4673/176f/f8c6/b97f/1d4b/0313/fb7d/18c5a30a8a901b7a.jpeg",' \
        '"social_medias":[{"type":"TWITTER","url":"https://twitter.com/samsung"},{"type":"FACEBOOK",' \
        '"url":"https://www.facebook.com/samsungelectronics/"},{"type":"LINKEDIN",' \
        '"url":"https://www.linkedin.com/company/samsung-electronics/"}],"name_cn_translation":"Samsung Electronics ' \
        'Co., Ltd","country":{"short_name":"Korea (the Republic of)","full_name":"the Republic of Korea",' \
        '"display_name":"South Korea","display_name_cn":"韩国","alias":["Korea (the Republic of)","KOR","Republic of ' \
        'Korea","South Korea","Korea","Korean","the Republic of Korea","KR"],"region_level":3,' \
        '"region_type":"country","parent_id":["fd950298-4d5d-3e72-9c62-b9664ae08b81",' \
        '"effe769c-c49f-34c7-a6ef-a74774b98a15","2ebc1f6a-39f0-3ec8-9f2b-4bfdaf802f4c",' \
        '"154a6734-0e8c-34dd-9253-dc4ff6120197"],"alpha_two_code":"KR","alpha_three_code":"KOR","numeric_code":"410",' \
        '"independent":true,"id":"52d1b118-b540-37ba-9cb2-f5aff686bb10"},"discovery_info":{' \
        '"entity_id":"08324673176ff8c6b97f1d4b0313fb7d","rank":2158,"startup":false,"unicorn":false},"offset_info":{' \
        '"entity_id":"08324673176ff8c6b97f1d4b0313fb7d","ownership_type":["Public"],"normalized_topic":[{' \
        '"normalized_display_name":"Computer hardware","normalized_id":"8bdac0b2-9827-4764-83c5-f1a5804afc7e",' \
        '"normalized_weight":1,"data_status":"ACTIVE"},{"normalized_display_name":"Semiconductor",' \
        '"normalized_id":"ab235378-83b2-4f50-af8e-a63325c8569b","normalized_weight":0.7506,"data_status":"ACTIVE"},' \
        '{"normalized_display_name":"Software","normalized_id":"50707e39-02a9-4699-9254-683fc6345321",' \
        '"normalized_weight":0.5394,"data_status":"ACTIVE"},{"normalized_display_name":"Mobile device",' \
        '"normalized_id":"929ae498-27a1-48b9-a70f-8b22ecb7d0fa","normalized_weight":0.5346,"data_status":"ACTIVE"},' \
        '{"normalized_display_name":"Electronics","normalized_id":"ebfc553e-829f-4cd3-ab72-15ee66e798db",' \
        '"normalized_weight":0.5026,"data_status":"ACTIVE"},{"normalized_display_name":"Peripheral",' \
        '"normalized_id":"4da2e903-bc4a-4ae4-91ea-b623ed373230","normalized_weight":0.4257,"data_status":"ACTIVE"},' \
        '{"normalized_display_name":"Solid-state drive","normalized_id":"52082747-068e-49f4-9c9d-a657e13ec873",' \
        '"normalized_weight":0.1794,"data_status":"ACTIVE"},{"normalized_display_name":"Electronic component",' \
        '"normalized_id":"46267f5a-0943-4524-bafd-6ce0e9fb430e","normalized_weight":0.1642,"data_status":"ACTIVE"},' \
        '{"normalized_display_name":"Image sensor","normalized_id":"032e191e-24d2-44a0-91fe-fcb32fa66dfc",' \
        '"normalized_weight":0.1045,"data_status":"ACTIVE"},{"normalized_display_name":"Optical disc drive",' \
        '"normalized_id":"221e614a-349e-41a7-8d8f-bc32d5e5f818","normalized_weight":0.0959,"data_status":"ACTIVE"},' \
        '{"normalized_display_name":"Display driver","normalized_id":"111a037b-3221-49fb-a6bf-4316d64773b6",' \
        '"normalized_weight":0.088,"data_status":"ACTIVE"},{"normalized_display_name":"Ultrasound",' \
        '"normalized_id":"cae39c45-a2f2-457e-bac4-d9dcef11788f","normalized_weight":0.0418,"data_status":"ACTIVE"},' \
        '{"normalized_display_name":"Optical disc","normalized_id":"cd76bd1a-868a-4a33-8bbe-e3010278375d",' \
        '"normalized_weight":0.0372,"data_status":"ACTIVE"},{"normalized_display_name":"DVD player",' \
        '"normalized_id":"d593c133-c687-4046-9a94-a238b1c239aa","normalized_weight":0.0254,"data_status":"ACTIVE"},' \
        '{"normalized_display_name":"LED display","normalized_id":"ef05238c-495e-484f-9efb-f6d587a8c400",' \
        '"normalized_weight":0.0174,"data_status":"ACTIVE"},{"normalized_display_name":"Mobile phone",' \
        '"normalized_id":"89cf0cce-e207-4fba-b049-53d8f9c885ce","normalized_weight":0.015,"data_status":"ACTIVE"},' \
        '{"normalized_display_name":"Smart card","normalized_id":"2014c836-fccd-44db-a47e-2ecdbb4f14f2",' \
        '"normalized_weight":0.0142,"data_status":"ACTIVE"},{"normalized_display_name":"CMOS",' \
        '"normalized_id":"a65fb4b1-1c15-4bbd-a7b4-1d25e93e07fd","normalized_weight":0.0105,"data_status":"ACTIVE"},' \
        '{"normalized_display_name":"Digital camera","normalized_id":"7b2a49bb-1b2b-4353-ac5d-83a92801b2d0",' \
        '"normalized_weight":0.0069,"data_status":"ACTIVE"},{"normalized_display_name":"Artificial intelligence",' \
        '"normalized_id":"b2907f4d-00c0-48e5-a6b7-d387f9ef631a","normalized_weight":0,"data_status":"ACTIVE"}],' \
        '"normalized_industry":[{"confidence":6.687183809280395,"code":"33","name":"Manufacturing (c)","hits":9,' \
        '"level":2,"source":["FACTSET","DISCOVERY"]},{"confidence":3.543371558189392,"code":"51",' \
        '"name":"Information","hits":4,"level":2,"source":["DISCOVERY"]},{"confidence":3.0535045742988585,' \
        '"code":"33411","name":"Computer and Peripheral Equipment Manufacturing","hits":4,"level":5,"source":[' \
        '"FACTSET","DISCOVERY"]},{"confidence":2.0336792349815367,"code":"33441","name":"Semiconductor and Other ' \
        'Electronic Component Manufacturing","hits":3,"level":5,"source":["FACTSET","DISCOVERY"]},' \
        '{"confidence":1.9099532961845398,"code":"51121","name":"Software Publishers","hits":2,"level":5,' \
        '"source":["DISCOVERY"]},{"confidence":1.6334182620048523,"code":"51913","name":"Internet Publishing and ' \
        'Broadcasting and Web Search Portals","hits":2,"level":5,"source":["DISCOVERY"]},{"confidence":0.8,' \
        '"code":"33431","name":"Audio and Video Equipment Manufacturing","hits":1,"level":5,"source":["FACTSET"]},' \
        '{"confidence":0.8,"code":"33422","name":"Radio and Television Broadcasting and Wireless Communications ' \
        'Equipment Manufacturing","hits":1,"level":5,"source":["FACTSET"]}]},"is_ls_related":false,"subsidiaries":0,' \
        '"id":"08324673176ff8c6b97f1d4b0313fb7d","name":"三星电子株式会社","display_name":"三星电子株式会社","description":"Samsung ' \
        'Electronics is a global technology company headquartered in South Korea that operates in various areas of ' \
        'the electronics industry, including consumer electronics, information technology, mobile communications, ' \
        'and device solutions. The company is involved in the development, manufacturing, and sale of a wide range of ' \
        'consumer products, such as mobile phones, tablets, TVs, home theater systems, digital cameras, ' \
        'and home appliances like refrigerators, air conditioners, washing machines, and ovens. \n\nAdditionally, ' \
        'it offers PCs, peripherals, printers, memory and storage products, healthcare and medical equipment, ' \
        'telecommunications infrastructures, and LED lighting solutions. The company is also involved in ' \
        'semiconductor manufacturing, cyber game match hosting, venture capital investments, sponsoring sports teams ' \
        'and games, credit management, and logistics services. \n\nSamsung Electronics operates in various regions ' \
        'worldwide, including Korea, China, North and Latin America, Europe, the Asia Pacific, and Africa. The ' \
        'company also provides repair services and consultation for electronic devices and communication systems.",' \
        '"normalized_entity_type":"其他","normalized_entity_status":"其他","data_type":"ORGANIZATION",' \
        '"need_redirect":false,"is_tffi":false,"is_synapse":false,"is_desc_cn_highlight":false,' \
        '"is_name_cn_highlight":true,"key_factors":{"factors":[{"key":"patent","count":12422}]},"highlight":{' \
        '"topic":[{"id":"b2907f4d-00c0-48e5-a6b7-d387f9ef631a","display_name":"Artificial intelligence",' \
        '"entity_id_list":["b2907f4d-00c0-48e5-a6b7-d387f9ef631a"]}]}}'
    print(len_safe_get_embedding(s))
