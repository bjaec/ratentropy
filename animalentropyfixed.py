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

df = pd.read_excel(r'/Users/bryantchung/Downloads/ExtraCurricular/UCI/transitionmarkov/transitionoutput.xls', usecols=range(1,256), header=None) #IV is column 256 & first column is the name 
transitions = [] 
#E=m, F=p, G=r, H=a, I=b,J=c,K=d (associated the different locations with letters adjacent on ASCII table)
#each are just place holders (Ex: ord value of 3 just means it went to C)
location = ['A', 'B','C', 'D', 'E', 'F','G','H','I','J','K',]
#entropy variables
entropy_vals=0
entropy=[]
entropy2=[]

#variables for transition matrix 
T=[]
T2=[]
wght_avg=[]
wght_avg2=[]
size = len(location)
prob_matrix = np.zeros((size, size))
prob_matrix2 = np.zeros((size, size))

#variables to print out to excel 
place=0
count=0
count2=0
df3=pd.DataFrame()
df4=pd.DataFrame()
df5=pd.DataFrame()
names=df.iloc[:, 0]
#rint(names)
#finds numerical difference between two points   
def rank(c):
   return ord(c) - ord('A')
#could just make a dictionary (think I've done it before) but this is clever way to do it 

#iterates through 182 rows
for rowindex in range(182):
    length = len(df.columns)
    for columnindex in range(length):
        c = df.iloc[rowindex, columnindex]
        #print(c)
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
        if c!='G':
            if T2==[]:
                for columnindex2 in range(columnindex, columnindex+120):
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
                        
                        #first 5 minutes (300 seconds and each box is 2.5 seconds)       
    #creates matrix
    #each array (basically looks like a row) corresponds to row in transition matrix 
    #print(T2)
    for (i,j) in zip(T,T[1:]): #groups each initial i and its next corresponding
        prob_matrix[i][j] += 1
    for (i,j) in zip(T2,T2[1:]): #groups each initial i and its next corresponding
        prob_matrix2[i][j] += 1
    #print(prob_matrix2)
    #print(prob_matrix)
    #converts to probabilities
    #prob_matrix_save = prob_matrix.copy()
    #prob_matrix_save2 = prob_matrix2.copy()
    #print(prob_matrix)
    #sums by row
    total = np.sum(prob_matrix, axis = 1)
    total2 = np.sum(prob_matrix2, axis = 1)
    #print(total)
    #calculates total for each row in each array
    #resets bc it is =
    #could literally just prob_matrix/total.T and it should divide properly to save time 
    for row in range(len(prob_matrix)):
        #print(prob_matrix[array])
        #iterates through each array 
        #????
        if total[row]> 0:
           for column in range(len(prob_matrix[row])):
               point = prob_matrix[row][column]
               #print(point)
               prob_matrix[row][column] /= total[row]
        #print(prob_matrix[array])
        #print(sum(prob_matrix[array]))
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
    #supposed to use probablitiess for this
    #just some print statements to check
    for row3 in range(len(prob_matrix2)):
        #print(prob_matrix[array])
        #iterates through each array 
        #????
        if total2[row3]> 0:
           for column in range(len(prob_matrix2[row3])):
               point = prob_matrix2[row3][column]
               #print(point)
               prob_matrix2[row3][column] /= total2[row3]
        #print(prob_matrix[array])
        #print(sum(prob_matrix[array]))
    #iterates through created probability matrix to calculate entropy values
    for row4 in range(len(prob_matrix2)):
        for column in range(len(prob_matrix2[row4])):
            #print(column)
            point2 = prob_matrix2[row4][column]
            if point2>0:
                   entropy_vals+=(point2*math.log(point2, 2))
        entropy2.append(entropy_vals*-1)
        entropy_vals=0
    #calculates stationary distribution of probability matrix 
    st_dst2=np.linalg.matrix_power(prob_matrix2, 200)
    #print(st_dst2)
    #supposed to use probablitiess for this
    #just some print statements to check
    '''
    print(entropy)
    print(st_dst[1])
    '''
    #if stationary distribution sums up to >0 (error otherwise) find weighted average of each row in excel 
    if sum(st_dst[0]!=0):
        wght_avg.append(np.average(entropy, weights = st_dst[0])) 
        #print(count)
        #print(len(wght_avg))
        #print(wght_avg[count])
        count+=1
    if sum(st_dst2[0]!=0):
        wght_avg2.append(np.average(entropy2, weights = st_dst2[0])) 
        #print(wght_avg2)
        print(wght_avg2[count2])
        count2+=1
    #i can reference by column name and use that thing dr. cox showed (have screenshot) would save space (everything undre print statement and make my code more flexible cuz using actual row names)
    #print(str(names[rowindex])
    #df3.insert(rowindex, "hi"+str(rowindex), [wght_avg[rowindex]], True) 
    #each value per row 
    #print(wght_avg2[rowindex])
    #df4.insert(rowindex, "hi2"+str(rowindex), [wght_avg2[rowindex]], True) 
    #values for first 5 mins of each row
    if rowindex==31 or rowindex==63 or rowindex==95 or rowindex==127 or rowindex==154 or rowindex==181:
            print("hi")
            #print order is EE s1, EE s2, SH s1, SH s2, WR s1, and WR s2)
            #df5.insert(place, "hi3"+str(rowindex), [statistics.mean(wght_avg)], True)
            #print(statistics.mean(wght_avg))
            #str(df.columns[rowindex:rowindex+1])
            #averagee for each group 
            wght_avg=[]
            count=0
            place+=1;
    #code for outputting to excel
    #resets variables for next row 
    prob_matrix = np.zeros((size, size))
    prob_matrix2 = np.zeros((size, size))
    T=[]
    T2=[]
    entropy=[]
    entropy2=[]
    
writer = pd.ExcelWriter('entropyoutputnew.xlsx', engine='xlsxwriter')
df3.to_excel(writer, sheet_name="output", index=False)
df4.to_excel(writer, sheet_name="output", index=False, startrow=4)
df5.to_excel(writer, sheet_name="output", index=False, startrow=8)
writer.save()              
writer.close()

#ignore
'''
    count=0
    print(prob_matrix)
    for k1, v1 in prob_matrix.items():
        for k2, v2 in v1.items():
            prob_matrix2[count] = v2 ** 20 #(every 10 is for every i)
            count+=1
    #prob_matrix2 = {key: value ** 2 for key, value in prob_matrix.items()}
    print(prob_matrix2)
    '''
            
            