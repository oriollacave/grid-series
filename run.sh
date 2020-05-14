#!/bin/sh

#cdo cat ../../../storage/edf-trial/488631/wrf.high.201* wrf.high.nc

while read line;do
	tag=`echo $line | awk '{print $1}'`
	lat=`echo $line | awk '{print $2}'`
	lon=`echo $line | awk '{print $3}'`
	lev=`echo $line | awk '{print $NF}'`
	#we only have 80,100,120 heights but need 50-80 heights. 
	levfake=$(( lev + 30 ))
	echo "$tag $lat $lon $lev"
	cdo remapdis,lon=$lon/lat=$lat -intlevel,$levfake wrf.high.nc input/rdm/points/wrf.high.point.$tag.nc
done < input/rdm/points-list.txt
