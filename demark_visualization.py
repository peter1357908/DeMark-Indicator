# usage: demark_visualization.py [csv_file [demark_interval]]
# 
# `csv_file`: a CSV file for some arbitrary stock that contains
#  a 'Date' column and a 'Adj Close' column.
# `demark_interval`: an integer specifying the interval between
# which the closing prices are compared
#
# This script plots the closing prices and annotate them according 
# to DeMark Indicators (here positive annotations are for the 
# bullish setup while negative annotations are for the bearish setup)
#
# Notably, exactly equal prices CONTINUE the trend (instead of
# terminating one), and the annotation starts assuming that a flip
# just happened at the first closing price to annotate
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import sys

# ---------------------------------------------------------------
# constant definitions
# ---------------------------------------------------------------
DEFAULT_DATA_FILENAME = 'sample_data_(ES=F).csv'
DEFAULT_DEMARK_INTERVAL = 4

# ---------------------------------------------------------------
# parsing input (expecting sane input)
# ---------------------------------------------------------------
arg_count = len(sys.argv)

if arg_count <= 1:
  data_filename = DEFAULT_DATA_FILENAME
else:
  data_filename = sys.argv[1]

if arg_count <= 2:
  demark_interval = DEFAULT_DEMARK_INTERVAL
else:
  demark_interval = int(sys.argv[2])

# ---------------------------------------------------------------
# loading data
# ---------------------------------------------------------------
df = pd.read_csv(data_filename, parse_dates=['Date'], index_col=[
                 'Date'], usecols=['Date', 'Adj Close'], delimiter=',')

# prune the rows with NaNs off the dataframe
df_pruned = df[df['Adj Close'].notnull()]

# ---------------------------------------------------------------
# plot set-up (excluding DeMark annotataion)
# ---------------------------------------------------------------
# plot the pruned dataframe and save the returned reference for annotation
plot_axes = df_pruned.plot(figsize=(15,9), style='.-')

# ---------------------------------------------------------------
# DeMark annotation
# ---------------------------------------------------------------
# update the plot with annotations; the above `pd.read_csv` ensures that
# the `index` returned by `iterrows()` contains the 'Date' value
#
# skip the first x closes (x is the demark_interval defined above)
comparing_row_index = 0
current_annotation = 0 # notice that 0 is a convenient starting value
for curr_date, curr_row in df_pruned[demark_interval:].iterrows():
  comparing_adj_close = df_pruned.iloc[comparing_row_index]['Adj Close']
  curr_adj_close = curr_row['Adj Close']

  if current_annotation < 0:
    # if we are in a bearish trend
    if comparing_adj_close < curr_adj_close:
      # and if we encounter a higher curr_adj_close,
      # switch the trend to be bullish
      current_annotation = 1
    else:
     # otherwise, keep going with the bearish trend
      current_annotation -= 1
  else:
    # if we are in a bullish trend... and so on.
    if comparing_adj_close > curr_adj_close:
      current_annotation = -1
    else:
      current_annotation += 1

  # label the trend and increment the index
  plot_axes.annotate(current_annotation, (curr_date, curr_adj_close), xytext=(0, 8), textcoords='offset points', fontsize=15)
  comparing_row_index += 1

# ---------------------------------------------------------------
# display the plot with matplotlib
# ---------------------------------------------------------------
plt.show()
