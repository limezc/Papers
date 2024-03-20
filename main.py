from fetch import get_cvpr_paper
from fetch import Search
from concurrent.futures import ThreadPoolExecutor
import json
import pandas as pd



fetch_res = []


def main():
    # 1.网站获取论文列表
    cvpr_url = 'https://cvpr.thecvf.com/Conferences/2024/AcceptedPapers'
    search = Search()
    paper_list = get_cvpr_paper(cvpr_url)
    fetch_res = []

    def fetch_paper(paper):
        return search.search(paper, max_res=1)

    with ThreadPoolExecutor() as executor:
        fetch_res.extend(executor.map(fetch_paper, paper_list))
    
    # 将论文列表保存到JSON文件中
    json.dump(fetch_res, open('output/CVPR2024_Papers_fetch.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)

    # 将论文列表保存到Excel文件中
    df = pd.DataFrame(fetch_res)
    df.to_excel('output/CVPR2024_Papers_fetch.xlsx', index=False)
        

if __name__ == '__main__':
    main()



