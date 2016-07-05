import collections
import os
import time
import re
import itertools

# Data Science
import numpy as np
import pandas as pd

from export_results import *
from utils import *
from scipy.stats import *
import pymysql.cursors

labels = ["1:1","1:2","1:4","1:6","1:10","1:25", "1:50", r"1:$10^2$", r"1:$10^3$", r"1:$10^6$"]
costs = np.array([2, 3, 4, 6, 10, 25, 50, 100, 1000, 1000000])
axis_costs = np.arange(1,11,1)
cxlim = [0.8, 10.15]

def load_results():

    results = []
    data = {}
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='agriculture_experiments',
                             charset='utf8')


    data["denormalized"] =[]
    data["grouped"] = [] 

    try:
        sql = \
        """
        SELECT nlp, algorithm, cost_ratio, prec AS `precision`, recall -- AVG(prec) AS `precision`, AVG(recall) recall
        FROM results
        WHERE nlp != 'Bigrams'
        -- GROUP BY nlp, algorithm, cost_ratio
        """

        data["denormalized"] = pd.read_sql(sql, connection)

        sql = \
        """
        SELECT nlp, algorithm, cost_ratio, AVG(prec) AS `precision`, AVG(recall) recall
        FROM results
        WHERE nlp != 'Bigrams'
        GROUP BY nlp, algorithm, cost_ratio
        """
        
        data["grouped"] = pd.read_sql(sql, connection)

    except Exception as e:
        print(e)
    finally:
        connection.close()
        
    return data


def get_best(data, algorithm):
    accepted_results = data["grouped"].loc[(data["grouped"]["algorithm"] == algorithm) & 
         (data["grouped"]["recall"] == data["grouped"].loc[(data["grouped"]["algorithm"] == 
                                      algorithm)]["recall"].max())]

    return accepted_results.loc[(accepted_results["precision"] == \
                                 accepted_results.loc[(accepted_results["algorithm"] \
                                                                            == algorithm)]["precision"].max())]
    
def get_best_costly_organised(data):

  recalls = []
  precisions = []

  for m in ["Naive Bayes", "Random Forest", "SVM", "Logistic", "Baseline"]:
    best = get_best(data, m).values[0]
    recalls.append((data["grouped"].loc[(data["grouped"]["algorithm"] == m) &
                   (data["grouped"]["nlp"] == best[0])]["recall"], m, best[0]))
    
    precisions.append((data["grouped"].loc[(data["grouped"]["algorithm"] == m) &
                   (data["grouped"]["nlp"] == best[0])]["precision"], m, best[0]))
    
  return recalls, precisions


def get_best_results_by_configuration(algorithm, nlp, data):
    conf_data = data["grouped"].loc[(data["grouped"]["algorithm"] == algorithm) & 
                      (data["grouped"]["nlp"] == nlp)]

    return conf_data[conf_data["recall"] == conf_data["recall"].max()].sort(["precision"], 
                     ascending=False).values[0]

def list_best_configurations(data):
  best_configurations = \
                      pd.DataFrame(
                         columns = ['nlp', 'algorithm', 'cost', 'precision', 'recall'])

  for element in itertools.product(data["grouped"]["algorithm"].unique(), 
                                   data["grouped"]["nlp"].unique()):
    result = get_best_results_by_configuration(element[0], element[1], data)
    dir_result = {"nlp": result[0],
          'algorithm': result[1],
          'cost': result[2],
          'precision': result[3],
          'recall': result[4]}

    best_configurations = best_configurations.append(pd.DataFrame(dir_result, index=[0]))

  return best_configurations



def are_different(data, factor, metric, threshold = 0.05):
    
    results = []
    tested_values = []
    
    values = data["denormalized"][factor].unique()

    for value in values:
      results.append(data["denormalized"].loc[(data["denormalized"][factor] == value)][metric])
    
    for value, result in zip(values,results):
        print(value, result.mean())
        if mstats.normaltest(result)[1] < 0.05:
            parametric = False

    print()
    if parametric:
      print("Parametric test")
    else:
      print("NON Parametric test")
    print()
        
    for value, result in zip(values,results):
        for value2, result2 in zip(values, results):
            if not value == value2 and value2 not in tested_values:
                tested_values.append(value)
                if not parametric:
                    # z_stat, p_val = wilcoxon(result, result2, zero_method='wilcox', correction=False)
                    z_stat, p_val = ttest_ind(result, result2, equal_var=False)
                else:
                    z_stat, p_val = ttest_ind(result, result2, equal_var=False)
                if p_val < threshold: # 0.05
                    print("Statistically significant different results between %s and %s" 
                          % (value, value2))
                else:
                    print("Statistically NON-significant different results between %s and %s" 
                          % (value, value2))