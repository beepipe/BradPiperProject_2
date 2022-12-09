import csv
from os import path

def save_time(name, splits, times, totals):

    filename = str(name[0]) + '_splittimelog.csv'

    if path.exists(filename) == False:


        with open(filename, 'a', newline='') as csvfile:


            fieldnames = ['Name', 'Splits', 'Times', 'Totals']
            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)


            csvwriter.writeheader()

            i = 0

            while i < len(splits):
                csvwriter.writerow({'Name': name[i], 'Splits': splits[i], 'Times': times[i], 'Totals': totals[i]})
                i = i + 1

    else:

        with open(filename, 'a', newline='') as csvfile:


            fieldnames = ['Name', 'Splits', 'Times', 'Totals']
            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

            i = 0

            while i < len(splits):
                csvwriter.writerow({'Name': name[i], 'Splits': splits[i], 'Times': times[i], 'Totals': totals[i]})
                i = i + 1





