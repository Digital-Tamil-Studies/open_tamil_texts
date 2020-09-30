#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Purpose: This script gets and saves project madurai works as html 
#          and text from: https://www.projectmadurai.org/pmworks.html
# Date: Sept 2020
# License: GPL-3.0 


# In[ ]:


# -*- coding: utf-8 -*-
from urllib.request import urlopen
from urllib.parse import quote  
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import html2text
import sys


# In[ ]:


def get_page(page_url):
    page = urlopen(page_url)
    soup = BeautifulSoup(page, "html.parser")
    return soup


# In[ ]:


def get_file_names(html_links):
    html_link_list  = []
    for html_link in html_links:
        html_link_text = html_link.text.strip()
        if len(html_link_text) > 9 :
            html_link_list.append(html_link_text)
    return html_link_list


# In[ ]:


def save_file(file_path, text_content):
    f = open(file_path, "a")
    f.write(text_content)
    f.close()


# In[ ]:


# Get all work entries
page_url = "https://www.projectmadurai.org/pmworks.html"
page = get_page(page_url)
tables = page.findAll('table')
main_table = tables[1]
rows = main_table.findAll('tr')


# In[ ]:


# Get the metadata
all_links = []
all_metadata = []
identifier = 1

for row in rows:
    metadata_dict = {}
    columns = row.findAll('td')
    if len(columns) == 6:
        metadata_dict["identifier"] = identifier
        identifier = identifier + 1
        project_madurai_id = columns[0].text.strip()
        metadata_dict["identifier_pmid"] = project_madurai_id
        title = columns[1].text
        title = title.replace('\n',' ')
        title = title.replace('\t','')
        metadata_dict["title"] = title
        creator = columns[2].text.strip()
        metadata_dict["creator"] = creator
        subject = columns[3].text.strip()
        metadata_dict["subject"] = subject
        html_links = columns[5].findAll('a')
        html_links_list = get_file_names(html_links)
        text_links_list = [f.replace('.html', '.txt') for f in html_links_list]
        metadata_dict["rights"] = "public-domain or with due consent from respective authors"
        metadata_dict["source"] = "https://www.projectmadurai.org/pmworks.html"
        metadata_dict["file_names_html"] = ' | '.join(html_links_list)
        metadata_dict["text_links_list"] = ' | '.join(text_links_list)
        for item in html_links_list:
            all_links.append(item)
        all_metadata.append(metadata_dict)


# In[ ]:


df = pd.DataFrame(all_metadata) 
df.head(2)


# In[ ]:


df.to_csv("metadata_list.csv", index=False)


# In[ ]:


sys.setrecursionlimit(25000)


# In[ ]:


for html_page in all_links:
    if len(html_page) < 9:
        print("WARNING: Not a valid html page : " + html_page)
        continue;
    pmuni_url = "https://www.projectmadurai.org/pm_etexts/utf8/" + html_page
    print(pmuni_url)
    # save html
    pmuni_page = get_page(pmuni_url)
    save_file("html/" + html_page, str(pmuni_page))
    text = pmuni_page.get_text()
    text_file_name = html_page.replace(".html", ".txt")
    save_file("text/" + text_file_name, text)
    print(html_page)


# In[ ]:




