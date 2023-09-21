
import json
import matplotlib
matplotlib.use('TkAgg')
from tkinter import N
from typing_extensions import Self
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sstats
import os
import seaborn as sns
import skfuzzy as fuzz
from sklearn.cluster import KMeans
import pandas as pd
from scipy import stats as st

def ReadFiles(Dir):
  Accept = []
  for d in os.listdir(Dir):
    try:
      if('Synapse_l.json' in os.listdir(Dir+d) ):
        Accept.append(d)
        print(".json file found!")
      else:
        print("No .json file found")
    except:
      
      pass
  Syn_a_arr = []
  bg_l   = []
  for a in Accept:
    with open(Dir+a+'/Synapse_l.json', 'r') as fp: Syn_a_arr.append(json.load(fp))
    try:
      bg_l.append(np.load(Dir+a+"/backgroundM.npy").squeeze())
    except:
      bg_l.append(np.load(Dir+a+"/background.npy").squeeze())
 
  #print(Syn_a_arr)

  Areas_arr = []
  Dist_arr = []
  bg_arr = []
  kk = 0
  for Syn_a,bg in zip(Syn_a_arr,bg_l):
    kk+=1
    areas = np.array([S["RawIntDen"] for S in Syn_a])
    bg_arr = np.zeros_like(areas)
    for i, Syn in enumerate(Syn_a):
      bg_arr[i,:] = Syn["area"]*bg/(0.066**2)
    if(not Syn_a[0]["Times"]==times):
      for l in np.sort(list(set(times)-set(Syn_a[0]["Times"]))[::-1]):
        areas = np.insert(areas,times.index(l),math.nan,-1)
        bg_arr = np.insert(bg_arr,times.index(l),math.nan,-1)
    dist_a = [S["distance"] for S in Syn_a]
    Dist_arr = Dist_arr+dist_a
    Areas_arr.append(areas-bg_arr)
  Areas_arr_b = np.vstack(Areas_arr)
  Dist_arr_b = np.array(Dist_arr)#
  Areas_arr_b = (Areas_arr_b.T/Areas_arr_b[:,:3].mean(axis=1)).T

  return Dist_arr_b,Areas_arr_b,(Areas_arr,Dist_arr), 





