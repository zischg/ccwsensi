#Lagekorrektur
import numpy
def gridasciitonumpyarrayfloat(ingridfilefullpath):
    i=0
    row = 0
    headerstr=''
    infile=open(ingridfilefullpath, "r")
    for line in infile:
        if i==0:
            ncols=int(line.strip().split()[-1])
            headerstr+=line
        elif i==1:
            nrows=int(line.strip().split()[-1])
            headerstr += line
        elif i==2:
            xllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==3:
            yllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==4:
            cellsize=float(line.strip().split()[-1])
            headerstr += line
        elif i==5:
            NODATA_value=float(line.strip().split()[-1])
            arr=numpy.zeros((nrows, ncols), dtype=float)
            arr[:,:]=NODATA_value
            headerstr += line.replace("\n","")
        elif i>5 and i<nrows:
            col=0
            while col<ncols:
                for item in line.strip().split():
                    arr[row,col]=float(item)
                    col+=1
            row+=1
        i+=1
    infile.close()
    return arr, ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value, headerstr
def gridasciitonumpyarrayint(ingridfilefullpath):
    i=0
    row = 0
    headerstr=''
    infile=open(ingridfilefullpath, "r")
    for line in infile:
        if i==0:
            ncols=int(line.strip().split()[-1])
            headerstr+=line
        elif i==1:
            nrows=int(line.strip().split()[-1])
            headerstr += line
        elif i==2:
            xllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==3:
            yllcorner=float(line.strip().split()[-1])
            headerstr += line
        elif i==4:
            cellsize=float(line.strip().split()[-1])
            headerstr += line
        elif i==5:
            NODATA_value=float(line.strip().split()[-1])
            arr=numpy.zeros((nrows, ncols), dtype=int)
            arr[:,:]=NODATA_value
            headerstr += line.replace("\n","")
        elif i>5 and i<nrows:
            col=0
            while col<ncols:
                for item in line.strip().split():
                    arr[row,col]=float(item)
                    col+=1
            row+=1
        i+=1
    infile.close()
    return arr, ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value, headerstr
#*****************************************************************************************************************
#input data
myworkspace="D:/CCW18sensi/GIS"

demarr, ncols, nrows, xllcorner, yllcorner, cellsize, NODATA_value, headerstr=gridasciitonumpyarrayfloat(myworkspace+"/"+"sgdem10.asc")
lagearr=gridasciitonumpyarrayint(myworkspace+"/"+"sggeldivrecl.asc")[0]
neigarr=gridasciitonumpyarrayfloat(myworkspace+"/"+"sgslpprc.asc")[0] #Prozent
flowaccarr=gridasciitonumpyarrayint(myworkspace+"/"+"sgflacc.asc")[0]

outarr=numpy.zeros((nrows,ncols),dtype=int)
outarr[0, :] = NODATA_value
outarr[-1, :] = NODATA_value
outarr[:, 0] = NODATA_value
outarr[:, -1] = NODATA_value
i=1
while i<nrows-1:
    j=1
    print i
    while j<ncols-1:
        #Anzahl der Nachbarspixel die tiefer als die Zentrumszelle sind
        outarr[i,j]=lagearr[i,j]
        count=0
        if demarr[i,j+1]<demarr[i,j]:
            count+=1
        if demarr[i-1,j+1]<demarr[i,j]:
            count+=1
        if demarr[i-1,j]<demarr[i,j]:
            count+=1
        if demarr[i-1,j-1]<demarr[i,j]:
            count+=1
        if demarr[i,j-1]<demarr[i,j]:
            count+=1
        if demarr[i+1,j-1]<demarr[i,j]:
            count+=1
        if demarr[i+1,j]<demarr[i,j]:
            count+=1
        if demarr[i+1,j+1]<demarr[i,j]:
            count+=1
        if count>=6 and lagearr[i,j]==4:
            outarr[i,j+1]=4
            outarr[i-1,j+1] = 4
            outarr[i-1,j] = 4
            outarr[i-1,j-1] = 4
            outarr[i,j - 1] = 4
            outarr[i+1,j-1] = 4
            outarr[i+1,j] = 4
            outarr[i+1,j+1] = 4
        #Ist mindestens 1 Nachbarpixel eine Kuppe 4
        count2=0
        sumneig=0
        if lagearr[i,j+1]==4:
            count2+=1
        if lagearr[i+1,j+1]==4:
            count2+=1
        if lagearr[i+1,j]==4:
            count2+=1
        if lagearr[i+1,j-1]==4:
            count2+=1
        if lagearr[i,j-1]==4:
            count2+=1
        if lagearr[i-1,j-1]==4:
            count2+=1
        if lagearr[i-1,j]==4:
            count2+=1
        if lagearr[i-1,j+1]==4:
            count2+=1
        sumneig=neigarr[i,j+1]+neigarr[i+1,j+1]+neigarr[i+1,j]+neigarr[i+1,j-1]+neigarr[i,j-1]+neigarr[i-1,j-1]+neigarr[i-1,j]+neigarr[i-1,j+1]
        if count2>=1 and sumneig>100:
            outarr[i,j]=4
        #Einzugsgebiet
        if flowaccarr[i,j]*cellsize*cellsize<=200:
            outarr[i, j] = 4
        #Ebene aufgrund der Neigung
        if neigarr[i,j]<10.0:
            outarr[i, j] = 1
        #Bereinigung Kuppen in Ebene
        sumneig=sumneig+neigarr[i,j]
        neigmittel=sumneig/9.0
        if lagearr[i,j]==4 and neigmittel<20:
            outarr[i,j]=1
        if flowaccarr[i,j]*cellsize*cellsize>=50000 and neigarr[i,j]>10 and neigarr[i,j]<30:
            outarr[i, j] = 2
        j+=1
    i+=1

numpy.savetxt(myworkspace+"/"+"sglagecorrected.asc", outarr, delimiter=' ',newline='\n', header=headerstr, comments='')
print "done ..."