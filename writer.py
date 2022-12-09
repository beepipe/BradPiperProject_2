import csv
from os import path

def save_time(name, splits, times, totals):

    filename = str(name[0]) + '.csv'


    with open(filename, 'a', newline='') as csvfile:


        fieldnames = ['Name', 'Splits', 'Times', 'Totals']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if path.exists(filename) == False:
            csvwriter.writeheader()

        i = 0

        while i < len(splits):
            csvwriter.writerow({'Name': name[i], 'Splits': splits[i], 'Times': times[i], 'Totals': totals[i]})
            i = i + 1




