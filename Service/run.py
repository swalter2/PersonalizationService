import wget
import os
import zipfile
import datetime
from database import Database
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


url = "http://ftp.forschungsdatenmanagement.org/nw/8586833-Kogni-"+datum+".zip"
filename = wget.download(url)
print(filename)
importer = XMLImporter(database)
with zipfile.ZipFile(filename, 'r') as z:
    z.extractall(filename.replace('.zip',''))
print('extracted file')
file_to_import = filename.replace('.zip','')+"/"+filename.replace('.zip', '.xml')
if os.path.isfile(file_to_import):
    print(file_to_import)
    importer.read_xml_file(file_to_import)
print('imported everything to DB')

database.checkanddeletearticleexceptdate(datum)
os.remove(filename)
os.rmdir(filename.replace('.zip',''))