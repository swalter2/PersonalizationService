from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from sklearn import metrics
from sklearn import cross_validation
import numpy as np
from database import Database
from general import *
from textblob_de.lemmatizers import PatternParserLemmatizer
import operator
from itertools import islice
import pickle
import sys
from feature import *

from feature_extraction import *
_lemmatizer = PatternParserLemmatizer()
host = 'localhost'
user = 'wikipedia_new'
password = '1234567'
db = 'wikipedia_new'
database = Database(host, user, password, db)
ONLY_PERSONS = 0
WITHOUT_PERSONS = 1
ALL_ARTICLES = 2
VALUE = 200
stopwords = set()
for line in open('resources/germanST.txt'):
    line = line.replace('\n','')
    stopwords.add(line)

train(database)


#
# def createRessortFeature(artikel_resort,ressorts, feature):
#     for r in ressorts:
#         feature[r] = 0
#     feature[artikel_resort] = 1
#
# def createAgeFeature(age,feature):
#     if age < 30:
#         feature['bis30'] = 1
#         feature['30-35'] = 0
#         feature['35-40'] = 0
#         feature['40-45'] = 0
#         feature['45-50'] = 0
#         feature['50-60'] = 0
#         feature['60-70'] = 0
#         feature['groeßer70'] = 0
#     if age >= 30 and age < 35:
#         feature['bis30'] = 0
#         feature['30-35'] = 1
#         feature['35-40'] = 0
#         feature['40-45'] = 0
#         feature['45-50'] = 0
#         feature['50-60'] = 0
#         feature['60-70'] = 0
#         feature['groeßer70'] = 0
#     if age >= 35 and age < 40:
#         feature['bis30'] = 0
#         feature['30-35'] = 0
#         feature['35-40'] = 1
#         feature['45-50'] = 0
#         feature['50-60'] = 0
#         feature['60-70'] = 0
#         feature['groeßer70'] = 0
#     if age >= 40 and age < 45:
#         feature['bis30'] = 0
#         feature['30-35'] = 0
#         feature['35-40'] = 0
#         feature['40-45'] = 1
#         feature['45-50'] = 0
#         feature['50-60'] = 0
#         feature['60-70'] = 0
#         feature['groeßer70'] = 0
#     if age >= 45 and age < 50:
#         feature['bis30'] = 0
#         feature['30-35'] = 0
#         feature['35-40'] = 0
#         feature['40-45'] = 0
#         feature['45-50'] = 1
#         feature['50-60'] = 0
#         feature['60-70'] = 0
#         feature['groeßer70'] = 0
#     if age >= 50 and age < 60:
#         feature['bis30'] = 0
#         feature['30-35'] = 0
#         feature['35-40'] = 0
#         feature['40-45'] = 0
#         feature['45-50'] = 0
#         feature['50-60'] = 1
#         feature['60-70'] = 0
#         feature['groeßer70'] = 0
#     if age >= 60 and age < 70:
#         feature['bis30'] = 0
#         feature['30-35'] = 0
#         feature['35-40'] = 0
#         feature['40-45'] = 0
#         feature['45-50'] = 0
#         feature['50-60'] = 0
#         feature['60-70'] = 1
#         feature['groeßer70'] = 0
#     if age >= 70:
#         feature['bis30'] = 0
#         feature['30-35'] = 0
#         feature['35-40'] = 0
#         feature['40-45'] = 0
#         feature['45-50'] = 0
#         feature['50-60'] = 0
#         feature['60-70'] = 0
#         feature['groeßer70'] = 1
#
# def createBagOfWordsVector(words, artikel, feature):
#     for w in words:
#         feature['w_'+w] = 0
#     for x in artikel.split(" "):
#         feature['w_' + x] = 1
#
# def createUserVectors(user_ids):
#     vector = {}
#     for id in user_ids:
#         tmp_vector = database.getuserinterestvector(id,ALL_ARTICLES)
#         sorted_article_vector = sorted(tmp_vector.items(), key=operator.itemgetter(1), reverse=True)
#         reduced_sorted_tmp_vector = list(islice(sorted_article_vector, VALUE))
#         reduced_sorted_tmp_vector_hm = {}
#         for x, y in reduced_sorted_tmp_vector:
#             reduced_sorted_tmp_vector_hm[x] = y
#
#         vector[id] = reduced_sorted_tmp_vector_hm
#     return vector
#
#
# def createEsaVectors(artikel_ids):
#     vector = {}
#     for id in artikel_ids:
#         artikel = database.getannotatedarticletext(id)
#         tags = combine_noun_adjectives(_lemmatizer.lemmatize(artikel[1]))
#         list_tags = tags.split(" ")
#         hm_tags = {}
#
#         # make sure each term in a text is called only once, if it occours multiple times,
#         # simply multiply by the frequency
#         for t in list_tags:
#             if t in hm_tags:
#                 value = hm_tags[t]
#                 hm_tags[t] = value + 1
#             else:
#                 hm_tags[t] = 1
#
#         article_vector = {}
#         for input in hm_tags:
#             tmp_vector = database.getarticlesfromwikipedia(ALL_ARTICLES, input, 100)
#             for title in tmp_vector:
#                 if title in article_vector:
#                     # in the moment only addition of the scores, maybe also try averaging of the scores
#                     tmp = article_vector[title]
#                     article_vector[title] = tmp + tmp_vector[title] * hm_tags[input]
#                 else:
#                     article_vector[title] = tmp_vector[title] * hm_tags[input]
#         sorted_article_vector = sorted(article_vector.items(), key=operator.itemgetter(1), reverse=True)
#         reduced_sorted_article_vector = list(islice(sorted_article_vector, VALUE))
#         reduced_sorted_article_vector_hm = {}
#         for x, y in reduced_sorted_article_vector:
#             reduced_sorted_article_vector_hm[x] = y
#
#         vector[id] = reduced_sorted_article_vector_hm
#     return vector
#
# def main():
#     #clf = svm.SVC(gamma=0.001, C=100.)
#     annotations = database.getannotations()
#
#     annotations_clean = []
#     artikel_ids = set()
#     user_ids = set()
#     for annotation in annotations:
#         if annotation[2] == 1:
#             annotations_clean.append(annotation)
#         if annotation[2] == 4:
#             annotations_clean.append(annotation)
#
#     for annotation in annotations_clean:
#         artikel_ids.add(annotation[1])
#         user_ids.add((annotation[0]))
#
#     print('create artikel vectors')
#     artikel_vectors = {}
#     try:
#         artikel_vectors = pickle.load(open("resources/"+str(VALUE)+"_annotated_article_vectors.p", "rb"))
#     except:
#         #print("Unexpected error:", sys.exc_info()[0])
#         pass
#     if len(artikel_vectors) < 100:
#         artikel_vectors = createEsaVectors(artikel_ids)
#         pickle.dump(artikel_vectors, open("resources/"+str(VALUE)+"_annotated_article_vectors.p", "wb"))
#
#     print('create user vectors')
#     user_vectors = {}
#     try:
#         user_vectors = pickle.load(open("resources/"+str(VALUE)+"_annotated_user_vectors.p", "rb"))
#     except:
#         #print("Unexpected error:", sys.exc_info()[0])
#         pass
#     if len(user_vectors) < 10:
#         user_vectors = createUserVectors(user_ids)
#         pickle.dump(user_vectors, open("resources/"+str(VALUE)+"_annotated_user_vectors.p", "wb"))
#
#     print('get interests')
#     interessen = {}
#     for id in user_ids:
#         interessen[id] = database.getuserinterests(id)
#
#     print('get text and title')
#     hm_artikel_text = {}
#     hm_artikel_titel = {}
#     hm_artikel_ressort = {}
#     bag_of_words = set()
#     ressorts = set()
#     for id in artikel_ids:
#         artikel = database.getannotatedarticletext(id)
#         hm_artikel_text[id] = artikel[1]
#         for x in artikel[1].split(" "):
#             if x not in stopwords:
#                 bag_of_words.add(x)
#         hm_artikel_titel[id] = artikel[0]
#         hm_artikel_ressort[id] = artikel[2]
#         ressorts.add(artikel[2])
#     print(len(bag_of_words))
#     print('get user informations')
#     user_informations = {}
#     for id in user_ids:
#         user_informations[id] = database.getuserinformations(id)
#
#     print('done preprocessing')
#
#     features_annotation_1 = []
#     features_annotation_0 = []
#     bewertungen_1 = []
#     bewertungen_0 = []
#     for annotation in annotations_clean:
#         nutzerid = annotation[0]
#         artikelid = annotation[1]
#         bewertung = annotation[2]
#         nutzerinformation = user_informations[nutzerid]
#         if bewertung == 4:
#             bewertung = 0
#         nutzer_interessen = interessen[nutzerid]
#         artikel_resort = hm_artikel_ressort[artikelid]
#
#         esa_cos = calcualtecos(user_vectors[nutzerid], artikel_vectors[artikelid])
#         artikel_text = hm_artikel_text[artikelid]
#         artikel_titel = hm_artikel_titel[artikelid]
#
#         interessen_text_feature = 0
#         interessen_titel_feature = 0
#
#         for i in nutzer_interessen:
#             tmp = nutzer_interessen[i]
#             interesse = tmp['name']
#             if interesse in artikel_text:
#                 interessen_text_feature = 1
#             if interesse in artikel_titel:
#                 interessen_titel_feature = 1
#
#         feature = {}
#         feature['interessen_artikel_feature'] = interessen_text_feature
#         feature['interessen_titel_feature'] = interessen_titel_feature
#         feature['esa_cos'] = esa_cos
#         if esa_cos > 0.99:
#             feature['is_similar'] = 1
#         else:
#             feature['is_similar'] = 0
#         if nutzerinformation[1] == "m":
#             feature['m'] =1
#             feature['w'] = 0
#         else:
#             feature['m'] = 0
#             feature['w'] = 1
#         age = int(nutzerinformation[0])
#         createAgeFeature(age,feature)
#
#         #createRessortFeature(artikel_resort, ressorts, feature)
#
#         createBagOfWordsVector(bag_of_words,artikel_text,feature)
#
#         feature['interessen_kultur'] = nutzerinformation[2]
#         feature['interessen_lokales'] = nutzerinformation[3]
#         feature['interessen_lokalsport'] = nutzerinformation[4]
#         feature['interessen_politik'] = nutzerinformation[5]
#         feature['interessen_sport'] = nutzerinformation[6]
#
#
#         if bewertung == 0:
#             bewertungen_0.append(bewertung)
#             features_annotation_0.append(feature)
#         else:
#             bewertungen_1.append(bewertung)
#             features_annotation_1.append(feature)
#
#
#
#     print('created features')
#     vec = DictVectorizer()
#     features = []
#     bewertungen = []
#     number = 0
#     if len(features_annotation_0) > len(features_annotation_1):
#         number = len(features_annotation_1)
#     else:
#         number = len(features_annotation_0)
#     for i in range(0,number):
#         features.append(features_annotation_1[i])
#         bewertungen.append(bewertungen_1[i])
#         features.append(features_annotation_0[i])
#         bewertungen.append(bewertungen_0[i])
#     #average_esa = 0.0
#     #for f in features:
#     #    average_esa += f['esa_cos']
#     #average_esa = average_esa/len(features)
#     #for f in features:
#     #    if f['esa_cos'] > 0.0:
#     #        f['esa_cos'] = f['esa_cos']/average_esa
#     #    else:
#     #        f['esa_cos'] = 0.0
#     #print(average_esa)
#     print(len(features))
#     print(len(bewertungen))
#     feature_vectorized = vec.fit_transform(features)
#     X = np.array(feature_vectorized.toarray())
#     y = np.array(bewertungen)
#     #X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size = 0.2)
#     #clf = svm.SVC(kernel='linear', C=1,class_weight='balanced').fit(X_train, y_train)
#     #print(clf.score(X_test, y_test))
#     #print(clf.predict(X_test))
#     #print(y_test)
#     clf = svm.SVC(kernel='linear', C=1)
#     scores = cross_validation.cross_val_score(clf, X, y, cv = 10)
#     value = 0.0
#     for s in scores:
#         value+=s
#     print(scores)
#     print(value/len(scores))
#
#
#
#
# if __name__ == '__main__':
#     main()