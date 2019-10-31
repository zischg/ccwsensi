import numpy
#Liste der möglichen Standortsregionen
standortsregionenlist=["1","2a","2b","3","4","5a","5b","J","M"]
#hoehenstufe_heute, aus Hoehenstufenmodell abenis
hoehenstufen_list=["Obersubalpin", "Subalpin", "Hochmontan im Tannen-Hauptareal", "Hochmontan im Tannen-Nebenareal", "Hochmontan im Tannen-Reliktareal","Unter- und Obermontan", "Obermontan", "Untermontan", "Submontan", "Collin mit Buche", "Collin", "Hyperinsubrisch"]

#create a list of NAIS types in Projektionspfade
infile=open("D:/CCW18sensi/code/test/naistypeninprojektionspfad.txt","r")
outfile=open("D:/CCW18sensi/code/test/naistypeninprojektionspfad_unique.txt","w")
naistypenliste=[]
for row in infile:
    if row not in ["", " ", "keine Angabe ", "keine Angabe", "\n", "\t"]:
        corr=row.replace(" ","").replace("\n","").replace("\t","")
        if corr not in naistypenliste:
            naistypenliste.append(corr)
infile.close()
naistypenliste.sort()
for item in naistypenliste:
    outfile.write(item+"\n")
outfile.close()


#make the test
outtestfile=open("D:/CCW18sensi/code/test/testresults.txt","w")
outtestfile.write("Standortsregion"+"\t"+"HoehenstufeHeute"+"\t"+"HoehenstufeZukunft"+"\t"+"NAISheute"+"\t"+"NAISzukunft"+"\t"+"schattig"+"\t"+"strahlungsreich"+"\t"+"Blockschutt"+"\t"+"Bodenverdichtung"+"\t"+"trocken"+"\t"+"Kuppenlage"+"\t"+"Hanglage"+"\t"+"Muldenlage"+"\t"+"Hangneigung"+"\t"+"VS"+"\t"+"SH"+"\t"+"Beschreibung"+"\n")

#alle Bedingungen False
schatten=False
strahlungsreich=False
blockschutt=False
bodenverdichtet=False
trocken=False
hanglage=False
kuppenlage=False
muldenlage=False
VS=False
SH=False
hangneigung=59
outfilelineslist=[]
for naistypheute in naistypenliste:
    for storeg in standortsregionenlist:
        for hsheute in hoehenstufen_list:
            for hszukunft in hoehenstufen_list[1:]:
                if hoehenstufen_list.index(hsheute)<hoehenstufen_list.index(hszukunft) and check_Projektionspfad_Standortregion_NAISmatrix(naistypheute, hsheute, storeg, naishsregarr) is True:
                    NAISzukunft=Projektionspfad(naistypheute, storeg, hsheute, hszukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                    linestring=storeg+"\t"+hsheute+"\t"+hszukunft+"\t"+naistypheute+"\t"+NAISzukunft+"\t"+str(schatten)+"\t"+str(strahlungsreich)+"\t" +str(blockschutt)+"\t"+str(bodenverdichtet)+"\t" + str(trocken) + "\t" + str(kuppenlage) + "\t" + str(hanglage) + "\t" + str(muldenlage) + "\t" + str(hangneigung) + "\t" + str(VS) + "\t" + str(SH) + "\t" +"NA" + "\n"
                    if linestring not in outfilelineslist:
                        outfilelineslist.append(linestring)
for item in outfilelineslist:
    outtestfile.write(item)
outtestfile.close()



#manual test
#Projektionspfad("46t", "M", "Submontan", "Collin", False, False, False, False, False, False, False, False, False, False,59)



