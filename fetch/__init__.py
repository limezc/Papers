from . import arxiv_search
from . import google_search

search_methods = {
    'arxiv': arxiv_search.search_paper,
    'google': google_search.search_paper
}

