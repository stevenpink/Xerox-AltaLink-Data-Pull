from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re, datetime, csv

# enter printer IP addresses seperated by commas as seen below
printers = ["10.10.10.10", "10.10.10.11"]

def tableDataText(table):       
    rows = []
    trs = table.find_all('tr')
    headerow = [td.get_text(strip=True) for td in trs[0].find_all('th')] # header row
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append([td.get_text(strip=True) for td in tr.find_all('td')]) # data row
    return rows

for printer in printers:
    geterror = False
    session1 = HTMLSession()
    session1.verify = False
    page1 = session1.get("http://" + printer + "/counters/usage.php", verify = False)
    page1.html.render()

    soup1 = BeautifulSoup(page1.html.html, 'lxml')

    datatable = tableDataText(soup1.find("table", {"class" : "tableDiv"}))

    for item in datatable:
        if item[0] == "Total Impressions":
            totalimpressions = item[1]
        if item[0] == "Black Copied 2 Sided Sheets":
            bc2ss = int(item [1])
        if item[0] == "Color Copied 2 Sided Sheets":
            cc2ss = int(item [1])
        if item[0] == "Black Printed 2 Sided Sheets":
            bp2ss = int(item [1])
        if item[0] == "Color Printed 2 Sided Sheets":
            cp2ss = int(item [1])
        if item[0] == "Embedded Fax 2 Sided Sheets":
            ef2ss = int(item [1])
    try:
        dupleximpressions = bc2ss + cc2ss + bp2ss + cp2ss + ef2ss
        print(printer)
        print(totalimpressions)
        print(dupleximpressions)
    except:
        print("Error gathering data for " + printer)

    with open('printerdata.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([printer, totalimpressions, dupleximpressions, geterror])
