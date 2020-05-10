import os
import shutil
import time
import datetime
import numpy as np
import json
import env
import matplotlib.pyplot as plt

def timestamp():
    return int(time.time())

def name(prefix="", suffix=""):
    return prefix + datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S") + suffix
    
def dump(json_object, path):
    f = open(path, 'w+')
    json.dump(json_object, f, indent=4)
    f.close()

def record(job, device, parameters, comment):
    properties = device.properties()
    json_object = {
        "timestamp": timestamp(),
        "account": env.ACCOUNT,
        "job": job.job_id(),
        "parameters": parameters,
        "build": env.BUILD,
        "comment": {
            "context": env.CONTEXT_COMMENT,
            "experiment": comment,
        }
    }

    if "simulator" in str(device):
        json_object["backend"] = {
            "name": str(device)
        }
    else:
        properties = device.properties()
        json_object["backend"] = {
            "name": properties.backend_name,
            "version": properties.backend_version,
            "last_update": int(datetime.datetime.timestamp(properties.last_update_date))
        }
    
    path = "../experiments/" + name("experiment_", ".json")
    dump(json_object, path)
    return path

def update(json_object, counts, path):
    json_object["counts"] = counts
    dump(json_object, path)
    
def retrieve(path):
    f = open(path, 'r')
    json_string = f.read()
    json_object = json.loads(json_string)
    f.close()
    return json_object

def accounts():
    return retrieve("../accounts.json")

def ft(values):
    return np.absolute(np.fft.fft(values))

def analytical_expectation(measurement_operator, state):
    return np.trace(np.matmul(measurement_operator, state))

# account_for_ examples
# ...to measure last qubit - [False, False, False, False, True] == I x I x I x I x Z
# ...to measure first two qubits state - [True, True, False, False, False] == Z x Z x I x I x I

def real_measurement(counts, account_for_):
    experiments_count = len(counts)
    results = []
    # all the experiments
    for i in range(experiments_count):
        # 1 experiment
        results.append(0)
        counts_i = counts[i]
        results_count = 0
        for key in counts_i:
            # 1 result
            coeff = 1
            j = -1
            for v in key:
                # 1 qubit
                j += 1
                if not account_for_[j]: continue
                # |0> = 1, |1> = -1
                if v == "1": coeff *= -1
            
            result = counts_i[key]
            results[i] += result * coeff
            results_count += result
            
        results[i] /= results_count
            
    return results

def plot(parameter_values, results, curves_names = None, title = '', x_name = '', y_name = '', path_to_file = None, include_ft = True):
    width = 15
    height = 15 if include_ft else 7
    rows = 2 if include_ft else 1
    columns = 1

    f = plt.figure(figsize=(width,height))
    sub1 = f.add_subplot(rows, columns, 1)
    sub1.set_title(title)
    sub1.set_xlabel(x_name)
    sub1.set_ylabel(y_name)
    sub1.set_ylim([-1.1, 1.1])

    sub2 = f.add_subplot(rows, columns, 2) if include_ft else None
    
    number_of_sets = len(parameter_values)
    for i in range(number_of_sets):
        result = results[i]
        result_ft = ft(result)
        
        curve_name = str(i) if curves_names == None else curves_names[i]

        # measurements
        sub1.plot(parameter_values[i], result, label = curve_name)
        sub1.legend()

        if not include_ft:
            continue

        # fft
        ft_range = range(len(result))
        sub2.bar(ft_range, result_ft, label = curve_name)
        sub2.legend()

    if not path_to_file == None:
        plt.savefig(path_to_file)

    plt.show()

def packExperiment(name, rename = None):
    if rename == None:
        rename = name
        
    original_path = '../experiments/' + name
    extensions = [
        '.json',
        '.pdf',
        '_transpiled.pdf',
        '_result.pdf'
    ]
    
    original_path = '../experiments/' + name
    target_path = '../experiments/' + rename 
    try:
        os.mkdir(target_path)
    except:
        pass
    
    target_path += '/' + rename
    
    for extension in extensions:
        original = original_path + extension
        target = target_path + extension
        try:
            shutil.copyfile(original, target)
        except:
            pass
