from .data_load import load_html
from .tags_extraction import start_sof
import pandas as pd


def primary_processing(url):
    df = pd.DataFrame({"tag": [], "parent_tag": [], "super_parent_tag": [], "location": [], "text": []})
    loc = []
    file_name = url
    html_object = load_html(file_name)
    d = start_sof(html_object.html)

    i = 0

    for l in d:
        if l:
            text = l[3].replace('\r', '').replace('\n', '').replace('\t', '').replace('\xa0', '')
            if text.replace(' ', '') != '':
                i += 1
                loc.append(i)
                df = pd.concat([df, pd.DataFrame.from_records([{"tag": l[0], "parent_tag": l[1],
                                                                "super_parent_tag": l[2],
                                                                "text": l[3].replace('\xa0', '')}])])

    loc = [x / i for x in loc]
    df['location'] = loc

    return df
