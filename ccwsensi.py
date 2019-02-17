#Modellierung der Transformation von Waldstandorten im Klimawandel
#Das Modell ueberlagert eine NAIS-Waldstandortskartierung mit einer Karte der Hoehenstufenverschiebung und berechnet die im Klimawandel
#zu erwartenden Waldstandorte sowie die Baumarten, die auf dem jeweiligen Standort ausfallen bzw. neu aufkommen können
#Verfahren nach Frehner et al.
#Andreas Paul Zischg, 17.02.2019

import numpy
import arcpy
import sys
import os
sys.path.append("D:/CCW18sensi/code/ccwsensi")
os.chdir("D:/CCW18sensi/code/ccwsensi")#directory where this script is stored
print os.getcwd()
from ccwsensifunctions import *
#Grundaetzliche Bedingungen
#moegliche Hoehenstufen im Ausgangsfile
hoehenstufen=["CO", "SM","UM","OM","HM","SA","OSA"]
hoehenstufenids=[1,2,3,4,5,6,7]
#Liste der möglichen Standortsregionen
standortsregionenlist=["1","2a","2b","3","4","5a","5b","J","M"]
#hoehenstufe_heute, aus Hoehenstufenmodell abenis
hoehenstufen_heute_list=["obersubalpin", "subalpin", "hochmontan", "unter- und obermontan", "obermontan", "untermontan", "submontan", "collin mit Buche", "collin", "hyperinsubrisch"]
hoehenstufen_heute_list_modelliert=["hyperinsubrisch","collin","collin mit Buche","submontan","untermontan","obermontan","unter- und obermontan","hochmontan im Tannen-Hauptareal","hochmontan im Tannen-Nebenareal","hochmontan im Tannen-Reliktareal","hochmontan","subalpin","obersubalpin"]
#hoehenstufe_zukunft
hoehenstufe_zukunft_list=["obersubalpin", "subalpin", "hochmontan im Tannen-Reliktareal", "hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal", "unter- und obermontan", "obermontan", "untermontan", "submontan", "collin mit Buche", "collin", "hyperinsubrisch"]
#tannenareal_heute
tannenareal_heute_list=["Hauptareal", "Nebenareal", "Reliktareal"]
#schatten [True, False], strahlungsreich  [True, False], blockschutt  [True, False], bodenverdichtet [True, False]
#trocken [True, False], kuppenlage [True, False], hanglage [True, False], muldenlage [True, False]
#VS ... Standort ist im Wallis [True, False], SH ... Standort ist in Schaffhausen [True, False]
#output ist NAIS_StandortstypZukunft
#Erforderliche Parameter
VS=False #True, falls Datensatz im Kanton Wallis - wegen Spezialbedingungen
SH=False #True, falls Datensatz im Kanton Schaffhauesen - wegen Spezialbedingungen
bodenverdichtet=False #man hat diese Information bis dato nicht

#Parameterfiles
myworkspace = "D:/CCW18sensi"
arcpy.env.workspace=myworkspace
arcpy.env.overwriteOutput = True
if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.CheckOutExtension('Spatial')
else:
    print "no spatial analyst license available"
geodatabase= myworkspace+"/GIS/sensi.gdb"
parameterdir=myworkspace+"/parameter"
matrixbaumarten=parameterdir+"/Matrix_Baum_inkl_collin_AZ.csv" #Baumartenmatrix von Monika Frehner
hoehenstufenregionnaisstandorte=parameterdir+"/hoehenstufenregionnaisstandorte.csv" #Extract aus der Datenbank von IWA-Wald und Landschaft AG: bildet
outputfile=geodatabase+"/"+"sensiCLM"

#input Daten
#Originale Waldstandortskartierung nach NAIS.
#Muss folgende Spalten aufweisen: String-Feld mit dem Namen "NAISheute", String-Feld mit dem Namen "Standortre"
waldstandortskartierung=myworkspace+"/GIS/stoSG.shp"
#Mache eine Kopie an der gearbeitet wird
stoshape0 = arcpy.Select_analysis(waldstandortskartierung, myworkspace+"/GIS/sensi.gdb/stoshape0")
#Geroellflaechen
geroellshape= geodatabase+"/pri25_a_Geroell"
#Kuppen und Mulden-Raster 1-Ebene, 2-Hangfuss/Mulde, 3-Hang, 4-Kuppe
geldivreclcor=myworkspace+"/GIS/sglagecor"
strahlungsraster=myworkspace+"/GIS/sgglobradjw"
neigungsraster=myworkspace+"/GIS/sgslpprc2m"
hoehenstufenkarte_heute=geodatabase+"/"+"Hoehenstufen_heute"
hoehenstufenkarte_zukunft=geodatabase+"/"+"Hoehenstufen_CLM"
#hoehenstufe_heute, aus Hoehenstufenmodell abenis
hoehenstufen_heute_list=["obersubalpin", "subalpin", "hochmontan", "unter- und obermontan", "obermontan", "untermontan", "submontan", "collin mit Buche", "collin", "hyperinsubrisch"]
#hoehenstufe_zukunft
hoehenstufe_zukunft_list=["obersubalpin", "subalpin", "hochmontan im Tannen-Reliktareal", "hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Hauptareal", "unter- und obermontan", "obermontan", "untermontan", "submontan", "collin mit Buche", "collin", "hyperinsubrisch"]

#Outputfile
stoshape =geodatabase+"/"+"sensitiveFlaechen_CLM"


#Einlesen der Baumartenmatrix
matrixbaumartenarr=numpy.loadtxt(matrixbaumarten,delimiter=";", dtype='object')
matrixrows=numpy.shape(matrixbaumartenarr)[0]
matrixcols=numpy.shape(matrixbaumartenarr)[1]
naisstandortsliste_matrix=matrixbaumartenarr[0,1:]
print "Baumartenmatrix geladen ..."
#bereinige Sonderzeichen in erster Zeile, z.B. '53L\xe4' wird zu "58Lae"
j=0
while j<matrixcols:
    instr=matrixbaumartenarr[0,j]
    if "\xe4" in instr:
        matrixbaumartenarr[0, j]=instr.replace("\xe4","ae")
    j+=1

#Einlesen der NAIS-IWA Tabelle
naishsregarr=numpy.loadtxt(hoehenstufenregionnaisstandorte,delimiter=",", dtype='object')
hoehenstufen=["OSA","SA","HM","OM","UM","SM","C","UMOM"]
standortsregionenlist=["1","2a","2b","3","4","5a","5b","J","M"]
naisrows=numpy.shape(matrixbaumartenarr)[0]
naiscols=numpy.shape(matrixbaumartenarr)[1]
naisstandortsliste_naishsreg=naishsregarr[1:,0]
print "NAIS Hoehenstufen und Regionen Matrix geladen ..."

#Kontrolliere ob die NAIS-Typen uebereinstimmen
naistyp_inmatrixnotinnaishsreg=[]
naistyp_innaishsregnotinmatrix=[]
for item in naisstandortsliste_matrix:
    if item not in naisstandortsliste_naishsreg:
        naistyp_inmatrixnotinnaishsreg.append(item)
for item in naisstandortsliste_naishsreg:
    if item not in naisstandortsliste_matrix:
        naistyp_innaishsregnotinmatrix.append(item)
print "NAIS Typen in Baumartenmatrix aber nicht in Hoehenstufenregionen: "
print naistyp_inmatrixnotinnaishsreg
print "NAIS Typen in Hoehenstufenregionen aber nicht in Baumartenmatrix: "
print naistyp_innaishsregnotinmatrix

