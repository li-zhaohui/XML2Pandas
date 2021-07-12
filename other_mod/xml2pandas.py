from xml.etree import cElementTree as ElementTree
from xml2dict import XmlDictConfig
import time
import pandas as pd
def convert_xmls2pd(xml_data):
    def inner_join(x, y):
        result = []
        for tx in x:
            for ty in y:
                result.append({**tx, **ty})
        if len(x) == 0:
            for ty in y:
                result.append({**ty})
        return result    

    def lasterize(prefix, dict_val):
        result = []
        for key, val in dict_val.items():
            # cur_prefix = prefix + key
            cur_prefix = key
            if isinstance(val, dict):
                result = inner_join(result, lasterize(cur_prefix, val))
            elif isinstance(val, str):
                result = inner_join(result, [{cur_prefix:val}])
            elif isinstance(val, list):
                arr = []
                for item in val:
                    arr += lasterize(cur_prefix, item)
                result = inner_join(result, arr)
        return result

    start = time.time()
    xml_arr = xml_data.split('\n')

    data = []
    for xml in xml_arr:
        if len(xml.strip()):
            tree = ElementTree.fromstring (xml)
            xmldict = XmlDictConfig(tree)
            data += lasterize('', xmldict)

    df = pd.DataFrame(data)
    end = time.time()
    print(end-start)
    return df

df = convert_xmls2pd(open('./result.xml').read())
print(df)
df.to_csv('result.csv')
