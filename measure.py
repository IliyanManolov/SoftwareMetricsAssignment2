
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import csv
import pandas as pd


def get_performance_entries():
  driver = webdriver.Chrome(ChromeDriverManager().install())
  driver.get('https://en.wikipedia.org/wiki/Software_metric')
  performance_entries = driver.execute_script('return window.performance.getEntries();')
  driver.quit()
  return performance_entries

def add_entries_to_dictionary(dictionary, entries):
  for entry in entries:
    if "name" in entry:
      if entry["name"] not in dictionary:
        dictionary[entry["name"]] = [entry["duration"]]
      else:
        dictionary[entry["name"]].append(entry["duration"])

def get_link_averages(dictionary):
  result = {}
  for key in dictionary.keys():
    times_sum = sum(dictionary[key])
    result[key] = times_sum / len(dictionary[key])
  return result

def init(mainDict):
  for i in range(10):
    perf_entries = get_performance_entries()
    add_entries_to_dictionary(mainDict, perf_entries)
    with open(f"performance_entries_{i + 1}.json", 'w') as f:
      json.dump(perf_entries, f)
  return mainDict

def save_to_csv(data):
  with open('performance_times.csv','w') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerows(data.items())

def save_to_excel(csvFile, excelFile):
  read_file = pd.read_csv(f'{csvFile}.csv', delimiter=';')
  read_file.to_excel(f'{excelFile}.xlsx', index = None, header=True)

result = {}
init(result)
# print(result)
final_result = get_link_averages(result)
save_to_csv(final_result)
save_to_excel("performance_times", "performance_spreadsheet")
