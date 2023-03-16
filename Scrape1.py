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
import pywhatkit as kt
import pyperclip as pc
import PySimpleGUI as sg
from itertools import chain
import pyautogui
import keyboard


import colorama
colorama.init()



# background = '#F0F0F0'
# sg.SetOptions(background_color=background, 
#     element_background_color=background, 
#     text_element_background_color=background,
#     window_location=(0, 0), 
#     margins=(0,0), 
#     text_color = 'Black',
#     input_text_color ='Black',
#     button_color = ('Black', 'gainsboro'))

od, do = input("Zadejte rozsah řádků oddělený pomlčkou: ").split("-")
# od, do = 1, 2

dfIn = pandas.read_excel("./uniqZdr.xlsx").reset_index().iloc[int(od)-1:int(do)]

dfOut = pandas.DataFrame(columns=["o_Title","o_Author","Title", "Author", "Query","URLs", "Match"])

primSlozka = Path("C:/Users/Admin/Downloads")
sekSlozka = Path("./downloaded")
sekSlozka.mkdir(parents=True, exist_ok=True)
veSlozce = set(sorted(primSlozka.glob("*.pdf"))) 

urls = []; querys = []

pc.copy("0"); predtim = "0"

for index, radek in dfIn.iterrows():
    
    autor = str(radek['Author']).replace(".", "")
    auts_ = autor.split(";")
    auts = [i.split(",") for i in auts_]
    Auth = str(sorted(list(chain.from_iterable(auts)), reverse=True)[0])
    
    ttl = str(radek["Title"]).replace("[online", "")
    
    query = Auth + " " + ttl + " pdf"
    print("\033[34m" + query + "\033[0m")
    
    if query not in querys:
        querys.append(query)
        kt.search(query)
    
    
    pocitac = 0
    match = 0
    lsrch = []
    indikace_schranky = 0
    while True: #nyní stále kontroluj, uživatel vyhledává a stahuje ... 
        schranka = pc.paste()
        
        if indikace_schranky == 0:
            klavesa = keyboard.read_key()
            if klavesa == "f5":
                sg.popup_auto_close("Byla stisknuta klávesa F5.\n\nZdroj nenalezen, přistupuji k dalšímu.", background_color="darkgreen" ,auto_close_duration=2, keep_on_top=True)
                break
            
            if klavesa == "f6": 
                pyautogui.hotkey('ctrl', 'c')    
            if predtim != schranka:
                pyautogui.hotkey('ctrl', 's')#takže by mělo stačit jen zkopírovat F6; Ctrl + C 
                pyautogui.click(100, 200) # stahovací okno musí mít určitou pozici
                pyautogui.hotkey("enter") #na zavření dialogi stahování
                pyautogui.hotkey('ctrl', 'w') 
                pyautogui.hotkey("enter") #na zavření tabu
                pyautogui.hotkey('ctrl', 'w') 
                predtim = schranka
                indikace_schranky = 1 

        elif indikace_schranky == 1:
            veSlozce_actual = set(sorted(primSlozka.glob("*.pdf")))
            newFile = veSlozce.symmetric_difference(veSlozce_actual)
            if len(newFile) != 0:
                cestaFile = list(newFile)[0]
            
                layout = [[sg.Text(f"Ve schránce nová url adresa a zároveň se objevil nový PDF soubor v primární složce.\n\tAktuální požadavek: {query}\n\n\tNový soubor: {cestaFile.name}\n\n\tAktuální schránka: {schranka}\n")],[[sg.Button('Jiný zajimavý zdroj', size = (15, 2), pad=((15,20),20)), sg.Button('Daný zdroj', size = (15, 2), pad=((15,20),20)), sg.Button("Daný zdroj\nDej další zdroj", size = (15, 2), pad=((15,20),20),button_color="red"), sg.Button("Jiný zajímavý zdroj\nDej další zdroj", size = (15, 2), pad=((15,20),20), button_color="purple")]]]
                
                # schranka = pc.paste() #joko možnost opravy v průběhu
                
                event, other = sg.Window('Stahování zdrojů pro DP', layout, keep_on_top=True).read(close=True) 
                
                if event == "":
                    break 
                elif event == "Jiný zajimavý zdroj":                    
                    pocitac += pocitac
                    indikatorValidity = f"_{pocitac}__"
                elif event == "Daný zdroj":
                    pocitac += pocitac
                    indikatorValidity = f"_{pocitac}_&&&__"
                    match += 1
                elif event == "Daný zdroj\nDej další zdroj":
                    pocitac += pocitac
                    indikatorValidity = f"_{pocitac}_&&&__"
                    match += 1
                elif event == "Jiný zajímavý zdroj\nDej další zdroj":
                    pocitac += pocitac
                    indikatorValidity = f"_{pocitac}__"                    
                
                if event != None:      
                    urls.append(schranka)
                    
                    try:
                        cestaFile.rename(str(sekSlozka.absolute()) + "/" + query.replace(" pdf", indikatorValidity) + cestaFile.name)
                        print("\tSoubor přesunut.")
                        lsrch.append(schranka)
                    except:
                        FileExistsError
                    
                                        
                if event == "Daný zdroj\nDej další zdroj" or event == "Jiný zajímavý zdroj\nDej další zdroj":
                    print("\tPřistupuji k dalšímu zdroji")
                    break


    
    dfOut.loc[len(dfOut)] = [radek["Title"], radek['Author'], ttl, Auth, query, lsrch, match]

    indikace_schranky = 0

dfOut.to_csv("./PruberStahovani.csv", encoding="utf-8")
print("Legitimní konec")

#https://stackoverflow.com/questions/52675506/get-chrome-tab-url-in-python

# https://stackoverflow.com/questions/71487463/why-cant-python-rich-print-text-styles-only-colors-on-windows-command-line
