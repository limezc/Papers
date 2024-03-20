import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


def get_cvpr_paper(url="https://cvpr.thecvf.com/Conferences/2024/AcceptedPapers"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')  # 这需要根据实际页面结构调整

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

        authors = cell.find('div').find('i').text.strip()
        authors = [author.split('(')[0].strip() for author in authors.split('·')]

        paper_list.append({'Title': title, 'Url': title_url, 'Authors': authors})

    return paper_list


if __name__ == '__main__':
    # 从CVPR 2024网站获取论文列表
    cvpr_url = 'https://cvpr.thecvf.com/Conferences/2024/AcceptedPapers'
    paper_list = get_cvpr_paper(cvpr_url)

    # 将论文列表保存到JSON文件中
    json.dump(paper_list, open('output/CVPR2024_Papers.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

    # 将论文列表保存到Excel文件中
    df = pd.DataFrame(paper_list)
    df.to_excel('output/CVPR2024_Papers.xlsx', index=False)


