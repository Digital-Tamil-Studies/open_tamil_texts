#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import numpy as np
import pandas as pd


# In[2]:


# Load the listing file  (https://ta.wikisource.org/wiki/விக்கிமூலம்:முதற்_பக்கம்/புதிய_உரைகள்#பிற_நூல்கள்)
data_file = open('wikisource_listing.txt', 'r') 
lines = data_file.readlines() 


# In[3]:


# Read each item and parse the metadata
wikisource_books = []
for line in lines:
    metadata = {}    
    pattern = "xport\|(.*?)}}"
    title = re.search(pattern, line).group(1)
    metadata["title"] = title    
    metadata["source"] = "https://ta.wikisource.org/wiki/" + title
    
    metadata["creator"] = ""
    pattern2 = "\[\[ஆசிரியர்:(.*?)\|"
    creator = re.search(pattern2, line)
    if creator is not None:
        creator = creator.group(1)
        metadata["creator"] = creator
        
        
    metadata["subject"] = ""
    pattern3 = "பகுப்பு:(.*?)\|"
    subject = re.search(pattern3, line)
    if subject is not None:
        subject = subject.group(1)
        metadata["subject"] = subject
        
    metadata["date"] = ""
    pattern4 = "(\d{4})"
    date = re.search(pattern4, line)
    if date is not None:
        date = date.group(1)
        metadata["date"] = date  
    wikisource_books.append(metadata)


# In[4]:


df = pd.DataFrame(wikisource_books) 
df.head(10)


# In[5]:


df.to_csv("metadata.csv", index=False)


# In[ ]:




