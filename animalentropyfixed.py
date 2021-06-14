#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 18:20:03 2021

@author: bryantchung
"""

import pandas as pd
from openpyxl import load_workbook
import math 
import numpy as np 
import statistics

df = pd.read_excel(r'/Users/bryantchung/Downloads/ExtraCurricular/UCI/transitionmarkov/data/temporaloutput.xls', usecols=range(1,256), header=None) 
transitions = [] 
#E=m, F=p, G=r, H=a, I=b,J=c,K=d (associated the different locations with letters adjacent on ASCII table)
#each are just place holders (Ex: ord value of 3 just means it went to C)
location = ['A', 'B','C', 'D', 'E', 'F','G','H','I','J','K']
#entropy variables
entropy_vals=0
entropy=[]
#entropy values for first 5 minutes
entropy2=[]

#variables for transition matrix 
#duplicate (2) is for entropy for first 5 minutes 
T=[]
T2=[]
wght_avg=[]
wght_avg2=[]
size = len(location)
prob_matrix = np.zeros((size, size))
prob_matrix2 = np.zeros((size, size))

#variables to print out to excel 
place=0
df5=pd.DataFrame()

#finds numerical difference between two points   
def rank(c):
   return ord(c) - ord('A')

#iterates through 182 rows
for rowindex in range(182):
    length = len(df.columns)
    for columnindex in range(length):
        c = df.iloc[rowindex, columnindex]
        #saves name for each row
        if columnindex==0:
            title=c
        else:
            if c == 'm':
                c='E'
            if c == 'p':
                c='F'
            if c == 'r':
                c='G'
            if c == 'a':
                c='H'
            if c == 'b':
                c='I'
            if c == 'c':
                c='J'
            if c == 'd':
                c='K'
            if type(c) == str:
                T.append(rank(c))
            #if value is no longer r 
            if c!='G':
                if T2==[]:
                    #makes sure only takes value for first 5 minutes
                    columnindexuse=columnindex+120
                    #5 min = 300 sec = 120 boxes (2.5 sec each)
                    if length<columnindexuse:
                            columnindexuse=length
                    for columnindex2 in range(columnindex, columnindexuse):
                        c2 = df.iloc[rowindex, columnindex2]
                        if c2 == 'm':
                            c2='E'
                        if c2 == 'p':
                            c2='F'
                        if c2 == 'r':
                            c2='G'
                        if c2 == 'a':
                            c2='H'
                        if c2 == 'b':
                            c2='I'
                        if c2 == 'c':
                            c2='J'
                        if c2 == 'd':
                            c2='K'
                        if type(c2) == str:
                            T2.append(rank(c2))
    #creates matrix
    #each array (basically looks like a row) corresponds to row in transition matrix 
    for (i,j) in zip(T,T[1:]): #groups each initial i and its next corresponding
        prob_matrix[i][j] += 1
    for (i,j) in zip(T2,T2[1:]): 
        prob_matrix2[i][j] += 1
    #converts to probabilities
    #sums by row
    total = np.sum(prob_matrix, axis = 1)
    total2 = np.sum(prob_matrix2, axis = 1)
    #calculates total for each row in each array
    #resets bc it is =
    for row in range(len(prob_matrix)):
        #iterates through each array 
        if total[row]> 0:
           for column in range(len(prob_matrix[row])):
               point = prob_matrix[row][column]
               #print(point)
               prob_matrix[row][column] /= total[row]
    #iterates through created probability matrix to calculate entropy values
    for row2 in range(len(prob_matrix)):
        for column in range(len(prob_matrix[row2])):
            point2 = prob_matrix[row2][column]
            if point2>0:
                   entropy_vals+=(point2*math.log(point2, 2))
        entropy.append(entropy_vals*-1)
        entropy_vals=0
    #calculates stationary distribution of probability matrix 
    st_dst=np.linalg.matrix_power(prob_matrix, 50)
    #supposed to use probablities for this
    for row3 in range(len(prob_matrix2)):
        #iterates through each array 
        if total2[row3]> 0:
           for column in range(len(prob_matrix2[row3])):
               point = prob_matrix2[row3][column]
               #print(point)
               prob_matrix2[row3][column] /= total2[row3]
    #iterates through created probability matrix to calculate entropy values
    for row4 in range(len(prob_matrix2)):
        for column in range(len(prob_matrix2[row4])):
            point2 = prob_matrix2[row4][column]
            if point2>0:
                   entropy_vals+=(point2*math.log(point2, 2))
        entropy2.append(entropy_vals*-1)
        entropy_vals=0
    #calculates stationary distribution of probability matrix 
    st_dst2=np.linalg.matrix_power(prob_matrix2, 200)
    #supposed to use probablities for this
    #if stationary distribution sums up to >0 (error otherwise) find weighted average of each row in excel 
    if sum(st_dst[0]!=0):
        wght_avg.append(np.average(entropy, weights = st_dst[0])) 
    if sum(st_dst2[0]!=0):
        wght_avg2.append(np.average(entropy2, weights = st_dst2[0])) 
    #each value per row 
    #values for first 5 mins of each row
    if rowindex!=0:
        beforetitle=df.iloc[rowindex-1, 0]
        if (title[7:9]=="S2" and beforetitle[7:9] =="S1") or (title[4]=="S" and beforetitle[4]=="E")or (title[4]=="W" and beforetitle[4]=="S"):
            df5.insert(place, beforetitle[4:9], [statistics.mean(wght_avg)], True)
            df5.insert(place+1, beforetitle[4:9], [statistics.mean(wght_avg2)], True)
            wght_avg=[]
            wght_avg2=[]
            place+=2
            #code for outputting to excel
            #resets variables for next group 
    prob_matrix = np.zeros((size, size))
    prob_matrix2 = np.zeros((size, size))
    T=[]
    T2=[]
    entropy=[]
    entropy2=[]
    #resets variables for next row
    
writer = pd.ExcelWriter('entropytemporalanalysis.xlsx', engine='xlsxwriter')
df5.to_excel(writer, sheet_name="output", index=False, startrow=0)
writer.save()              
writer.close()
  
            
