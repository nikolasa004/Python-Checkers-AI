from tabulate import tabulate
def debag_u_konzoli(novo_stanje_moji_tokeni,novo_stanje_protivnicki_tokeni,jedno_polje,pocetna_sirina,pocetna_visina):
    zaglavlje=[51,132,213,294,375,456,537,618]
    prvi_red=["-" for i in range(8)]
    prvi_red.append(76)
    drugi_red=["-" for i in range(8)]
    drugi_red.append(157)
    treci_red=["-" for i in range(8)]
    treci_red.append(238)
    cetvrti_red=["-" for i in range(8)]
    cetvrti_red.append(319)
    peti_red=["-" for i in range(8)]
    peti_red.append(400)
    sesti_red=["-" for i in range(8)]
    sesti_red.append(481)
    sedmi_red=["-" for i in range(8)]
    sedmi_red.append(562)
    osmi_red=["-" for i in range(8)]
    osmi_red.append(643)
    for pozicije in novo_stanje_moji_tokeni.keys():
        if pozicije[1]==pocetna_visina:
            if pozicije[0]==pocetna_sirina:
                prvi_red[0]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                prvi_red[1]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                prvi_red[2]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                prvi_red[3]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                prvi_red[4]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                prvi_red[5]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                prvi_red[6]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                prvi_red[7]="M"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height():
            if pozicije[0]==pocetna_sirina:
                drugi_red[0]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                drugi_red[1]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                drugi_red[2]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                drugi_red[3]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                drugi_red[4]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                drugi_red[5]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                drugi_red[6]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                drugi_red[7]="M"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height()*2:
            if pozicije[0]==pocetna_sirina:
                treci_red[0]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                treci_red[1]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                treci_red[2]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                treci_red[3]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                treci_red[4]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                treci_red[5]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                treci_red[6]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                treci_red[7]="M"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height()*3:
            if pozicije[0]==pocetna_sirina:
                cetvrti_red[0]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                cetvrti_red[1]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                cetvrti_red[2]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                cetvrti_red[3]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                cetvrti_red[4]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                cetvrti_red[5]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                cetvrti_red[6]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                cetvrti_red[7]="M"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height()*4:
            if pozicije[0]==pocetna_sirina:
                peti_red[0]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                peti_red[1]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                peti_red[2]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                peti_red[3]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                peti_red[4]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                peti_red[5]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                peti_red[6]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                peti_red[7]="M"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height()*5:
            if pozicije[0]==pocetna_sirina:
                sesti_red[0]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                sesti_red[1]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                sesti_red[2]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                sesti_red[3]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                sesti_red[4]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                sesti_red[5]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                sesti_red[6]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                sesti_red[7]="M"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height()*6:
            if pozicije[0]==pocetna_sirina:
                sedmi_red[0]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                sedmi_red[1]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                sedmi_red[2]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                sedmi_red[3]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                sedmi_red[4]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                sedmi_red[5]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                sedmi_red[6]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                sedmi_red[7]="M"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height()*7:
            if pozicije[0]==pocetna_sirina:
                osmi_red[0]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                osmi_red[1]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                osmi_red[2]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                osmi_red[3]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                osmi_red[4]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                osmi_red[5]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                osmi_red[6]="M"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                osmi_red[7]="M"
    for pozicije in novo_stanje_protivnicki_tokeni.keys():
        if pozicije[1]==pocetna_visina:
            if pozicije[0]==pocetna_sirina:
                prvi_red[0]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                prvi_red[1]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                prvi_red[2]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                prvi_red[3]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                prvi_red[4]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                prvi_red[5]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                prvi_red[6]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                prvi_red[7]="P"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height():
            if pozicije[0]==pocetna_sirina:
                drugi_red[0]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                drugi_red[1]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                drugi_red[2]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                drugi_red[3]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                drugi_red[4]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                drugi_red[5]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                drugi_red[6]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                drugi_red[7]="P"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height()*2:
            if pozicije[0]==pocetna_sirina:
                treci_red[0]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                treci_red[1]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                treci_red[2]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                treci_red[3]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                treci_red[4]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                treci_red[5]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                treci_red[6]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                treci_red[7]="P"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height()*3:
            if pozicije[0]==pocetna_sirina:
                cetvrti_red[0]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                cetvrti_red[1]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                cetvrti_red[2]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                cetvrti_red[3]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                cetvrti_red[4]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                cetvrti_red[5]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                cetvrti_red[6]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                cetvrti_red[7]="P"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height()*4:
            if pozicije[0]==pocetna_sirina:
                peti_red[0]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                peti_red[1]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                peti_red[2]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                peti_red[3]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                peti_red[4]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                peti_red[5]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                peti_red[6]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                peti_red[7]="P"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height()*5:
            if pozicije[0]==pocetna_sirina:
                sesti_red[0]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                sesti_red[1]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                sesti_red[2]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                sesti_red[3]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                sesti_red[4]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                sesti_red[5]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                sesti_red[6]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                sesti_red[7]="P"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height()*6:
            if pozicije[0]==pocetna_sirina:
                sedmi_red[0]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                sedmi_red[1]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                sedmi_red[2]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                sedmi_red[3]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                sedmi_red[4]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                sedmi_red[5]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                sedmi_red[6]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                sedmi_red[7]="P"
        elif pozicije[1]==pocetna_visina+jedno_polje.slika.get_height()*7:
            if pozicije[0]==pocetna_sirina:
                osmi_red[0]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width():
                osmi_red[1]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*2:
                osmi_red[2]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*3:
                osmi_red[3]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*4:
                osmi_red[4]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*5:
                osmi_red[5]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*6:
                osmi_red[6]="P"
            elif pozicije[0]==pocetna_sirina+jedno_polje.slika.get_width()*7:
                osmi_red[7]="P"
    print(tabulate([zaglavlje,prvi_red,drugi_red,treci_red,cetvrti_red,peti_red,sesti_red,sedmi_red,osmi_red],tablefmt="fancy_grid"))