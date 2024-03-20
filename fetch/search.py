from . import arxiv_search
from . import google_search

# import sys
# sys.path.append('.')
# from fetch import arxiv_search, google_search

search_methods = {
    'arxiv': arxiv_search.search_paper,
    'google': google_search.search_paper
}



class Search:
    def __init__(self, method='arxiv'):
        self.method = method
        self.search_paper = search_methods[method]
        self.authors = []
        self.title = ""
        self.abstract = ""
        self.published = ""
        self.doi = ""
        self.links = []
        self.pdf_url = ""

    def is_search_valid(self, title, author):
        if self.title.split(' ')[0].strip().lower() == title.split(' ')[0].strip().lower() and self.authors[0].strip().lower() == author.strip().lower():
            return True
        return False
    
    def to_json(self):
        return {
            'authors': self.authors,
            'title': self.title,
            'abstract': self.abstract,
            'published': self.published,
            'doi': self.doi,
            'links': self.links,
            'pdf_url': self.pdf_url
        }

    def search(self, paper, max_res=1):
        self.title = paper["Title"]
        self.authors = paper["Authors"]
        self.links = [paper["Url"]]


        search_results = self.search_paper(self.title, self.authors[0], max_res)
        if len(search_results) == 0:
            print("No result found")
            return
        
        search_result = search_results[0]

        if not self.is_search_valid(search_result['title'], search_result['authors'][0].name):
            print("Search result is not valid")
            return
        
        self.title = search_result['title']
        self.authors = [author.name for author in search_result['authors']]

        if search_result['summary'] is not None:
            self.abstract = search_result['summary']

        if search_result["published"] is not None:
            self.published = search_result['published']

        if search_result['doi'] is not None:
            self.doi = search_result['doi']
        
        if search_result['links']:
            self.links = [link.href for link in search_result['links']]

        if search_result['pdf_url'] is not None:
            self.pdf_url = search_result['pdf_url']
        elif len(search_result['links']) >= 2:
            self.pdf_url = search_result['links'][1].href
        else:
            pass
        print("Search success")
        return self.to_json()

    
if __name__ == '__main__':
    paper = {
        "Title": "Attention Is All You Need",
        "Authors": ['Ashish Vaswani', 'Noam Shazeer', 'Niki Parmar', 'Jakob Uszkoreit', 'Llion Jones', 'Aidan N. Gomez', 'Lukasz Kaiser', 'Illia Polosukhin'],
        "Url": ""
    }
    search = Search()
    res = search.search(paper, max_res=1)
    print(res)
    