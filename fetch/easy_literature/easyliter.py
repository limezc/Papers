import logging 
import argparse
import os
import re

import json

from tqdm import tqdm

from .utils import patternRecognizer, note_modified, get_pdf_paths, get_pdf_paths_from_notes, get_update_content, get_pdf_paths_from_notes_dict
from .downloads import get_paper_info_from_paperid, classify, get_paper_pdf_from_paperid


logging.basicConfig()
logger = logging.getLogger('easyliter')
logger.setLevel(logging.INFO)


def set_args():
    parser = argparse.ArgumentParser(description='EasyLiterature')
    parser.add_argument('-i', '--input', type=str, default="output/md/liter_input.md",
                        help="The path to the note file or note file folder.")
    parser.add_argument('-o', '--output', type=str, default="output/pdf",
                        help='Folder path to save paper pdfs and images. NOTE: MUST BE FOLDER.')
    parser.add_argument('-p', '--proxy', type=str, default="127.0.0.1:7890", 
                        help='The proxy address. e.g. 127.0.0.1:1080. If this argument is specified, the google scholar will automatically use a free proxy (not necessarily using the specified proxy address). To use other proxies for google scholar, specify the -gp option. If you want to set up the proxies mannually, change the behaviour in GoogleScholar.set_proxy().  See more at https://scholarly.readthedocs.io/en/stable/ProxyGenerator.html.')
    parser.add_argument('-gp', '--gproxy_mode', type=str, default='single', 
                        help='The proxy type used for scholarly. e.g., free, single, Scraper. (Note: 1. <free> will automatically choose a free proxy address to use, which is free, but may not be fast. 2. <single> will use the proxy address you specify. 3. <Scraper> is not free to use and need to buy the api key.).')
    parser.add_argument('-d', '--delete', action='store_true',
                        help='Delete unreferenced attachments in notes. Use with caution, '
                        'when used, -i must be a folder path including all notes.')
    parser.add_argument('-m', '--migration', type=str, default="output/pdf_new", 
                        help="The pdf folder path you want to reconnect to.")
    args = parser.parse_args()
    
    return args 

def check_args():
    args = set_args()
    input_path = args.input
    output_path = args.output 
    delete_bool = args.delete
    migration_path = args.migration
    proxy = args.proxy
    gproxy_mode = args.gproxy_mode
        
    return input_path, output_path, delete_bool, proxy, migration_path, gproxy_mode


def get_bib_and_pdf(note_file, output_path, proxy, paper_recognizer, gproxy_mode):
    
    pdfs_path = output_path
    if not os.path.exists(pdfs_path):
        os.makedirs(pdfs_path)
    
    with open(note_file, 'r') as f:
        content = f.read()
            
    m = paper_recognizer.findall(content)
    logger.info("Number of files to download -  {}".format(len(m)))

    if not m:
        logger.info("The file {} is not found, or there is no valid entry in the file.".format(note_file))
    else:
        replace_dict = get_update_content(m, note_file, pdfs_path, proxy=proxy, gproxy_mode=gproxy_mode)
            
        return replace_dict


def file_update(input_path, output_path, proxy, paper_recognizer, gproxy_mode):
    
    replace_dict =  get_bib_and_pdf(input_path, output_path,
                                    proxy, paper_recognizer, gproxy_mode)
    
    if replace_dict:
        note_modified(paper_recognizer, input_path, **replace_dict)



def literature_search(input_path="output/md/liter_input.md", output_path="output/pdf", delete_bool=False, proxy=None, migration_path="output/pdf_new", gproxy_mode='single'):
    if output_path:
        paper_recognizer = patternRecognizer(r'- \{.{3,}\}')
        
        if os.path.isfile(input_path):
            logger.info("Updating the file {}".format(input_path))
            file_update(input_path, output_path, proxy, paper_recognizer, gproxy_mode)
            
        elif os.path.isdir(input_path):
            note_paths = []
            for root, _, files in os.walk(input_path):
                for file in files:
                    if file.lower().endswith('md') or file.lower().endswith('markdown'):
                        note_paths.append(os.path.join(root, file))
            for note_path in note_paths:
                logger.info("Updating the file {}".format(note_path))
                file_update(note_path, output_path, proxy, paper_recognizer, gproxy_mode)
        else:
            logger.info("input path {} does not exist".format(input_path))
    
    
        # Delete unreferenced attachments
        if delete_bool:
            if os.path.isfile(input_path):
                logger.info("To delete the PDF entities unrelated to the notes, the input path must be the main notes folder!!! Please use this parameter with caution!!!")
            else:
                pdf_path_recognizer = patternRecognizer(r'\[pdf\]\(.{5,}\.pdf\)')
                pdf_paths_in_notes = get_pdf_paths_from_notes(input_path, pdf_path_recognizer)
                pdf_paths = get_pdf_paths(output_path)
                # TODO the path between mac and win could be different，“/” 和 “\\”
                pdf_paths_in_notes = [os.path.abspath(i).replace('\\', '/') for i in pdf_paths_in_notes]
                pdf_paths = [os.path.abspath(i).replace('\\', '/') for i in pdf_paths]
                
                removed_pdf_paths = list(set(pdf_paths) - set(pdf_paths_in_notes))
                try:
                    for pdf_p in removed_pdf_paths:
                        os.remove(pdf_p)
                except:
                    pass 
                
                logger.info("Deleted {} files".format(len(removed_pdf_paths)))
            
    
    if migration_path:
        pdf_path_recognizer = patternRecognizer(r'\[pdf\]\(.{5,}\.pdf\)')
        
        pdf_paths = get_pdf_paths(migration_path)
        pdf_paths_in_notes = get_pdf_paths_from_notes_dict(input_path, pdf_path_recognizer)
        
        # match based on paper title
        matched_numb = 0
        pdf_paths_dict = {os.path.basename(i): i for i in pdf_paths}
        for md_file, pdf_paths_ in  pdf_paths_in_notes.items():
                
            pdf_paths_in_notes_dict = {os.path.basename(i): i for i in pdf_paths_}
            matched_pdfs = pdf_paths_dict.keys() & pdf_paths_in_notes_dict.keys()
            
            matched_numb += len(matched_pdfs)

            replace_paths_dict = {}
            for matched in matched_pdfs:
                replaced_str = os.path.relpath(pdf_paths_dict[matched], md_file).split('/',1)[-1]
                replaced_str = "[pdf]({})".format(replaced_str)
                ori_str = "[pdf]({})".format(pdf_paths_in_notes_dict[matched])
                replace_paths_dict[ori_str] = replaced_str
            
            if replace_paths_dict: 
                note_modified(pdf_path_recognizer, md_file, **replace_paths_dict)
        
        logger.info("Found - {} - pdf files".format(matched_numb))
        

    if not output_path and not migration_path:
        logger.info("lacking the arguments -o or -m, use -h to see the help")


