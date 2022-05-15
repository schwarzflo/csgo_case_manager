from datetime import datetime
import matplotlib.dates
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import numpy as np
import json
import funcs
import csv


case_stats = "case_stats_n"
case_lib = "case_lib_n"
tot = "tot_n"


def pieplot(cutoff):

    y = []
    tiv = funcs.get_total_inv_value()
    f = open(case_lib, "r")
    data = json.load(f)
    for c in data["cases"]:
        pr = c["amount"] * funcs.price_from_website(c["link"])
        try:
            vs = 100*pr/tiv
        except:
            return
        dic = {"value_share": vs, "name": c["name"]}
        y.append(dic)

    y = sorted(y, key=lambda case: case["value_share"])
    y_cut = y[-cutoff:]
    rest = sum(case["value_share"] for case in y[:-cutoff])
    y_cut.append({"value_share": rest, "name": "Rest"})

    y_cut_plot = [case["value_share"] for case in y_cut]
    labels = [case["name"] for case in y_cut]

    plt.pie(y_cut_plot, labels=labels, autopct='%.1f%%')
    plt.show()


def barchart():

    y = []
    f = open(case_lib, "r")
    data = json.load(f)
    for c in data["cases"]:
        pr = c["amount"] * funcs.price_from_website(c["link"])
        y.append(pr)

    all = funcs.all_cases(printout=False)

    fig, ax = plt.subplots()
    bars = ax.bar(np.arange(len(data["cases"])),y)
    ax.set_xticks(np.arange(len(data["cases"])), labels=all)
    ax.bar_label(bars, fmt='%.2f')
    ax.set_ylabel("€")
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)
    plt.show()


def plot_tot(cutoff): #also plots case values

    f = open(tot, "r")
    tivs = []
    times = []
    for line in f:
        for cnt, char in enumerate(line):
            if char == " ":
                tiv = float(line[:cnt])
                time = line[cnt+1:-1]
                tivs.append(tiv)
                times.append(datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))
                break
    f.close()
    plt.plot(times,tivs)
    times2 = []
    f = open(case_stats, "r")
    data = json.load(f)
    da = len(data["dates"]) + 1#date amount
    ca = len(data["dates"][-1])-1 #case amount
    all_vals = []
    legend_data = ["TIV"]

    for cnti, case in enumerate(data["dates"][-1]):
        vals = []
        for cntj, date in enumerate(data["dates"]):
            if case == "time":
                vals.append(datetime.strptime(date[case], '%Y-%m-%d %H:%M:%S'))
            else:
                vals.append(date[case])
        vals.append(case)
        all_vals.append(vals)

    all_vals[1:] = sorted(all_vals[1:], key=lambda x: int(x[-2]))
    all_vals.reverse()

    for i in range(len(all_vals)-1): #last element is time
        if i < cutoff:
            legend_data.append(all_vals[i][-1])
            plt.plot(all_vals[-1][:-1], all_vals[i][:-1])
        else:
            plt.plot(all_vals[-1][:-1], all_vals[i][:-1],color="grey")

    plt.xlabel("time")
    plt.ylabel("Total Inventory Value (€)")
    plt.legend(legend_data)
    plt.show()
