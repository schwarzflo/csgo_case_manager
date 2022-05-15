import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import urllib.request
from PIL import Image, ImageTk

case_stats = "case_stats_n"
case_lib = "case_lib_n"
tot = "tot_n"

def get_amount(case):
    f = open(case_lib, "r")
    data = json.load(f)
    for c in data["cases"]:
        if c["name"] == case:
            am = c["amount"]
            f.close()
            return am
    f.close()
    return None


def get_price(case):
    f = open(case_lib, "r")
    data = json.load(f)
    for c in data["cases"]:
        if c["name"] == case:
            pr = price_from_website(c["link"])
            f.close()
            return pr
    f.close()
    return None


def alter_amount(case, am):
    f = open(case_lib, "r")
    data = json.load(f)
    f.close()
    for c in data["cases"]:
        if c["name"] == case:
            c["amount"] = am
    f = open(case_lib, "w")
    f.write(json.dumps(data))
    f.close()


def add_case(case, am, link):
    f = open(case_lib, "r")
    data = json.load(f)
    f.close()
    data["cases"].append({"name": case, "amount": am, "link": link})
    data["cases"] = sorted(data["cases"],key=lambda case: case["name"])
    f = open(case_lib, "w")
    f.write(json.dumps(data))
    f.close()
    print("Case successfully added.")


def delete_case(case):
    f = open(case_lib, "r")
    data = json.load(f)
    f.close()
    deletion = False
    for c in data["cases"]:
        if c["name"] == case:
            data["cases"].remove(c)
            deletion = True
    f = open(case_lib, "w")
    f.write(json.dumps(data))
    f.close()
    return deletion


def get_total_inv_value():
    now = datetime.now()
    now = now.replace(microsecond=0)
    date_dict = {"time": str(now)}
    f = open(case_lib, "r")
    data = json.load(f)
    total = 0
    for c in data["cases"]:
        if c["amount"] != 0:
            add = c["amount"] * price_from_website(c["link"])
            total += add
            date_dict[c["name"]] = add
        else:
            date_dict[c["name"]] = 0
    f.close()
    save_to_file(total,now)
    g = open(case_stats, "r")
    data = json.load(g)
    g.close()
    data["dates"].append(date_dict)
    g = open(case_stats, "w")
    g.write(json.dumps(data))
    g.close()

    return total


def all_cases(printout):
    f = open(case_lib, "r")
    data = json.load(f)
    all = []
    for c in data["cases"]:
        all.append(c["name"])
    if printout == True:
        print(all)
    else:
        return all


def price_from_website(site):

    try:
        page = requests.get(site)
    except:
        return(0.00)

    soup = BeautifulSoup(page.content, 'html.parser')
    relevant_str = str(soup.find_all('a', class_="btn btn-default market-button-item")[0])

    pos = relevant_str.find('>')
    string = ''
    i = 1

    while relevant_str[pos + i] != "€":
        if relevant_str[pos + i] == ",":
            string = string + "."
        elif relevant_str[pos + i] == "-":
            string += "0"
        else:
            string = string + relevant_str[pos + i]
        i += 1

    return float(string)


def get_all_info():

    f = open(case_lib, "r")
    data = json.load(f)
    #print(data["cases"])
    return data["cases"]


def save_to_file(tiv,now):

    f = open(tot, "a+") #tiv over time
    f.write(str(tiv))
    f.write(" ")
    f.write(str(now))
    f.write("\n")
    f.close()


def get_im_from_site(chosen_case):

    f = open(case_lib, "r")
    data = json.load(f)
    for case in data["cases"]:
        if case["name"] == chosen_case:
            site = case["link"]
            page = requests.get(site)
            soup = BeautifulSoup(page.content, 'html.parser')
            img_link = soup.find_all('a', class_="market-button-item")[0].findAll('img')[0]['src']
            urllib.request.urlretrieve(img_link,"case.png")
            img = ImageTk.PhotoImage(Image.open("case.png"))

            return img

    print("Error, Image not found.")