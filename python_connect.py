import csv


name = input('What is your name?')
skin_type = input('What is your skin type?')


with open('database.csv', mode='a', newline='') as database:
    csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow([name,skin_type])