def literature_search_api(input_path="output/doc/CVPR2024_Papers.json", output_path="output", proxy="127.0.0.1:7890", gproxy_mode='single'):
    results_md = dict()
    results_bib = []

    save_note_path = os.path.join(output_path, 'md', input_path.split('/')[-1].split(".")[0]+"_literature.md")
    save_json_path = os.path.join(output_path, 'doc', input_path.split('/')[-1].split(".")[0]+"_literature.json")

    if os.path.exists(save_json_path):
        logger.info(f"The file {save_json_path} already exists.")
        return

    papers = json.load(open(input_path, 'r'))
    def convert_title_pdfname(title):
        # remove blank symbol, like \n, \t, \r
        title = re.sub(r'[\n\t\r]', '', title)
        # remove multiple blank spaces
        title = re.sub(r' +', ' ', title)
        title = re.sub(r'[.]', '', title)
        title = '_'.join(title.split(' ')) + '.pdf'
        # remove the special characters in the pdf name: / \ : * ? " < > |
        title = re.sub(r'[\\/:*?"<>|]', '', title)
        return title

    # select part of the papers to download
    # papers = papers[:10]

    for paper in tqdm(papers, desc="Downloading papers", total=len(papers)):
        # use title as the key word
        search_idx = "title"
        keyword = paper[search_idx]

        bib = get_paper_info_from_paperid(keyword, proxy=proxy, gproxy_mode=gproxy_mode)
        if bib:
            pdf_name = convert_title_pdfname(bib['title'])
            if search_idx  == "title":
                if convert_title_pdfname(keyword) != pdf_name:
                    logger.info(f"The paper's title: {keyword}; The search pdf name: {pdf_name}.")
                    continue

            id_type = classify(keyword)

            if id_type == "title":
                for pattern_str in [r'10\.(?!1101)[0-9]{4}/', r'10\.1101/', r'[0-9]{2}[0-1][0-9]\.[0-9]{3,}', r'.*/[0-9]{2}[0-1][0-9]{4}']:
                    res = re.search(pattern_str, bib['url'])  # search for the arxiv id in the url
                    if res:
                        literature_id = res.group(0)
                        if bib['pdf_link'] is None:
                            bib['pdf_link'] = f'https://arxiv.org/pdf/{literature_id}.pdf'
                        logger.info(f"The paper's arxiv url: {bib['url']}; The converted arxiv id: {literature_id}; The pdf link: {bib['pdf_link']}.")

            logger.info("Can not find a downloading source for literature id {}. You may need to manually download this paper, a template has been generated in the markdown file. Put the pdf file in the folder you specified just now and add its name in the '(pdf)' of your markdown entry.".format(literature_id))
            
            replaced_literature = "- **{}**. {} et.al. **{}**, **{}**, **Number of Citations: **{}, ([link]({})).".format(
                                    bib['title'], bib["author"].split(" and ")[0], bib['journal'], 
                                    bib['year'], bib['cited_count'], bib['url']
                                    )
            
            results_bib.append(bib)
            results_md[keyword] = replaced_literature

    if results_md:
        with open(save_note_path, 'w') as f:
            f.write(''.join(results_md))

    if results_bib:
        with open(save_json_path, 'w') as f:
            json.dump(results_bib, f)

def main():
    input_path, output_path, delete_bool, proxy, migration_path, gproxy_mode = check_args()
    literature_search(input_path, output_path, delete_bool, proxy, migration_path, gproxy_mode)
    

if __name__ == "__main__":
    main()