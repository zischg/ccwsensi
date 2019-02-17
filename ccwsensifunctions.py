import numpy

#************************************************************************************************
#Funktion zum Kontrollieren der Hoehenstufe
#************************************************************************************************
def check_hoehenstufe(NAIS_standort, NAIS_hoehenstufe, NAIS_standortregion, Tannenareal, naishsregarr):
    #Wichtig: NAIS_hoehenstufe muss als Kuerzel von hoehenstufen_heute_list_kurz eingegben werden
    #naishsregarr ist die Tabelle von IWA
    hoehenstufen_heute_list_kurz=["OSA","SA","HM","OM","UM","SM","C","UMOM"]
    standortsregionenlist = ["1", "2a", "2b", "3", "4", "5a", "5b", "J", "M"]
    feldnamelist=naishsregarr[0][1:].tolist()
    stonamelist=naishsregarr[1:,0].tolist()
    spaltenname="HS"+"_"+NAIS_hoehenstufe+"-"+NAIS_standortregion
    if Tannenareal in ["Nebenareal","Reliktareal"]:
        spaltenname = spaltenname + "-" + Tannenareal
    NAIS_standort_neu=""
    NAIS_hoehenstufe_neu=""
    if spaltenname in feldnamelist and NAIS_standort in stonamelist:
        arrspaltenummer=feldnamelist.index(spaltenname)+1
        arrzeilennummer=stonamelist.index(NAIS_standort)+1
        if naishsregarr[arrzeilennummer,arrspaltenummer] in ["1","2"]:
            #gibt zurueck, dass der Standort in der richtigen Hoehenstufe ist
            return True, NAIS_standort, NAIS_hoehenstufe
        else:
            #hier checken, welche Hoehenstufe es sonst sein koennte
            moeglichehoehenstufen=[]
            i=1
            while i<numpy.shape(naishsregarr)[1]:
                if naishsregarr[arrzeilennummer,i] in ["1","2"] and naishsregarr[0,i].replace("-"," ").replace("_"," ").strip().split()[1] not in moeglichehoehenstufen:# and naishsregarr[0,i].replace("-"," ").replace("_"," ").strip().split()[2]==NAIS_standortregion:
                        moeglichehoehenstufen.append(naishsregarr[0,i].replace("-"," ").replace("_"," ").strip().split()[1])
                i+=1
            if NAIS_hoehenstufe in moeglichehoehenstufen:
                return True, NAIS_standort, NAIS_hoehenstufe
            else:
                #weise die oberst moeglichen Hoehenstufe als neue Hoehenstufe zu
                NAIS_hoehenstufe_neu=moeglichehoehenstufen[-1]
                return False, NAIS_standort, NAIS_hoehenstufe_neu
    else:
        return True, NAIS_standort, NAIS_hoehenstufe
def check_hoehenstufe_langeLegende(NAIS_standort, NAIS_hoehenstufe, NAIS_standortregion, Tannenareal, naishsregarr):
    #Wichtig: NAIS_hoehenstufe muss als Legendeeinheit von hoehenstufen_heute_list eingegben werden
    hoehenstufenabkuerzungendict = {"hyperinsubrisch": "HYP", "collin": "C", "collin mit Buche": "C", "submontan": "SM",
                                  "untermontan": "UM", "obermontan": "OM", "unter- und obermontan": "UMOM",
                                  "hochmontan im Tannen-Hauptareal": "HM", "hochmontan im Tannen-Nebenareal": "HM",
                                  "hochmontan im Tannen-Reliktareal": "HM", "hochmontan": "HM", "subalpin": "SA",
                                  "obersubalpin": "OSA"}
    hoehenstufenabkuerzungendict2 = {"HYP": "hyperinsubrisch", "C": "collin", "SM": "submontan", "UM": "untermontan",
                                     "OM": "obermontan", "UMOM": "unter- und obermontan", "HM": "hochmontan",
                                     "SA": "subalpin", "OSA": "obersubalpin"}

    #naishsregarr ist die Tabelle von IWA
    hoehenstufen_heute_list_kurz=["OSA","SA","HM","OM","UM","SM","C","UMOM"]
    standortsregionenlist = ["1", "2a", "2b", "3", "4", "5a", "5b", "J", "M"]
    feldnamelist=naishsregarr[0][1:].tolist()
    stonamelist=naishsregarr[1:,0].tolist()
    spaltenname="HS"+"_"+hoehenstufenabkuerzungendict[NAIS_hoehenstufe]+"-"+NAIS_standortregion
    if Tannenareal in ["Nebenareal","Reliktareal"]:
        spaltenname = spaltenname + "-" + Tannenareal
    if spaltenname in feldnamelist and NAIS_standort in stonamelist:
        arrspaltenummer=feldnamelist.index(spaltenname)+1
        arrzeilennummer=stonamelist.index(NAIS_standort)+1
        if naishsregarr[arrzeilennummer,arrspaltenummer] in ["1","2"]:
            #gibt zurueck, dass der Standort in der richtigen Hoehenstufe ist
            return True, NAIS_standort, NAIS_hoehenstufe
        else:
            #hier checken, welche Hoehenstufe es sonst sein koennte
            moeglichehoehenstufen=[]
            i=1
            while i<numpy.shape(naishsregarr)[1]:
                if naishsregarr[arrzeilennummer,i] in ["1","2"] and naishsregarr[0,i].replace("-"," ").replace("_"," ").strip().split()[1] not in moeglichehoehenstufen:# and naishsregarr[0,i].replace("-"," ").replace("_"," ").strip().split()[2]==NAIS_standortregion:
                        moeglichehoehenstufen.append(naishsregarr[0,i].replace("-"," ").replace("_"," ").strip().split()[1])
                i+=1
            if hoehenstufenabkuerzungendict[NAIS_hoehenstufe] in moeglichehoehenstufen:
                return True, NAIS_standort, NAIS_hoehenstufe
            else:
                #weise die oberst moeglichen Hoehenstufe als neue Hoehenstufe zu
                NAIS_hoehenstufe_neu= hoehenstufenabkuerzungendict2[moeglichehoehenstufen[-1]]
                if Tannenareal in ["Hauptareal", "Nebenareal", "Reliktareal"] and NAIS_hoehenstufe_neu=="hochmontan":
                    NAIS_hoehenstufe_neu = NAIS_hoehenstufe_neu+" im Tannen-"+Tannenareal
                elif NAIS_hoehenstufe_neu=="C" and NAIS_hoehenstufe=="collin mit Buche":
                    NAIS_hoehenstufe_neu = "collin mit Buche"
                return False, NAIS_standort, NAIS_hoehenstufe_neu
    else:
        return True, NAIS_standort, NAIS_hoehenstufe

