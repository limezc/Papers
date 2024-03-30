from fetch import Search
from fetch import Paper
from fetch.easy_literature import literature_search
from fetch.easy_literature import literature_search_api


# def main():
#     paper = {
#         "title": "Attention Is All You Need",
#         "authors": ['Ashish Vaswani', 'Noam Shazeer', 'Niki Parmar', 'Jakob Uszkoreit', 'Llion Jones', 'Aidan N. Gomez', 'Lukasz Kaiser', 'Illia Polosukhin'],
#         "pdf_url": ""
#     }

#     # paper = {
#     #     "title": "A2XP: Towards Private Domain Generalization",
#     #     "authors": ["Geunhyeok Yu", "Hyoseok Hwang"],
#     #     "pdf_url": ""
#     # }

#     paper_origin = Paper(**paper)
#     search = Search(paper_origin=paper_origin, method='arxiv')
#     res = search.search(max_res=1)
#     print(res)


def main():
    # literature_search(input_path="output/md/lite.md", output_path="output/pdf", gproxy_mode='free')
    # literature_search(input_path="output/md/lite.md", output_path="output/pdf", gproxy_mode='single', proxy="127.0.0.1:7890")
    literature_search_api(input_path="output/doc/CVPR2024_Papers.json", output_path="output", proxy="127.0.0.1:7890", gproxy_mode='single')

if __name__ == '__main__':
    main()



