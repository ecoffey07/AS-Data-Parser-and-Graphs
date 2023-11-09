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

  # TEMPLATE BELOW:
  # Get the providers / possible peers
  #     provider_peer = as_relationships[as_relationships[0] == 42]
  # Filter out the peers from the providers
  #     peer1 = provider_peer[provider_peer[2] == 0]
  #     peer1.reset_index()
  # Filter out the providers from the peers
  #     provider = provider_peer[provider_peer[2] == -1]
  # Get the customers / possible peers
  #     customer_peer = as_relationships[as_relationships[1] == 42]
  # Filter out the peers from the customers
  #     peer2 = customer_peer[customer_peer[2] == 0]
  # Swap the first and second columns of the peers to line it up with the first group
  #     peer2 = peer2[peer2.columns[[1,0,2,3]]]
  #     peer2.reset_index()
  # Filter out the customers from the pe
  #     customer = customer_peer[customer_peer[2] == -1]
  # Combine both frames of peers into one and drop any duplicate data points
  #     peers = pd.concat([peer1,peer2]).drop_duplicates().reset_index(drop=True)
  # END TEMPLATE
  
  print("Total providers for 42 " + str(len(provider)))
  print("Total customers for 42 " + str(len(customer)))
  print("Total peers for 42 " + str((len(peer1) + len(peer2))))

  # Create a mapping between AS_i and all the data we will be collecting
  @dataclass
  class Entry:
    ID: int
    global_degree: int = 0
    customer_degree: int = 0
    peer_degree: int = 0
    provider_degree: int = 0
  
  entryMap = {}

  for i in range(maxAS):
    # Following template as shown and commented above
    provider_peer = as_relationships[as_relationships[0] == i]
    peer1 = provider_peer[provider_peer[2] == 0]
    peer1.reset_index()
    provider = provider_peer[provider_peer[2] == -1]

  #for row in as_relationships.itertuples():
  
    

# part1()
part2()