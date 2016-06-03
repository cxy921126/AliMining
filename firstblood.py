# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 18:37:35 2016

@author: acer
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 12:24:37 2016

@author: acer
"""

from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import datetime
import csv



# read data from csv file
action_names = ['user_id', 'song_id', 'gmt_create', 'action_type', 'Ds']
data = pd.read_table('mars_tianchi_user_actions.csv', sep=',', header=None, names=action_names)
song_names = ['song_id', 'artist_id', 'publish_time', 'song_init_plays', 'Language', 'Gender']
data2 = pd.read_table('mars_tianchi_songs.csv', sep=',', header=None, names=song_names)

# merge 2 dataframes
total_data = pd.merge(data, data2)
table=total_data
# extract data from the a specific artist
# 第一步，把所有歌手的id都放在一个dataframe中
artist=table.groupby('artist_id').artist_id.nunique()
artist=pd.Series(artist)
#print(artist.index,artist.index[1])
with open('firstblood\predict\mars_tianchi_artist_plays_predict.csv','wb') as csvfile:
    aid=0
    while aid<50:
        data_per_artist = total_data[(total_data['artist_id'] == artist.index[aid])]
        
        # traverse from 20150301 to 20150630
        start = datetime.datetime.strptime("20150301", "%Y%m%d")
        end = datetime.datetime.strptime("20150701", "%Y%m%d")
    
        # step length = 1 day
        oneday = datetime.timedelta(days=1)
    
        # to put the results of plays, downloads and favorites every day
        # each element is also a python 'list' object in the form of
        # [play, downloads, favorites]
        result_list = []
    
        count=0
        while start != end:
            datestr = start.strftime("%Y%m%d")
            # date increment
            start = start + oneday
            
            # [play, downloads, favorites]
            day_tuple = []
            
            # select data of this day
            day_data = data_per_artist[(data_per_artist['Ds'] == int(datestr))]
            
            # do stat
            plays = len(day_data[day_data['action_type'] == 1])
            downloads = len(day_data[day_data['action_type'] == 2])
            favorites = len(day_data[day_data['action_type'] == 3])
    
            # very bad practices.........
            # plays = len(total_data[(total_data['artist_id'] == artist_id) & (total_data['Ds'] == int(datestr)) & (total_data['action_type'] == 1)])
            # downloads = len(total_data[(total_data['artist_id'] == artist_id) & (total_data['Ds'] == int(datestr)) & (total_data['action_type'] == 2)])
            # favorites = len(total_data[(total_data['artist_id'] == artist_id) & (total_data['Ds'] == int(datestr)) & (total_data['action_type'] == 3)])
    
            day_tuple.append(float(plays))
            day_tuple.append(float(downloads))
            day_tuple.append(float(favorites))
            result_list.append(day_tuple)
            count=count+1
            
            # output results
            result = pd.DataFrame(result_list)
            #result.to_csv(artist_id+'.csv', header=None, index=None)
    
    
        #计算均值和方差
        dta=result.iloc[:,0]
        dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2015',None,122))
        dta=pd.Series(dta)
        narray=np.array(dta)
        sum1=narray.sum()
        mean=sum1/count
        dta0=dta/mean
        
        narray=np.array(dta0)
        narray2=narray*narray
        sum2=narray2.sum()
        var=sum2/count-1
        
        # 第二步，循环输入判断是否为平稳型的
        if(var<0.03):
            print(artist.index[aid],"---",var)#2,3,9,13个
            #print(dta)
            #第三步，采用AR（2）、ARMA（1,1）和AR（3）来分别检验
            arma_mod20 = sm.tsa.ARMA(dta,(2,0)).fit()
            #print(arma_mod20.aic,arma_mod20.bic,arma_mod20.hqic)
            arma_mod30 = sm.tsa.ARMA(dta,(3,0)).fit()
            #print(arma_mod30.aic,arma_mod30.bic,arma_mod30.hqic)
            arma_mod11 = sm.tsa.ARMA(dta,(0,1)).fit()
            #print(arma_mod11.aic,arma_mod11.bic,arma_mod11.hqic)
    
            #这里进行一下判断，每个模型选择最好的
    
            if((arma_mod20.aic<arma_mod30.aic)&(arma_mod20.aic<arma_mod11.aic)):
                predict_sunspots = arma_mod20.predict('2137', '2197', dynamic=True)
                #print(predict_sunspots)
                fig, ax = plt.subplots(figsize=(12, 8))
                ax = dta.ix['2015':].plot(ax=ax)
                predict_sunspots.plot(ax=ax)
                pcount=0
                start = datetime.datetime.strptime("20150701", "%Y%m%d")
                #plt.savefig("firstblood/predict/"+artist.index[aid]+"_AR(2,0).png")
                datestr = start.strftime("%Y%m%d")
                spamwriter = csv.writer(csvfile, dialect='excel')
                while(pcount<61):
                    spamwriter.writerow([artist.index[aid], predict_sunspots[pcount], int(datestr)])
                    start = start + datetime.timedelta(days=1)
                    datestr = start.strftime("%Y%m%d")
                    pcount=pcount+1
                              
                
            elif((arma_mod30.aic<arma_mod20.aic)&(arma_mod30.aic<arma_mod11.aic)):
                predict_sunspots = arma_mod11.predict('2137', '2197', dynamic=True)
                #print(predict_sunspots)
                fig, ax = plt.subplots(figsize=(12, 8))
                ax = dta.ix['2015':].plot(ax=ax)
                predict_sunspots.plot(ax=ax)
                pcount=0
                start = datetime.datetime.strptime("20150701", "%Y%m%d")
                #plt.savefig("firstblood/predict/"+artist.index[aid]+"_AR(2,0).png")
                datestr = start.strftime("%Y%m%d")
                spamwriter = csv.writer(csvfile, dialect='excel')
                while(pcount<61):
                    spamwriter.writerow([artist.index[aid], predict_sunspots[pcount], int(datestr)])
                    start = start + datetime.timedelta(days=1)
                    pcount=pcount+1
                    datestr = start.strftime("%Y%m%d")
                
            elif((arma_mod11.aic<arma_mod20.aic)&(arma_mod11.aic<arma_mod30.aic)):
                predict_sunspots = arma_mod11.predict('2137', '2197', dynamic=True)
                #print(predict_sunspots)
                fig, ax = plt.subplots(figsize=(12, 8))
                ax = dta.ix['2015':].plot(ax=ax)
                predict_sunspots.plot(ax=ax)
                pcount=0
                start = datetime.datetime.strptime("20150701", "%Y%m%d")
                #plt.savefig("firstblood/predict/"+artist.index[aid]+"_AR(2,0).png")
                datestr = start.strftime("%Y%m%d")            
                spamwriter = csv.writer(csvfile, dialect='excel')
                while(pcount<61):
                    spamwriter.writerow([artist.index[aid], predict_sunspots[pcount], int(datestr)])
                    start = start + datetime.timedelta(days=1)
                    datestr = start.strftime("%Y%m%d")
                    pcount=pcount+1
                
        aid=aid+1      
    
    csvfile.close();        