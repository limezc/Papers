import os

import json
import pandas as pd
from typing import Literal
import time

from tqdm import tqdm

from fetch import get_cvpr_paper
from fetch import Search
from fetch import Paper
from fetch import json2pd
from proccess import analysis_engine
from proccess import AIGC_TASK_TYPES
from proccess import AIGC_TASK_TYPES_ENGLISH
from export import download_arxiv_papers
from export import convert_to_md


def get_paper_list():
    save_dir = "output/doc"
    md_dir = "output/md"
    os.makedirs(save_dir, exist_ok=True)
    json_file_name = "CVPR2024_Papers.json"
    excel_file_name = "CVPR2024_Papers.xlsx"
    md_file_name = "CVPR2024_Papers.md"
    md_file_pdf_name = "CVPR2024_Papers_Pdf.md"
    json_path = os.path.join(save_dir, json_file_name)
    excel_path = os.path.join(save_dir, excel_file_name)
    md_path = os.path.join(md_dir, md_file_name)
    md_pdf_path = os.path.join(md_dir, md_file_pdf_name)

    if os.path.exists(json_path):
        paper_list = json.load(open(json_path, "r", encoding="utf-8"))
    else:
        cvpr_url = "https://cvpr.thecvf.com/Conferences/2024/AcceptedPapers"
        paper_list = get_cvpr_paper(cvpr_url)

        # 将论文列表保存到JSON文件中
        json.dump(
            paper_list,
            open(json_path, "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4,
        )
        # 将论文列表保存到Excel文件中
        df = pd.DataFrame(paper_list)
        df.to_excel(excel_path, index=False)
        # 将论文列表保存到Markdown文件中
        with open(md_path, "w", encoding="utf-8") as f:
            for paper in paper_list:
                f.write("- {" + paper["title"] + "}\n")
        # 将论文列表保存到Markdown文件中
        with open(md_pdf_path, "w", encoding="utf-8") as f:
            for paper in paper_list:
                f.write("- {{" + paper["title"] + "}}\n")
    return paper_list


def search_paper_list(paper_list):
    # 这里可以调整爬取的paper数量
    paper_num = len(paper_list)
    paper_list = paper_list[:paper_num]

    save_dir = "output/doc"
    os.makedirs(save_dir, exist_ok=True)
    json_file_name = "CVPR2024_Papers_fetch_{}.json".format(paper_num)
    excel_file_name = "CVPR2024_Papers_fetch_{}.xlsx".format(paper_num)
    json_path = os.path.join(save_dir, json_file_name)
    excel_path = os.path.join(save_dir, excel_file_name)

    if os.path.exists(json_path):
        fetch_res = json.load(open(json_path, "r", encoding="utf-8"))
    else:
        search = Search()
        fetch_res = []
        # 防止接口访问过快，导致被封IP
        for paper in tqdm(paper_list, total=paper_num):
            paper_origin = Paper(**paper)
            search.paper_origin = paper_origin
            fetch_res.append(search.search())
            search.reset()
        # 将论文列表保存到JSON文件中
        json.dump(
            fetch_res,
            open(json_path, "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4,
        )
        # 将论文列表保存到Excel文件中
        df = pd.DataFrame(json2pd(fetch_res))
        df.to_excel(excel_path, index=False)

    return fetch_res


# 经过实际测试moonshot的效果更好,因此默认使用moonshot
def llm_analysis_search_list(
    search_list, engine: Literal["gpt", "moonshot"] = "moonshot", num: int = 5
):
    paper_num = len(search_list)
    save_dir = "output/doc"
    os.makedirs(save_dir, exist_ok=True)
    json_file_name = "CVPR2024_Papers_search_{}.json".format(paper_num)
    json_path = os.path.join(save_dir, json_file_name)

    if os.path.exists(json_path):
        search_results = json.load(open(json_path, "r", encoding="utf-8"))
    else:
        aigc_task_names = AIGC_TASK_TYPES_ENGLISH
        search_results = {}

        for aigc_task_name in aigc_task_names:
            search_results[aigc_task_name] = []

        for search in tqdm(search_list, total=paper_num):
            if search["valid"]:
                search_cur = search["paper_search"]
                abstract = search_cur["abstract"]
                task_id = analysis_engine[engine](abstract)
                if task_id != -1:
                    search_results[aigc_task_names[task_id]].append(search_cur)
                    time.sleep(21)

            paper_all = sum(
                [
                    len(search_results[aigc_task_name])
                    for aigc_task_name in aigc_task_names
                ]
            )
            if paper_all >= num:
                break

        # 将论文列表保存到JSON文件中
        json.dump(
            search_results,
            open(json_path, "w", encoding="utf-8"),
            ensure_ascii=False,
            indent=4,
        )

    return search_results


def export_pdf_md(search_results):
    save_md_dir = "output/md/cvpr2024"
    save_pdf_dir = "output/pdf/cvpr2024"

    os.makedirs(save_md_dir, exist_ok=True)
    os.makedirs(save_pdf_dir, exist_ok=True)

    md_file_name_template = "CVPR2024_Papers_search_{}.md"

    for task_name, papers in search_results.items():
        arxiv_ids = []
        save_md_cur_file = os.path.join(
            save_md_dir, md_file_name_template.format(task_name)
        )
        save_pdf_cur_dir = os.path.join(save_pdf_dir, task_name)

        os.makedirs(os.path.dirname(save_md_cur_file), exist_ok=True)
        os.makedirs(save_pdf_cur_dir, exist_ok=True)

        if os.path.exists(save_md_cur_file):
            continue

        for paper in papers:
            arxiv_ids.append(paper["pdf_url"].split("/")[-1])

        download_arxiv_papers(arxiv_ids, save_pdf_cur_dir)
        convert_to_md(arxiv_ids, save_md_cur_file)


def main():
    # 1.网站获取论文列表
    paper_list = get_paper_list()

    # 2.搜索引擎搜索论文
    search_list = search_paper_list(paper_list)

    # 3.使用chatgpt分析论文
    search_results = llm_analysis_search_list(search_list, engine="moonshot", num=2)

    # 4.导出pdf和md文件
    export_pdf_md(search_results)


if __name__ == "__main__":
    main()
