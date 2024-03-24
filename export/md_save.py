from urllib import request
import re
import feedparser
from pathlib import Path


class Information():
    '''
    extract information from arxiv api
    '''    
    def __init__(self, query_id) -> None:

        query_url = f'http://export.arxiv.org/api/query?id_list={query_id}'
        export_arxiv = request.urlopen(query_url).read().decode('utf-8')
        feed = feedparser.parse(export_arxiv)

        self.title = re.sub(r'[^\w\s-]', '', feed.entries[0].title)
        self.authors = [author.name for author in feed.entries[0].authors]
        self.abs_url_version = feed.entries[0].id
        self.abs_url = self.abs_url_version[:-2]
        self.pdf_url = self.abs_url.replace('abs', 'pdf')
        self.id_version = self.abs_url_version[-12:]
        self.year = feed.entries[0].published[:4]
        self.summary = feed.entries[0].summary

        p = Path(__file__)
        with open(p.parents[0] / 'conf_list.txt', 'r') as f:
            data = f.read()
        CONF = data.split('\n')
        CONF = '|'.join(CONF)

        try: # try for no attribute 'arxiv_comment'
            self.comment = feed.entries[0].arxiv_comment
            self.conf = re.findall(rf'({CONF})', self.comment)[0]
            self.conf_year = re.findall(r'(\d{4})', self.comment)[0]
            self.publish = f'{self.conf} {self.conf_year}' if self.conf else f'arXiv {self.year}'
        except:
            self.publish = f'arXiv {self.year}'

    def write_notes(self):
        '''
        define the markdown format and write notes
        '''
        res = []
        title_url = f'[{self.title}]({self.abs_url})  '
        publish = f'**[`{self.publish}`]**'
        authors = ', '.join(self.authors)
        authors = f'*{authors}*'

        res.append('- ' + title_url)
        res.append('  ' + publish + ' ' + authors)
        res.append('')

        return res
    
def convert_to_md(query_ids, output_file_path):
    results = []
    for id in query_ids:
        if re.match(r'\d{4}\.\d{5}', id):
            information = Information(id)
            results.extend(information.write_notes())
    
    with open(output_file_path, "w") as f:
        for item in results:
            f.write(item + '\n')


def main():
    results = []
    query_ids = ["2303.09373v2"]
    for id in query_ids:
        if re.match(r'\d{4}\.\d{5}', id):
            information = Information(id)
            results.extend(information.write_notes())
    
    with open("output/md/test.md", "w") as f:
        for item in results:
            f.write(item + '\n')


if __name__ == "__main__":
    main()