class Plots:

    """" accepts array of directories, and returns arrays of each dataset
    Input: 
     Dir_Arr: array
     N: number of directories 

     Output:


    """
    
    def __init__(self, path, number_dirs, choice, median, mean, std, kde, clusters, x_axis, y_axis, title): 
      self.Dir_Arr= path
      
      self.number_dirs=number_dirs 
      if choice=="Spine Area [Histogram]":
        do= self.sizebins(title, median, mean, std, kde, x_axis, y_axis)
      if choice=="Spine Clustering [C-means]":
        do= self.c_means_cluster(clusters, title)
      if choice=="Spine Clustering [K-means]":
        do= self.k_means(clusters, title)
      if choice=="Spine Intensity vs Time [Heatmap]":
        do=self.intensity_heatmap(title, x_axis, y_axis)

    # def __init__(self):
    #   self.Dir_Arr= "/Users/bhavikagopalani/hp/TestImages"
    #   self.number_dirs=1 
    #   title= "our plot"
    #   median= True
    #   mean= True
    #   mode= True
    #   std= True
    #   x_axis= "our x axis"
    #   y_axis= "our y axis"
    #   stat= "percent"
    #   kde= True
    #   do= self.intensity_heatmap(title, x_axis, y_axis)
      

         
          

    def get_factors(self, n, m):
    
     factors = []
     factor = int(n**(1.0/m) + .1) # fudged to deal with precision problem with float roots
     while n % factor != 0:
        factor = factor - 1
     factors.append(factor)
     if m > 1:
        factors = factors + self.get_factors(n / factor, m - 1)
     return factors


    def sizebins(self, title, median, mean, std, kde, x_axis, y_axis):
        

        Syn_Arr, bg_l= self.json_arr(self.Dir_Arr, self.number_dirs)
        for Syn_a,bg in zip(Syn_Arr,bg_l):
            size= np.array([S["area"] for S in Syn_a])
            times= np.array([S["Times"] for S in Syn_a])

        n= len(times[1, :])
        

        for i in range(n):
            x= size[:, i]
            if (n%2==0): 
               m= int(n/2)
               plt.subplot(m, 2, i+1)
            else:
               plt.subplot(n, 1, i+1)
            sns.histplot(x, kde= kde)
            plt.xlabel(x_axis)
            plt.ylabel(y_axis)
            if (mean):
              plt.axvline(x=x.mean(),color='red')
            if (median):
              plt.axvline(x=np.median(x),color='green')
            # if (mode):
            #   plt.axvline(x=st.mode(x),color='blue')
            if (std):
              plt.axvline(x=x.std(),color='yellow')

            print(i)
           
        plt.suptitle(title)

        plt.show()


    def int_loc(self):
        Syn_Arr, bg_l= self.json_arr(self.Dir_Arr, self.number_dirs)
        for Syn_a,bg in zip(Syn_Arr,bg_l):
            location= np.array([S["Location"] for S in Syn_a])
            Intensity= np.array([S["RawIntDen"] for S in Syn_a])
            time= np.array([S["Times"] for S in Syn_a])
        

    # def spine_density(self):
    #   Syn_Arr, bg_l= self.json_arr(self.Dir_Arr, self.number_dirs)
    #   for Syn_a,bg in zip(Syn_Arr,bg_l):



    def c_means_cluster(self, clusters, title):
      Syn_Arr, bg_l= self.json_arr(self.Dir_Arr, self.number_dirs)
      for Syn_a,bg in zip(Syn_Arr,bg_l):
            location= np.array([S["location"] for S in Syn_a])
            Intensity= np.array([S["RawIntDen"] for S in Syn_a])
            time= np.array([S["Times"] for S in Syn_a])
      
      colors = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
		  '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
		  '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
		  '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
		  '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
		  '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
		  '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
		  '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
		  '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
		  '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF']


      if (clusters):
        a, b= self.get_factors(clusters, 2)
      else:
        a=3 
        b=3
    
      xpts= location[:, 0]
      ypts= location[:, 1]



      fig1, axes1 = plt.subplots(a, b, figsize=(8, 8))
      alldata = np.vstack((xpts, ypts))
      fpcs = []
    

      for ncenters, ax in enumerate(axes1.reshape(-1), 2):
        cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(alldata, ncenters, 2, error=0.005, maxiter=1000, init=None)

    # Store fpc values for later
        fpcs.append(fpc)

    # Plot assigned clusters, for each data point in training set
        cluster_membership = np.argmax(u, axis=0)
        for j in range(ncenters):
          ax.plot(xpts[cluster_membership == j], ypts[cluster_membership == j], '.', color=colors[j])
          
      

    # Mark the center of each fuzzy cluster
        for pt in cntr:
          ax.plot(pt[0], pt[1], 'rs')
          
          

        ax.set_title('Centers = {0}; FPC = {1:.2f}'.format(ncenters, fpc))
        ax.axis('on')
        plt.suptitle(title)
        

      fig1.tight_layout()
      plt.show()

    
    def k_means(self, clusters, title):
      Syn_Arr, bg_l= self.json_arr(self.Dir_Arr, self.number_dirs)
      for Syn_a,bg in zip(Syn_Arr,bg_l):
            location= np.array([S["location"] for S in Syn_a])
            Intensity= np.array([S["RawIntDen"] for S in Syn_a])
            time= np.array([S["Times"] for S in Syn_a])

      X= location
      if (clusters):
         n_clusters= clusters
      else:
        n_clusters= 5


      kmean=KMeans(n_clusters)
      kmean.fit(X)
      k_means_labels = kmean.labels_
      k_means_cluster_centers = kmean.cluster_centers_
      k_means_labels_unique = np.unique(k_means_labels)
      colors = ['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6', 
		  '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
		  '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A', 
		  '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
		  '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC', 
		  '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
		  '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680', 
		  '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
		  '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3', 
		  '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF']

      



      #plt.figure()
      #plt.hold(True)
      for k, col in zip(range(n_clusters), colors):
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        plt.plot(X[my_members, 0], X[my_members, 1], 'o', markerfacecolor=col, markersize=6)
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)
      plt.title(title)    
      plt.grid(True)
      plt.show()


      #def avg_area_time(self): 
      #def pca(self):

    def intensity_heatmap(self, title, x_label, y_label):
        Syn_Arr, bg_l= self.json_arr(self.Dir_Arr, self.number_dirs)
        for Syn_a,bg in zip(Syn_Arr,bg_l):
            location= np.array([S["location"] for S in Syn_a])
            Intensity= np.array([S["RawIntDen"] for S in Syn_a])
            time= np.array([S["Times"] for S in Syn_a])

        num_of_spines= len(time)
        time_arr= time[1, :]
        index_arr= range(num_of_spines)
        df = pd.DataFrame(data = Intensity, 
                  index = np.flip(index_arr), 
                  columns = time_arr)

        #print(df)
        cmap = sns.cm.rocket_r
        sns.heatmap(df, cmap=cmap)
        plt.suptitle(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.show()



        




    
    def json_arr(self, Dir_Arr, number_dirs):
        
        Accept = []
        print(Dir_Arr)
        for d in os.listdir(Dir_Arr):
          print("loop started")
          try:
            if('Synapse_l.json' in os.listdir(Dir_Arr+ '/'+ d) ):
             #print(".json file found!")
             Accept.append(d)
            #else:
              #print("No .json file found!")
          except:
            print("No .json file found!")
  
            pass
        Syn_Arr_full= []
        bg_l_full= []
        for Dir in Dir_Arr:
          Syn_a_arr = []
          bg_l   = []
          for a in Accept:
            with open(Dir_Arr+'/'+a+'/Synapse_l.json', 'r') as fp: Syn_a_arr.append(json.load(fp))
            try:
              bg_l.append(np.load(Dir_Arr+'/'+a+"/backgroundM.npy").squeeze())
            except:
              bg_l.append(np.load(Dir_Arr+'/'+a+"/background.npy").squeeze())
            Syn_Arr_full.append(Syn_a_arr)
            bg_l_full.append(bg_l)
 
        return Syn_a_arr, bg_l
        


    








if __name__ == '__main__':
  do= Plots()
   

