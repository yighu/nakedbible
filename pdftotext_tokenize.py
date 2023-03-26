import fitz
import pandas as pd
import re
import nltk
from string import punctuation
import numpy as np
from pyarrow import csv, parquet
from nltk.corpus import stopwords
nltk.download("stopwords")
stopwords_ = set(stopwords.words("english"))

doc = fitz.open("NBPTranscripts1-458.pdf")
id =  0
episode = 0
title=""

def cleanedToken(txt):
   #clean_text = re.sub(f"[{re.escape(punctuation)}]", "", txt) #this removes verse
   clean_text = txt.replace(",","").replace(".","").replace(";","").replace("?","")
   tokens = set(clean_text.split())	
   clean_tokens = [t for t in tokens if not t in stopwords_]
   clean_text = " ".join(clean_tokens)
   return clean_text.lower()

results = []

for page in doc:
   id +=1
   text=page.getText("text")
   line1 = text.split("\n")[0]
   if (line1.startswith("Naked Bible Podcast")):
   	episodes = re.findall(r'\d+', line1)
   	if (len(episodes)>0):
     		episode = episodes[0]
     		epstr=f"{episode}" 
     		titleindex =  line1.index(epstr)+len(epstr)
     		title= line1[titleindex:].strip().lstrip(':').lstrip()
   		
   tokens = cleanedToken(text)    
   #print(f"{id} {episode} {title} {tokens}") #write to parquet file
   results.append([id,episode,title,tokens,text])

df = pd.DataFrame(data=np.array(results), 
               index=np.arange(len(results)), 
               columns=['PageNumb','EpisodeNum','Title','Tokens','Text'])

#parquet.write_table(df, "file.parquet")
df.to_parquet("nakebibletranscript.parquet")

#Intention
#use duckDb to search by page number, episode, title, token and then use page number to display the page png by reading it out of pdf file

