import requests
from bs4 import BeautifulSoup
import pandas as pd
from googletrans import Translator
import os
import urllib.request
import json
import re



# 清理函数，用于移除非法字符
def clean_text(text):
    # 这个正则表达式将匹配所有非法字符
    illegal_re = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
    # 使用空字符串替换所有非法字符
    return illegal_re.sub('', text)


def get_cvpr_paper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 解析网页以提取论文标题和摘要的URL（这部分代码需要根据实际的网页结构调整）
    # 假设论文标题和摘要URL都在<a>标签内
    rows = soup.find_all('tr')  # 这需要根据实际页面结构调整

    translator = Translator()
    paper_list = []

    for row in rows:
        if not row.find_all('td'):
            continue
        cell = row.find_all('td')[0]
        if cell.find('strong'):
            title = cell.find('strong').text.strip()
            title_url = None
        elif cell.find('a'):
            a_tag = cell.find('a')
            title_url = a_tag['href'].strip()
            title = a_tag.text.strip()
        else:
            print('No title found')
            continue

        author = cell.find('div').find('i').text.strip()

        # 将摘要翻译成中文
        # translated_abstract = translator.translate(abstract_text, dest='zh-cn').text

        # paper_list.append({'Title': title, 'url': title_url, 'Author': author})

        # 在将数据添加到paper_list之前，清理文本
        paper_list.append({'Title': clean_text(title), 'url': title_url, 'Author': clean_text(author)})

    return paper_list


def main():
    # 从CVPR 2024网站获取论文列表
    cvpr_url = 'https://cvpr.thecvf.com/Conferences/2024/AcceptedPapers'
    paper_list = get_cvpr_paper(cvpr_url)

    # 将论文列表保存到JSON文件中
    # json.dump(paper_list, open('output/CVPR2024_Papers.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

    # 将论文列表保存到Excel文件中
    df = pd.DataFrame(paper_list)
    df.to_excel('output/CVPR2024_Papers.xlsx', index=False)



if __name__ == '__main__':
    main()


