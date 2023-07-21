from p1.myapp.WebProcessor.data_load import load_html
from p1.myapp.WebProcessor.tags_extraction import start_sof
import pandas as pd

with open('url.txt') as file:
    urls = [line.rstrip() for line in file]

n=0
for url in urls:
    n += 1
    print(n)
    df = pd.DataFrame({"tag": [], "parent_tag": [], "super_parent_tag": [], "location": [], "text": [], "label": []})
    loc = []

    if (n>=1) and (n<51):
        file_name = url
        html_obj = load_html(file_name)
        d = start_sof(html_obj.html)

        i = 0

        for l in d:
            if l != []:
                text = l[3].replace('\r', '').replace('\n', '').replace('\t', '').replace('\xa0', '')
                if text.replace(' ', '') != '':
                    i += 1
                    print(l[0], text)
                    flag = int(input())
                    loc.append(i)
                    df = pd.concat([df, pd.DataFrame.from_records([{"tag": l[0], "parent_tag": l[1], "super_parent_tag": l[2], "text": l[3].replace('\xa0', ''), "label": flag}])])

        loc = [x / i for x in loc]
        df['location'] = loc

        str_file = str(n) + ".csv"
        df.to_csv(str_file, index=False)