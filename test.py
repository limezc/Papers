from fetch import Search
from fetch import Paper


def main():
    paper = {
        "title": "Attention Is All You Need",
        "authors": ['Ashish Vaswani', 'Noam Shazeer', 'Niki Parmar', 'Jakob Uszkoreit', 'Llion Jones', 'Aidan N. Gomez', 'Lukasz Kaiser', 'Illia Polosukhin'],
        "pdf_url": ""
    }

    # paper = {
    #     "title": "A2XP: Towards Private Domain Generalization",
    #     "authors": ["Geunhyeok Yu", "Hyoseok Hwang"],
    #     "pdf_url": ""
    # }

    paper_origin = Paper(**paper)
    search = Search(paper_origin=paper_origin, method='arxiv')
    res = search.search(max_res=1)
    print(res)


if __name__ == '__main__':
    main()



