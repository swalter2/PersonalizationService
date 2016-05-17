# -*- coding: utf-8 -*-
import wget
import os
import zipfile
import datetime
from database import Database
from learning import Learning
from xmlimporter import XMLImporter


host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'
#
#kogni_learning = Learning(host, user, password, db)
#kogni_learning.learn([], '1', '5')

database = Database(host, user, password, db)

today = datetime.datetime.now()
datum = today.strftime("%d%m%Y")
#datum = '21032016'

url = "http://ftp.forschungsdatenmanagement.org/nw/8586833-Kogni-"+datum+".zip"
#print(url)
#filename = wget.download(url)
filename = "8586833-Kogni-"+datum+".zip"
#print(filename)
#importer = XMLImporter(database)
#with zipfile.ZipFile(filename, 'r') as z:
#    z.extractall(filename.replace('.zip',''))
#print('extracted file')
#
#file_to_import = filename.replace('.zip','')+"/"+filename.replace('.zip', '.xml')
#if os.path.isfile(file_to_import):
#    print(file_to_import)
#    importer.read_xml_file(file_to_import)
#print('imported everything to DB')
#

database.checkanddeletearticleexceptdate(datum)
print('cleaned database from old articles')


print('start global learning')
learning = Learning(host, user, password, db, datum)
learning.global_learn()
print('done global learning')


for the_file in os.listdir(filename.replace('.zip','')):
    file_path = os.path.join(filename.replace('.zip',''), the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)
os.remove(filename)
os.rmdir(filename.replace('.zip',''))
print('done with all')