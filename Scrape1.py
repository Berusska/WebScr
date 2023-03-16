#jde po řádcích tabulky a
    # otevře google s zadaným vyhledáváním
    # uživatel volně prochází a 
        #bud dané pdfko, resp jeho url adresu uloží do clipdoard -> module paperclip
        # a to se samovolně stahne pojmenuje
        #nebo pdf stáhne uživatel a skript odhalí nový soubor ve složce a tak ho vhodně pojmenuje dle aktuálních hodnot title-author
    #
    #


import pandas
from pathlib import Path
import requests
import pywhatkit as kt
import pyperclip as pc
import PySimpleGUI as sg

# background = '#F0F0F0'
# sg.SetOptions(background_color=background, 
#     element_background_color=background, 
#     text_element_background_color=background,
#     window_location=(0, 0), 
#     margins=(0,0), 
#     text_color = 'Black',
#     input_text_color ='Black',
#     button_color = ('Black', 'gainsboro'))


dfIn = pandas.read_excel("./uniqZdr.xlsx").reset_index().iloc[40:50]

dfOut = pandas.DataFrame(columns=["o_Title","o_Author","Title", "Author", "Query","URLs", "Match", "Match_n"])

primSlozka = Path("C:/Users/Admin/Downloads")
sekSlozka = Path("./downloaded")
sekSlozka.mkdir(parents=True, exist_ok=True)
veSlozce = set(sorted(primSlozka.glob("*.pdf"))) 

urls = []; querys = []

pc.copy("0"); predtim = "0"

for index, radek in dfIn.iterrows():
    
    autor = str(radek['Author']).replace(".", "")
    auts = autor.split(";")[0].split(sep = ", ")
    Auth = str(sorted(auts)[0])
    
    ttl = str(radek["Title"]).replace("[online", "")
    
    query = Auth + " " + ttl + " pdf"
    print("\033[34m" + query + "\033[0m")
    
    if query not in querys:
        querys.append(query)
        kt.search(query)
        
    pocitac = 0
    match = 0
    # predtim = pc.paste() 
    lsrch = []
    indikace_schranky = 0
    
    while True: #nyní stále kontroluj, uživatel vyhledává a stahuje ... 
        schranka = pc.paste()
        
        if indikace_schranky == 0:
            if predtim != schranka:
                predtim = schranka
                indikace_schranky = 1   
        elif indikace_schranky == 1:
            veSlozce_actual = set(sorted(primSlozka.glob("*.pdf")))
            newFile = veSlozce.symmetric_difference(veSlozce_actual)
            if len(newFile) != 0:
                cestaFile = list(newFile)[0]
            
                layout = [[sg.Text(f"Ve schránce nová url adresa a zároveň se objevil nový PDF soubor v primární složce.\n\tNový soubor: {cestaFile.name}\n\n\tAktuální schránka: {schranka}\n")],[sg.Button('Jiný zajimavý zdroj', pad=((20,15),3)), sg.Button('Daný zdroj', pad=((20,15),3)), sg.Button("Dej další zdroj", pad=((20,15),3), button_color="red")]]
                
                event, other = sg.Window('Stahování zdrojů pd DP', layout, keep_on_top=True).read(close=True) 
                
                if event == "Dej další zdroj" or "":
                    break 
                elif event == "Další zajimavý zdroj":                    
                    pocitac += pocitac
                    indikatorValidity = f"{pocitac} "
                elif event == "Daný zdroj":
                    pocitac += pocitac
                    indikatorValidity += f"{pocitac} &&&_"
                    match += 1
                
                if event in ["Jiný zajímavý zdroj", "Daný zdroj"]:      
                    urls.append(schranka)
                    
                    cestaFile.rename(str(sekSlozka.absolute()) + "/" + query.replace(" pdf", indikatorValidity) + cestaFile.name)
                    
                    lsrch.append(schranka)


    
    dfOut.loc[len(dfOut)] = [radek["Title"], radek['Author'], ttl, Auth, query, lsrch, match]
    indikace_schranky = 0
    
    input("\033[31m\tČekám na stisk klávesy abych mohl hledat další položku ve zdrojích...\033[0m") 



