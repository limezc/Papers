import arxiv

# arxiv api documentation:
# element	explanation
# entry_id	A url http://arxiv.org/abs/{id}.
# updated	When the result was last updated.
# published	When the result was originally published.
# title	The title of the result.
# authors	The result's authors, as arxiv.Authors.
# summary	The result abstract.
# comment	The authors' comment if present.
# journal_ref	A journal reference if present.
# doi	A URL for the resolved DOI to an external resource if present.
# primary_category	The result's primary arXiv category. See arXiv: Category Taxonomy[4].
# categories	All of the result's categories. See arXiv: Category Taxonomy.
# links	Up to three URLs associated with this result, as arxiv.Links.
# pdf_url	A URL for the result's PDF if present. Note: this URL also appears among result.links.


# prefix	explanation
# ti	Title
# au	Author
# abs	Abstract
# co	Comment
# jr	Journal Reference
# cat	Subject Category
# rn	Report Number
# id	Id (use id_list instead)
# all	All of the above

def search_paper(title, author, max_res=1):
    search_results = []
    query_str = 'ti:{} AND au:{}'.format(title, author)

    search = arxiv.Search(
        query = query_str,
        max_results = max_res
    )

    if len(list(search.results())) == 0:
        return search_results
    
    for result in search.results():
        res = {}
        res['entry_id'] = result.entry_id
        res['updated'] = result.updated
        res['published'] = result.published
        res['title'] = result.title
        res['authors'] = result.authors
        res['summary'] = result.summary
        res['comment'] = result.comment
        res['journal_ref'] = result.journal_ref
        res['doi'] = result.doi
        res['primary_category'] = result.primary_category
        res['categories'] = result.categories
        res['links'] = result.links
        res['pdf_url'] = result.pdf_url
        search_results.append(res)

    return search_results

if __name__ == '__main__':
    title = "A2XP: Towards Private Domain Generalization"
    author = "Geunhyeok Yu"
    search_results = search_paper(title, author, max_res=1)
    print(search_results)