from . import search_methods

class Search:
    def __init__(self, method='arxiv'):
        self.method = method
        self.search_paper = search_methods[method]
        self.authors = []
        self.title = ""
        self.abstract = ""
        self.published = ""
        self.references = []
        self.doi = ""
        self.links = []
        self.pdf_url = ""

    def search(self, title, author, max_res=1):
        return self.search_paper(title, author, max_res)