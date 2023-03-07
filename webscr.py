from googlesearch import search
import pandas
from pathlib import Path
import webbrowser
import keyboard

xx = pandas.read_excel("../css/uniqZdr.xlsx")
xx = xx.reset_index()
x = xx.iloc[:5]

for index, row in x.iterrows():
    aut = str(row['Author']).replace(".", "")
    b = []
    if ";" in aut:
        auts = aut.split(";")
    else:
        auts = list(aut)
        
    for each in auts: b.extend(max(each.split(","), key = len))
    
    ttl = str(row["Title"]).replace("[online", "")
    
    query = b[0] + " " + ttl + " pdf"
    
    srch = search(query, tld="co.in", num=3, stop=10, pause=2)
        
    for url in srch:
        webbrowser.open(url)
    
    print(query)
    print("\t\tČekám na stisk klávesy abych mohl hledat další...")
    keyboard.sleep()
    