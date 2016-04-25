# -*- coding: utf-8 -*-
#from learning import Learning
from database import Database
from xmlimporter import XMLImporter
import csv
#
host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'
#
#kogni_learning = Learning(host, user, password, db)
#kogni_learning.learn([], '1', '5')

database = Database(host, user, password, db)


with open('/Users/swalter/Desktop/test/personendaten.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in csvreader:
        id = row[0]
        interessen = row[9]
        #print(interessen)
        if ',' in interessen:
            for x in interessen.split(','):
                x = x.strip()
                print(id,x)
                database._tmp_add_interesse(id, x, '0.5')
        else:
            interessen = interessen.strip()
            print(id, interessen)
            database._tmp_add_interesse(id, interessen, '0.5')

#for line in codecs.open('/Users/swalter/Desktop/test/personendaten.csv','r','utf-8'):
#    line = line.split(',')
#    #database._tmp_add_interesse('1','aufräumen','0.2')

