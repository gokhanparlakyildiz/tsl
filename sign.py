#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 11 18:41:03 2019

@author: gokhanparlakyildiz
"""
import serial
serialport = serial.Serial('/dev/ttyUSB0', 9600)
while 1:
	input=serialport.readline()
	v=input.decode("utf-8")
	#v="448,531,481,511,516"
	values=v.split(',')

	a1=int(values[0])
	a2=int(values[1])
	a3=int(values[2])
	a4=int(values[3])
	a5=int(values[4])

	open=630
	close=510

	if a1>510:
		a1=2
	elif 450<a1:
		a1=1
	else:
	 a1=0

	if a2>open:
		a2=2
	elif close<a2<open:
		a2=1
	else:
	 a2=0

	if a3>open:
		a3=2
	elif close<a3<open:
		a3=1
	else:
		a3=0   

	if a4>open:
		a4=2
	elif close<a4<open:
		a4=1
	else:
		a4=0   

	if a5>open:
		a5=2
	elif 530<a5<open:
		a5=1
	else:
		a5=0     

	pred="x"
			
	if a1<=1 and a2==2 and a3<=1 and a4<=1 and a5<=1:
		pred="1"
		
	elif (a2+a3) == 4 and a4<=1 and a1<=1 and a5<=1:
			pred="2"
		
	elif (a1+a2+a3) >= 5 and (a4+a5)<=2:
			pred="3"
		
	elif a1<=1 and (a2+a3+a5+a5)>=6:
			pred="4"
		
	elif  (a1+a2+a3+a5+a5)==10:
			pred="5"
		
	elif a1>=1 and a2<=1 and a3<=1 and a4<=1 and a5<=1:
		pred="6"
	   
	elif (a1+a5)>=2 and (a2+a3+a4)<=2:
			pred="Y"

	elif (a1+a4+a5)<=1 and (a2+a3)>=2 :
			pred="8"

	elif a2>=1 and (a1+a3+a4)==0 and a5<=1:
			pred="9"
	elif a1==0 and a2<=1 and a3<=1 and a4<=1 and a5<=1:
		pred="0"
			 		 
	
	print(v)
	print(a1,a2,a3,a4,a5)
	print(pred)
        
        
     
    
    