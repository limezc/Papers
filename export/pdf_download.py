import arxiv

import re


def clean_text(text):
    cleaned_text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    return cleaned_text


def convert_title_pdfname(title):
    # remove blank symbol, like \n, \t, \r
    title = re.sub(r"[\n\t\r]", "", title)
    # remove multiple blank spaces
    title = re.sub(r" +", " ", title)
    title = re.sub(r"[.]", "", title)
    title = "_".join(title.split(" ")) + ".pdf"
    # remove the special characters in the pdf name: / \ : * ? " < > |
    title = re.sub(r'[\\/:*?"<>|]', "", title)
    return title


def download_arxiv_papers(arxiv_ids, output_dir="output/pdf"):
    search_papers = arxiv.Client().results(arxiv.Search(id_list=arxiv_ids))
    for paper in search_papers:
        title = paper.title
        paper.download_pdf(
            dirpath=output_dir, filename="{}.pdf".format(clean_text(title))
        )


def main():
    arxiv_ids = ["2111.10121v2", "2303.09373v2"]
    search_papers = arxiv.Client().results(arxiv.Search(id_list=arxiv_ids))
    for paper in search_papers:
        title = paper.title
        paper.download_pdf(
            dirpath="output/pdf", filename="{}.pdf".format(clean_text(title))
        )


if __name__ == "__main__":
    main()
