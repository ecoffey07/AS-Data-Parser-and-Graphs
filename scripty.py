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

  globalList = {}
  customerList = {}
  providerList = {}
  peerList = {}

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
  ip_space = pd.read_csv("routeviews-rv6-20231105-1200.pfx2as.txt", sep = "\t", comment = "#", header=None)
  print(ip_space)

  spacelist = ip_space[1].to_list()
  
  X = ["0-25", "26-30", "31-32", "33-45", "36-37", "38-40", "41-43", "44-47", "47-50", "51-80", "80+"]
  X_axis = np.arange(len(X))
  bins=[0,25,30,32,35,37,40,43,46,50,80]
  hist, bin_edges = np.histogram(spacelist,bins) # make the histogram
  fig,ax = plt.subplots()
  ax.bar(range(len(hist)),hist,width=1,align='center',tick_label=
        ['{} - {}'.format(bins[i],bins[i+1]) for i,j in enumerate(hist)])
  
  i = 0
  for bar in hist:
    plt.text(X_axis[i] - 0.4, bar + 1000, bar)
    i += 1

  plt.xticks(X_axis, X)
  plt.xlabel("Amount of ASes with given IP Space")
  plt.ylabel("IP Space Size")
  plt.title("IP space size histogram")
  plt.show()


def part4():
  # Read in data 
  as_relationships = pd.read_csv("2023.AS-rel.txt", sep = "|", comment = "#", header=None)
  # as_relationships.reset_index()

  # Get the total amount of ASes
  maxAS = as_relationships[0].max()
  temp1 = as_relationships[0].tolist() # Get existing ASes to save processing power
  temp2 = as_relationships[1].tolist()
  ASList = list(set(temp1 + temp2)) # Remove duplicates
  ASList.sort()

  globalList = {}
  customerList = {}
  providerList = {}
  peerList = {}

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
  
  transit_count = 0
  entriprise_count = 0
  content_count = 0

  for i in ASList:
    if i not in customerList:
      # Enterprise or Content
      if i not in peerList:
        # Enterprise
        entriprise_count += 1
      else:
        # Content
        content_count += 1
    else:
      # Transit
      transit_count += 1

  class_data_2023 = [transit_count, entriprise_count, content_count]
  X = ['Transit','Enterprise','Content']
  X_axis = np.arange(len(X))

  bars2023 = plt.bar(X_axis, class_data_2023, 0.4)
  for bar in bars2023:
    yval = bar.get_height()
    plt.text(bar.get_x() + 0.1, yval + 1000, yval)

  plt.xticks(X_axis, X)
  plt.xlabel("Types of Classes")
  plt.ylabel("Number of ASes in Each Class")
  plt.title("Identifcation of AS Class by 2023 Relationship Data")
  plt.show()

def part5():
  # Read in data 
  as_relationships = pd.read_csv("2023.AS-rel.txt", sep = "|", comment = "#", header=None)
  # as_relationships.reset_index()

  connections = {}

  globalList = {}
  customerList = {}
  providerList = {}
  peerList = {}

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

  print("Creating connections")

  for row in as_relationships.itertuples():
    if row._1 not in connections:
      connections[row._1] = []
      connections[row._1].append(row._2)
    else:
      connections[row._1].append(row._2)
      # connections[row._1] = list(set(connections[row._1]))
    if row._2 not in connections:
      connections[row._2] = []
      connections[row._2].append(row._1)
    else:
      connections[row._2].append(row._1)
      # connections[row._2] = list(set(connections[row._2]))
  
  print("Finished creating connections, creating cliquea")
  
  # sortedGlobal = sorted(globalList, reverse=True) # Sort greatest to least
  globalList = dict(sorted(globalList.items(), key=lambda item: item[1], reverse=True))
  sortedGlobal = list(globalList.keys())
  Set = []
  for AS in sortedGlobal:
    if len(Set) == 0:
      print("Adding default " + str(AS))
      print(globalList[AS])
      print()
      Set.append(AS)
      continue
    connectionList = connections[AS]
    terminate = False
    for setvalue in Set:
      if setvalue not in connectionList and len(Set) > 10:
        terminate = True
        break
        # continue
    if terminate == True:
      terminate = False
      # break
      continue
    # Did not terminate, add to list
    print("Adding AS " + str(AS))
    Set.append(AS)
    # Check if the connectionList contains every value in the Set
  print("Connections analysed: ")
  print(Set)
  print("Size: " + str(len(Set)))

# part1()
# part2()
# part3()
# part4()
part5()