#************************************************************************************************
#Ergaenze den Datensatz mit den topographischen Standorteigenschaften Hangneigung, Kuppenlage, Muldenlage, Schatten, Strahlung, Blockschutt
#Verschneide den Input Datensatz (NAIS-Standortkartierung) mit weiteren Daten
#************************************************************************************************
#Blockschutt
arcpy.AddField_management(in_table=geroellshape, field_name="blockschutt", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=geroellshape, field="blockschutt", expression="1", expression_type="PYTHON", code_block="")
stoshape1=arcpy.Union_analysis(in_features=[stoshape0, geroellshape], out_feature_class=geodatabase+"/stoshape1", join_attributes="ALL", cluster_tolerance="", gaps="GAPS")
stoshape2= arcpy.Select_analysis(stoshape1, geodatabase+"/stoshape2", "NAISheute <> ''")
arcpy.DeleteField_management(in_table=stoshape2, drop_field="FID_pri25_a_Geroell")
#Kuppenlage und Muldenlage
#generalisiere das Gelaendedivergenz Raster
sglagecorg= myworkspace+"/GIS/sglagecorg" #generalisertes Raster
arcpy.gp.MajorityFilter_sa(geldivreclcor, sglagecorg, "FOUR", "MAJORITY")
sglagecorpg=geodatabase+"/sglagecorpg"
#convert Raster to Polygon
arcpy.RasterToPolygon_conversion(in_raster=sglagecorg, out_polygon_features=sglagecorpg, simplify="NO_SIMPLIFY", raster_field="VALUE", create_multipart_features="SINGLE_OUTER_PART", max_vertices_per_feature="")
#generalisiere das Polygon
arcpy.MakeFeatureLayer_management(in_features=sglagecorpg, out_layer="sglagecorpg_Layer", where_clause="", workspace="", field_info="OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Id Id VISIBLE NONE;gridcode gridcode VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="sglagecorpg_Layer", selection_type="NEW_SELECTION", where_clause="Shape_Area <=300")
sglagecorpg2=geodatabase+"/sglagecorpg2"
arcpy.Eliminate_management(in_features="sglagecorpg_Layer", out_feature_class=sglagecorpg2, selection="AREA", ex_where_clause="", ex_features="")
#Fuege Attribute hinzu
arcpy.AddField_management(in_table=sglagecorpg2, field_name="kuppenlage", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=sglagecorpg2, field_name="hanglage", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=sglagecorpg2, field_name="muldenlage", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
#berechne diese Spalten
arcpy.CalculateField_management(in_table=sglagecorpg2, field="kuppenlage", expression="decis( !gridcode!)", expression_type="PYTHON", code_block="def decis(y):\n    if y==4: \n        x=1\n    else:\n        x=0\n    return x")
arcpy.CalculateField_management(in_table=sglagecorpg2, field="hanglage", expression="decis( !gridcode!)", expression_type="PYTHON", code_block="def decis(y):\n    if y==3: \n        x=1\n    else:\n        x=0\n    return x")
arcpy.CalculateField_management(in_table=sglagecorpg2, field="muldenlage", expression="decis( !gridcode!)", expression_type="PYTHON", code_block="def decis(y):\n    if y==2: \n        x=1\n    else:\n        x=0\n    return x")
#Union zwischen Standortskarte und Gelaendelagekarte
stoshape3=arcpy.Union_analysis(in_features=[stoshape2, sglagecorpg2], out_feature_class=geodatabase+"/stoshape3", join_attributes="ALL", cluster_tolerance="", gaps="GAPS")
stoshape4= arcpy.Select_analysis(stoshape3, geodatabase+"/stoshape4", "NAISheute <> ''")
arcpy.DeleteField_management(in_table=stoshape4, drop_field="FID_stoshape2;FID_stoshape0;FID_sglagecorpg2;Id;gridcode")
#generalisierie kleine Flaechen
arcpy.MakeFeatureLayer_management(in_features=stoshape4, out_layer="stoshape4_Layer", where_clause="", workspace="", field_info="OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Id Id VISIBLE NONE;gridcode gridcode VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")
arcpy.SelectLayerByAttribute_management(in_layer_or_view="stoshape4_Layer", selection_type="NEW_SELECTION", where_clause="Shape_Area <=600") #das ist ein wichtiger Faktor der Minimalgroesse von Polygons zum Generalisieren (600 m2)
stoshape5=geodatabase+"/stoshape5"
arcpy.Eliminate_management(in_features="stoshape4_Layer", out_feature_class=stoshape5, selection="AREA", ex_where_clause="", ex_features="")
#add fields schatten, strahlungsreich, trocken, hangneigung
arcpy.AddField_management(in_table=stoshape5, field_name="schatten", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape5, field_name="strahlungsreich", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape5, field_name="trocken", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape5, field_name="hangneigung", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.DeleteField_management(in_table=stoshape5, drop_field="OBJECTID")
#Berechne Hangneigung
zonstatneig=geodatabase+"/zonstatneig"
arcpy.gp.ZonalStatisticsAsTable_sa(stoshape5, "OBJECTID_1", neigungsraster, zonstatneig, "DATA", "MEAN")
arcpy.MakeFeatureLayer_management(in_features=stoshape5, out_layer="stoshape5_Layer", where_clause="", workspace="", field_info="OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Id Id VISIBLE NONE;gridcode gridcode VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE")
#arcpy.AddJoin_management(in_layer_or_view="stoshape5_Layer", in_field="OBJECTID_1", join_table=zonstatneig, join_field="OBJECTID_1", join_type="KEEP_ALL")
arcpy.JoinField_management(in_data="stoshape5", in_field="OBJECTID_1", join_table="zonstatneig", join_field="OBJECTID_1", fields="MEAN")
arcpy.CalculateField_management(in_table=stoshape5, field="hangneigung", expression="hangn( !MEAN!)", expression_type="PYTHON_9.3", code_block="def hangn(y):\n    if y>=0:\n        return y")
arcpy.DeleteField_management(in_table=stoshape5, drop_field="MEAN")
#Berechne Attribut Strahlungsreich: Oberstes 20% Quantil Strahlung und Attribut Schatten: Unterstes 20% Quantile Strahlung
#Berechne Attribut trocken (Strahlungsreich==1 und Muldenlage ==0)
strahlungsrasterarr=arcpy.RasterToNumPyArray(arcpy.Raster(strahlungsraster))
threshold_strahlungsreich=numpy.percentile(strahlungsrasterarr, 80)
threshold_schatten=numpy.percentile(strahlungsrasterarr, 20)
numpy.max(strahlungsrasterarr)
numpy.min(strahlungsrasterarr)
zonstatstrahlung=geodatabase+"/zonstatstrahlung"
arcpy.gp.ZonalStatisticsAsTable_sa(stoshape5, "OBJECTID_1", strahlungsraster, zonstatstrahlung, "DATA", "MEAN")
arcpy.JoinField_management(in_data=stoshape5, in_field="OBJECTID_1", join_table=zonstatstrahlung, join_field="OBJECTID_1", fields="MEAN")
fields=["MEAN", "strahlungsreich", "trocken", "schatten", "muldenlage"]
with arcpy.da.UpdateCursor(stoshape5, fields) as cursor:
    for row in cursor:
        strahlung = row[0]
        if strahlung >=threshold_strahlungsreich:
            row[1]=1
        else:
            row[1] = 0
        if strahlung <=threshold_schatten:
            row[3] = 1
        else:
            row[3] = 0
        if row[1]==1 and row[4]==0:
            row[2]=1
        else:
            row[2] = 0
        cursor.updateRow(row)
arcpy.DeleteField_management(in_table=stoshape5, drop_field="MEAN")
#loesche die kleinen Flaechen
stoshape6=geodatabase+"/stoshape6"
arcpy.Select_analysis(in_features=stoshape5, out_feature_class=stoshape6, where_clause="Shape_Area >300")
#**********************************************************
#Ueberlagerung von mit der Hoehenstufenmodellierung HEUTE
wuk_heute=geodatabase+"/wuk_heute"
arcpy.Select_analysis(in_features=hoehenstufenkarte_heute, out_feature_class=wuk_heute, where_clause="")
arcpy.DeleteField_management(in_table=wuk_heute, drop_field="HS;sample;region;HS_text;collin;Buche;Standortre;Tannenarea;Kombi;StoregKomb;Buchenarea;BuBIN;Lithonew7g;Buchenar_1;Region_CO;dhm_1000;Areal;Tanne;tjulmax")
stoshape7=arcpy.Union_analysis(in_features=[stoshape6,wuk_heute], out_feature_class=geodatabase+"/stoshape7", join_attributes="ALL", cluster_tolerance="", gaps="GAPS")
arcpy.DeleteField_management(in_table=stoshape7, drop_field="FID_wuk_heute;FID_stoshape6")
stoshape8= geodatabase+"/stoshape8"
arcpy.Select_analysis(stoshape7, stoshape8, "NAISheute <> ''")
#**********************************************************
#Ueberlagerung mit der Hoehenstufenmodellierung ZUKUNFT
wuk_zukunft=geodatabase+"/wuk_zukunft"
arcpy.Select_analysis(in_features=hoehenstufenkarte_zukunft, out_feature_class=wuk_zukunft, where_clause="")
arcpy.DeleteField_management(in_table=wuk_zukunft, drop_field="HS;sample;region;HS_text;collin;Buche;Standortre;Tannenarea;Kombi;StoregKomb;Buchenarea;BuBIN;Lithonew7g;Region_CO;dhm_1400;Buchenar_1;Areal;CH_Karte;tjulmax")
stoshape9=geodatabase+"/stoshape9"
arcpy.Union_analysis(in_features=[stoshape8,wuk_zukunft], out_feature_class=stoshape9, join_attributes="ALL", cluster_tolerance="", gaps="GAPS")
arcpy.DeleteField_management(in_table=stoshape9, drop_field="FID_stoshape8;FID_stoshape6;Shape_Leng;FID_wuk_zukunft")
stoshape10=geodatabase+"/stoshape10"
arcpy.Select_analysis(stoshape9, stoshape10, "NAISheute <> '' AND HS_1 <> ''")
arcpy.DeleteField_management(in_table=stoshape10, drop_field="GRIDCODE;GRIDCODE_1")
#**********************************************************
#nimm Uebergaenge und kombinierte Standorte auseinander
#spalte mosaik. 0=kein Mosaik, 1=Mosaik
arcpy.AddField_management(in_table=stoshape10, field_name="mosaik", field_type="SHORT", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=stoshape10, field="mosaik", expression="0", expression_type="PYTHON", code_block="")
#spalte Uebergang. 0=kein Uebergang, 1=Uebergang
arcpy.AddField_management(in_table=stoshape10, field_name="uebergang", field_type="SHORT", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=stoshape10, field="uebergang", expression="0", expression_type="PYTHON", code_block="")
#Teile NAISheute in zwei Spalten auf: Hauptstandortstyp und Nebenstandortstyp
arcpy.AddField_management(in_table=stoshape10, field_name="NAISheuteHaupt", field_type="TEXT", field_precision="", field_scale="", field_length="10", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape10, field_name="NAISheuteNeben", field_type="TEXT", field_precision="", field_scale="", field_length="10", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.CalculateField_management(in_table=stoshape10, field="NAISheuteHaupt", expression="''", expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape10, field="NAISheuteNeben", expression="''", expression_type="PYTHON", code_block="")
#berechne die Spalten Uebergang und Mosaik sowie die Spalten Haupt- und Nebenstandortstyp
cursor1 = arcpy.da.UpdateCursor(stoshape10, ['NAISheute',"mosaik","uebergang","NAISheuteHaupt","NAISheuteNeben"])
#loop through the shapefile
for row in cursor1:
    xtempstr=""
    # read the values in the row
    NAISheute=row[0].replace("/u","")
    if "/" in NAISheute:
        xtempstr=NAISheute.replace("/"," ")
        row[1]=1
        row[2]=0
        row[3]=str(xtempstr.strip().split()[0])
        row[4]=str(xtempstr.strip().split()[1])
    elif "(" in NAISheute:
        xtempstr=NAISheute.replace("("," ")
        xtempstr = xtempstr.replace(')', "")
        row[1] = 0
        row[2] = 1
        row[3] = str(xtempstr.strip().split()[0])
        row[4] = str(xtempstr.strip().split()[1])
    elif NAISheute=="":
        row[1] = 0
        row[2] = 0
        row[3] = ""
        row[4] = ""
    else:
        row[1] = 0
        row[2] = 0
        row[3] = str(NAISheute)
        row[4] = ""
    cursor1.updateRow(row)
cursor1.reset()
del cursor1
#**********************************************************
#Kontrolliere die Hoehenstufenmodellierung heute
#wenn der NAIStyp nicht zusammenstimmt mit der NAIS-Tabelle von IWA, korrigiere die Hoehenstufe heute
#hoenstufenabkuerzungendict={"hyperinsubrisch":"HYP","collin":"C","collin mit Buche":"C","submontan":"SM","untermontan":"UM","obermontan":"OM","unter- und obermontan":"UMOM","hochmontan im Tannen-Hauptareal":"HM","hochmontan im Tannen-Nebenareal":"HM","hochmontan im Tannen-Reliktareal":"HM","hochmontan":"HM","subalpin":"SA","obersubalpin":"OSA"}
#hoehenstufenabkuerzungendict2={"HYP":"hyperinsubrisch","C":"collin", "SM":"submontan","UM":"untermontan","OM":"obermontan","UMOM":"unter- und obermontan", "HM":"hochmontan","SA":"subalpin","OSA":"obersubalpin"}
cursor2 = arcpy.da.UpdateCursor(stoshape10, ['NAISheuteHaupt', 'Standortre',"HS_2","Tannenarea"])
#moegliche Standortregionen: 1,2a,2b,3,4,5,5a,5b,J,M
for row in cursor2:
    naisheute=row[0]
    storeg=row[1]
    if row[2] in hoehenstufen_heute_list_modelliert:
        hoehenstufe_heute=row[2]
        #hoehenstufe_heute_kurz=hoenstufenabkuerzungendict[hoehenstufe_heute]
        if row[3]=="Reliktareal":
            Tannenareal = "Reliktareal"
        elif row[3] == "Nebenareal":
            Tannenareal = "Nebenareal"
        else:
            Tannenareal = "Hauptareal"
        if "Reliktareal" in row[2]:
            Tannenareal = "Reliktareal"
        elif "Nebenareal" in row[2]:
            Tannenareal = "Nebenareal"
        check=check_hoehenstufe_langeLegende(naisheute, hoehenstufe_heute, storeg, Tannenareal, naishsregarr)
        if check[0]==False:
            row[2] = check[2]
        cursor2.updateRow(row)
cursor2.reset()
del cursor2

#*******************************************************************************
#Bereite den output file vor
#*******************************************************************************
arcpy.Select_analysis(stoshape10, stoshape)
#delete existing fields
#arcpy.DeleteField_management(in_table=stoshape, drop_field="mosaik;uebergang;XStandortZukunft;XheuteFoerdern;XheuteMitnehmen;XheuteReduzieren;XheuteAchtung;XZukunftFoerdern;XZukunftMitnehmen;XZukunftAchtung;YStandortZukunft;YheuteFoerdern;YheuteMitnehmen;YheuteReduzieren;YheuteAchtung;YZukunftFoerdern;YZukunftMitnehmen;YZukunftAchtung")
#Mosaik Standortstyp X
arcpy.AddField_management(in_table=stoshape, field_name="XStandortZukunft", field_type="TEXT", field_precision="", field_scale="", field_length="10", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="XheuteFoerdern", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="XheuteMitnehmen", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="XheuteReduzieren", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="XheuteAchtung", field_type="TEXT", field_precision="", field_scale="", field_length="250", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="XZukunftFoerdern", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="XZukunftMitnehmen", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="XZukunftAchtung", field_type="TEXT", field_precision="", field_scale="", field_length="250", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
#Mosaik Standortstyp Y
arcpy.AddField_management(in_table=stoshape, field_name="YStandortZukunft", field_type="TEXT", field_precision="", field_scale="", field_length="10", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="YheuteFoerdern", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="YheuteMitnehmen", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="YheuteReduzieren", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="YheuteAchtung", field_type="TEXT", field_precision="", field_scale="", field_length="250", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="YZukunftFoerdern", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="YZukunftMitnehmen", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="YZukunftAchtung", field_type="TEXT", field_precision="", field_scale="", field_length="250", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")

#delete attributes in case the columns are already existing
arcpy.CalculateField_management(in_table=stoshape, field="XStandortZukunft", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="XheuteFoerdern", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="XheuteMitnehmen", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="XheuteReduzieren", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="XheuteAchtung", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="XZukunftFoerdern", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="XZukunftMitnehmen", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="XZukunftAchtung", expression='""', expression_type="PYTHON", code_block="")

arcpy.CalculateField_management(in_table=stoshape, field="YStandortZukunft", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="YheuteFoerdern", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="YheuteMitnehmen", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="YheuteReduzieren", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="YheuteAchtung", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="YZukunftFoerdern", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="YZukunftMitnehmen", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="YZukunftAchtung", expression='""', expression_type="PYTHON", code_block="")


#*******************************************************************************
#Kontrolliere ob Hoehenstufe Zukunft gleich oder hoeher ist als Hoehenstufe heute
#*******************************************************************************
cursor5 = arcpy.da.UpdateCursor(stoshape, ['HS_1', 'HS_2',"HS_1z","HS_2z"])
#moegliche Standortregionen: 1,2a,2b,3,4,5,5a,5b,J,M
for row in cursor5:
    HS_1 = row[0]
    HS_2 = row[1]
    HS_1z = row[2]
    HS_2z = row[3]
    if HS_1 =="collin" and HS_1z in ["submontan","untermontan","obermontan","hochmontan","subalpin","obersubalpin"]:
        HS_1z=HS_1
    elif HS_1=="submontan" and HS_1z in ["untermontan","obermontan","hochmontan","subalpin","obersubalpin"]:
        HS_1z = HS_1
    elif HS_1 == "untermontan" and HS_1z in ["obermontan", "hochmontan", "subalpin", "obersubalpin"]:
        HS_1z = HS_1
    elif HS_1 == "obermontan" and HS_1z in ["hochmontan", "subalpin", "obersubalpin"]:
        HS_1z = HS_1
    elif HS_1 == "hochmontan" and HS_1z in ["subalpin", "obersubalpin"]:
        HS_1z = HS_1
    elif HS_1 == "subalpin" and HS_1z in ["obersubalpin"]:
        HS_1z = HS_1
    #****************
    if HS_2 in ["collin", "collin mit Buche"] and HS_2z in ["submontan","untermontan","obermontan","unter- und obermontan","hochmontan","hochmontan im Tannen-Hauptareal","hochmontan im Tannen-Nebenareal","hochmontan im Tannen-Reliktareal","subalpin","obersubalpin"]:
        HS_2z=HS_2
    elif HS_2=="submontan" and HS_1z in ["untermontan","obermontan","unter- und obermontan","hochmontan","hochmontan im Tannen-Hauptareal","hochmontan im Tannen-Nebenareal","hochmontan im Tannen-Reliktareal","subalpin","obersubalpin"]:
        HS_2z = HS_2
    elif HS_2 == "untermontan" and HS_1z in ["obermontan","hochmontan","hochmontan im Tannen-Hauptareal","hochmontan im Tannen-Nebenareal","hochmontan im Tannen-Reliktareal","subalpin","obersubalpin"]:
        HS_2z = HS_2
    elif HS_2 == "unter- und obermontan" and HS_1z in ["hochmontan","hochmontan im Tannen-Hauptareal","hochmontan im Tannen-Nebenareal","hochmontan im Tannen-Reliktareal","subalpin","obersubalpin"]:
        HS_2z = HS_2
    elif HS_2 == "obermontan" and HS_1z in ["hochmontan","hochmontan im Tannen-Hauptareal","hochmontan im Tannen-Nebenareal","hochmontan im Tannen-Reliktareal","subalpin","obersubalpin"]:
        HS_2z = HS_2
    elif HS_2 in ["hochmontan","hochmontan im Tannen-Hauptareal","hochmontan im Tannen-Nebenareal","hochmontan im Tannen-Reliktareal"] and HS_1z in ["subalpin", "obersubalpin"]:
        HS_2z = HS_2
    elif HS_2 == "subalpin" and HS_1z in ["obersubalpin"]:
        HS_2z = HS_2
    row[2]=HS_1z
    row[3]=HS_2z
    cursor5.updateRow(row)
cursor5.reset()
del cursor5


#*******************************************************************************
#Berechnung des neuen Standortstyps nach Wechsel der Hoehenstufe
#*******************************************************************************
#feature cursor
cursor = arcpy.da.UpdateCursor(stoshape, ['NAISheute', 'Standortre',"HS_2", "HS_2z", "schatten", "strahlungsreich", "blockschutt", "trocken", "kuppenlage", "hanglage", "muldenlage", "hangneigung","mosaik", "uebergang", "XStandortZukunft","XheuteFoerdern","XheuteMitnehmen","XheuteReduzieren","XheuteAchtung","XZukunftFoerdern","XZukunftMitnehmen", "XZukunftAchtung","YStandortZukunft","YheuteFoerdern","YheuteMitnehmen","YheuteReduzieren","YheuteAchtung","YZukunftFoerdern","YZukunftMitnehmen", "YZukunftAchtung"])
#12 "mosaik", 13 "uebergang",
#14 "XStandortZukunft",15 "XheuteFoerdern",16 "XheuteMitnehmen",17 "XheuteReduzieren",18 "XheuteAchtung",19 "XZukunftFoerdern",20 "XZukunftMitnehmen",21 "XZukunftAchtung",
#22 "YStandortZukunft",23 "YheuteFoerdern","24 YheuteMitnehmen",25 "YheuteReduzieren",26 "YheuteAchtung",27 "YZukunftFoerdern",28 "YZukunftMitnehmen",29 "YZukunftAchtung"])
#loop through the shapefile
#cursor.reset()
for row in cursor:
    #print row[0]
    mosaik=row[12]
    uebergang=row[13]
    # read the values in the row
    NAISheute=row[0]
    NAIS_StandortstypHeute=[]
    NAISheute = row[0].replace("/u", "")
    if "/" in NAISheute:
        xtempstr=NAISheute.replace("/"," ")
        NAIS_StandortstypHeute.append(xtempstr.strip().split()[0])
        NAIS_StandortstypHeute.append(xtempstr.strip().split()[1])
        mosaik=1
        uebergang = 0
    elif "(" in NAISheute:
        xtempstr=NAISheute.replace("("," ")
        xtempstr = xtempstr.replace(')', "")
        NAIS_StandortstypHeute.append(xtempstr.strip().split()[0])
        NAIS_StandortstypHeute.append(xtempstr.strip().split()[1])
        uebergang=1
        mosaik = 0
    else:
        NAIS_StandortstypHeute.append(NAISheute.strip().split()[0])
        mosaik = 0
        uebergang = 0
    #schreibe Ergebnis in die entsprechenden Spalten. Spalte 12 = mosaik, Spalte 13 = uebergang
    row[12] = mosaik
    row[13] = uebergang
    standortsregion = row[1]
    hoehenstufe_heute = row[2]#.lower()
    hoehenstufe_zukunft = row[3]#.lower()
    if row[4] == 1:
        schatten = True
    else:
        schatten = False
    if row[5] == 1:
        strahlungsreich = True
    else:
        strahlungsreich = False
    if row[6] == 1:
        blockschutt = True
    else:
        blockschutt = False
    if row[7] == 1:
        trocken = True
    else:
        trocken = False
    if row[8] == 1:
        kuppenlage = True
    else:
        kuppenlage = False
    if row[9] == 1:
        hanglage = True
    else:
        hanglage = False
    if row[10] == 1:
        muldenlage = True
    else:
        muldenlage = False
    hangneigung = row[11]
    # *******************************************************************************
    ListeStandortstypZukunft=[]
    if len(NAIS_StandortstypHeute)>0 and len(NAIS_StandortstypHeute)<3:
        #Berechne den Standortstyp in Zukunft jeweils für Haupt- und Nebenstandort
        for item in NAIS_StandortstypHeute:
            NAIS_StandortstypZukunft = "NA"
            tempNAIS1 = "NA"
            tempNAIS2 = "NA"
            tempNAIS3 = "NA"
            tempNAIS4 = "NA"
            tempNAIS5 = "NA"
            tempNAIS6 = "NA"
            if standortsregion in ["J","M","1","2","2a","2b","3"]:
                if hoehenstufe_heute==hoehenstufe_zukunft:
                    NAIS_StandortstypZukunft = item
                else:
                    if hoehenstufe_heute=="obersubalpin":
                        if hoehenstufe_zukunft == "subalpin":
                            NAIS_StandortstypZukunft=Projektionspfad_regJM12a2b3_OSA_SA(item, standortsregion, hoehenstufe_heute,hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet,trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft in ["hochmontan im Tannen-Hauptareal", "hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Reliktareal"]:
                            tempNAIS1=Projektionspfad_regJM12a2b3_OSA_SA(item, standortsregion, hoehenstufe_heute, "subalpin", schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                            if hoehenstufe_zukunft == "hochmontan im Tannen-Hauptareal":
                                NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_SA_HMTannenHaupt(tempNAIS1, standortsregion,"subalpin",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet,trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            elif hoehenstufe_zukunft == "hochmontan im Tannen-Nebenareal":
                                NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_SA_HMTannenNeben(tempNAIS1, standortsregion,"subalpin",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet,trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            elif hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
                                NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_SA_HMTannenRelikt(tempNAIS1, standortsregion,"subalpin",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet,trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft =="obermontan":
                            #hier koennte man noch die Abfrage nach Art des Tannenareals einbauen, wenn man die Tannenareal-Karte fuer die Zukunft explizit haette
                            tempNAIS1 = Projektionspfad_regJM12a2b3_OSA_SA(item, standortsregion,hoehenstufe_heute, "subalpin", schatten, strahlungsreich,blockschutt, bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS2 = Projektionspfad_regJM12a2b3_SA_HMTannenHaupt(tempNAIS1, standortsregion,"subalpin","hochmontan im Tannen-Hauptareal",schatten, strahlungsreich,blockschutt,bodenverdichtet, trocken,kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft =Projektionspfad_regJM12a2b3_HM_OM(tempNAIS2, standortsregion, "hochmontan",hoehenstufe_zukunft,schatten, strahlungsreich,blockschutt,bodenverdichtet, trocken,kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "untermontan":
                            tempNAIS1 = Projektionspfad_regJM12a2b3_OSA_SA(item, standortsregion, hoehenstufe_heute, "subalpin", schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                            if standortsregion in ["2b","3"]:
                                #hier Fragezeichen Relikt oder Nebenareal
                                tempNAIS2=Projektionspfad_regJM12a2b3_SA_HMTannenNeben(tempNAIS1, standortsregion, "subalpin","hochmontan im Tannen-Nebenareal", schatten,strahlungsreich, blockschutt, bodenverdichtet,trocken, kuppenlage, hanglage, muldenlage, VS,SH,hangneigung)
                            else:
                                tempNAIS2 = Projektionspfad_regJM12a2b3_SA_HMTannenHaupt(tempNAIS1, standortsregion, "subalpin","hochmontan im Tannen-Hauptareal", schatten,strahlungsreich, blockschutt, bodenverdichtet,trocken, kuppenlage, hanglage, muldenlage, VS,SH,hangneigung)
                            tempNAIS3 = Projektionspfad_regJM12a2b3_HM_OM(tempNAIS2, standortsregion, "hochmontan","obermontan", schatten,strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft=Projektionspfad_regJM12a2b3_OM_UM(tempNAIS3, standortsregion, "obermontan",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "submontan":
                            tempNAIS1 = Projektionspfad_regJM12a2b3_OSA_SA(item, standortsregion,hoehenstufe_heute, "subalpin", schatten,strahlungsreich, blockschutt, bodenverdichtet,trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                            if standortsregion in ["2b", "3"]:
                                # hier Fragezeichen Relikt oder Nebenareal
                                tempNAIS2 = Projektionspfad_regJM12a2b3_SA_HMTannenNeben(tempNAIS1, standortsregion, "subalpin","hochmontan im Tannen-Nebenareal",schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            else:
                                tempNAIS2 = Projektionspfad_regJM12a2b3_SA_HMTannenHaupt(tempNAIS1, standortsregion, "subalpin","hochmontan im Tannen-Hauptareal",schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS3 = Projektionspfad_regJM12a2b3_HM_OM(tempNAIS2, standortsregion, "hochmontan","obermontan", schatten, strahlungsreich,blockschutt, bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS4 = Projektionspfad_regJM12a2b3_OM_UM(tempNAIS3, standortsregion,"obermontan", "untermontan",schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft =Projektionspfad_regJM12a2b3_UM_SM(tempNAIS4, standortsregion,"untermontan", hoehenstufe_zukunft,schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "collin":
                            tempNAIS1 = Projektionspfad_regJM12a2b3_OSA_SA(item, standortsregion,hoehenstufe_heute, "subalpin", schatten, strahlungsreich,blockschutt, bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            if standortsregion in ["2b", "3"]:
                                # hier Fragezeichen Relikt oder Nebenareal
                                tempNAIS2 = Projektionspfad_regJM12a2b3_SA_HMTannenNeben(tempNAIS1, standortsregion, "subalpin","hochmontan im Tannen-Nebenareal",schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            else:
                                tempNAIS2 = Projektionspfad_regJM12a2b3_SA_HMTannenHaupt(tempNAIS1, standortsregion, "subalpin","hochmontan im Tannen-Hauptareal",schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS3 = Projektionspfad_regJM12a2b3_HM_OM(tempNAIS2, standortsregion, "hochmontan","obermontan", schatten, strahlungsreich,blockschutt, bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS4 = Projektionspfad_regJM12a2b3_OM_UM(tempNAIS3, standortsregion, "obermontan","untermontan", schatten, strahlungsreich,blockschutt, bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS5 = Projektionspfad_regJM12a2b3_UM_SM(tempNAIS4, standortsregion, "untermontan","submontan", schatten,strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            if standortsregion in ["J","M","1","2a"]:
                                NAIS_StandortstypZukunft =Projektionspfad_regJM12a2b3_SM_CO(tempNAIS5, standortsregion, "submontan",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            elif standortsregion in ["2b","3"]:
                                NAIS_StandortstypZukunft =Projektionspfad_regJM12a2b3_SM_CO(tempNAIS5, standortsregion, "submontan", hoehenstufe_zukunft,
                                                                  schatten, strahlungsreich, blockschutt, bodenverdichtet,
                                                                  trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                    elif hoehenstufe_heute=="subalpin":
                        if hoehenstufe_zukunft in ["hochmontan im Tannen-Hauptareal", "hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Reliktareal"]:
                            if hoehenstufe_zukunft == "hochmontan im Tannen-Hauptareal":
                                NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_SA_HMTannenHaupt(item, standortsregion,"subalpin",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet,trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            elif hoehenstufe_zukunft == "hochmontan im Tannen-Nebenareal":
                                NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_SA_HMTannenNeben(item, standortsregion,"subalpin",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet,trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            elif hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
                                NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_SA_HMTannenRelikt(item, standortsregion,"subalpin",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet,trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft =="obermontan":
                            #hier koennte man noch zwischen Haupt- Neben und Reliktareal unterscheiden
                            tempNAIS1 = Projektionspfad_regJM12a2b3_SA_HMTannenHaupt(item, standortsregion,hoehenstufe_heute,"hochmontan im Tannen-Hauptareal",schatten, strahlungsreich,blockschutt,bodenverdichtet, trocken,kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft =Projektionspfad_regJM12a2b3_HM_OM(tempNAIS1, standortsregion, "hochmontan",hoehenstufe_zukunft,schatten, strahlungsreich,blockschutt,bodenverdichtet, trocken,kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "untermontan":
                            if standortsregion in ["2b","3"]:
                                tempNAIS1=Projektionspfad_regJM12a2b3_SA_HMTannenNeben(item, standortsregion, "subalpin","hochmontan im Tannen-Nebenareal", schatten,strahlungsreich, blockschutt, bodenverdichtet,trocken, kuppenlage, hanglage, muldenlage, VS,SH,hangneigung)
                            else:
                                tempNAIS1 = Projektionspfad_regJM12a2b3_SA_HMTannenHaupt(item, standortsregion, "subalpin","hochmontan im Tannen-Hauptareal", schatten,strahlungsreich, blockschutt, bodenverdichtet,trocken, kuppenlage, hanglage, muldenlage, VS,SH,hangneigung)
                            tempNAIS2 = Projektionspfad_regJM12a2b3_HM_OM(tempNAIS1, standortsregion, "hochmontan","obermontan", schatten,strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft=Projektionspfad_regJM12a2b3_OM_UM(tempNAIS2, standortsregion, "obermontan",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "submontan":
                            if standortsregion in ["2b", "3"]:
                                tempNAIS1 = Projektionspfad_regJM12a2b3_SA_HMTannenNeben(item, standortsregion, "subalpin","hochmontan im Tannen-Nebenareal",schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            else:
                                tempNAIS1 = Projektionspfad_regJM12a2b3_SA_HMTannenHaupt(item, standortsregion, "subalpin","hochmontan im Tannen-Hauptareal",schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS2 = Projektionspfad_regJM12a2b3_HM_OM(tempNAIS1, standortsregion, "hochmontan","obermontan", schatten, strahlungsreich,blockschutt, bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS3 = Projektionspfad_regJM12a2b3_OM_UM(tempNAIS2, standortsregion,"obermontan", "untermontan",schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft=Projektionspfad_regJM12a2b3_UM_SM(tempNAIS3, standortsregion,"untermontan", hoehenstufe_zukunft,schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "collin":
                            if standortsregion in ["2b", "3"]:
                                tempNAIS1 = Projektionspfad_regJM12a2b3_SA_HMTannenNeben(item, standortsregion, "subalpin","hochmontan im Tannen-Nebenareal",schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            else:
                                tempNAIS2 = Projektionspfad_regJM12a2b3_SA_HMTannenHaupt(tempNAIS1, standortsregion, "subalpin","hochmontan im Tannen-Hauptareal",schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS3 = Projektionspfad_regJM12a2b3_HM_OM(tempNAIS2, standortsregion, "hochmontan","obermontan", schatten, strahlungsreich,blockschutt, bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS4 = Projektionspfad_regJM12a2b3_OM_UM(tempNAIS3, standortsregion, "obermontan","untermontan", schatten, strahlungsreich,blockschutt, bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS5 = Projektionspfad_regJM12a2b3_UM_SM(tempNAIS4, standortsregion, "untermontan","submontan", schatten,strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            if standortsregion in ["J","M","1","2a"]:
                                NAIS_StandortstypZukunft =Projektionspfad_regJM12a2b3_SM_CO(tempNAIS5, standortsregion, "submontan",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                            elif standortsregion in ["2b","3"]:
                                NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_SM_CO(tempNAIS5, standortsregion,
                                                                                             "submontan",
                                                                                             hoehenstufe_zukunft, schatten,
                                                                                             strahlungsreich, blockschutt,
                                                                                             bodenverdichtet, trocken,
                                                                                             kuppenlage, hanglage,
                                                                                             muldenlage, VS, SH,hangneigung)
                    elif "hochmontan" in hoehenstufe_heute:
                        if hoehenstufe_zukunft == "obermontan":
                            NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_HM_OM(item, standortsregion,"hochmontan", hoehenstufe_zukunft,schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "untermontan":
                            tempNAIS1 = Projektionspfad_regJM12a2b3_HM_OM(item, standortsregion, "hochmontan", "obermontan", schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_OM_UM(tempNAIS1, standortsregion,"obermontan", hoehenstufe_zukunft,schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "submontan":
                            tempNAIS1 = Projektionspfad_regJM12a2b3_HM_OM(item, standortsregion, "hochmontan","obermontan", schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            tempNAIS2 = Projektionspfad_regJM12a2b3_OM_UM(tempNAIS1, standortsregion, "obermontan","untermontan", schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_UM_SM(tempNAIS2, standortsregion,"untermontan", hoehenstufe_zukunft,schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "collin":
                            tempNAIS1 = Projektionspfad_regJM12a2b3_HM_OM(item, standortsregion, "hochmontan","obermontan", schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            tempNAIS2 = Projektionspfad_regJM12a2b3_OM_UM(tempNAIS1, standortsregion, "obermontan","untermontan", schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            tempNAIS3 = Projektionspfad_regJM12a2b3_UM_SM(tempNAIS2, standortsregion, "untermontan", "submontan", schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                            if standortsregion in ["J", "M", "1", "2a"]:
                                NAIS_StandortstypZukunft=Projektionspfad_regJM12a2b3_SM_CO(tempNAIS3, standortsregion, "submontan", hoehenstufe_zukunft,schatten, strahlungsreich, blockschutt, bodenverdichtet,trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                            elif standortsregion in ["2b", "3"]:
                                NAIS_StandortstypZukunft=Projektionspfad_regJM12a2b3_SM_CO(tempNAIS3, standortsregion, "submontan", hoehenstufe_zukunft,
                                                                  schatten, strahlungsreich, blockschutt, bodenverdichtet,
                                                                  trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                    elif "ober" in hoehenstufe_heute:
                        if hoehenstufe_zukunft == "untermontan":
                            NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_OM_UM(item, standortsregion,"obermontan", hoehenstufe_zukunft,schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "submontan":
                            tempNAIS1 = Projektionspfad_regJM12a2b3_OM_UM(item, standortsregion, "obermontan","untermontan", schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_UM_SM(tempNAIS1, standortsregion,"untermontan", hoehenstufe_zukunft,schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "collin":
                            tempNAIS1 = Projektionspfad_regJM12a2b3_OM_UM(item, standortsregion, "obermontan","untermontan", schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            tempNAIS2 = Projektionspfad_regJM12a2b3_UM_SM(tempNAIS1, standortsregion, "untermontan", "submontan", schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                            if standortsregion in ["J", "M", "1", "2a"]:
                                NAIS_StandortstypZukunft=Projektionspfad_regJM12a2b3_SM_CO(tempNAIS2, standortsregion, "submontan", hoehenstufe_zukunft,schatten, strahlungsreich, blockschutt, bodenverdichtet,trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                            elif standortsregion in ["2b", "3"]:
                                NAIS_StandortstypZukunft=Projektionspfad_regJM12a2b3_SM_CO(tempNAIS2, standortsregion, "submontan", hoehenstufe_zukunft,
                                                                  schatten, strahlungsreich, blockschutt, bodenverdichtet,
                                                                  trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                    elif hoehenstufe_heute == "untermontan":
                        if hoehenstufe_zukunft == "submontan":
                            NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_UM_SM(item, standortsregion,"untermontan", hoehenstufe_zukunft,schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "collin":
                            tempNAIS1 = Projektionspfad_regJM12a2b3_UM_SM(item, standortsregion, "untermontan","submontan", schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            if standortsregion in ["J", "M", "1", "2a"]:
                                NAIS_StandortstypZukunft=Projektionspfad_regJM12a2b3_SM_CO(tempNAIS1, standortsregion, "submontan", hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                            elif standortsregion in ["2b", "3"]:
                                NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_SM_CO(tempNAIS1, standortsregion, "submontan", hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                    elif hoehenstufe_heute == "submontan":
                        if hoehenstufe_zukunft == "collin":
                            NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_SM_CO(item, standortsregion, "submontan", hoehenstufe_zukunft,schatten, strahlungsreich, blockschutt, bodenverdichtet,trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                    elif hoehenstufe_heute == "collin":
                        NAIS_StandortstypZukunft = Projektionspfad_regJM12a2b3_CO_CO(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute,
                                                          hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt,
                                                          bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS,
                                                          SH,hangneigung)
            elif standortsregion == "4":
                if hoehenstufe_heute==hoehenstufe_zukunft:
                    NAIS_StandortstypZukunft = item
                else:
                    if hoehenstufe_heute=="obersubalpin":
                        if hoehenstufe_zukunft == "subalpin":
                            NAIS_StandortstypZukunft=Projektionspfad_reg4_OSA_SA(item, standortsregion, hoehenstufe_heute,hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft in ["hochmontan im Tannen-Hauptareal", "hochmontan im Tannen-Nebenareal", "hochmontan im Tannen-Reliktareal"]:
                            tempNAIS1=Projektionspfad_reg4_OSA_SA(item, standortsregion, hoehenstufe_heute, "subalpin", schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                            if hoehenstufe_zukunft == "hochmontan im Tannen-Hauptareal":
                                NAIS_StandortstypZukunft = Projektionspfad_reg4_SA_HMTannenHaupt(tempNAIS1, standortsregion,"subalpin",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet,trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            elif hoehenstufe_zukunft == "hochmontan im Tannen-Nebenareal":
                                NAIS_StandortstypZukunft = Projektionspfad_reg4_SA_HMTannenNeben(tempNAIS1, standortsregion,"subalpin",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet,trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            elif hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
                                NAIS_StandortstypZukunft = Projektionspfad_reg4_SA_HMTannenRelikt(tempNAIS1, standortsregion,"subalpin",hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet,trocken, kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            elif hoehenstufe_zukunft == "collin":
                                tempNAIS1 = Projektionspfad_reg4_OSA_SA(item, standortsregion,hoehenstufe_heute, "subalpin", schatten, strahlungsreich,blockschutt, bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                                tempNAIS2 = Projektionspfad_reg4_SA_HMTannenNeben(tempNAIS1, standortsregion, "subalpin","hochmontan im Tannen-Nebenareal",schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                                NAIS_StandortstypZukunft = Projektionspfad_reg4_HM_CO(tempNAIS2, standortsregion, "hochmontan","collin", schatten, strahlungsreich,blockschutt, bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                    elif hoehenstufe_heute=="subalpin":
                        if hoehenstufe_zukunft in ["hochmontan im Tannen-Hauptareal", "hochmontan im Tannen-Nebenareal","hochmontan im Tannen-Reliktareal"]:
                            if hoehenstufe_zukunft == "hochmontan im Tannen-Hauptareal":
                                NAIS_StandortstypZukunft = Projektionspfad_reg4_SA_HMTannenHaupt(item, standortsregion,"subalpin",hoehenstufe_zukunft,schatten, strahlungsreich,blockschutt,bodenverdichtet, trocken,kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            elif hoehenstufe_zukunft == "hochmontan im Tannen-Nebenareal":
                                NAIS_StandortstypZukunft = Projektionspfad_reg4_SA_HMTannenNeben(item, standortsregion,"subalpin",hoehenstufe_zukunft,schatten, strahlungsreich,blockschutt,bodenverdichtet, trocken,kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            elif hoehenstufe_zukunft == "hochmontan im Tannen-Reliktareal":
                                NAIS_StandortstypZukunft = Projektionspfad_reg4_SA_HMTannenRelikt(item,standortsregion,"subalpin",hoehenstufe_zukunft,schatten, strahlungsreich,blockschutt,bodenverdichtet, trocken,kuppenlage, hanglage,muldenlage, VS, SH,hangneigung)
                            elif hoehenstufe_zukunft == "collin":
                                #hier koennte man noch zwischen Neben- und Reliktareal unterscheiden
                                tempNAIS1 = Projektionspfad_reg4_SA_HMTannenNeben(item, standortsregion, "subalpin","hochmontan im Tannen-Nebenareal",schatten, strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                                NAIS_StandortstypZukunft = Projektionspfad_reg4_HM_CO(tempNAIS2, standortsregion,"hochmontan", hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
                    elif "hochmontan" in hoehenstufe_heute:
                        if hoehenstufe_zukunft == "collin":
                            NAIS_StandortstypZukunft = Projektionspfad_reg4_HM_CO(tempNAIS2, standortsregion,"hochmontan", hoehenstufe_zukunft, schatten,strahlungsreich, blockschutt,bodenverdichtet, trocken, kuppenlage,hanglage, muldenlage, VS, SH,hangneigung)
            elif standortsregion in ["5a", "5b", "5"]:
                if hoehenstufe_heute==hoehenstufe_zukunft:
                    NAIS_StandortstypZukunft = item
                else:
                    if hoehenstufe_heute in ["subalpin","obersubalpin"]:
                        if hoehenstufe_zukunft in ["hochmontan","hochmontan im Tannen-Hauptareal","hochmontan im Tannen-Nebenareal","hochmontan im Tannen-Reliktareal"]:
                            NAIS_StandortstypZukunft=Projektionspfad_reg5_OSASA_HM(NAIS_StandortstypHeute, standortsregion, hoehenstufe_heute, "hochmontan", schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft in ["obermontan", "untermontan", "unter- und obermontan"]:
                            tempNAIS1 = Projektionspfad_reg5_OSASA_HM(NAIS_StandortstypHeute,
                                                                                     standortsregion, hoehenstufe_heute,
                                                                                     "hochmontan", schatten,
                                                                                     strahlungsreich, blockschutt,
                                                                                     bodenverdichtet, trocken, kuppenlage,
                                                                                     hanglage, muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft=Projektionspfad_reg5_HM_OMUM(tempNAIS1, standortsregion, "hochmontan", hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                        elif "collin" in hoehenstufe_zukunft:
                            tempNAIS1 = Projektionspfad_reg5_OSASA_HM(NAIS_StandortstypHeute,
                                                                      standortsregion, hoehenstufe_heute,
                                                                      "hochmontan", schatten,
                                                                      strahlungsreich, blockschutt,
                                                                      bodenverdichtet, trocken, kuppenlage,
                                                                      hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS2 = Projektionspfad_reg5_HM_OMUM(tempNAIS1, standortsregion,
                                                                                    "hochmontan", "unter- und obermontan", schatten,
                                                                                    strahlungsreich, blockschutt,
                                                                                    bodenverdichtet, trocken, kuppenlage,
                                                                                    hanglage, muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft=Projektionspfad_reg5_OMUM_CObu(tempNAIS2, standortsregion, "unter- und obermontan", hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                    elif "hochmontan" in hoehenstufe_heute:
                        if hoehenstufe_zukunft in ["obermontan", "untermontan", "unter- und obermontan"]:
                            NAIS_StandortstypZukunft=Projektionspfad_reg5_HM_OMUM(NAIS_StandortstypHeute, standortsregion, "hochmontan", "unter- und obermontan", schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                        elif "collin" in hoehenstufe_zukunft:
                            tempNAIS1 = Projektionspfad_reg5_HM_OMUM(NAIS_StandortstypHeute, standortsregion,
                                                                                    "hochmontan", "unter- und obermontan", schatten,
                                                                                    strahlungsreich, blockschutt,
                                                                                    bodenverdichtet, trocken, kuppenlage,
                                                                                    hanglage, muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft=Projektionspfad_reg5_OMUM_CObu(tempNAIS1, standortsregion, "unter- und obermontan", hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft=="hyperinsubrisch":
                            tempNAIS1 = Projektionspfad_reg5_HM_OMUM(NAIS_StandortstypHeute, standortsregion,
                                                                     "hochmontan", "unter- und obermontan", schatten,
                                                                     strahlungsreich, blockschutt,
                                                                     bodenverdichtet, trocken, kuppenlage,
                                                                     hanglage, muldenlage, VS, SH,hangneigung)
                            tempNAIS2 = Projektionspfad_reg5_OMUM_CObu(tempNAIS1, standortsregion,
                                                                                      "unter- und obermontan",
                                                                                      "collin", schatten,
                                                                                      strahlungsreich, blockschutt,
                                                                                      bodenverdichtet, trocken, kuppenlage,
                                                                                      hanglage, muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft=Projektionspfad_reg5_COBu_hyp(tempNAIS2, standortsregion, "collin", hoehenstufe_zukunft, schatten, strahlungsreich, blockschutt, bodenverdichtet, trocken, kuppenlage, hanglage, muldenlage, VS, SH,hangneigung)
                    elif hoehenstufe_heute in ["obermontan", "untermontan", "unter- und obermontan"]:
                        if "collin" in hoehenstufe_zukunft:
                            NAIS_StandortstypZukunft = Projektionspfad_reg5_OMUM_CObu(NAIS_StandortstypHeute, standortsregion,
                                                                                      "unter- und obermontan",
                                                                                      "collin", schatten,
                                                                                      strahlungsreich, blockschutt,
                                                                                      bodenverdichtet, trocken, kuppenlage,
                                                                                      hanglage, muldenlage, VS, SH,hangneigung)
                        elif hoehenstufe_zukunft == "hyperinsubrisch":
                            tempNAIS1 = Projektionspfad_reg5_OMUM_CObu(NAIS_StandortstypHeute, standortsregion,
                                                                       "unter- und obermontan",
                                                                       "collin", schatten,
                                                                       strahlungsreich, blockschutt,
                                                                       bodenverdichtet, trocken, kuppenlage,
                                                                       hanglage, muldenlage, VS, SH,hangneigung)
                            NAIS_StandortstypZukunft = Projektionspfad_reg5_COBu_hyp(tempNAIS1, standortsregion, "collin",
                                                                                     hoehenstufe_zukunft, schatten,
                                                                                     strahlungsreich, blockschutt,
                                                                                     bodenverdichtet, trocken, kuppenlage,
                                                                                     hanglage, muldenlage, VS, SH,hangneigung)
                    elif "collin" in hoehenstufe_heute and hoehenstufe_zukunft == "hyperinsubrisch":
                            NAIS_StandortstypZukunft = Projektionspfad_reg5_COBu_hyp(NAIS_StandortstypHeute, standortsregion, "collin",
                                                                                     hoehenstufe_zukunft, schatten,
                                                                                     strahlungsreich, blockschutt,
                                                                                     bodenverdichtet, trocken, kuppenlage,
                                                                                     hanglage, muldenlage, VS, SH,hangneigung)
            ListeStandortstypZukunft.append(NAIS_StandortstypZukunft)
        #************************************************************************************
        #Baumartenempfehlung
        # ************************************************************************************
        #erglist_heute_foerdern, erglist_heute_mitnehmen, erglist_heute_reduzieren, erglist_heute_achtung, erglist_zukunft_foerdern, erglist_zukunft_mitnehmen, erglist_zukunft_achtung
        if len(NAIS_StandortstypHeute) >0:
            haupt = BaumartenempfehlungCC(matrixbaumartenarr, NAIS_StandortstypHeute[0], ListeStandortstypZukunft[0])
            # schreibe Ergebnis in die Spalten
            row[14] = ListeStandortstypZukunft[0]
            if len(haupt[0]) > 0:
                row[15] = str(haupt[0]).replace("[","").replace("]","")
            else:
                row[15]="-"
            if len(haupt[1]) > 0:
                row[16] = str(haupt[1]).replace("[","").replace("]","")
            else:
                row[16]="-"
            if len(haupt[2]) > 0:
                row[17] = str(haupt[2]).replace("[","").replace("]","")
            else:
                row[17]="-"
            if len(haupt[3]) > 0:
                row[18] = str(haupt[3]).replace("[","").replace("]","")
            else:
                row[18]="-"
            if len(haupt[4]) > 0:
                row[19] = str(haupt[4]).replace("[","").replace("]","")
            else:
                row[19]="-"
            if len(haupt[5]) > 0:
                row[20] = str(haupt[5]).replace("[","").replace("]","")
            else:
                row[20]="-"
            if len(haupt[6]) > 0:
                row[21] = str(haupt[6]).replace("[","").replace("]","")
            else:
                row[21]="-"
        if len(NAIS_StandortstypHeute) ==2:
            neben=BaumartenempfehlungCC(matrixbaumartenarr, NAIS_StandortstypHeute[1], ListeStandortstypZukunft[1])
            # schreibe Ergebnis in die Spalten
            row[22] = ListeStandortstypZukunft[1]
            if len(neben[0]) > 0:
                row[23] = str(neben[0]).replace("[","").replace("]","")
            else:
                row[23]="-"
            if len(neben[1]) > 0:
                row[24] = str(neben[1]).replace("[","").replace("]","")
            else:
                row[24]="-"
            if len(neben[2]) > 0:
                row[25] = str(neben[2]).replace("[","").replace("]","")
            else:
                row[25]="-"
            if len(neben[3]) > 0:
                row[26] = str(neben[3]).replace("[","").replace("]","")
            else:
                row[26]="-"
            if len(neben[4]) > 0:
                row[27] = str(neben[4]).replace("[","").replace("]","")
            else:
                row[27]="-"
            if len(neben[5]) > 0:
                row[28] = str(neben[5]).replace("[","").replace("]","")
            else:
                row[28]="-"
            if len(neben[6]) > 0:
                row[29] = str(neben[6]).replace("[","").replace("]","")
            else:
                row[29]="-"
    else:
        if NAIS_StandortstypHeute[0] not in matrixbaumartenarr[0,1:].tolist():
            row[14]="not in matrix"
        else:
            row[14] = "NA"
        row[22] = "NA"
    # **********************************************************************************************
    cursor.updateRow(row)
cursor.reset()
del cursor

#**************************************************************************************************
#Berechne die Uebergaenge
#**************************************************************************************************
#Mosaik Standortstyp X
arcpy.AddField_management(in_table=stoshape, field_name="UEheuteFoerdern", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="UEheuteMitnehmen", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="UEheuteReduzieren", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="UEheuteAchtung", field_type="TEXT", field_precision="", field_scale="", field_length="250", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="UEZukunftFoerdern", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="UEZukunftMitnehmen", field_type="TEXT", field_precision="", field_scale="", field_length="800", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=stoshape, field_name="UEZukunftAchtung", field_type="TEXT", field_precision="", field_scale="", field_length="250", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
#overwrite field values if the columns already exist
arcpy.CalculateField_management(in_table=stoshape, field="UEheuteFoerdern", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="UEheuteMitnehmen", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="UEheuteReduzieren", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="UEheuteAchtung", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="UEZukunftFoerdern", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="UEZukunftMitnehmen", expression='""', expression_type="PYTHON", code_block="")
arcpy.CalculateField_management(in_table=stoshape, field="UEZukunftAchtung", expression='""', expression_type="PYTHON", code_block="")

#feature cursor
cursor6 = arcpy.da.UpdateCursor(stoshape, ["uebergang", "NAISheuteHaupt", "NAISheuteNeben","XStandortZukunft","YStandortZukunft","UEheuteFoerdern","UEheuteMitnehmen","UEheuteReduzieren","UEheuteAchtung","UEZukunftFoerdern","UEZukunftMitnehmen", "UEZukunftAchtung"])
#loop through the shapefile
#cursor.reset()
for row in cursor6:
    #print row[0]
    uebergang=row[0]
    StandortstypXheute=str(row[1])
    StandortstypYheute=str(row[2])
    StandortstypXzukunft=str(row[3])
    StandortstypYzukunft=str(row[4])
    if uebergang ==1 and StandortstypXheute not in ["", "NA"] and StandortstypYheute not in ["", "NA"] and StandortstypXzukunft not in ["", "NA"] and StandortstypYzukunft not in ["", "NA"]:
        erg=Uebergang(matrixbaumartenarr, StandortstypXheute, StandortstypYheute, StandortstypXzukunft,StandortstypYzukunft)
        #erglist_heute_foerdern, erglist_heute_mitnehmen, erglist_heute_reduzieren, erglist_heute_achtung, erglist_zukunft_foerdern, erglist_zukunft_mitnehmen, erglist_zukunft_achtung
        if len(erg[0]) > 0:
            row[5]=str(erg[0]).replace("[","").replace("]","") #UEheuteFoerdern
        else:
            row[5]="-"
        if len(erg[0]) > 0:
            row[6] = str(erg[1]).replace("[","").replace("]","")  #UEheuteMitnehmen
        else:
            row[6]="-"
        if len(erg[0]) > 0:
            row[7] = str(erg[2]).replace("[","").replace("]","")  #UEheuteReduzieren
        else:
            row[7] = "-"
        if len(erg[0]) > 0:
            row[8] = str(erg[3]).replace("[","").replace("]","")  #UEheuteAchtung
        else:
            row[8]="-"
        if len(erg[0]) > 0:
            row[9] = str(erg[4]).replace("[","").replace("]","") #UEZukunftFoerdern
        else:
            row[9]="-"
        if len(erg[0]) > 0:
            row[10] = str(erg[5]).replace("[","").replace("]","")  #UEZukunftMitnehmen
        else:
            row[10]="-"
        if len(erg[0]) > 0:
            row[11] = str(erg[6]).replace("[","").replace("]","")  #UEZukunftAchtung"
        else:
            row[11]="-"
    cursor6.updateRow(row)
cursor6.reset()
del cursor6



print "done ..."