#************************************************************************************************
#Funktionen zum Model Veraenderungen der Waldstandorte im Klimawandel
#************************************************************************************************
#standortsregion in ["J","M","1","2","2a","2b","3"], Projektionspfad von obersubalpin nach subalpin
def Projektionspfad_regJM12a2b3_OSA_SA(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    if hoehenstufe_heute == "obersubalpin" and hoehenstufe_zukunft == "subalpin":
        NAIS_StandortstypZukunft = "NA"
        if NAIS_StandortstypHeute == "59" and hangneigung > 60: # and tannenareal_zukunft in ["Reliktareal","Hauptareal", "Nebenareal"]:
            NAIS_StandortstypZukunft = "57C"
        elif NAIS_StandortstypHeute == "59" and hangneigung <= 60:
            NAIS_StandortstypZukunft = "57V"
        elif NAIS_StandortstypHeute == "59Lae" and hangneigung > 60:
            NAIS_StandortstypZukunft = "57CLae"
        elif NAIS_StandortstypHeute == "59Lae" and hangneigung <= 60:
            NAIS_StandortstypZukunft = "57VLae"
        elif NAIS_StandortstypHeute == "59" and blockschutt == True:
            NAIS_StandortstypZukunft = "57Bl"
        elif NAIS_StandortstypHeute == "59A":
            NAIS_StandortstypZukunft = "60"
        # 59A in Lawinenzuegen
        elif NAIS_StandortstypHeute == "59C":
            NAIS_StandortstypZukunft = "58Bl"
        elif NAIS_StandortstypHeute == "59E":
            NAIS_StandortstypZukunft = "53*s"
        elif NAIS_StandortstypHeute == "59H":
            NAIS_StandortstypZukunft = "57VM"
        elif NAIS_StandortstypHeute == "59L":
            NAIS_StandortstypZukunft = "58L"
        elif NAIS_StandortstypHeute == "59LLae":
            NAIS_StandortstypZukunft = "58LLae"
        elif NAIS_StandortstypHeute == "59R":
            NAIS_StandortstypZukunft = "59R"
        elif NAIS_StandortstypHeute == "59V":
            NAIS_StandortstypZukunft = "59M"
        elif NAIS_StandortstypHeute == "59VLae" and hangneigung > 60:
            NAIS_StandortstypZukunft = "57CLae"
        elif NAIS_StandortstypHeute == "59VLae" and hangneigung <= 60:
            NAIS_StandortstypZukunft = "57VLae"
        elif NAIS_StandortstypHeute == "67" and hangneigung > 60:
            NAIS_StandortstypZukunft = "67"
        elif NAIS_StandortstypHeute == "69" and hangneigung > 60:
            NAIS_StandortstypZukunft = "69"
        elif NAIS_StandortstypHeute == "70" and hangneigung > 60:
            NAIS_StandortstypZukunft = "70"
        elif NAIS_StandortstypHeute == "71" and hangneigung > 60:
            NAIS_StandortstypZukunft = "71"
        elif NAIS_StandortstypHeute == "AV" and hangneigung > 60:
            NAIS_StandortstypZukunft = "AV"
    else:
        NAIS_StandortstypZukunft="NA"
    return NAIS_StandortstypZukunft
#standortsregion in ["J","M","1","2","2a","2b","3"], Projektionspfad von subalpin nach hochmontan im Tannen-Reliktareal
def Projektionspfad_regJM12a2b3_SA_HMTannenRelikt(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "subalpin" and hoehenstufe_zukunft=="hochmontan im Tannen-Reliktareal":
        if NAIS_StandortstypHeute=="57C":
            NAIS_StandortstypZukunft="55"
        elif NAIS_StandortstypHeute=="57CTa":
            NAIS_StandortstypZukunft="55"
        elif NAIS_StandortstypHeute=="57CLae":
            NAIS_StandortstypZukunft="55"
        elif NAIS_StandortstypHeute=="57VM":
            NAIS_StandortstypZukunft="51Re"
        elif NAIS_StandortstypHeute=="49*":
            NAIS_StandortstypZukunft="49*"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion in ["J","M","1","2","2a","2b","3"], Projektionspfad von subalpin nach hochmontan im Tannen-Nebenareal
def Projektionspfad_regJM12a2b3_SA_HMTannenNeben(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "subalpin" and hoehenstufe_zukunft=="hochmontan im Tannen-Nebenareal":
        if NAIS_StandortstypHeute == "57C":
            NAIS_StandortstypZukunft = "51"
        elif NAIS_StandortstypHeute == "57CTa":
            NAIS_StandortstypZukunft = "51"
        elif NAIS_StandortstypHeute == "57CLae":
            NAIS_StandortstypZukunft = "51"
        elif NAIS_StandortstypHeute == "57VM":
            NAIS_StandortstypZukunft = "51"
        elif NAIS_StandortstypHeute == "49*":
            NAIS_StandortstypZukunft = "49*Ta"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion in ["J","M","1","2","2a","2b","3"], Projektionspfad von subalpin nach hochmontan im Tannen-Hauptareal
def Projektionspfad_regJM12a2b3_SA_HMTannenHaupt(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "subalpin" and hoehenstufe_zukunft=="hochmontan im Tannen-Hauptareal":
        if NAIS_StandortstypHeute == "57VLae":
            NAIS_StandortstypZukunft = "46M"
        elif NAIS_StandortstypHeute == "57VLae" and bodenverdichtet == True:
            NAIS_StandortstypZukunft = "46"
        elif NAIS_StandortstypHeute == "57Bl":
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "57Bl" and schatten == True:
            NAIS_StandortstypZukunft = "57Bl"
        elif NAIS_StandortstypHeute == "57BlTa":
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "60":
            NAIS_StandortstypZukunft = "50"
        elif NAIS_StandortstypHeute == "60Ta":
            NAIS_StandortstypZukunft = "50"
        elif NAIS_StandortstypHeute == "60Lae":
            NAIS_StandortstypZukunft = "50"
        elif NAIS_StandortstypHeute == "58Bl":
            NAIS_StandortstypZukunft = "47H"
        elif NAIS_StandortstypHeute == "58Bl" and trocken == True and blockschutt == True:
            NAIS_StandortstypZukunft = "58Bl"
        elif NAIS_StandortstypHeute == "57VLae":
            NAIS_StandortstypZukunft = "46M"
        elif NAIS_StandortstypHeute == "57VLae" and bodenverdichtet == True:
            NAIS_StandortstypZukunft = "46"
        elif NAIS_StandortstypHeute == "67" and standortsregion in ["J", "M", "1"]:
            NAIS_StandortstypZukunft = "67"
        elif NAIS_StandortstypHeute == "67" and standortsregion in ["2", "2a", "2b", "3"]:
            NAIS_StandortstypZukunft = "65*"
        elif NAIS_StandortstypHeute == "69" and standortsregion in ["J", "M", "1"]:
            NAIS_StandortstypZukunft = "69"
        elif NAIS_StandortstypHeute == "69" and standortsregion in ["2", "2a", "2b", "3"]:
            NAIS_StandortstypZukunft = "65"
        elif NAIS_StandortstypHeute == "70" and standortsregion in ["J", "M", "1"]:
            NAIS_StandortstypZukunft = "70"
        elif NAIS_StandortstypHeute == "70" and standortsregion in ["2", "2a", "2b"]:
            NAIS_StandortstypZukunft = "68"
        elif NAIS_StandortstypHeute == "70" and standortsregion == "3":
            NAIS_StandortstypZukunft = "68*"
        elif NAIS_StandortstypHeute == "71":
            NAIS_StandortstypZukunft = "71"
        elif NAIS_StandortstypHeute == "AV":
            NAIS_StandortstypZukunft = "50"
        elif NAIS_StandortstypHeute == "23":
            NAIS_StandortstypZukunft = "23"
        elif NAIS_StandortstypHeute == "24*":
            NAIS_StandortstypZukunft = "24*"
        elif NAIS_StandortstypHeute == "27*":
            NAIS_StandortstypZukunft = "27*"
        elif NAIS_StandortstypHeute == "32S":
            NAIS_StandortstypZukunft = "32V"
        elif NAIS_StandortstypHeute == "71":
            NAIS_StandortstypZukunft = "71"
        elif NAIS_StandortstypHeute == "53" and standortsregion in ["M", "2a", "J", "1"]:
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "53" and standortsregion in ["2b", "3"]:
            NAIS_StandortstypZukunft = "53*"
        elif NAIS_StandortstypHeute == "53Ta":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "53Lae":
            NAIS_StandortstypZukunft = "53Lae"
        elif NAIS_StandortstypHeute == "53A":
            NAIS_StandortstypZukunft = "52"
        elif NAIS_StandortstypHeute == "53ATa":
            NAIS_StandortstypZukunft = "52"
        elif NAIS_StandortstypHeute == "57S":
            NAIS_StandortstypZukunft = "46*"
        elif NAIS_StandortstypHeute == "57STa":
            NAIS_StandortstypZukunft = "46*"
        elif NAIS_StandortstypHeute == "58":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "58Lae":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "58C":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "60A":
            NAIS_StandortstypZukunft = "50*"
        elif NAIS_StandortstypHeute == "60ATa":
            NAIS_StandortstypZukunft = "50*"
        elif NAIS_StandortstypHeute == "60ALae":
            NAIS_StandortstypZukunft = "50"
        elif NAIS_StandortstypHeute == "60E" and standortsregion in ["M", "2a", "J", "1"]:
            NAIS_StandortstypZukunft = "49"
        elif NAIS_StandortstypHeute == "60ETa" and standortsregion in ["M", "2a", "J", "1"]:
            NAIS_StandortstypZukunft = "49"
        elif NAIS_StandortstypHeute == "60E" and standortsregion in ["2b", "3"]:
            NAIS_StandortstypZukunft = "49*"
        elif NAIS_StandortstypHeute == "60ETa" and standortsregion in ["2b", "3"]:
            NAIS_StandortstypZukunft = "49*"
        elif NAIS_StandortstypHeute == "60*" and hangneigung > 70:
            NAIS_StandortstypZukunft = "60*Ta"
        elif NAIS_StandortstypHeute == "60*" and hangneigung <= 70:
            NAIS_StandortstypZukunft = "50*"
        elif NAIS_StandortstypHeute == "60*Lae" and hangneigung > 70:
            NAIS_StandortstypZukunft = "60*Lae"
        elif NAIS_StandortstypHeute == "60*Lae" and hangneigung <= 70:
            NAIS_StandortstypZukunft = "50*"
        elif NAIS_StandortstypHeute == "60*Ta" and hangneigung > 70:
            NAIS_StandortstypZukunft = "60*Ta"
        elif NAIS_StandortstypHeute == "60*ta" and hangneigung <= 70:
            NAIS_StandortstypZukunft = "50*"
        elif NAIS_StandortstypHeute == "72":
            NAIS_StandortstypZukunft = "57Bl"
        elif NAIS_StandortstypHeute == "72Lae":
            NAIS_StandortstypZukunft = "57Bl"
        elif NAIS_StandortstypHeute == "66PM":
            NAIS_StandortstypZukunft = "32V"
        elif NAIS_StandortstypHeute == "67*":
            NAIS_StandortstypZukunft = "65*"
    if hoehenstufe_heute == "subalpin" and hoehenstufe_zukunft == "hochmontan im Tannen-Hauptareal" and standortsregion in ["2b","3"]:
        if NAIS_StandortstypHeute == "55":
            NAIS_StandortstypZukunft = "55collin"
        elif NAIS_StandortstypHeute == "51":
            NAIS_StandortstypZukunft = "51collin"
        elif NAIS_StandortstypHeute == "46M":
            NAIS_StandortstypZukunft = "46Mcollin"
        elif NAIS_StandortstypHeute == "46":
            NAIS_StandortstypZukunft = "46collin"
        elif NAIS_StandortstypHeute == "48":
            NAIS_StandortstypZukunft = "48collin"
        elif NAIS_StandortstypHeute == "57Bl":
            NAIS_StandortstypZukunft = "48collin"
        elif NAIS_StandortstypHeute == "50":
            NAIS_StandortstypZukunft = "50collin"
        elif NAIS_StandortstypHeute == "47H":
            NAIS_StandortstypZukunft = "47Hcollin"
        elif NAIS_StandortstypHeute == "58Bl":
            NAIS_StandortstypZukunft = "47Hcollin"
        elif NAIS_StandortstypHeute == "53*":
            NAIS_StandortstypZukunft = "53*collin"
        elif NAIS_StandortstypHeute == "53*Ta":
            NAIS_StandortstypZukunft = "53*collin"
        elif NAIS_StandortstypHeute == "51Re":
            NAIS_StandortstypZukunft = "51collin"
        elif NAIS_StandortstypHeute == "55*":
            NAIS_StandortstypZukunft = "55*collin"
        elif NAIS_StandortstypHeute == "59R":
            NAIS_StandortstypZukunft = "47Hcollin"
        elif NAIS_StandortstypHeute == "65*":
            NAIS_StandortstypZukunft = "65*collin"
        elif NAIS_StandortstypHeute == "65":
            NAIS_StandortstypZukunft = "65collin"
        elif NAIS_StandortstypHeute == "68":
            NAIS_StandortstypZukunft = "68collin"
        elif NAIS_StandortstypHeute == "68*":
            NAIS_StandortstypZukunft = "68*collin"
        elif NAIS_StandortstypHeute == "71":
            NAIS_StandortstypZukunft = "45collin"
        elif NAIS_StandortstypHeute == "AV":
            NAIS_StandortstypZukunft = "50collin"
        elif NAIS_StandortstypHeute == "23":
            NAIS_StandortstypZukunft = "23collin"
        elif NAIS_StandortstypHeute == "24*":
            NAIS_StandortstypZukunft = "24*collin"
        elif NAIS_StandortstypHeute == "27*":
            NAIS_StandortstypZukunft = "27*collin"
        elif NAIS_StandortstypHeute == "32V":
            NAIS_StandortstypZukunft = "32Ccollin"
        elif NAIS_StandortstypHeute == "49*Ta":
            NAIS_StandortstypZukunft = "49*collin"
        elif NAIS_StandortstypHeute == "49*":
            NAIS_StandortstypZukunft = "49*collin"
        elif NAIS_StandortstypHeute == "53Ta":
            NAIS_StandortstypZukunft = "53collin"
        elif NAIS_StandortstypHeute == "53*":
            NAIS_StandortstypZukunft = "53*collin"
        elif NAIS_StandortstypHeute == "53*Ta":
            NAIS_StandortstypZukunft = "53*collin"
        elif NAIS_StandortstypHeute == "53Lae":
            NAIS_StandortstypZukunft = "53collin"
        elif NAIS_StandortstypHeute == "52":
            NAIS_StandortstypZukunft = "52collin"
        elif NAIS_StandortstypHeute == "46*":
            NAIS_StandortstypZukunft = "46*collin"
        elif NAIS_StandortstypHeute == "55*":
            NAIS_StandortstypZukunft = "55*collin"
        elif NAIS_StandortstypHeute == "50":
            NAIS_StandortstypZukunft = "50collin"
        elif NAIS_StandortstypHeute == "49":
            NAIS_StandortstypZukunft = "49collin"
        elif NAIS_StandortstypHeute == "49*":
            NAIS_StandortstypZukunft = "49*collin"
        elif NAIS_StandortstypHeute == "60*Ta":
            NAIS_StandortstypZukunft = "60*collin"
        elif NAIS_StandortstypHeute == "50*":
            NAIS_StandortstypZukunft = "50*collin"
        elif NAIS_StandortstypHeute == "60*Lae":
            NAIS_StandortstypZukunft = "60*collin"
        elif NAIS_StandortstypHeute == "57Bl":
            NAIS_StandortstypZukunft = "48collin"
        elif NAIS_StandortstypHeute == "32V":
            NAIS_StandortstypZukunft = "32Ccollin"
        elif NAIS_StandortstypHeute == "23H":
            NAIS_StandortstypZukunft = "23Hcollin"
        elif NAIS_StandortstypHeute == "26":
            NAIS_StandortstypZukunft = "26collin"
        elif NAIS_StandortstypHeute == "26w":
            NAIS_StandortstypZukunft = "26wcollin"
        elif NAIS_StandortstypHeute == "32*":
            NAIS_StandortstypZukunft = "32*collin"
        elif NAIS_StandortstypHeute == "33V":
            NAIS_StandortstypZukunft = "33Vcollin"
        elif NAIS_StandortstypHeute == "24":
            NAIS_StandortstypZukunft = "24collin"
        elif NAIS_StandortstypHeute == "40PBl":
            NAIS_StandortstypZukunft = "40PBlcollin"
        elif NAIS_StandortstypHeute == "40P":
            NAIS_StandortstypZukunft = "40Pcollin"
        elif NAIS_StandortstypHeute == "46Re":
            NAIS_StandortstypZukunft = "46collin"
        elif NAIS_StandortstypHeute == "46MRe":
            NAIS_StandortstypZukunft = "46Mcollin"
        elif NAIS_StandortstypHeute == "46*Re":
            NAIS_StandortstypZukunft = "46*collin"
        elif NAIS_StandortstypHeute == "47":
            NAIS_StandortstypZukunft = "55collin"
        elif NAIS_StandortstypHeute == "50Re":
            NAIS_StandortstypZukunft = "50collin"
        elif NAIS_StandortstypHeute == "50P":
            NAIS_StandortstypZukunft = "50Pcollin"
        elif NAIS_StandortstypHeute == "50*re":
            NAIS_StandortstypZukunft = "50*collin"
        elif NAIS_StandortstypHeute == "51C":
            NAIS_StandortstypZukunft = "51collin"
        elif NAIS_StandortstypHeute == "52Re":
            NAIS_StandortstypZukunft = "52collin"
        elif NAIS_StandortstypHeute == "52T":
            NAIS_StandortstypZukunft = "52collin"
        elif NAIS_StandortstypHeute == "54":
            NAIS_StandortstypZukunft = "54collin"
        elif NAIS_StandortstypHeute == "54A":
            NAIS_StandortstypZukunft = "54Acollin"
        elif NAIS_StandortstypHeute == "56":
            NAIS_StandortstypZukunft = "45collin"
        elif NAIS_StandortstypHeute == "66":
            NAIS_StandortstypZukunft = "66collin"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion in ["J","M","1","2","2a","2b","3"], Projektionspfad von hochmontan nach obermontan
def Projektionspfad_regJM12a2b3_HM_OM(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute in ["hochmontan", "hochmontan im Tannen-Hauptareal","hochmontan im Tannen-Nebenareal","hochmontan im Tannen-Reliktareal"] and hoehenstufe_zukunft=="obermontan":
        NAIS_StandortstypZukunft = "NA"
        if NAIS_StandortstypHeute == "55":
            NAIS_StandortstypZukunft = "19"
        elif NAIS_StandortstypHeute == "51" and kuppenlage == True:
            NAIS_StandortstypZukunft = "19"
        elif NAIS_StandortstypHeute == "51" and hanglage==True:
            NAIS_StandortstypZukunft = "18"
        elif NAIS_StandortstypHeute == "46M" and muldenlage==True:
            NAIS_StandortstypZukunft = "1h"
        elif NAIS_StandortstypHeute == "46" and hangneigung<=20:
            NAIS_StandortstypZukunft = "46"
        elif NAIS_StandortstypHeute == "46" and hangneigung > 20:
            NAIS_StandortstypZukunft = "19"
        elif NAIS_StandortstypHeute == "51" and hanglage==True:
            NAIS_StandortstypZukunft = "18"
        elif NAIS_StandortstypHeute == "51" and muldenlage==True:
            NAIS_StandortstypZukunft = "18"
        elif NAIS_StandortstypHeute == "48" and schatten==False:
            NAIS_StandortstypZukunft = "22"
        elif NAIS_StandortstypHeute == "48" and schatten==True:
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "57Bl" and schatten==False:
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "57Bl" and schatten==True:
            NAIS_StandortstypZukunft = "57Bl"
        elif NAIS_StandortstypHeute == "50":
            NAIS_StandortstypZukunft = "20"
        elif NAIS_StandortstypHeute == "47H":
            NAIS_StandortstypZukunft = "k.A."
        elif NAIS_StandortstypHeute == "58Bl":
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "53*":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "53*Ta":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "51" and kuppenlage==True:
            NAIS_StandortstypZukunft = "19"
        elif NAIS_StandortstypHeute == "51" and hanglage==True:
            NAIS_StandortstypZukunft = "18"
        elif NAIS_StandortstypHeute == "51" and muldenlage==True:
            NAIS_StandortstypZukunft = "18"
        elif NAIS_StandortstypHeute == "51Re" and kuppenlage==True:
            NAIS_StandortstypZukunft = "19"
        elif NAIS_StandortstypHeute == "51Re" and hanglage==True:
            NAIS_StandortstypZukunft = "18"
        elif NAIS_StandortstypHeute == "51Re" and muldenlage==True:
            NAIS_StandortstypZukunft = "18"
        elif NAIS_StandortstypHeute == "55*":
            NAIS_StandortstypZukunft = "1h"
        elif NAIS_StandortstypHeute == "59R":
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "51" and kuppenlage==True:
            NAIS_StandortstypZukunft = "19"
        elif NAIS_StandortstypHeute == "51" and hanglage==True:
            NAIS_StandortstypZukunft = "18"
        elif NAIS_StandortstypHeute == "51" and muldenlage==True:
            NAIS_StandortstypZukunft = "18"
        elif NAIS_StandortstypHeute == "46M":
            NAIS_StandortstypZukunft = "1h"
        elif NAIS_StandortstypHeute == "46" and hangneigung<=20:
            NAIS_StandortstypZukunft = "46"
        elif NAIS_StandortstypHeute == "46" and hangneigung>20:
            NAIS_StandortstypZukunft = "19"
        elif NAIS_StandortstypHeute == "67":
            NAIS_StandortstypZukunft = "65"
        elif NAIS_StandortstypHeute == "65*":
            NAIS_StandortstypZukunft = "65*"
        elif NAIS_StandortstypHeute == "69":
            NAIS_StandortstypZukunft = "65"
        elif NAIS_StandortstypHeute == "65":
            NAIS_StandortstypZukunft = "65"
        elif NAIS_StandortstypHeute == "70":
            NAIS_StandortstypZukunft = "68"
        elif NAIS_StandortstypHeute == "68":
            NAIS_StandortstypZukunft = "68"
        elif NAIS_StandortstypHeute == "68*":
            NAIS_StandortstypZukunft = "68"
        elif NAIS_StandortstypHeute == "71":
            NAIS_StandortstypZukunft = "71"
        elif NAIS_StandortstypHeute == "50":
            NAIS_StandortstypZukunft = "20"
        elif NAIS_StandortstypHeute == "AV":
            NAIS_StandortstypZukunft = "20"
        elif NAIS_StandortstypHeute == "23":
            NAIS_StandortstypZukunft = "23"
        elif NAIS_StandortstypHeute == "24*":
            NAIS_StandortstypZukunft = "24*"
        elif NAIS_StandortstypHeute == "27*" and hangneigung <=20:
            NAIS_StandortstypZukunft = "27h"
        elif NAIS_StandortstypHeute == "27*" and hangneigung >20:
            NAIS_StandortstypZukunft = "26h"
        elif NAIS_StandortstypHeute == "32V":
            NAIS_StandortstypZukunft = "32V"
        elif NAIS_StandortstypHeute == "49*Ta" and hangneigung <=20:
            NAIS_StandortstypZukunft = "27h"
        elif NAIS_StandortstypHeute == "49*Ta" and hangneigung >20:
            NAIS_StandortstypZukunft = "26h"
        elif NAIS_StandortstypHeute == "49*" and hangneigung >20:
            NAIS_StandortstypZukunft = "26h"
        elif NAIS_StandortstypHeute == "49*" and hangneigung <=20:
            NAIS_StandortstypZukunft = "27h"
        elif NAIS_StandortstypHeute == "53Ta":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "53*":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "53*Ta":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "53Lae":
            NAIS_StandortstypZukunft = "53Lae"
        elif NAIS_StandortstypHeute == "52":
            NAIS_StandortstypZukunft = "18*"
        elif NAIS_StandortstypHeute == "46*" and hangneigung <=20:
            NAIS_StandortstypZukunft = "46*"
        elif NAIS_StandortstypHeute == "46*" and hangneigung >20:
            NAIS_StandortstypZukunft = "46"
        elif NAIS_StandortstypHeute == "55*":
            NAIS_StandortstypZukunft = "1h"
        elif NAIS_StandortstypHeute == "55*Ta":
            NAIS_StandortstypZukunft = "1h"
        elif NAIS_StandortstypHeute == "50":
            NAIS_StandortstypZukunft = "20"
        elif NAIS_StandortstypHeute == "49" and hangneigung<=20:
            NAIS_StandortstypZukunft = "49"
        elif NAIS_StandortstypHeute == "49" and hangneigung>20:
            NAIS_StandortstypZukunft = "19f"
        elif NAIS_StandortstypHeute == "49*" and hangneigung<=20:
            NAIS_StandortstypZukunft = "27h"
        elif NAIS_StandortstypHeute == "49*" and hangneigung>20:
            NAIS_StandortstypZukunft = "26h"
        elif NAIS_StandortstypHeute == "60*Ta" and schatten==False:
            NAIS_StandortstypZukunft = "18w"
        elif NAIS_StandortstypHeute == "60*Ta" and schatten==True:
            NAIS_StandortstypZukunft = "18v"
        elif NAIS_StandortstypHeute == "50*":
            NAIS_StandortstypZukunft = "18M"
        elif NAIS_StandortstypHeute == "60*Lae" and schatten==False:
            NAIS_StandortstypZukunft = "18w"
        elif NAIS_StandortstypHeute == "60*Lae" and schatten==True:
            NAIS_StandortstypZukunft = "18v"
        elif NAIS_StandortstypHeute == "60*Ta" and schatten==False:
            NAIS_StandortstypZukunft = "18w"
        elif NAIS_StandortstypHeute == "60*Ta" and schatten==True:
            NAIS_StandortstypZukunft = "18v"
        elif NAIS_StandortstypHeute == "32V":
            NAIS_StandortstypZukunft = "32V"
        elif NAIS_StandortstypHeute == "21":
            NAIS_StandortstypZukunft = "20"
        elif NAIS_StandortstypHeute == "23H":
            NAIS_StandortstypZukunft = "20"
        elif NAIS_StandortstypHeute == "26":
            NAIS_StandortstypZukunft = "26h"
        elif NAIS_StandortstypHeute == "26w":
            NAIS_StandortstypZukunft = "26w"
        elif NAIS_StandortstypHeute == "32C":
            NAIS_StandortstypZukunft = "32V"
        elif NAIS_StandortstypHeute == "32*":
            NAIS_StandortstypZukunft = "32*"
        elif NAIS_StandortstypHeute == "33V":
            NAIS_StandortstypZukunft = "k.A."
        elif NAIS_StandortstypHeute == "24":
            NAIS_StandortstypZukunft = "24"
        elif NAIS_StandortstypHeute == "46Re" and hangneigung <=20:
            NAIS_StandortstypZukunft = "46"
        elif NAIS_StandortstypHeute == "46Re" and hangneigung >20:
            NAIS_StandortstypZukunft = "19"
        elif NAIS_StandortstypHeute == "46MRe":
            NAIS_StandortstypZukunft = "1h"
        elif NAIS_StandortstypHeute == "46*Re" and hangneigung <=20:
            NAIS_StandortstypZukunft = "46*"
        elif NAIS_StandortstypHeute == "46*Re" and hangneigung>20:
            NAIS_StandortstypZukunft = "46"
        elif NAIS_StandortstypHeute == "47":
            NAIS_StandortstypZukunft = "19"
        elif NAIS_StandortstypHeute == "50Re":
            NAIS_StandortstypZukunft = "20"
        elif NAIS_StandortstypHeute == "50P":
            NAIS_StandortstypZukunft = "20"
        elif NAIS_StandortstypHeute == "50*Re":
            NAIS_StandortstypZukunft = "18M"
        elif NAIS_StandortstypHeute == "51C" and kuppenlage==True:
            NAIS_StandortstypZukunft = "19"
        elif NAIS_StandortstypHeute == "51C" and hanglage == True:
            NAIS_StandortstypZukunft = "18"
        elif NAIS_StandortstypHeute == "51C" and muldenlage == True:
            NAIS_StandortstypZukunft = "18"
        elif NAIS_StandortstypHeute == "52Re":
            NAIS_StandortstypZukunft = "18*"
        elif NAIS_StandortstypHeute == "52T":
            NAIS_StandortstypZukunft = "18*"
        elif NAIS_StandortstypHeute == "54":
            NAIS_StandortstypZukunft = "18*"
        elif NAIS_StandortstypHeute == "54A":
            NAIS_StandortstypZukunft = "18"
        elif NAIS_StandortstypHeute == "56":
            NAIS_StandortstypZukunft = "56"
        elif NAIS_StandortstypHeute == "66":
            NAIS_StandortstypZukunft = "k.A."
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion in ["J","M","1","2","2a","2b","3"], Projektionspfad von collin nach collin
def Projektionspfad_regJM12a2b3_CO_CO(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "collin" and hoehenstufe_zukunft=="collin" and standortsregion in ["R","J","1","2","2a","2b"]:
        if NAIS_StandortstypHeute == "25A":
            NAIS_StandortstypZukunft = "23Hcollin"
        elif NAIS_StandortstypHeute == "25Q":
            NAIS_StandortstypZukunft = "52collin"
        elif NAIS_StandortstypHeute == "35":
            NAIS_StandortstypZukunft = "15collin"
        elif NAIS_StandortstypHeute == "35A":
            NAIS_StandortstypZukunft = "7acollin"
        elif NAIS_StandortstypHeute == "35M":
            NAIS_StandortstypZukunft = "17collin"
        elif NAIS_StandortstypHeute == "38S":
            NAIS_StandortstypZukunft = "65*collin"
        elif NAIS_StandortstypHeute == "40*":
            NAIS_StandortstypZukunft = "40*collin"
    #elif standortsregion=="3"
        #NAIS_StandortstypZukunft =NAIS_StandortstypHeute #stimmt das?
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion in ["J","M","1","2","2a","2b","3"], Projektionspfad von obermontan nach untermontan
def Projektionspfad_regJM12a2b3_OM_UM(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "obermontan" and hoehenstufe_zukunft=="untermontan":
        if NAIS_StandortstypHeute == "19":
            NAIS_StandortstypZukunft = "8d"
        elif NAIS_StandortstypHeute == "18":
            NAIS_StandortstypZukunft = "8a"
        elif NAIS_StandortstypHeute == "1h":
            NAIS_StandortstypZukunft = "1"
        elif NAIS_StandortstypHeute == "46":
            NAIS_StandortstypZukunft = "8*"
        elif NAIS_StandortstypHeute == "18":
            NAIS_StandortstypZukunft = "8a"
        elif NAIS_StandortstypHeute == "22":
            NAIS_StandortstypZukunft = "22"
        elif NAIS_StandortstypHeute == "48":
            NAIS_StandortstypZukunft = "22"
        elif NAIS_StandortstypHeute == "57Bl":
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "22":
            NAIS_StandortstypZukunft = "22"
        elif NAIS_StandortstypHeute == "20":
            NAIS_StandortstypZukunft = "8S"
        elif NAIS_StandortstypHeute == "53Ta":
            NAIS_StandortstypZukunft = "62"
        elif NAIS_StandortstypHeute == "46":
            NAIS_StandortstypZukunft = "8*"
        elif NAIS_StandortstypHeute == "65":
            NAIS_StandortstypZukunft = "65"
        elif NAIS_StandortstypHeute == "65*" and standortsregion in ["J", "M", "1"]:
            NAIS_StandortstypZukunft = "65"
        elif NAIS_StandortstypHeute == "65*" and standortsregion in ["2", "2a", "2b"]:
            NAIS_StandortstypZukunft = "65*"
        elif NAIS_StandortstypHeute == "68" and strahlungsreich == False:
            NAIS_StandortstypZukunft = "68"
        elif NAIS_StandortstypHeute == "68" and strahlungsreich == True:
            NAIS_StandortstypZukunft = "41*"
        elif NAIS_StandortstypHeute == "71":
            NAIS_StandortstypZukunft = "45"
        elif NAIS_StandortstypHeute == "20":
            NAIS_StandortstypZukunft = "8S"
        elif NAIS_StandortstypHeute == "23":
            NAIS_StandortstypZukunft = "25*"
        elif NAIS_StandortstypHeute == "24*":
            NAIS_StandortstypZukunft = "25F"
        elif NAIS_StandortstypHeute == "27h":
            NAIS_StandortstypZukunft = "27"
        elif NAIS_StandortstypHeute == "26h":
            NAIS_StandortstypZukunft = "26"
        elif NAIS_StandortstypHeute == "32V":
            NAIS_StandortstypZukunft = "28"  # hier muesste man noch ueberschwemmung mit einbauen
        elif NAIS_StandortstypHeute == "53Lae":
            NAIS_StandortstypZukunft = "62"
        elif NAIS_StandortstypHeute == "18*" and hanglage == True:
            NAIS_StandortstypZukunft = "14"
        elif NAIS_StandortstypHeute == "18*" and muldenlage == True:
            NAIS_StandortstypZukunft = "14"
        elif NAIS_StandortstypHeute == "18*" and kuppenlage == True:
            NAIS_StandortstypZukunft = "15"
        elif NAIS_StandortstypHeute == "46*":
            NAIS_StandortstypZukunft = "46t"
        elif NAIS_StandortstypHeute == "53Lae":
            NAIS_StandortstypZukunft = "62"
        elif NAIS_StandortstypHeute == "49":
            NAIS_StandortstypZukunft = "27"
        elif NAIS_StandortstypHeute == "19f":
            NAIS_StandortstypZukunft = "8b"
        elif NAIS_StandortstypHeute == "18w":
            NAIS_StandortstypZukunft = "17"
        elif NAIS_StandortstypHeute == "18v":
            NAIS_StandortstypZukunft = "17"
        elif NAIS_StandortstypHeute == "18M":
            NAIS_StandortstypZukunft = "12a"
        elif NAIS_StandortstypHeute == "26w":
            NAIS_StandortstypZukunft = "26"
        elif NAIS_StandortstypHeute == "24":
            NAIS_StandortstypZukunft = "25"
        elif NAIS_StandortstypHeute == "46*":
            NAIS_StandortstypZukunft = "46t"
        elif NAIS_StandortstypHeute == "18*" and hanglage == True:
            NAIS_StandortstypZukunft = "14"
        elif NAIS_StandortstypHeute == "18*" and muldenlage == True:
            NAIS_StandortstypZukunft = "14"
        elif NAIS_StandortstypHeute == "18*" and kuppenlage == True:
            NAIS_StandortstypZukunft = "15"
        elif NAIS_StandortstypHeute == "56":
            NAIS_StandortstypZukunft = "45"
        elif NAIS_StandortstypHeute == "20E":
            NAIS_StandortstypZukunft = "8S"
        elif NAIS_StandortstypHeute == "29h":
            NAIS_StandortstypZukunft = "29"
        elif NAIS_StandortstypHeute == "13h":
            NAIS_StandortstypZukunft = "13a"
        elif NAIS_StandortstypHeute == "13eh":
            NAIS_StandortstypZukunft = "13e"
        elif NAIS_StandortstypHeute == "61":
            NAIS_StandortstypZukunft = "61"
        elif NAIS_StandortstypHeute == "22A":
            NAIS_StandortstypZukunft = "22A"
        elif NAIS_StandortstypHeute == "29A":
            NAIS_StandortstypZukunft = "29A"
        elif NAIS_StandortstypHeute == "19a" and standortsregion == "2a" and VS == True:  # sollte nur fuer Wallis gelten
            NAIS_StandortstypZukunft = "3"
        elif NAIS_StandortstypHeute == "19a" and standortsregion == "2a" and schatten == True and VS == True:  # Wallis: hier muesste noch tiefgruendiger Boden rein
            NAIS_StandortstypZukunft = "4"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion in ["J","M","1","2","2a","2b","3"], Projektionspfad von untermontan nach submontan
def Projektionspfad_regJM12a2b3_UM_SM(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "untermontan" and hoehenstufe_zukunft=="submontan":
        if NAIS_StandortstypHeute == "1":
            NAIS_StandortstypZukunft = "1"
        elif NAIS_StandortstypHeute == "2":
            NAIS_StandortstypZukunft = "2"
        elif NAIS_StandortstypHeute == "3":
            NAIS_StandortstypZukunft = "3"
        elif NAIS_StandortstypHeute == "4":
            NAIS_StandortstypZukunft = "4"
        elif NAIS_StandortstypHeute == "14":
            NAIS_StandortstypZukunft = "14"
        elif NAIS_StandortstypHeute == "15":
            NAIS_StandortstypZukunft = "15"
        elif NAIS_StandortstypHeute == "16" and SH == True:
            NAIS_StandortstypZukunft = "39"
        elif NAIS_StandortstypHeute == "16" and SH == False and standortsregion in ["J", "M"]:
            NAIS_StandortstypZukunft = "39"
        elif NAIS_StandortstypHeute == "16" and standortsregion in ["1", "2", "3"]:
            NAIS_StandortstypZukunft = "40*"
        elif NAIS_StandortstypHeute == "17":
            NAIS_StandortstypZukunft = "17"
        elif NAIS_StandortstypHeute == "22":
            NAIS_StandortstypZukunft = "22"
        elif NAIS_StandortstypHeute == "25":
            NAIS_StandortstypZukunft = "25"
        elif NAIS_StandortstypHeute == "26":
            NAIS_StandortstypZukunft = "26"
        elif NAIS_StandortstypHeute == "27":
            NAIS_StandortstypZukunft = "27"
        elif NAIS_StandortstypHeute == "28":
            NAIS_StandortstypZukunft = "28"
        elif NAIS_StandortstypHeute == "29":
            NAIS_StandortstypZukunft = "29"
        elif NAIS_StandortstypHeute == "30":
            NAIS_StandortstypZukunft = "30"
        elif NAIS_StandortstypHeute == "39":
            NAIS_StandortstypZukunft = "39"
        elif NAIS_StandortstypHeute == "43":
            NAIS_StandortstypZukunft = "43"
        elif NAIS_StandortstypHeute == "44":
            NAIS_StandortstypZukunft = "44"
        elif NAIS_StandortstypHeute == "45":
            NAIS_StandortstypZukunft = "45"
        elif NAIS_StandortstypHeute == "48":
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "61":
            NAIS_StandortstypZukunft = "61"
        elif NAIS_StandortstypHeute == "62":
            NAIS_StandortstypZukunft = "62"
        elif NAIS_StandortstypHeute == "65" and standortsregion in ["J", "M"]:
            NAIS_StandortstypZukunft = "38"
        elif NAIS_StandortstypHeute == "65" and standortsregion in ["1", "2", "3"]:
            NAIS_StandortstypZukunft = "40*"
        elif NAIS_StandortstypHeute == "68" and schatten == False:
            NAIS_StandortstypZukunft = "41*"
        elif NAIS_StandortstypHeute == "68" and schatten == True:
            NAIS_StandortstypZukunft = "68"
        elif NAIS_StandortstypHeute == "12a":
            NAIS_StandortstypZukunft = "9a"
        elif NAIS_StandortstypHeute == "12e":
            NAIS_StandortstypZukunft = "10a"
        elif NAIS_StandortstypHeute == "12S":
            NAIS_StandortstypZukunft = "11"
        elif NAIS_StandortstypHeute == "12w":
            NAIS_StandortstypZukunft = "10w"
        elif NAIS_StandortstypHeute == "13a":
            NAIS_StandortstypZukunft = "13a"
        elif NAIS_StandortstypHeute == "13e":
            NAIS_StandortstypZukunft = "13e"
        elif NAIS_StandortstypHeute == "22A":
            NAIS_StandortstypZukunft = "22C"
        elif NAIS_StandortstypHeute == "22C":
            NAIS_StandortstypZukunft = "22C"
        elif NAIS_StandortstypHeute == "25*":
            NAIS_StandortstypZukunft = "25*"
        elif NAIS_StandortstypHeute == "25F":
            NAIS_StandortstypZukunft = "25F"
        elif NAIS_StandortstypHeute == "29A":
            NAIS_StandortstypZukunft = "29A"
        elif NAIS_StandortstypHeute == "29C":
            NAIS_StandortstypZukunft = "29C"
        elif NAIS_StandortstypHeute == "32C":  # hier sollte noch ueberschwemmung rein
            NAIS_StandortstypZukunft = "32C"
        elif NAIS_StandortstypHeute == "34*":
            NAIS_StandortstypZukunft = "34*"
        elif NAIS_StandortstypHeute == "39*":
            NAIS_StandortstypZukunft = "39*"
        elif NAIS_StandortstypHeute == "40*":
            NAIS_StandortstypZukunft = "40*"
        elif NAIS_StandortstypHeute == "41*":
            NAIS_StandortstypZukunft = "41*"
        elif NAIS_StandortstypHeute == "43S":
            NAIS_StandortstypZukunft = "43S"
        elif NAIS_StandortstypHeute == "46t":
            NAIS_StandortstypZukunft = "7*"
        elif NAIS_StandortstypHeute == "65*":
            NAIS_StandortstypZukunft = "65*"
        elif NAIS_StandortstypHeute == "8*":
            NAIS_StandortstypZukunft = "7*"
        elif NAIS_StandortstypHeute == "8a":
            NAIS_StandortstypZukunft = "7a"
        elif NAIS_StandortstypHeute == "8b":
            NAIS_StandortstypZukunft = "7b"
        elif NAIS_StandortstypHeute == "8d":
            NAIS_StandortstypZukunft = "6"
        elif NAIS_StandortstypHeute == "8S":
            NAIS_StandortstypZukunft = "7S"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion in ["J","M","1","2","2a","2b","3"], Projektionspfad von submontan nach collin
def Projektionspfad_regJM12a2b3_SM_CO(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung): #noch zu ergaenzen
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "submontan" and hoehenstufe_zukunft == "collin" and standortsregion in ["J", "M", "1", "2a"]:
        if NAIS_StandortstypHeute == "1":
            NAIS_StandortstypZukunft = "1collin"
        elif NAIS_StandortstypHeute == "2":
            NAIS_StandortstypZukunft = "2collin"
        elif NAIS_StandortstypHeute == "3":
            NAIS_StandortstypZukunft = "1collin"
        elif NAIS_StandortstypHeute == "4":
            NAIS_StandortstypZukunft = "6collin"
        elif NAIS_StandortstypHeute == "6":
            NAIS_StandortstypZukunft = "6collin"
        elif NAIS_StandortstypHeute == "11":
            NAIS_StandortstypZukunft = "11collin"
        elif NAIS_StandortstypHeute == "14":
            NAIS_StandortstypZukunft = "14collin"
        elif NAIS_StandortstypHeute == "15":
            NAIS_StandortstypZukunft = "15collin"
        elif NAIS_StandortstypHeute == "17":
            NAIS_StandortstypZukunft = "17collin"
        elif NAIS_StandortstypHeute == "22":
            NAIS_StandortstypZukunft = "22collin"
        elif NAIS_StandortstypHeute == "25":
            NAIS_StandortstypZukunft = "25collin"
        elif NAIS_StandortstypHeute == "26":
            NAIS_StandortstypZukunft = "26collin"
        elif NAIS_StandortstypHeute == "27":
            NAIS_StandortstypZukunft = "27collin"
        elif NAIS_StandortstypHeute == "28":
            NAIS_StandortstypZukunft = "28collin"
        elif NAIS_StandortstypHeute == "29":
            NAIS_StandortstypZukunft = "29collin"
        elif NAIS_StandortstypHeute == "30":
            NAIS_StandortstypZukunft = "30collin"
        elif NAIS_StandortstypHeute == "31":
            NAIS_StandortstypZukunft = "31collin"
        elif NAIS_StandortstypHeute == "38":
            NAIS_StandortstypZukunft = "38collin"
        elif NAIS_StandortstypHeute == "39":
            NAIS_StandortstypZukunft = "39collin"
        elif NAIS_StandortstypHeute == "41":
            NAIS_StandortstypZukunft = "41collin"
        elif NAIS_StandortstypHeute == "43":
            NAIS_StandortstypZukunft = "43collin"
        elif NAIS_StandortstypHeute == "44":
            NAIS_StandortstypZukunft = "44collin"
        elif NAIS_StandortstypHeute == "45":
            NAIS_StandortstypZukunft = "45collin"
        elif NAIS_StandortstypHeute == "61":
            NAIS_StandortstypZukunft = "61collin"
        elif NAIS_StandortstypHeute == "62":
            NAIS_StandortstypZukunft = "62collin"
        elif NAIS_StandortstypHeute == "66":
            NAIS_StandortstypZukunft = "66collin"
        elif NAIS_StandortstypHeute == "68":
            NAIS_StandortstypZukunft = "41*collin"
        elif NAIS_StandortstypHeute == "10a":
            NAIS_StandortstypZukunft = "10acollin"
        elif NAIS_StandortstypHeute == "10w":
            NAIS_StandortstypZukunft = "10wcollin"
        elif NAIS_StandortstypHeute == "13a":
            NAIS_StandortstypZukunft = "13acollin"
        elif NAIS_StandortstypHeute == "13e":
            NAIS_StandortstypZukunft = "13ecollin"
        elif NAIS_StandortstypHeute == "22C":
            NAIS_StandortstypZukunft = "22Ccollin"
        elif NAIS_StandortstypHeute == "25*":
            NAIS_StandortstypZukunft = "25*collin"
        elif NAIS_StandortstypHeute == "25e":
            NAIS_StandortstypZukunft = "25ecollin"
        elif NAIS_StandortstypHeute == "25F":
            NAIS_StandortstypZukunft = "25Fcollin"
        elif NAIS_StandortstypHeute == "29A":
            NAIS_StandortstypZukunft = "29Acollin"
        elif NAIS_StandortstypHeute == "32C":
            NAIS_StandortstypZukunft = "32Ccollin"
        elif NAIS_StandortstypHeute == "34*":
            NAIS_StandortstypZukunft = "34*collin"
        elif NAIS_StandortstypHeute == "39*":
            NAIS_StandortstypZukunft = "39*collin"
        elif NAIS_StandortstypHeute == "40*":
            NAIS_StandortstypZukunft = "40*collin"
        elif NAIS_StandortstypHeute == "41*":
            NAIS_StandortstypZukunft = "41*collin"
        elif NAIS_StandortstypHeute == "43S":
            NAIS_StandortstypZukunft = "43Scollin"
        elif NAIS_StandortstypHeute == "65*":
            NAIS_StandortstypZukunft = "65*collin"
        elif NAIS_StandortstypHeute == "7*":
            NAIS_StandortstypZukunft = "7*collin"
        elif NAIS_StandortstypHeute == "7a":
            NAIS_StandortstypZukunft = "7acollin"
        elif NAIS_StandortstypHeute == "7b":
            NAIS_StandortstypZukunft = "7bcollin"
        elif NAIS_StandortstypHeute == "7S":
            NAIS_StandortstypZukunft = "7Scollin"
        elif NAIS_StandortstypHeute == "9a":
            NAIS_StandortstypZukunft = "9acollin"
        elif NAIS_StandortstypHeute == "46t":
            NAIS_StandortstypZukunft = "7*collin"
    elif hoehenstufe_heute == "submontan" and hoehenstufe_zukunft == "collin" and standortsregion in ["2b","3"]:
        if NAIS_StandortstypHeute == "6":
            NAIS_StandortstypZukunft = "55collin"
        elif NAIS_StandortstypHeute == "7a":
            NAIS_StandortstypZukunft = "51collin"
        elif NAIS_StandortstypHeute == "1":
            NAIS_StandortstypZukunft = "46Mcollin"
        elif NAIS_StandortstypHeute == "7*":
            NAIS_StandortstypZukunft = "46collin"
        elif NAIS_StandortstypHeute == "22":
            NAIS_StandortstypZukunft = "48collin"
        elif NAIS_StandortstypHeute == "7S":
            NAIS_StandortstypZukunft = "50collin"
        elif NAIS_StandortstypHeute == "34*":
            NAIS_StandortstypZukunft = "47Hcollin"
        elif NAIS_StandortstypHeute == "62":
            NAIS_StandortstypZukunft = "53*collin"
        elif NAIS_StandortstypHeute == "38":
            NAIS_StandortstypZukunft = "65*collin"
        elif NAIS_StandortstypHeute == "41*":
            NAIS_StandortstypZukunft = "68collin"
        elif NAIS_StandortstypHeute == "45":
            NAIS_StandortstypZukunft = "45collin"
        elif NAIS_StandortstypHeute == "25*":
            NAIS_StandortstypZukunft = "23collin"
        elif NAIS_StandortstypHeute == "25F":
            NAIS_StandortstypZukunft = "24*collin"
        elif NAIS_StandortstypHeute == "27":
            NAIS_StandortstypZukunft = "27*collin"
        elif NAIS_StandortstypHeute == "26":
            NAIS_StandortstypZukunft = "27*collin"
        elif NAIS_StandortstypHeute == "28":
            NAIS_StandortstypZukunft = "32Ccollin"
        elif NAIS_StandortstypHeute == "14":
            NAIS_StandortstypZukunft = "52collin"
        elif NAIS_StandortstypHeute == "7b":
            NAIS_StandortstypZukunft = "49collin"
        elif NAIS_StandortstypHeute == "9a":
            NAIS_StandortstypZukunft = "50*collin"
        elif NAIS_StandortstypHeute == "17":
            NAIS_StandortstypZukunft = "60*collin"
        elif NAIS_StandortstypHeute == "25":
            NAIS_StandortstypZukunft = "24collin"
        elif NAIS_StandortstypHeute == "66":
            NAIS_StandortstypZukunft = "66collin"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion "4", Projektionspfad von obersubalpin nach subalpin
def Projektionspfad_reg4_OSA_SA(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "obersubalpin" and hoehenstufe_zukunft == "subalpin":
        if NAIS_StandortstypHeute == "59" and hangneigung > 60 and blockschutt == False:
            NAIS_StandortstypZukunft = "57C"
        elif NAIS_StandortstypHeute == "59" and hangneigung <= 60 and blockschutt == False:
            NAIS_StandortstypZukunft = "57V"
        elif NAIS_StandortstypHeute == "59" and hangneigung > 60 and blockschutt == True:
            NAIS_StandortstypZukunft = "57Bl"
        elif NAIS_StandortstypHeute == "59" and hangneigung <= 60 and blockschutt == True:
            NAIS_StandortstypZukunft = "57Bl"
        elif NAIS_StandortstypHeute == "59A":
            NAIS_StandortstypZukunft = "60A"
        elif NAIS_StandortstypHeute == "59A" and schatten == True:
            NAIS_StandortstypZukunft = "59A"
        elif NAIS_StandortstypHeute == "59J":
            NAIS_StandortstypZukunft = "58L"
        elif NAIS_StandortstypHeute == "59J" and schatten == True:
            NAIS_StandortstypZukunft = "59J"
        elif NAIS_StandortstypHeute == "59R":
            NAIS_StandortstypZukunft = "59R"
        elif NAIS_StandortstypHeute == "59S":
            NAIS_StandortstypZukunft = "59S"
        elif NAIS_StandortstypHeute == "59*":
            NAIS_StandortstypZukunft = "47*"
        elif NAIS_StandortstypHeute == "59*" and schatten == True:
            NAIS_StandortstypZukunft = "59*"
        elif NAIS_StandortstypHeute == "67":
            NAIS_StandortstypZukunft = "67"
        elif NAIS_StandortstypHeute == "69":
            NAIS_StandortstypZukunft = "69"
        elif NAIS_StandortstypHeute == "70":
            NAIS_StandortstypZukunft = "70"
        elif NAIS_StandortstypHeute == "71":
            NAIS_StandortstypZukunft = "71"
        elif NAIS_StandortstypHeute == "AV":
            NAIS_StandortstypZukunft = "60"  #hier muessten noch Lawinen rein (24*)
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion "4", Projektionspfad von subalpin nach hochmontan im Tannen-Reliktareal"
def Projektionspfad_reg4_SA_HMTannenRelikt(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "subalpin" and hoehenstufe_zukunft =="hochmontan im Tannen-Reliktareal":
        if NAIS_StandortstypHeute == "57C" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "47Re"
        elif NAIS_StandortstypHeute == "57CTa" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "47Re"
        elif NAIS_StandortstypHeute == "57V" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "46MRe"
        elif NAIS_StandortstypHeute == "57VTa" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "46MRe"
        elif NAIS_StandortstypHeute == "57Bl" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal" and schatten == False:
            NAIS_StandortstypZukunft = "47H"
        elif NAIS_StandortstypHeute == "57Bl" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal" and schatten == True:
            NAIS_StandortstypZukunft = "57Bl"
        elif NAIS_StandortstypHeute == "60A" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "47DRe"
        elif NAIS_StandortstypHeute == "60ATa" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "47DRe"
        elif NAIS_StandortstypHeute == "59A" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "47DRe"
        elif NAIS_StandortstypHeute == "58L":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "59J":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "59R":
            NAIS_StandortstypZukunft = "59R"
        elif NAIS_StandortstypHeute == "59S" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "52Re"
        elif NAIS_StandortstypHeute == "47*":
            NAIS_StandortstypZukunft = "47*"
        elif NAIS_StandortstypHeute == "59*":
            NAIS_StandortstypZukunft = "47*"
        elif NAIS_StandortstypHeute == "67" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "53*"
        elif NAIS_StandortstypHeute == "70":
            NAIS_StandortstypZukunft = "68"
        elif NAIS_StandortstypHeute == "71":
            NAIS_StandortstypZukunft = "71"
        elif NAIS_StandortstypHeute == "60" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "47DRe"
        elif NAIS_StandortstypHeute == "60Ta" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "47DRe"
        elif NAIS_StandortstypHeute == "24*":
            NAIS_StandortstypZukunft = "24*"
        elif NAIS_StandortstypHeute == "21*":
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "27*":
            NAIS_StandortstypZukunft = "27h"
        elif NAIS_StandortstypHeute == "53":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "53Lae":
            NAIS_StandortstypZukunft = "53Lae"
        elif NAIS_StandortstypHeute == "53Ta":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "57CLae" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "47Re"
        elif NAIS_StandortstypHeute == "57VLae" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "46MRe"
        elif NAIS_StandortstypHeute == "57BlTa":
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "57VM" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "47MRe"
        elif NAIS_StandortstypHeute == "57S":
            NAIS_StandortstypZukunft = "56"
        elif NAIS_StandortstypHeute == "57STa":
            NAIS_StandortstypZukunft = "56"
        elif NAIS_StandortstypHeute == "58":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "58Bl":
            NAIS_StandortstypZukunft = "47H"
        elif NAIS_StandortstypHeute == "58Bl" and schatten == True and blockschutt == True and trocken == True:
            NAIS_StandortstypZukunft = "58Bl"
        elif NAIS_StandortstypHeute == "58C":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "60*" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
            NAIS_StandortstypZukunft = "50*Re"
        elif NAIS_StandortstypHeute == "32V":  # hier muesste noch Ueberschwemmung rein
            NAIS_StandortstypZukunft = "43S"
        elif NAIS_StandortstypHeute == "AV":
            NAIS_StandortstypZukunft = "24*"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion "4", Projektionspfad von subalpin nach hochmontan Nebenareal
def Projektionspfad_reg4_SA_HMTannenNeben(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "subalpin" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
        if NAIS_StandortstypHeute == "57C" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47"
        elif NAIS_StandortstypHeute == "57CTa" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47"
        elif NAIS_StandortstypHeute == "57V" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "46M"
        elif NAIS_StandortstypHeute == "57VTa" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "46M"
        elif NAIS_StandortstypHeute == "57Bl" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "60A" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "60ATa" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "59A" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "58L":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "59J":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "59R":
            NAIS_StandortstypZukunft = "59R"
        elif NAIS_StandortstypHeute == "59S" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "52"
        elif NAIS_StandortstypHeute == "47*":
            NAIS_StandortstypZukunft = "47*"
        elif NAIS_StandortstypHeute == "59*":
            NAIS_StandortstypZukunft = "47*"
        elif NAIS_StandortstypHeute == "67" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "70":
            NAIS_StandortstypZukunft = "68"
        elif NAIS_StandortstypHeute == "71":
            NAIS_StandortstypZukunft = "71"
        elif NAIS_StandortstypHeute == "60" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "60Ta" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "24*":
            NAIS_StandortstypZukunft = "24*"
        elif NAIS_StandortstypHeute == "21*":
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "27*":
            NAIS_StandortstypZukunft = "27h"
        elif NAIS_StandortstypHeute == "53":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "53Lae":
            NAIS_StandortstypZukunft = "53Lae"
        elif NAIS_StandortstypHeute == "53Ta":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "57CLae" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47"
        elif NAIS_StandortstypHeute == "57VLae" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "46M"
        elif NAIS_StandortstypHeute == "57BlTa":
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "57VM" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47M"
        elif NAIS_StandortstypHeute == "57S":
            NAIS_StandortstypZukunft = "56"
        elif NAIS_StandortstypHeute == "57STa":
            NAIS_StandortstypZukunft = "56"
        elif NAIS_StandortstypHeute == "58":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "58Bl":
            NAIS_StandortstypZukunft = "47H"
        elif NAIS_StandortstypHeute == "58Bl" and schatten == True and blockschutt == True and trocken == True:
            NAIS_StandortstypZukunft = "58Bl"
        elif NAIS_StandortstypHeute == "58C":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "60*" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "50*"
        elif NAIS_StandortstypHeute == "32V":  # hier muesste noch Ueberschwemmung rein
            NAIS_StandortstypZukunft = "43S"
        elif NAIS_StandortstypHeute == "AV":
            NAIS_StandortstypZukunft = "24*"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion "4", Projektionspfad von subalpin nach hochmontan Hauptareal
def Projektionspfad_reg4_SA_HMTannenHaupt(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "subalpin" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
        if NAIS_StandortstypHeute == "57C" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47"
        elif NAIS_StandortstypHeute == "57CTa" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47"
        elif NAIS_StandortstypHeute == "57V" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "46M"
        elif NAIS_StandortstypHeute == "57VTa" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "46M"
        elif NAIS_StandortstypHeute == "57Bl" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "60A" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "60ATa" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "59A" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "58L":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "59J":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "59R":
            NAIS_StandortstypZukunft = "59R"
        elif NAIS_StandortstypHeute == "59S" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "52"
        elif NAIS_StandortstypHeute == "47*":
            NAIS_StandortstypZukunft = "47*"
        elif NAIS_StandortstypHeute == "59*":
            NAIS_StandortstypZukunft = "47*"
        elif NAIS_StandortstypHeute == "67" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "70":
            NAIS_StandortstypZukunft = "68"
        elif NAIS_StandortstypHeute == "71":
            NAIS_StandortstypZukunft = "71"
        elif NAIS_StandortstypHeute == "60" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "60Ta" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "24*":
            NAIS_StandortstypZukunft = "24*"
        elif NAIS_StandortstypHeute == "21*":
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "27*":
            NAIS_StandortstypZukunft = "27h"
        elif NAIS_StandortstypHeute == "53":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "53Lae":
            NAIS_StandortstypZukunft = "53Lae"
        elif NAIS_StandortstypHeute == "53Ta":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "57CLae" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47"
        elif NAIS_StandortstypHeute == "57VLae" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "46M"
        elif NAIS_StandortstypHeute == "57BlTa":
            NAIS_StandortstypZukunft = "48"
        elif NAIS_StandortstypHeute == "57VM" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "47M"
        elif NAIS_StandortstypHeute == "57S":
            NAIS_StandortstypZukunft = "56"
        elif NAIS_StandortstypHeute == "57STa":
            NAIS_StandortstypZukunft = "56"
        elif NAIS_StandortstypHeute == "58":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "58Bl":
            NAIS_StandortstypZukunft = "47H"
        elif NAIS_StandortstypHeute == "58Bl" and schatten == True and blockschutt == True and trocken == True:
            NAIS_StandortstypZukunft = "58Bl"
        elif NAIS_StandortstypHeute == "58C":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "60*" and hoehenstufe_zukunft in ["hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal"]:
            NAIS_StandortstypZukunft = "50*"
        elif NAIS_StandortstypHeute == "32V":  # hier muesste noch Ueberschwemmung rein
            NAIS_StandortstypZukunft = "43S"
        elif NAIS_StandortstypHeute == "AV":
            NAIS_StandortstypZukunft = "24*"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion "4", Projektionspfad von hochmontan nach hochmontan Tannen-Reliktareal
def Projektionspfad_reg4_HM_HMTannenRelikt(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "hochmontan" and hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
        if NAIS_StandortstypHeute in ["24", "56", "66", "68", "71", "23*", "24*", "27h", "32*", "32V", "40P", "40PBl",
                                      "43S", "47DRe", "47H", "47MRe", "47Re", "50*Re", "52Re", "53*", "55*", "55*Ta", "57Bl",
                                      "58Bl", "59R", "AV", "46MRe","25a"]:
            NAIS_StandortstypZukunft = NAIS_StandortstypHeute
        elif NAIS_StandortstypHeute == "47":
            NAIS_StandortstypZukunft = "47Re"
        elif NAIS_StandortstypHeute == "52":
            NAIS_StandortstypZukunft = "52Re"
        elif NAIS_StandortstypHeute == "46M":
            NAIS_StandortstypZukunft = "46MRe"
        elif NAIS_StandortstypHeute == "47D":
            NAIS_StandortstypZukunft = "47DRe"
        elif NAIS_StandortstypHeute == "47M":
            NAIS_StandortstypZukunft = "47MRe"
        elif NAIS_StandortstypHeute == "50*":
            NAIS_StandortstypZukunft = "50*Re"
        elif NAIS_StandortstypHeute == "53Lae":
            NAIS_StandortstypZukunft = "53*"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion "4", Projektionspfad von hochmontan nach hochmontan Tannen-Nebenareal
def Projektionspfad_reg4_HM_HMTanneNeben(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "hochmontan" and hoehenstufe_zukunft == "hochmontan im Tannen-Nebenareal":
        if NAIS_StandortstypHeute in ["47", "24", "48", "52", "56", "66", "68", "71", "23*", "24*", "27h", "32*", "32V","33V", "40P", "40PBl", "43S", "46M", "47*", "47D", "47H", "47M", "50*", "53Lae","53Ta", "55*", "55*Ta","57Bl", "58Bl", "59R", "AV"]:
            NAIS_StandortstypZukunft = NAIS_StandortstypHeute
        elif NAIS_StandortstypHeute == "46MRe":
            NAIS_StandortstypZukunft = "46M"
        elif NAIS_StandortstypHeute == "47DRe":
            NAIS_StandortstypZukunft = "47D"
        elif NAIS_StandortstypHeute == "47MRe":
            NAIS_StandortstypZukunft = "47M"
        elif NAIS_StandortstypHeute == "47Re":
            NAIS_StandortstypZukunft = "47"
        elif NAIS_StandortstypHeute == "50*Re":
            NAIS_StandortstypZukunft = "50*"
        elif NAIS_StandortstypHeute == "52Re":
            NAIS_StandortstypZukunft = "52"
        elif NAIS_StandortstypHeute == "53*":
            NAIS_StandortstypZukunft = "53Ta"
        elif NAIS_StandortstypHeute == "53*Ta":
            NAIS_StandortstypZukunft = "53Ta"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion "4", Projektionspfad von hochmontan nach hochmontan Tannen-Hauptareal
def Projektionspfad_reg4_HM_HMTanneHaupt(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute == "hochmontan" and hoehenstufe_zukunft == "hochmontan im Tannen-Hauptareal":
        NAIS_StandortstypZukunft=NAIS_StandortstypHeute
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion "4", Projektionspfad von hochmontan nach collin
def Projektionspfad_reg4_HM_CO(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if "hochmontan" in hoehenstufe_heute and hoehenstufe_zukunft == "collin":
        if NAIS_StandortstypHeute == "24":
            NAIS_StandortstypZukunft = "25a"
        elif NAIS_StandortstypHeute == "47":
            NAIS_StandortstypZukunft = "25a"
        elif NAIS_StandortstypHeute == "48":
            NAIS_StandortstypZukunft = "25au"
        elif NAIS_StandortstypHeute == "52":
            NAIS_StandortstypZukunft = "34b"
        elif NAIS_StandortstypHeute == "56":
            NAIS_StandortstypZukunft = "k.A."
        elif NAIS_StandortstypHeute == "66":
            NAIS_StandortstypZukunft = "66"
        elif NAIS_StandortstypHeute == "68":
            NAIS_StandortstypZukunft = "42r"
        elif NAIS_StandortstypHeute == "71":
            NAIS_StandortstypZukunft = "k.A."
        elif NAIS_StandortstypHeute == "23*":
            NAIS_StandortstypZukunft = "42r"
        elif NAIS_StandortstypHeute == "24*":  # hier muesste noch Schlucht rein
            NAIS_StandortstypZukunft = "25au"
        elif NAIS_StandortstypHeute == "27h":
            NAIS_StandortstypZukunft = "27"
        elif NAIS_StandortstypHeute == "32*":
            NAIS_StandortstypZukunft = "k.A."
        elif NAIS_StandortstypHeute == "32V":
            NAIS_StandortstypZukunft = "28"  # hier muessten noch ueberschwemmungen rein
        elif NAIS_StandortstypHeute == "33V":
            NAIS_StandortstypZukunft = "33m"
        elif NAIS_StandortstypHeute == "40P":
            NAIS_StandortstypZukunft = "40Pt"
        elif NAIS_StandortstypHeute == "40PBl":
            NAIS_StandortstypZukunft = "40PBlt"
        elif NAIS_StandortstypHeute == "43S":
            NAIS_StandortstypZukunft = "43S"
        elif NAIS_StandortstypHeute == "46M":
            NAIS_StandortstypZukunft = "42V"
        elif NAIS_StandortstypHeute == "46MRe":
            NAIS_StandortstypZukunft = "42V"
        elif NAIS_StandortstypHeute == "47*":
            NAIS_StandortstypZukunft = "33a"
        elif NAIS_StandortstypHeute == "47D":
            NAIS_StandortstypZukunft = "25au"
        elif NAIS_StandortstypHeute == "47DRe":
            NAIS_StandortstypZukunft = "25au"
        elif NAIS_StandortstypHeute == "47H":
            NAIS_StandortstypZukunft = "25as"
        elif NAIS_StandortstypHeute == "47M":
            NAIS_StandortstypZukunft = "34a"
        elif NAIS_StandortstypHeute == "47MRe":
            NAIS_StandortstypZukunft = "34a"
        elif NAIS_StandortstypHeute == "47Re":
            NAIS_StandortstypZukunft = "25a"
        elif NAIS_StandortstypHeute == "50*":
            NAIS_StandortstypZukunft = "25b"
        elif NAIS_StandortstypHeute == "50*Re":
            NAIS_StandortstypZukunft = "25b"
        elif NAIS_StandortstypHeute == "52Re":
            NAIS_StandortstypZukunft = "34b"
        elif NAIS_StandortstypHeute == "53*":
            NAIS_StandortstypZukunft = "34b"
        elif NAIS_StandortstypHeute == "53*Ta":
            NAIS_StandortstypZukunft = "34b"
        elif NAIS_StandortstypHeute == "53Lae":
            NAIS_StandortstypZukunft = "34b"
        elif NAIS_StandortstypHeute == "53Ta":
            NAIS_StandortstypZukunft = "34b"
        elif NAIS_StandortstypHeute == "55*":  # hier muesste noch tiefgruendig rein
            NAIS_StandortstypZukunft = "42Q"
        elif NAIS_StandortstypHeute == "55*Ta":  # hier muesste noch tiefgruendig rein
            NAIS_StandortstypZukunft = "42Q"
        elif NAIS_StandortstypHeute == "57Bl":
            NAIS_StandortstypZukunft = "25au"
        elif NAIS_StandortstypHeute == "58Bl":
            NAIS_StandortstypZukunft = "42Q"
        elif NAIS_StandortstypHeute == "59R":
            NAIS_StandortstypZukunft = "k.A."
        elif NAIS_StandortstypHeute == "AV":
            NAIS_StandortstypZukunft = "25au"
        elif NAIS_StandortstypHeute == "25a":
            NAIS_StandortstypZukunft = "25a"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion "5", Projektionspfad von obersubalpin oder subalpin nach hochmontan
def Projektionspfad_reg5_OSASA_HM(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute in ["obersubalpin", "subalpin"] and "hochmontan" in hoehenstufe_zukunft:
        if NAIS_StandortstypHeute == "58":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "59":
            NAIS_StandortstypZukunft = "47"
        elif NAIS_StandortstypHeute == "67":
            NAIS_StandortstypZukunft = "67"
        elif NAIS_StandortstypHeute == "69":
            NAIS_StandortstypZukunft = "69"
        elif NAIS_StandortstypHeute == "70":
            NAIS_StandortstypZukunft = "68"
        elif NAIS_StandortstypHeute == "71":
            NAIS_StandortstypZukunft = "k.A."
        elif NAIS_StandortstypHeute == "21*":
            NAIS_StandortstypZukunft = "21*"
        elif NAIS_StandortstypHeute == "21L":
            NAIS_StandortstypZukunft = "21L"
        elif NAIS_StandortstypHeute == "47*":
            NAIS_StandortstypZukunft = "47*"
        elif NAIS_StandortstypHeute == "57C":
            NAIS_StandortstypZukunft = "47"
        elif NAIS_StandortstypHeute == "57CTa":
            NAIS_StandortstypZukunft = "47"
        elif NAIS_StandortstypHeute == "59*":
            NAIS_StandortstypZukunft = "47*"
        elif NAIS_StandortstypHeute == "59A":
            NAIS_StandortstypZukunft = "21L"
        elif NAIS_StandortstypHeute == "59J":
            NAIS_StandortstypZukunft = "55*"
        elif NAIS_StandortstypHeute == "59S":
            NAIS_StandortstypZukunft = "52"
        elif NAIS_StandortstypHeute == "AV":
            NAIS_StandortstypZukunft = "24*"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion "5", Projektionspfad von hochmontan nach obermontan oder untermontan
def Projektionspfad_reg5_HM_OMUM(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if "hochmontan" in hoehenstufe_heute and hoehenstufe_zukunft in ["obermontan", "untermontan", "unter- und obermontan"]:
        if NAIS_StandortstypHeute == "24":
            NAIS_StandortstypZukunft = "24"
        elif NAIS_StandortstypHeute == "47":
            NAIS_StandortstypZukunft = "19a"
        elif NAIS_StandortstypHeute == "48":
            NAIS_StandortstypZukunft = "24*"
        elif NAIS_StandortstypHeute == "52":
            NAIS_StandortstypZukunft = "14*"
        elif NAIS_StandortstypHeute == "66":
            NAIS_StandortstypZukunft = "k.A."
        elif NAIS_StandortstypHeute == "67":
            NAIS_StandortstypZukunft = "16*"
        elif NAIS_StandortstypHeute == "68":
            NAIS_StandortstypZukunft = "68"
        elif NAIS_StandortstypHeute == "68" and strahlungsgreich == True:
            NAIS_StandortstypZukunft = "42r"
        elif NAIS_StandortstypHeute == "69":
            NAIS_StandortstypZukunft = "14*"
        elif NAIS_StandortstypHeute == "21*":
            NAIS_StandortstypZukunft = "19P"
        elif NAIS_StandortstypHeute == "21L":
            NAIS_StandortstypZukunft = "21L"
        elif NAIS_StandortstypHeute == "23*":
            NAIS_StandortstypZukunft = "23*"
        elif NAIS_StandortstypHeute == "24*":
            NAIS_StandortstypZukunft = "24*"
        elif NAIS_StandortstypHeute == "27h":
            NAIS_StandortstypZukunft = "27"
        elif NAIS_StandortstypHeute == "32*":
            NAIS_StandortstypZukunft = "32*"
        elif NAIS_StandortstypHeute == "32V":
            NAIS_StandortstypZukunft = "32V"
        elif NAIS_StandortstypHeute == "40P":
            NAIS_StandortstypZukunft = "40P"
        elif NAIS_StandortstypHeute == "40PBl":
            NAIS_StandortstypZukunft = "40PBl"
        elif NAIS_StandortstypHeute == "43S":
            NAIS_StandortstypZukunft = "43S"
        elif NAIS_StandortstypHeute == "47*":
            NAIS_StandortstypZukunft = "4"
        elif NAIS_StandortstypHeute == "47D":
            NAIS_StandortstypZukunft = "19m"
        elif NAIS_StandortstypHeute == "47H":
            NAIS_StandortstypZukunft = "47H"
        elif NAIS_StandortstypHeute == "47M":
            NAIS_StandortstypZukunft = "3"
        elif NAIS_StandortstypHeute == "50*":
            NAIS_StandortstypZukunft = "12*"
        elif NAIS_StandortstypHeute == "55*":
            NAIS_StandortstypZukunft = "3s"
        elif NAIS_StandortstypHeute == "55*Ta":
            NAIS_StandortstypZukunft = "3s"
        elif NAIS_StandortstypHeute == "57Bl":
            NAIS_StandortstypZukunft = "24*"
        elif NAIS_StandortstypHeute == "AV":
            NAIS_StandortstypZukunft = "24*"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion "5", Projektionspfad von obermontan oder untermontan nach collin mit Buche
def Projektionspfad_reg5_OMUM_CObu(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute in ["obermontan", "untermontan", "unter- und obermontan"] and hoehenstufe_zukunft == "collin mit Buche":
        if NAIS_StandortstypHeute == "21L":
            NAIS_StandortstypZukunft = "25au"
        elif NAIS_StandortstypHeute == "19P":
            NAIS_StandortstypZukunft = "33m"
        elif NAIS_StandortstypHeute == "23*":
            NAIS_StandortstypZukunft = "42B"
        elif NAIS_StandortstypHeute == "24":
            NAIS_StandortstypZukunft = "25a"
        elif NAIS_StandortstypHeute == "24*":
            NAIS_StandortstypZukunft = "25au"
        elif NAIS_StandortstypHeute == "32V":
            NAIS_StandortstypZukunft = "32C"
        elif NAIS_StandortstypHeute == "32*":
            NAIS_StandortstypZukunft = "27"
        elif NAIS_StandortstypHeute == "27":
            NAIS_StandortstypZukunft = "27"
        elif NAIS_StandortstypHeute == "40P":
            NAIS_StandortstypZukunft = "40Pt"
        elif NAIS_StandortstypHeute == "40PBl":
            NAIS_StandortstypZukunft = "25as"
        elif NAIS_StandortstypHeute == "43S":
            NAIS_StandortstypZukunft = "43S"
        elif NAIS_StandortstypHeute == "19a":
            NAIS_StandortstypZukunft = "3L/4L"
        elif NAIS_StandortstypHeute == "19m":
            NAIS_StandortstypZukunft = "3L/4L"
        elif NAIS_StandortstypHeute == "47H":
            NAIS_StandortstypZukunft = "25as"
        elif NAIS_StandortstypHeute == "3":
            NAIS_StandortstypZukunft = "42V"  # hier muesste noch die Bedingung tiefgruendig mit rein (34a)
        elif NAIS_StandortstypHeute == "4":
            NAIS_StandortstypZukunft = "3L/4L"
        elif NAIS_StandortstypHeute == "14*":
            NAIS_StandortstypZukunft = "37"
        elif NAIS_StandortstypHeute == "14*" and blockschutt == True:
            NAIS_StandortstypZukunft = "25O"
        elif NAIS_StandortstypHeute == "24*":
            NAIS_StandortstypZukunft = "25au"
        elif NAIS_StandortstypHeute == "3s":
            NAIS_StandortstypZukunft = "42Q"  # hier muesste noch flachgruendig rein (42r)
        elif NAIS_StandortstypHeute == "12*":
            NAIS_StandortstypZukunft = "36"
        elif NAIS_StandortstypHeute == "68":
            NAIS_StandortstypZukunft = "42r"
        elif NAIS_StandortstypHeute == "42r":
            NAIS_StandortstypZukunft = "42r"
        elif NAIS_StandortstypHeute == "16*":
            NAIS_StandortstypZukunft = "38*"
        elif NAIS_StandortstypHeute == "3*/4*":
            NAIS_StandortstypZukunft = "3LV"
        elif NAIS_StandortstypHeute == "12*h":
            NAIS_StandortstypZukunft = "36"
        elif NAIS_StandortstypHeute == "13*":
            NAIS_StandortstypZukunft = "13*"
        elif NAIS_StandortstypHeute == "27h":
            NAIS_StandortstypZukunft = "27"
        elif NAIS_StandortstypHeute == "AV":
            NAIS_StandortstypZukunft = "25au"
        elif NAIS_StandortstypHeute == "40Pt":
            NAIS_StandortstypZukunft = "40Pt"
        elif NAIS_StandortstypHeute == "40PBlt":
            NAIS_StandortstypZukunft = "25as"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
#standortsregion "5", Projektionspfad von obermontan oder untermontan nach hyperinsubrisch
def Projektionspfad_reg5_OMUM_hyp(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute in ["obermontan", "untermontan", "unter- und obermontan"] and hoehenstufe_zukunft == "hyperinsubrisch":
        if NAIS_StandortstypHeute == "21L":
            NAIS_StandortstypZukunft = "25auhyp"
        elif NAIS_StandortstypHeute == "19P":
            NAIS_StandortstypZukunft = "33mhyp"
        elif NAIS_StandortstypHeute == "23*":
            NAIS_StandortstypZukunft = "42Bhyp"
        elif NAIS_StandortstypHeute == "24":
            NAIS_StandortstypZukunft = "25ahyp"
        elif NAIS_StandortstypHeute == "24*":
            NAIS_StandortstypZukunft = "25auhyp"
        elif NAIS_StandortstypHeute == "32V":
            NAIS_StandortstypZukunft = "32Chyp"
        elif NAIS_StandortstypHeute == "32*":
            NAIS_StandortstypZukunft = "27hyp"
        elif NAIS_StandortstypHeute == "27":
            NAIS_StandortstypZukunft = "27hyp"
        elif NAIS_StandortstypHeute == "40P":
            NAIS_StandortstypZukunft = "40Phyp"
        elif NAIS_StandortstypHeute == "40PBl":
            NAIS_StandortstypZukunft = "25ashyp"
        elif NAIS_StandortstypHeute == "43S":
            NAIS_StandortstypZukunft = "43Shyp"
        elif NAIS_StandortstypHeute == "19a":
            NAIS_StandortstypZukunft = "3L/4Lhyp"
        elif NAIS_StandortstypHeute == "19m":
            NAIS_StandortstypZukunft = "3L/4Lhyp"
        elif NAIS_StandortstypHeute == "47H":
            NAIS_StandortstypZukunft = "25ashyp"
        elif NAIS_StandortstypHeute == "3":
            NAIS_StandortstypZukunft = "42Vhyp"  # hier muesste noch tiefgruendig rein (34ahyp)
        elif NAIS_StandortstypHeute == "4":
            NAIS_StandortstypZukunft = "3L/4Lhyp"
        elif NAIS_StandortstypHeute == "14*" and blockschutt == False:
            NAIS_StandortstypZukunft = "37hyp"
        elif NAIS_StandortstypHeute == "14*" and blockschutt == True:
            NAIS_StandortstypZukunft = "25Ohyp"
        elif NAIS_StandortstypHeute == "24*":
            NAIS_StandortstypZukunft = "25auhyp"
        elif NAIS_StandortstypHeute == "3s":
            NAIS_StandortstypZukunft = "42Qhyp"  # hier muesste noch flachgruendig rein (42rhyp)
        elif NAIS_StandortstypHeute == "12*":
            NAIS_StandortstypZukunft = "36hyp"
        elif NAIS_StandortstypHeute == "68":
            NAIS_StandortstypZukunft = "42rhyp"
        elif NAIS_StandortstypHeute == "42r":
            NAIS_StandortstypZukunft = "42rhyp"
        elif NAIS_StandortstypHeute == "16*":
            NAIS_StandortstypZukunft = "38*hyp"
        elif NAIS_StandortstypHeute == "3*/4*":
            NAIS_StandortstypZukunft = "3LVhyp"
        elif NAIS_StandortstypHeute == "12*h":
            NAIS_StandortstypZukunft = "36Lhyp"
        elif NAIS_StandortstypHeute == "13*":
            NAIS_StandortstypZukunft = "313*hyp"
        elif NAIS_StandortstypHeute == "27h":
            NAIS_StandortstypZukunft = "27hyp"
        elif NAIS_StandortstypHeute == "AV":
            NAIS_StandortstypZukunft = "25auhyp"
        elif NAIS_StandortstypHeute == "40Pt":
            NAIS_StandortstypZukunft = "40Phyp"
        elif NAIS_StandortstypHeute == "40PBlt":
            NAIS_StandortstypZukunft = "25ashyp"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft
def Projektionspfad_reg5_COBu_hyp(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung):
    NAIS_StandortstypZukunft = "NA"
    if hoehenstufe_heute in ["collin", "collin mit Buche"] and hoehenstufe_zukunft == "hyperinsubrisch":
        if NAIS_StandortstypHeute == "25au":
            NAIS_StandortstypZukunft = "25auhyp"
        elif NAIS_StandortstypHeute == "33m":
            NAIS_StandortstypZukunft = "33mhyp"
        elif NAIS_StandortstypHeute == "42B":
            NAIS_StandortstypZukunft = "42Bhyp"
        elif NAIS_StandortstypHeute == "25a":
            NAIS_StandortstypZukunft = "25ahyp"
        elif NAIS_StandortstypHeute == "32C":
            NAIS_StandortstypZukunft = "32Chyp"
        elif NAIS_StandortstypHeute == "27":
            NAIS_StandortstypZukunft = "27hyp"
        elif NAIS_StandortstypHeute == "40Pt":
            NAIS_StandortstypZukunft = "40Phyp"
        elif NAIS_StandortstypHeute == "25as":
            NAIS_StandortstypZukunft = "25ashyp"
        elif NAIS_StandortstypHeute == "43S":
            NAIS_StandortstypZukunft = "43Shyp"
        elif NAIS_StandortstypHeute == "3L/4L":
            NAIS_StandortstypZukunft = "3L/4Lhyp"
        elif NAIS_StandortstypHeute == "3L":
            NAIS_StandortstypZukunft = "3Lhyp"
        elif NAIS_StandortstypHeute == "4L":
            NAIS_StandortstypZukunft = "4Lhyp"
        elif NAIS_StandortstypHeute == "37":
            NAIS_StandortstypZukunft = "37hyp"
        elif NAIS_StandortstypHeute == "25O":
            NAIS_StandortstypZukunft = "25Ohyp"
        elif NAIS_StandortstypHeute == "42Q":
            NAIS_StandortstypZukunft = "42Qhyp"
        elif NAIS_StandortstypHeute == "43S":
            NAIS_StandortstypZukunft = "43Shyp"
        elif NAIS_StandortstypHeute == "42V":
            NAIS_StandortstypZukunft = "42Vhyp"
        elif NAIS_StandortstypHeute == "42r":
            NAIS_StandortstypZukunft = "42rhyp"
        elif NAIS_StandortstypHeute == "36":
            NAIS_StandortstypZukunft = "36hyp"
        elif NAIS_StandortstypHeute == "66":
            NAIS_StandortstypZukunft = "66hyp"
        elif NAIS_StandortstypHeute == "38*":
            NAIS_StandortstypZukunft = "38*hyp"
        elif NAIS_StandortstypHeute == "3LV":
            NAIS_StandortstypZukunft = "3LVhyp"
        elif NAIS_StandortstypHeute == "13*":
            NAIS_StandortstypZukunft = "13*hyp"
        elif NAIS_StandortstypHeute == "7a":
            NAIS_StandortstypZukunft = "7ahyp"
        elif NAIS_StandortstypHeute == "22*":
            NAIS_StandortstypZukunft = "22*hyp"
        elif NAIS_StandortstypHeute == "25f":
            NAIS_StandortstypZukunft = "25fhyp"
        elif NAIS_StandortstypHeute == "27O":
            NAIS_StandortstypZukunft = "27Ohyp"
        elif NAIS_StandortstypHeute == "28":
            NAIS_StandortstypZukunft = "28hyp"
        elif NAIS_StandortstypHeute == "30":
            NAIS_StandortstypZukunft = "30hyp"
        elif NAIS_StandortstypHeute == "31":
            NAIS_StandortstypZukunft = "31hyp"
        elif NAIS_StandortstypHeute == "33a":
            NAIS_StandortstypZukunft = "33ahyp"
        elif NAIS_StandortstypHeute == "33b":
            NAIS_StandortstypZukunft = "33bhyp"
        elif NAIS_StandortstypHeute == "35Q":
            NAIS_StandortstypZukunft = "35Qhyp"
        elif NAIS_StandortstypHeute == "35S":
            NAIS_StandortstypZukunft = "35Shyp"
        elif NAIS_StandortstypHeute == "40PBlt":
            NAIS_StandortstypZukunft = "40PBlthyp"
        elif NAIS_StandortstypHeute == "42C":
            NAIS_StandortstypZukunft = "42thyp"
        elif NAIS_StandortstypHeute == "43":
            NAIS_StandortstypZukunft = "43hyp"
        elif NAIS_StandortstypHeute == "43*":
            NAIS_StandortstypZukunft = "43*hyp"
        elif NAIS_StandortstypHeute == "44":
            NAIS_StandortstypZukunft = "44hyp"
        elif NAIS_StandortstypHeute == "91":
            NAIS_StandortstypZukunft = "91hyp"
        elif NAIS_StandortstypHeute == "92a":
            NAIS_StandortstypZukunft = "92ahyp"
        elif NAIS_StandortstypHeute == "92z":
            NAIS_StandortstypZukunft = "92zhyp"
        elif NAIS_StandortstypHeute == "93":
            NAIS_StandortstypZukunft = "93hyp"
    else:
        NAIS_StandortstypZukunft = "NA"
    return NAIS_StandortstypZukunft







#************************************************************************************************
def BaumartenempfehlungCC(matrixbaumartenarr, NAIS_StandortstypHeute, NAIS_StandortstypZukunft):
    #Standortstyp: NaiS Standortstyp
    #Klimaszenario: maessig=REGCM, stark=CLM
    erglist_heute_foerdern=[]
    erglist_heute_mitnehmen=[]
    erglist_heute_reduzieren=[]
    erglist_heute_achtung=[]
    erglist_zukunft_foerdern=[]
    erglist_zukunft_mitnehmen=[]
    erglist_zukunft_achtung=[]
    #check the column index
    rows = numpy.shape(matrixbaumartenarr)[0]
    if NAIS_StandortstypHeute in matrixbaumartenarr[0,1:].tolist() and NAIS_StandortstypZukunft in matrixbaumartenarr[0, 1:].tolist():
        col_heute=matrixbaumartenarr[0,:].tolist().index(NAIS_StandortstypHeute)
        col_zukunft=matrixbaumartenarr[0,:].tolist().index(NAIS_StandortstypZukunft)
        #loop through the rows
        row=1
        while row < rows:
            #heute moegliche Baumarten
            if matrixbaumartenarr[row, col_zukunft] in ["a","b"] and matrixbaumartenarr[row, col_heute] in ["a","b","c"] and matrixbaumartenarr[row, 0]<>"Ailanthus altissima":
                if matrixbaumartenarr[row, 0] not in erglist_heute_foerdern:
                    erglist_heute_foerdern.append(matrixbaumartenarr[row, 0])
            elif matrixbaumartenarr[row, col_zukunft] =="c" and matrixbaumartenarr[row, col_heute] in ["a","b","c"] and matrixbaumartenarr[row, 0]<>"Ailanthus altissima":
                if matrixbaumartenarr[row, 0] not in erglist_heute_mitnehmen:
                    erglist_heute_mitnehmen.append(matrixbaumartenarr[row, 0])
            elif matrixbaumartenarr[row, col_zukunft] not in ["a","b","c"] and matrixbaumartenarr[row, col_heute] in ["a","b","c"] and matrixbaumartenarr[row, 0]<>"Ailanthus altissima":
                if matrixbaumartenarr[row, 0] not in erglist_heute_reduzieren:
                    erglist_heute_reduzieren.append(matrixbaumartenarr[row, 0])
            #Goetterbaum
            if matrixbaumartenarr[row, 0]=="Ailanthus altissima" and matrixbaumartenarr[row, col_zukunft] in ["a","b","c"] and matrixbaumartenarr[row, col_heute] in ["a","b","c"]:
                erglist_heute_achtung.append("Ailanthus altissima")
            #in Zukunft moegliche Baumarten
            if matrixbaumartenarr[row, col_heute] not in ["a","b","c"] and matrixbaumartenarr[row, col_zukunft] in ["a","b"]:
                if matrixbaumartenarr[row, 0] not in erglist_zukunft_foerdern and matrixbaumartenarr[row, 0] not in erglist_zukunft_mitnehmen and matrixbaumartenarr[row, 0] not in erglist_zukunft_achtung:
                    erglist_zukunft_foerdern.append(matrixbaumartenarr[row, 0])
            elif matrixbaumartenarr[row, col_heute] not in ["a", "b", "c"] and matrixbaumartenarr[row, col_zukunft] =="c":
                if matrixbaumartenarr[row, 0] not in erglist_zukunft_foerdern and matrixbaumartenarr[row, 0] not in erglist_zukunft_mitnehmen and matrixbaumartenarr[row, 0] not in erglist_zukunft_achtung:
                    erglist_zukunft_mitnehmen.append(matrixbaumartenarr[row, 0])
            # Goetterbaum
            if matrixbaumartenarr[row, 0] == "Ailanthus altissima" and matrixbaumartenarr[row, col_zukunft] in ["a", "b", "c"] and matrixbaumartenarr[row, col_heute] not in ["a", "b", "c"]:
                erglist_zukunft_achtung.append("Ailanthus altissima")
            row+=1
    else:
        #print "Achtung: kein Eintrag in Baumartenmatrix"
        erglist_heute_foerdern.append("NA")
        erglist_heute_mitnehmen.append("NA")
        erglist_heute_reduzieren.append("NA")
        erglist_heute_achtung.append("NA")
        erglist_zukunft_foerdern.append("NA")
        erglist_zukunft_mitnehmen.append("NA")
        erglist_zukunft_achtung.append("NA")
    return erglist_heute_foerdern, erglist_heute_mitnehmen, erglist_heute_reduzieren, erglist_heute_achtung, erglist_zukunft_foerdern, erglist_zukunft_mitnehmen, erglist_zukunft_achtung
#************************************************************************************************
def logikUebergang(x,y):
    u=""
    if x=="a":
        if y=="a":
            u="a"
        elif y=="b":
            u="a"
        elif y=="c":
            u="b"
        elif y in ["","ex"]:
            u="c"
    elif x=="b":
        if y=="a":
            u="b"
        elif y=="b":
            u="b"
        elif y=="c":
            u="b"
        elif y in ["","ex"]:
            u="c"
    elif x=="c":
        if y=="a":
            u="b"
        elif y=="b":
            u="c"
        elif y=="c":
            u="c"
        elif y in ["","ex"]:
            u=""
    elif x=="ex":
        if y=="a":
            u="c"
        elif y=="b":
            u="c"
        elif y=="c":
            u=""
        elif y in ["","ex"]:
            u=""
    elif x=="":
        if y=="a":
            u="c"
        elif y=="b":
            u="c"
        elif y=="c":
            u=""
        elif y in ["","ex"]:
            u=""
    return u
#************************************************************************************************



#************************************************************************************************
def Uebergang(matrixbaumartenarr, StandortstypXheute, StandortstypYheute,StandortstypXzukunft, StandortstypYzukunft):
    erglist_heute_foerdern = []
    erglist_heute_mitnehmen = []
    erglist_heute_reduzieren = []
    erglist_heute_achtung = []
    erglist_zukunft_foerdern = []
    erglist_zukunft_mitnehmen = []
    erglist_zukunft_achtung = []
    rows = numpy.shape(matrixbaumartenarr)[0]
    #neuer array um die uebergaenge zu speichern
    uebergangarr=numpy.empty([rows,2],dtype="string")
    uebergangarr[:,:]=""
    if StandortstypXheute in matrixbaumartenarr[0, 1:].tolist() and StandortstypXzukunft in matrixbaumartenarr[0, 1:].tolist() and StandortstypYheute in matrixbaumartenarr[0, 1:].tolist() and StandortstypYzukunft in matrixbaumartenarr[0, 1:].tolist():
        col_heuteX = matrixbaumartenarr[0, :].tolist().index(StandortstypXheute)
        col_heuteY = matrixbaumartenarr[0, :].tolist().index(StandortstypYheute)
        col_zukunftX = matrixbaumartenarr[0, :].tolist().index(StandortstypXzukunft)
        col_zukunftY = matrixbaumartenarr[0, :].tolist().index(StandortstypYzukunft)
        # Berechne Uebergang von Standort heute (linke Spalte) und Standort Zukunft (rechts)
        i = 1
        while i < rows:
            uebergangarr[i,0]=logikUebergang(matrixbaumartenarr[i,col_heuteX],matrixbaumartenarr[i,col_heuteY])
            uebergangarr[i,1]=logikUebergang(matrixbaumartenarr[i, col_zukunftX], matrixbaumartenarr[i, col_zukunftY])
            i += 1
        # loop through the rows
        row = 1
        while row < numpy.shape(uebergangarr)[0]:
            # heute moegliche Baumarten
            if uebergangarr[row, 1] in ["a", "b"] and uebergangarr[row, 0] in ["a", "b","c"] and \
                    matrixbaumartenarr[row, 0] <> "Ailanthus altissima":
                if matrixbaumartenarr[row, 0] not in erglist_heute_foerdern:
                    erglist_heute_foerdern.append(matrixbaumartenarr[row, 0])
            elif uebergangarr[row, 1] == "c" and uebergangarr[row, 0] in ["a", "b","c"] and \
                    matrixbaumartenarr[row, 0] <> "Ailanthus altissima":
                if matrixbaumartenarr[row, 0] not in erglist_heute_mitnehmen:
                    erglist_heute_mitnehmen.append(matrixbaumartenarr[row, 0])
            elif uebergangarr[row, 1] not in ["a", "b", "c"] and uebergangarr[row, 0] in [
                "a", "b", "c"] and matrixbaumartenarr[row, 0] <> "Ailanthus altissima":
                if matrixbaumartenarr[row, 0] not in erglist_heute_reduzieren:
                    erglist_heute_reduzieren.append(matrixbaumartenarr[row, 0])
            # Goetterbaum
            if matrixbaumartenarr[row, 0] == "Ailanthus altissima" and uebergangarr[row, 1] in ["a","b","c"] and \
                    uebergangarr[row, 0] in ["a", "b", "c"]:
                erglist_heute_achtung.append("Ailanthus altissima")
            # in Zukunft moegliche Baumarten
            if uebergangarr[row, 0] not in ["a", "b", "c"] and uebergangarr[row, 1] in ["a", "b"]:
                if matrixbaumartenarr[row, 0] not in erglist_zukunft_foerdern and matrixbaumartenarr[
                    row, 0] not in erglist_zukunft_mitnehmen and matrixbaumartenarr[
                    row, 0] not in erglist_zukunft_achtung:
                    erglist_zukunft_foerdern.append(matrixbaumartenarr[row, 0])
            elif uebergangarr[row, 0] not in ["a", "b", "c"] and uebergangarr[
                row, 1] == "c":
                if matrixbaumartenarr[row, 0] not in erglist_zukunft_foerdern and matrixbaumartenarr[
                    row, 0] not in erglist_zukunft_mitnehmen and matrixbaumartenarr[
                    row, 0] not in erglist_zukunft_achtung:
                    erglist_zukunft_mitnehmen.append(matrixbaumartenarr[row, 0])
            # Goetterbaum
            if matrixbaumartenarr[row, 0] == "Ailanthus altissima" and uebergangarr[row, 1] in ["a","b","c"] and \
                    uebergangarr[row, 0] not in ["a", "b", "c"]:
                erglist_zukunft_achtung.append("Ailanthus altissima")
            row += 1
    else:
        # print "Achtung: kein Eintrag in Baumartenmatrix"
        erglist_heute_foerdern.append("NA")
        erglist_heute_mitnehmen.append("NA")
        erglist_heute_reduzieren.append("NA")
        erglist_heute_achtung.append("NA")
        erglist_zukunft_foerdern.append("NA")
        erglist_zukunft_mitnehmen.append("NA")
        erglist_zukunft_achtung.append("NA")
    return erglist_heute_foerdern, erglist_heute_mitnehmen, erglist_heute_reduzieren, erglist_heute_achtung, erglist_zukunft_foerdern, erglist_zukunft_mitnehmen, erglist_zukunft_achtung