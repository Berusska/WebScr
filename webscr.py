from googlesearch  import search #https://www.geeksforgeeks.org/performing-google-search-using-python-code/
import pandas
from pathlib import Path
import webbrowser
import requests
import openpyxl
import time

xx = pandas.read_excel("./uniqZdr.xlsx")
xx = xx.reset_index()
x = xx.iloc[0:5]

urls = []

for index, row in x.iterrows():
    aut = str(row['Author']).replace(".", "")
    b = []
    if ";" in aut:
        auts = aut.split(";")
    else:
        auts = list(aut)
        
    b = max([each.split(",") for each in auts][0], key = len)
    
    ttl = str(row["Title"]).replace("[online", "")
    
    query = str(b) + " " + ttl + " pdf"
    print(query)
    srch = search(query, tld="co.in", num=10, stop=10, pause=2)
    print([srch])
        
    for url in srch:
        print(url)
        if ".pdf" in str(url):
            webbrowser.open(url)
            
            urls.append(url)
            
            nazev = url.split("/")[-1].split(".pdf")[0].replace("%", "")
            cesta = Path("./downloaded/" + query + "_@_" + nazev + ".pdf")
            response = requests.get(url)
            cesta.write_bytes(response.content)

    
    print("\tČekám na stisk klávesy abych mohl hledat další...")
    
    input("\033[31m\tPress Enter to continue...\033[0m") #https://stackoverflow.com/questions/66206815/how-to-change-the-ouput-color-in-the-terminal-of-visual-code

query = "Geeksforgeeks"

# https://pypi.org/project/websearch-python/