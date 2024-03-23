import os

import json
import pandas as pd

from fetch import get_cvpr_paper
from fetch import Search
from fetch import Paper
from fetch import json2pd


def get_paper_list():
    if os.path.exists('output/doc/CVPR2024_Papers.json'):
        paper_list = json.load(open('output/doc/CVPR2024_Papers.json', 'r', encoding='utf-8'))
    else:
        cvpr_url = 'https://cvpr.thecvf.com/Conferences/2024/AcceptedPapers'
        paper_list = get_cvpr_paper(cvpr_url)
        # 将论文列表保存到JSON文件中
        json.dump(paper_list, open('output/doc/CVPR2024_Papers.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
        # 将论文列表保存到Excel文件中
        df = pd.DataFrame(paper_list)
        df.to_excel('output/doc/CVPR2024_Papers.xlsx', index=False)
    return paper_list


def search_paper_list(paper_list):
    # 这里可以调整爬取的paper数量
    paper_num = len(paper_list)
    paper_list = paper_list[:paper_num]
    if os.path.exists('output/doc/CVPR2024_Papers_fetch_{}.json'.format(paper_num)):
        fetch_res = json.load(open('output/doc/CVPR2024_Papers_fetch_{}.json'.format(paper_num), 'r', encoding='utf-8'))
    else:
        search = Search()
        fetch_res = []
        # 防止接口访问过快，导致被封IP
        for paper in paper_list:
            paper_origin = Paper(**paper)
            search.paper_origin = paper_origin
            fetch_res.append(search.search())
            search.reset()
        # 将论文列表保存到JSON文件中
        json.dump(fetch_res, open('output/doc/CVPR2024_Papers_fetch_{}.json'.format(paper_num), 'w', encoding='utf-8'), ensure_ascii=False, indent=4)
        # 将论文列表保存到Excel文件中
        df = pd.DataFrame(json2pd(fetch_res))
        df.to_excel('output/doc/CVPR2024_Papers_fetch_{}.xlsx'.format(paper_num), index=False)


def main():
    # 1.网站获取论文列表
    paper_list = get_paper_list()

    # 2.搜索引擎搜索论文
    search_paper_list(paper_list)

        

if __name__ == '__main__':
    main()



