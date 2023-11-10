import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from collections import defaultdict

def part1():
  # Read in data for both years
  data_2015 = pd.read_csv("20150801.as2types.txt", sep = "|", comment = "#", header=None)
  data_2021 = pd.read_csv("20210401.as2types.txt", sep = "|", comment = "#", header=None)

  # Filter the data and count how many of each type
  class_data_2015 = [0] * 3
  class_data_2015[0] = len(data_2015[data_2015[2].str.contains("Transit")])
  class_data_2015[1] = len(data_2015[data_2015[2].str.contains("Enterpise")])
  class_data_2015[2] = len(data_2015[data_2015[2].str.contains("Content")])

  class_data_2021 = [0] * 3
  class_data_2021[0] = len(data_2021[data_2021[2].str.contains("Transit")])
  class_data_2021[1] = len(data_2021[data_2021[2].str.contains("Enterprise")])
  class_data_2021[2] = len(data_2021[data_2021[2].str.contains("Content")])

  # Debug prints
  print(class_data_2015)
  print("#####")
  print(class_data_2021)

  # Graph data: GRAPH #1
  # Graphing code taken from https://www.geeksforgeeks.org/plotting-multiple-bar-charts-using-matplotlib-in-python/
  X = ['Transit','Enterprise','Content']
  X_axis = np.arange(len(X))
  bars2015 = plt.bar(X_axis - 0.2, class_data_2015, 0.4, label = '2015 Data')
  bars2021 = plt.bar(X_axis + 0.2, class_data_2021, 0.4, label = '2021 Data')
  for bar in bars2015:
    yval = bar.get_height()
    plt.text(bar.get_x() + 0.1, yval + 1000, yval)
  for bar in bars2021:
    yval = bar.get_height()
    plt.text(bar.get_x() + 0.1, yval + 1000, yval)
  plt.xticks(X_axis, X)
  plt.xlabel("Types of Classes")
  plt.ylabel("Number of ASes in Each Class")
  plt.title("Comparison of 2015 and 2021 AS Classes")
  plt.legend()
  plt.show()

def part2():
  # Read in data 
  as_relationships = pd.read_csv("2023.AS-rel.txt", sep = "|", comment = "#", header=None)
  # as_relationships.reset_index()

  # Get the total amount of ASes
  maxAS = as_relationships[0].max()
  temp1 = as_relationships[0].tolist() # Get existing ASes to save processing power
  temp2 = as_relationships[1].tolist()
  ASList = list(set(temp1 + temp2)) # Remove duplicates
  ASList.sort()

  # Create a mapping between AS_i and all the data we will be collecting
  # @dataclass
  # class Entry:
  #   ID: int
  #   global_degree: int = 0
  #   customer_degree: int = 0
  #   peer_degree: int = 0
  #   provider_degree: int = 0
  globalList = {}
  customerList = {}
  providerList = {}
  peerList = {}
  
  entryMap = {}

  for row in as_relationships.itertuples():
    if row._3 == 0:
      # Peer
      skip1 = False
      skip1global = False
      skip2 = False
      skip2global = False
      if row._1 not in peerList:
        peerList[row._1] = 1
        skip1 = True
      if row._2 not in peerList:
        peerList[row._2] = 1
        skip2 = True
      if row._1 not in globalList:
        globalList[row._1] = 1
        skip1global = True
      if row._2 not in globalList:
        globalList[row._2] = 1
        skip2global = True
      if not skip1:
        peerList[row._1] = peerList[row._1] + 1
      if not skip1global:
        globalList[row._1] = globalList[row._1] + 1
      if not skip2:
        peerList[row._2] = peerList[row._2] + 1
      if not skip2global:
        globalList[row._2] = globalList[row._2] + 1
    else:
      # Customer/Provider
      # The AS in the first column is a provider to the AS customer in the second column
      skip1 = False
      skip1global = False
      skip2 = False
      skip2global = False
      if row._1 not in customerList:
        customerList[row._1] = 1
        skip1 = True
      if row._2 not in providerList:
        providerList[row._2] = 1
        skip2 = True
      if row._1 not in globalList:
        globalList[row._1] = 1
        skip1global = True
      if row._2 not in globalList:
        globalList[row._2] = 1
        skip2global = True
      if not skip1:
        customerList[row._1] = customerList[row._1] + 1
      if not skip1global:
        globalList[row._1] = globalList[row._1] + 1
      if not skip2:
        providerList[row._2] = providerList[row._2] + 1
      if not skip2global:
        globalList[row._2] = globalList[row._2] + 1
  
  X = ["0", "1", "2-5", "6-100", "101-200", "201-1000", "1000+"]
  X_axis = np.arange(len(X))
  bins=[0,1,2,5,100,200,1000]
  hist, bin_edges = np.histogram(list(globalList.values()),bins) # make the histogram
  fig,ax = plt.subplots()
  ax.bar(range(len(hist)),hist,width=1,align='center',tick_label=
        ['{} - {}'.format(bins[i],bins[i+1]) for i,j in enumerate(hist)])
  plt.xticks(X_axis, X)
  plt.xlabel("Amount of Global Connections")
  plt.ylabel("Number of ASes")
  plt.title("Global Degree (All Connections) Histogram")
  plt.show()

  plt.figure()

  bins=[0,1,2,5,100,200,1000]
  hist, bin_edges = np.histogram(list(customerList.values()),bins) # make the histogram
  fig,ax = plt.subplots()
  ax.bar(range(len(hist)),hist,width=1,align='center',tick_label=
        ['{} - {}'.format(bins[i],bins[i+1]) for i,j in enumerate(hist)])
  plt.xticks(X_axis, X)
  plt.xlabel("Amount of Customer Connections")
  plt.ylabel("Number of ASes")
  plt.title("Customer Degree Histogram")
  plt.show()

  plt.figure()

  bins=[0,1,2,5,100,200,1000]
  hist, bin_edges = np.histogram(list(peerList.values()),bins) # make the histogram
  fig,ax = plt.subplots()
  ax.bar(range(len(hist)),hist,width=1,align='center',tick_label=
        ['{} - {}'.format(bins[i],bins[i+1]) for i,j in enumerate(hist)])
  plt.xticks(X_axis, X)
  plt.xlabel("Amount of Peer Connections")
  plt.ylabel("Number of ASes")
  plt.title("Peer Degree Histogram")
  plt.show()

  plt.figure()
  
  bins=[0,1,2,5,100,200,1000]
  hist, bin_edges = np.histogram(list(providerList.values()),bins) # make the histogram
  fig,ax = plt.subplots()
  ax.bar(range(len(hist)),hist,width=1,align='center',tick_label=
        ['{} - {}'.format(bins[i],bins[i+1]) for i,j in enumerate(hist)])
  plt.xticks(X_axis, X)
  plt.xlabel("Amount of Provider Connections")
  plt.ylabel("Number of ASes")
  plt.title("Provider Degree Histogram")
  plt.show()

def part3():
  print("TEMP")

# part1()
#part2()
part3()