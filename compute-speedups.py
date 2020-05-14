#!python
import functions as custom
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
site="rdm"



dirs_tmp=np.arange(7.5,352.5,15)
tmp=np.append([352.5],dirs_tmp)
directions=np.append(tmp,[352.5])
ndirs=len(directions)-1

mypath="input/"+site+"/points/"

#files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
numberscustom=[10,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,21,22,23,24,25]
filescustom =  []
for number in numberscustom:
	filescustom.append("wrf.high.point."+str(number)+".nc")

files=filescustom
nfiles=len(files)+1
print("found "+str(nfiles))
#header
line="Initiation Target "
for i in range(0,24):
	line=line+str(directions[i])+"-"+str(directions[i+1])+" "
line=line+"Overall"

print(line)
table=line+"\n"
tablefreq=line+"\n"
#compute
for nfile in range(0,nfiles-1):
	filename=mypath+"wrf.high.point."+str(nfile)+".nc"
	filename=mypath+files[nfile]
	xr_tmp=custom.read_netcdf(filename)
	lev=xr_tmp.lev.values[0]
	#xr1=xr_tmp.interp(lev=lev)
	xr1=xr_tmp
	df1=xr1.to_dataframe()
	df1.reset_index(inplace=True)
	df1.set_index('time',inplace=True)
	for nfile2 in range(nfile+1,nfiles-1):
		line=str(nfile)+" "+str(nfile2)+" "
		line=str(numberscustom[nfile])+" "+str(numberscustom[nfile2])+" "
		linefreq=str(nfile)+" "+str(nfile2)+" "
		filename2=mypath+"wrf.high.point."+str(nfile2)+".nc"
		filename2=mypath+files[nfile2]
		xr_tmp=custom.read_netcdf(filename2)
		lev=xr_tmp.lev.values[0]
		xr2=xr_tmp
		#xr2=xr_tmp.interp(lev=lev)

		df2=xr2.to_dataframe()
		df2.reset_index(inplace=True)
		df2.set_index('time',inplace=True)

		df=pd.concat([df1,df2],axis=1,join='inner')
		df.columns=['lat','lev1','lon','HGT','U1','V1','M1','Dir1','lat2','lev2','lon2','HGT2','U2','V2','M2','Dir2']

		#full xr1 vs xr2
		#subset by sectors
		#first sector appart
		#CHECK | vs &  TODO
		np1=df[(df['Dir2'] <= directions[1]) | (df['Dir2'] >=directions[0])]['M1'].to_numpy()
		np2=df[(df['Dir2'] <= directions[1]) | (df['Dir2'] >=directions[0])]['M2'].to_numpy()
		#np1=df[(df['Dir1'] <= directions[1]) & (df['Dir1'] >=directions[0])]['M1'].to_numpy()
		#np2=df[(df['Dir1'] <= directions[1]) & (df['Dir1'] >=directions[0])]['M2'].to_numpy()
		slope=custom.fit_tls(np1,np2)
		line=line+str(slope)+" "
		linefreq=linefreq+str(len(np1)/len(df1['M']))+" "
		for idir in range(1,24):
			np1=df[(df['Dir2'] <= directions[idir+1]) & (df['Dir2'] >=directions[idir])]['M1'].to_numpy()
			np2=df[(df['Dir2'] <= directions[idir+1]) & (df['Dir2'] >=directions[idir])]['M2'].to_numpy()
			slope=custom.fit_tls(np1,np2)
			line=line+str(slope)+" "
			linefreq=linefreq+str(len(np1)/len(df1['M']))+" "

		np1=df['M1'].to_numpy()
		np2=df['M2'].to_numpy()
		slope=custom.fit_tls(np1,np2)
		line=line+str(slope)+"\n"
		linefreq=linefreq+str(len(np1)/len(df1['M']))+"\n"
		table=table+line
		tablefreq=tablefreq+linefreq
print("########## SPEEDUPS")
print(table)
print("########## SPEEDUPS END")
print("\n\n\n")
print("########## FREQ")
print(tablefreq)
print("########## FREQ END")
