
import json
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
    #do= DACC.Plots(choice, Dir_Arr, x_label, y_label, plot_title, um_pixel, pixel_size, median, mean, std_err, error_bars, legend) 
    
    def __init__(self, choice, Dir_Arr, x_label, y_label, plot_title, um_pixel, pixel_size, median, mean, std_err, error_bars, legend ): #“Spine Density  [Bar-Graph]”, “Average Spine Area [Line Graph]”, “Average Spine Area [Bar Graph]” 
      self.Dir_Arr= Dir_Arr
      
      self.number_dirs=len(self.Dir_Arr)
      
      if choice=="Spine Density[Bar-Graph]":
        do= self.spine_desnity(x_label, y_label, plot_title, um_pixel, pixel_size, median, mean, std_err, error_bars, legend) #self, x_label, y_label, plot_title, um_pixel, pixel_size, median, mean, std_err, error_bars, legend)
      if choice=="Average Spine Area[Line Graph]":
        do= self.avg_area_line(x_label, y_label, plot_title, um_pixel, pixel_size, median, mean, std_err, error_bars, legend)
      if choice=="Average Spine Area[Bar Graph]":
        do=self.avg_area_bar(x_label, y_label, plot_title, um_pixel, pixel_size, median, mean, std_err, error_bars, legend)

  

    # def __init__(self):
    #   self.Dir_Arr= ["/Users/bhavikagopalani/hp/TestImages", "/Users/bhavikagopalani/Downloads/TestImages"]
    #   self.number_dirs= 2
    #   names= ["first", "second"]
    #   um_pixel= 0.66
    #   pixel_size= 1024*1024
    #   do= self.avg_area_line("Dataset Name", "No. of spines/um", "Spine Density", names, um_pixel, pixel_size, True, True, True )
      

         
          

    def get_factors(self, n, m):
    
     factors = []
     factor = int(n**(1.0/m) + .1) # fudged to deal with precision problem with float roots
     while n % factor != 0:
        factor = factor - 1
     factors.append(factor)
     if m > 1:
        factors = factors + self.get_factors(n / factor, m - 1)
     return factors


    def avg_area_bar(self, x_label, y_label, plot_title, um_pixel, pixel_size, median, mean, std_err, error_bars, legend): #xlabel, ylabel, title, error_bars, legend 
      Syn_Arr, bg_l= self.json_arr(self.Dir_Arr, self.number_dirs)
      size= []
      times= []
      location=[]
      avg_area= []

      
      for Syn_a,bg, i in zip(Syn_Arr,bg_l, range(len(Syn_Arr))):
            print(i)
            size.append(np.array([S["area"] for S in Syn_a]))
            times.append(np.array([S["Times"] for S in Syn_a])) 
            location.append([S["location"] for S in Syn_a])

      for i in range(self.number_dirs):
        avg_area.append(np.mean(size[i]))

      plt.bar(self.dataset_names, avg_area, color ='blue', width = 0.3)
 
      plt.xlabel(x_label)
      plt.ylabel(y_label)
      plt.title(plot_title)
      plt.show()

    def avg_area_line(self, x_label, y_label, plot_title, um_pixel, pixel_size, median, mean, std_err, error_bars, legend): #xlabel, ylabel, title, error_bars, legend
      Syn_Arr, bg_l= self.json_arr(self.Dir_Arr, self.number_dirs)
      size= []
      times= []
      location=[]
      avg_area= []

      
      for Syn_a,bg, i in zip(Syn_Arr,bg_l, range(len(Syn_Arr))):
            print(i)
            size.append(np.array([S["area"] for S in Syn_a]))
            times.append(np.array([S["Times"] for S in Syn_a])) 
            location.append([S["location"] for S in Syn_a])

      for i in range(self.number_dirs):
        avg_area.append(np.mean(size[i]))

      sns.lineplot(self.dataset_names, avg_area, color ='blue')
 
      plt.xlabel(x_label)
      plt.ylabel(y_label)
      plt.title(plot_title)
      plt.show()



    def spine_desnity(self, x_label, y_label, plot_title, um_pixel, pixel_size, median, mean, std_err, error_bars, legend): #um/pixel, pixel size, xlabel, ylabel, title, mean, median, std, error_bars, legend
      Syn_Arr, bg_l= self.json_arr(self.Dir_Arr, self.number_dirs)
      size= []
      times= []
      location=[]
    

      
      for Syn_a,bg, i in zip(Syn_Arr,bg_l, range(len(Syn_Arr))):
            print(i)
            size.append(np.array([S["area"] for S in Syn_a]))
            times.append(np.array([S["Times"] for S in Syn_a])) 
            location.append([S["location"] for S in Syn_a])

      # density= no. of spines per um= [(no. of spines)/ (um/pixel)]* pixels 

      density= []
      density= self.calc_density(location, size, um_pixel, pixel_size, self.number_dirs) 

      plt.bar(self.dataset_names, density, color ='blue', width = 0.3)
 
      plt.xlabel(x_label)
      plt.ylabel(y_label)
      plt.title(plot_title)
      if (mean):
        plt.axhline(y=np.mean(density),color='red')
      if (median):
        plt.axhline(y=np.median(density),color='green')
            # if (mode):
            #   plt.axvline(x=st.mode(x),color='blue')
      if (std_err):
        plt.axhline(y=np.std(density),color='yellow')

      plt.show()

    
    def calc_density(self, location, size, um_pixel, pixel_size, number_dirs):

      num_spines= []
      density_arr= []
      for i in range(number_dirs):
        a=len(size[i])
        print(a)
        density_arr.append((a/um_pixel)*pixel_size)

      return density_arr








       

       

      



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
            sns.histplot(x, stat= stat, kde= kde)
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



        

    
    def json_arr(self, Dir_Arr_N, number_dirs):
        
        Accept = []
        self.dataset_names= []

        

        #print(Dir_Arr)
        for Dir_Arr in Dir_Arr_N:

         #print(Dir_Arr)
         for d in os.listdir(Dir_Arr):
          #print("loop started")
          try:
            if('Synapse_l.json' in os.listdir(Dir_Arr+ '/'+ d) ):
             #print(".json file found!")
              Accept.append(d)
            #else:
              #print("No .json file found!")
          except:
            #print("No .json file found!")
  
            pass

        self.dataset_names= Accept
        Syn_Arr_full= []
        bg_l_full= []
        
        Syn_a_arr = []
        bg_l   = []
        for a, Dir_Arr in zip(Accept, Dir_Arr_N):
          with open(Dir_Arr+'/'+a+'/Synapse_l.json', 'r') as fp: Syn_a_arr.append(json.load(fp))
          try:
              bg_l.append(np.load(Dir_Arr+'/'+a+"/backgroundM.npy").squeeze())
          except:
              bg_l.append(np.load(Dir_Arr+'/'+a+"/background.npy").squeeze())
          Syn_Arr_full.append(Syn_a_arr)
          bg_l_full.append(bg_l)

        #print(Syn_a_arr, bg_l)
 
        return Syn_a_arr, bg_l
        


    








if __name__ == '__main__':
  do= Plots()
   

