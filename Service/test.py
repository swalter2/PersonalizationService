# -*- coding: utf-8 -*-
#from learning import Learning
from database import Database
from xmlimporter import XMLImporter
#
host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'
#
#kogni_learning = Learning(host, user, password, db)
#kogni_learning.learn([], '1', '5')

database = Database(host, user, password, db)

importer = XMLImporter(database)

importer.read_xml_file('/Users/swalter/Downloads/xmlNW/8586833-Kogni-01072015.xml')

