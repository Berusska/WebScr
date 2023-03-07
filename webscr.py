from googlesearch import search
import pandas
from pathlib import Path
import webbrowser
import requests


xx = pandas.read_excel("../css/uniqZdr.xlsx")
xx = xx.reset_index()
x = xx.iloc[1:5]

urls = []

for index, row in x.iterrows():
    aut = str(row['Author']).replace(".", "")
    b = []
    if ";" in aut:
        auts = aut.split(";")
    else:
        auts = list(aut)
        
    for each in auts: b.extend(max(each.split(","), key = len))
    
    ttl = str(row["Title"]).replace("[online", "")
    
    query = str(b[0]).split(" ")[0] + " " + ttl + " pdf"
    
    srch = search(query, tld="co.in", num=3, stop = 3, pause=2)
        
    for url in srch:
        if ".pdf" in str(url):
            webbrowser.open(url)
            
            urls.append(url)
            
            nazev = url.split("/")[-1].split(".pdf")[0].replace("%", "")
            cesta = Path("./downloaded/" + query + "_@_" + nazev + ".pdf")
            response = requests.get(url)
            cesta.write_bytes(response.content)

    print(query)
    print("\tČekám na stisk klávesy abych mohl hledat další...")
    
    input("\033[31m\tPress Enter to continue...\033[0m") #https://stackoverflow.com/questions/66206815/how-to-change-the-ouput-color-in-the-terminal-of-visual-code


    