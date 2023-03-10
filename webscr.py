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

df = pandas.DataFrame(columns=["o_Title","o_Author","Title", "Author", "Query","URLs", "Match", "Match_n"])

urls = []

lsrch = ['https://loschmidt.chemi.muni.cz/peg/wp-content/uploads/2013/01/chemlisty2010.pdf', 'https://dspace.cvut.cz/bitstream/handle/10467/75175/FBMI-DP-2016-Vobecka-Katerina-prace.pdf?sequence=-1&isAllowed=y', 'https://dspace.cvut.cz/bitstream/handle/10467/91403/FBMI-DP-2020-Vesela-Katerina-prace.pdf?sequence=-1&isAllowed=y', 'https://dk.upce.cz/bitstream/handle/10195/46323/Chladkova_Vyuziti%20Biosensoru_SS_2012.pdf?sequence=3&isAllowed=y', 'https://dk.upce.cz/bitstream/handle/10195/68479/PorizkovaP_Priprava_cholinesterazoveho_MP_2017.pdf?sequence=1&isAllowed=y', 'https://www.researchgate.net/profile/Pavla_Martinkova4/publication/323869415_Stanoveni_glykemie_pomoci_biosenzoru_soucasny_stav_a_trendy_ve_vyzkumu/links/5ab0c8f10f7e9b4897c237d9/Stanoveni-glykemie-pomoci-biosenzoru-soucasny-stav-a-trendy-ve-vyzkumu.pdf', 'https://theses.cz/id/owjtyx/16321490', 'https://core.ac.uk/download/pdf/161964838.pdf', 'http://chemicke-listy.cz/Bulletin/bulletin413/bulletin413.pdf', 'https://dspace.cuni.cz/bitstream/handle/20.500.11956/47744/150007322.pdf?sequence=1&isAllowed=y']

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
    print("\033[34m" + query + "\033[0m")
    
    # srch = search(query, tld="co.in", num=10, stop=10, pause=2)
    # lsrch = list(srch)
    
    citac = 0
    match = 0
    n = ""
    for url in lsrch:
        print("\t" + url)
        citac += 1
        if ".pdf" in str(url):
            if input("\t\tJe to vážně pdf?\t") == 0: 
                break
            
            nazev = url.split("/")[-1].split(".pdf")[0].replace("%", "")
            if input("\t\tJe validní: " + nazev + "?\t") == 0:
                nazev = str(b) + " " + ttl + " " + citac
            
            webbrowser.open(url)            
            urls.append(url)
            
            if input("\t\tZdá se že je to daný zdroj?\t") == 1:
                nazev += "&&&"
                match += 1
                n = nazev
            
            cesta = Path("./downloaded/" + query + "_@_" + nazev + ".pdf")
            response = requests.get(url)
            cesta.write_bytes(response.content)
    
    df.loc[len(df)] = [row["Title"], row['Author'], ttl, b, query, lsrch, match, n]
    
    input("\033[31m\tČekám na stisk klávesy abych mohl hledat další...\033[0m") #https://stackoverflow.com/questions/66206815/how-to-change-the-ouput-color-in-the-terminal-of-visual-code


# https://pypi.org/project/websearch-python/



#['https://loschmidt.chemi.muni.cz/peg/wp-content/uploads/2013/01/chemlisty2010.pdf', 'https://dspace.cvut.cz/bitstream/handle/10467/75175/FBMI-DP-2016-Vobecka-Katerina-prace.pdf?sequence=-1&isAllowed=y', 'https://dspace.cvut.cz/bitstream/handle/10467/91403/FBMI-DP-2020-Vesela-Katerina-prace.pdf?sequence=-1&isAllowed=y', 'https://dk.upce.cz/bitstream/handle/10195/46323/Chladkova_Vyuziti%20Biosensoru_SS_2012.pdf?sequence=3&isAllowed=y', 'https://dk.upce.cz/bitstream/handle/10195/68479/PorizkovaP_Priprava_cholinesterazoveho_MP_2017.pdf?sequence=1&isAllowed=y', 'https://www.researchgate.net/profile/Pavla_Martinkova4/publication/323869415_Stanoveni_glykemie_pomoci_biosenzoru_soucasny_stav_a_trendy_ve_vyzkumu/links/5ab0c8f10f7e9b4897c237d9/Stanoveni-glykemie-pomoci-biosenzoru-soucasny-stav-a-trendy-ve-vyzkumu.pdf', 'https://theses.cz/id/owjtyx/16321490', 'https://core.ac.uk/download/pdf/161964838.pdf', 'http://chemicke-listy.cz/Bulletin/bulletin413/bulletin413.pdf', 'https://dspace.cuni.cz/bitstream/handle/20.500.11956/47744/150007322.pdf?sequence=1&isAllowed=y']