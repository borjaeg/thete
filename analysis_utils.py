import collections
import os
import time
import re
import itertools

# Data Science
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# Plotting
from matplotlib.markers import MarkerStyle
from PIL import Image

from export_results import *
from utils import *
from scipy.stats import *
import pymysql.cursors

def load_results():

    results = []
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='agriculture_experiments',
                             charset='utf8')

    try:
        sql = \
        """
        SELECT nlp, algorithm, cost_ratio, AVG(prec) AS `precision`, AVG(recall) recall
        FROM results
        GROUP BY nlp, algorithm, cost_ratio
        """
        results = pd.read_sql(sql, connection)
    except Exception as e:
        print(e)
    finally:
        connection.close()
        
    return results

def get_best(data, algorithm):
    accepted_results = data.loc[(data["algorithm"] == algorithm) & 
         (data["recall"] == data.loc[(data["algorithm"] == 
                                      algorithm)]["recall"].max())]

    return accepted_results.loc[(accepted_results["precision"] == \
                                 accepted_results.loc[(accepted_results["algorithm"] \
                                                                            == algorithm)]["precision"].max())]
def save_image(image, url='../images/', name = 'default'):
    image.savefig(url + name)
#    Image.open(url + name + '.png').convert('L').save(url + name + '.png')
    
def plot_image(x, results, title="title", ylim = [0, 1.02], xlim = [2, 50.5], 
               colors="rgbmyc", file_name="name", labels=[], ylabel = "ylabel", 
               loc="better", markers=".,ov<>"):
    plt.figure(figsize=(14,13))
    plt.ylim(ylim)
    plt.xlim(xlim)
    plt.xlabel("Misclassification Cost Ratio")
    plt.ylabel(ylabel)
    plt.style.use('paper.mplstyle')
    
    filled_markers = ('<', 'D', 'o', '|', 'v', '>', 'p', 'd') #' '^', ', '>', '8', 's', 'p', '*', 'h', 'H', , 'd')
    fillstyles = ('full', 'full', 'full', 'full', 'top', 'none')
    colors = "rgbk"

    i = 0
    for record in results:
        model_name = record[1] + "-" + record[2]
        plt.plot(x, record[0], label=model_name, c=colors[i])
        marker = MarkerStyle(marker='o', fillstyle=fillstyles[i])
        plt.scatter(x, record[0], marker=marker, s=300, c=colors[i]) #, label=model_name)
        i+=1
    
    plt.xticks(x, labels, rotation='vertical')
    plt.legend(loc=loc, prop={'size':30})

    save_image(plt,'../images/', file_name)
    plt.show()
    
def get_best_by_cost(data, important_metric, algorithm, plot_metric):
    best_rf_experiment = data.loc[(data["algorithm"] == algorithm) & 
         (data[important_metric] == data.loc[(data["algorithm"] == 
                                      algorithm)][important_metric].max())]["n_experiment"].values[0]
    
    best_rf_nlp = data.loc[(data["algorithm"] == algorithm) & 
         (data[important_metric] == data.loc[(data["algorithm"] == 
                                      algorithm)][important_metric].max())]["nlp"].values[0]
    
    return np.array(data.loc[(data["algorithm"] == algorithm) & 
         (data["n_experiment"] == best_rf_experiment) &
         (data["nlp"] == best_rf_nlp)][plot_metric].values), algorithm, best_rf_nlp

def are_different(data, factor, metric, threshold = 0.05):
    
    results = []
    tested_values = []
    
    values = data[factor].unique()

    for value in values:
      results.append(data.loc[(data[factor] == value)][metric])
    
    for value, result in zip(values,results):
        print(value, result.mean())
        if mstats.normaltest(result)[1] < 0.05:
            parametric = False
    print()
        
    for value, result in zip(values,results):
        for value2, result2 in zip(values, results):
            if not value == value2 and value2 not in tested_values:
                tested_values.append(value)
                if not parametric:
                    z_stat, p_val = wilcoxon(result, result2, zero_method='wilcox', correction=False)
                else:
                    z_stat, p_val = ttest_ind(result, result2, equal_var=False)
                if p_val < threshold: # 0.05
                    print("Statistically significant different results between %s and %s" 
                          % (value, value2))
                else:
                    print("Statistically NON-significant different results between %s and %s" 
                          % (value, value2))