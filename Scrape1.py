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

primSlozka = Path("C:/Users/karas/Downloads")
sekSlozka = Path("./downloaded")
sekSlozka.mkdir(parents=True, exist_ok=True)
veSlozce = set(sorted(primSlozka.iterdir())) 

urls = []; querys = []

pc.copy(""); predtim = ""

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
    # predtim = pc.paste() #TODO: nefunguje mi to s tím porovnáváním, resp neotevírá se mi ani okno a tudíž to pak nezná 
    event = "" #TODO: nepomohlo
    lsrch = []
    indikace_schranky = 0
    indikace_stazeni = 0
    
    while True: #nyní stále kontroluj, uživatel vyhledává a stahuje ... #TODO: já nevím jak se to bude chovat - protože: jakmile bude ve schránce nová polozka, musí to čekat než bude nová položka i ve složce, až pak může vyskožit okno a PŘEJMENOVAT SE TO 
        schranka = pc.paste()
        if predtim != schranka:
            nazev = schranka.split("/")[-1].split(".pdf")[0].replace("%", "")

            layout = [[sg.Text(f"Ve schránce nová url adresa.\n\tAktuální zdroj je:\n\t{schranka}\nNazev bude: {nazev}")],[sg.Button('Pouze validní', pad=((20,15),3)), sg.Button('Daný zdroj', pad=((20,15),3)), sg.Button('Nevalidní daný zdroj', pad=((20,15),3)), sg.Button("Dej další zdroj", pad=((20,15),3), button_color="red")]] #TODO: DALŠÍ button pro daný zdroj ale s nevalidním názvem

            event, other = sg.Window('Choose an option', layout, keep_on_top=True).read(close=True) 
            predtim = schranka           
        if event == "":
            pass
        elif event == "Dej další zdroj":
            break 
        elif event == "Pouze validní":
            nazev = query.replace(" pdf", "") + nazev + str(pocitac)
            pocitac += pocitac
        elif event == "Daný zdroj":
            nazev += "&&&"
            match += 1
        elif event == "Nevalidní daný zdroj":
            nazev = query.replace(" pdf", "") + str(pocitac) + "&&&"
        
        if event in ["Dej další zdroj", "Pouze validní", "Daný zdroj"]:      
            urls.append(schranka)
            
            cesta = Path("./downloaded/" + query.replace(" pdf", "") + "_@_" + nazev + ".pdf")
            response = requests.get(schranka)
            if response.status_code == 200:
                cesta.write_bytes(response.content)
            
            lsrch.append(schranka)
    
    dfOut.loc[len(dfOut)] = [radek["Title"], radek['Author'], ttl, Auth, query, lsrch, match]
    
    input("\033[31m\tČekám na stisk klávesy abych mohl hledat další...\033[0m") 



