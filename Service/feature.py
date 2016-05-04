# -*- coding: utf-8 -*-

from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from sklearn import cross_validation
import numpy as np
import pickle
import sys

#normalisiert seiten auf die von philipp recherchierten bereiche
def normalize_pages(page):
    dict = {'1':0,'2':0,'3':0,'4-5':0,'6-7':0,'8':0,'9-16':0,'17-24':0,'25+':0}
    if page == 1:
        dict['1'] = 1
    elif page == 2:
        dict['2'] = 1
    elif page == 3:
        dict['3'] = 1
    elif page < 6:
        dict['4-5'] = 1
    elif page < 8:
        dict['6-7'] = 1
    elif page == 8:
        dict['8'] = 1
    elif page < 17:
        dict['9-16'] = 1
    elif page < 25:
        dict['17-24'] = 1
    else:
        dict['25+'] = 1
    return dict


def normalize_age(age):
    feature = {}
    if age < 30:
        feature['bis30'] = 1
        feature['30-35'] = 0
        feature['35-40'] = 0
        feature['40-45'] = 0
        feature['45-50'] = 0
        feature['50-60'] = 0
        feature['60-70'] = 0
        feature['groeßer70'] = 0
    if age >= 30 and age < 35:
        feature['bis30'] = 0
        feature['30-35'] = 1
        feature['35-40'] = 0
        feature['40-45'] = 0
        feature['45-50'] = 0
        feature['50-60'] = 0
        feature['60-70'] = 0
        feature['groeßer70'] = 0
    if age >= 35 and age < 40:
        feature['bis30'] = 0
        feature['30-35'] = 0
        feature['35-40'] = 1
        feature['45-50'] = 0
        feature['50-60'] = 0
        feature['60-70'] = 0
        feature['groeßer70'] = 0
    if age >= 40 and age < 45:
        feature['bis30'] = 0
        feature['30-35'] = 0
        feature['35-40'] = 0
        feature['40-45'] = 1
        feature['45-50'] = 0
        feature['50-60'] = 0
        feature['60-70'] = 0
        feature['groeßer70'] = 0
    if age >= 45 and age < 50:
        feature['bis30'] = 0
        feature['30-35'] = 0
        feature['35-40'] = 0
        feature['40-45'] = 0
        feature['45-50'] = 1
        feature['50-60'] = 0
        feature['60-70'] = 0
        feature['groeßer70'] = 0
    if age >= 50 and age < 60:
        feature['bis30'] = 0
        feature['30-35'] = 0
        feature['35-40'] = 0
        feature['40-45'] = 0
        feature['45-50'] = 0
        feature['50-60'] = 1
        feature['60-70'] = 0
        feature['groeßer70'] = 0
    if age >= 60 and age < 70:
        feature['bis30'] = 0
        feature['30-35'] = 0
        feature['35-40'] = 0
        feature['40-45'] = 0
        feature['45-50'] = 0
        feature['50-60'] = 0
        feature['60-70'] = 1
        feature['groeßer70'] = 0
    if age >= 70:
        feature['bis30'] = 0
        feature['30-35'] = 0
        feature['35-40'] = 0
        feature['40-45'] = 0
        feature['45-50'] = 0
        feature['50-60'] = 0
        feature['60-70'] = 0
        feature['groeßer70'] = 1

    return feature

#fuer das prior feature mit den ressorts
def normalize_article_ressort_to_dict(article_ressort,ressort_list):
    result = {}
    for ressort in ressort_list:
        if article_ressort.lower() == ressort.lower():
            result[ressort] = 1
        else:
            result[ressort] = 0
    return result

def user_information_vector(user):
    result = {}

    if user[1]=='m':
        result['gender_m'] = 1
        result['gender_f'] = 0
    else:
        result['gender_m'] = 0
        result['gender_f'] = 1

    result['Mittlere Reife'] = 0
    result['Hochschulabschluss'] = 0
    result['Abitur'] = 0
    result['Sonstiges'] = 0
    result[user[2]] = 1
    result.update(normalize_age(user[0]))


    #informations.append(row.get('geschlecht'))
    #informations.append(row.get('abschluss'))
    #if user[3] == 1:
    #    result['interessen_kultur'] = 0
    #else:
    #    result['interessen_kultur'] = 1
#
    #if user[4] == 1:
    #    result['interessen_lokales'] = 0
    #else:
    #    result['interessen_lokales'] = 1
#
    #if user[5] == 1:
    #    result['interessen_lokalsport'] = 0
    #else:
    #    result['interessen_lokalsport'] = 1

    #if user[6] == 1:
    #    result['interessen_politik'] = 0
    #else:
    #    result['interessen_politik'] = 1

    #if user[7] == 1:
    #    result['interessen_sport'] = 0
    #else:
    #    result['interessen_sport'] = 1
    #result['interessen_kultur'] = user[3]
    #result['interessen_lokales'] = user[4]
    #result['interessen_lokalsport'] = user[5]
    #result['interessen_politik'] = user[6]
    #result['interessen_sport'] = user[7]

    return result

def train(database):
    annotations = database.getannotations()

    features = []
    features_0=[]
    features_1 = []
    bewertungen = []
    bewertungen_0 = []
    bewertungen_1 = []

    annotations_clean = []
    artikel_ids = set()
    user_ids = set()

    for annotation in annotations:
        if annotation[2] == 1:
            annotations_clean.append(annotation)
        if annotation[2] == 4:
            annotations_clean.append(annotation)

    for annotation in annotations_clean:
        artikel_ids.add(annotation[1])
        user_ids.add((annotation[0]))

    user_informations = {}
    for id in user_ids:
        user_informations[id] = database.getuserinformations(id)

    article_informations = {}
    for id in artikel_ids:
        article_informations[id] = database.getannotatedarticleinformations(id)

    ressort_list = database.get_ressort_list()

    for annotation in annotations:
        if annotation[2] == 1 or annotation[2] == 4:
            artikel_id = annotation[1]
            user_id = annotation[0]
            feature = {}
            article = article_informations[artikel_id]
            user = user_informations[user_id]
            feature.update(normalize_article_ressort_to_dict(article[2],ressort_list))
            feature.update(normalize_pages(article[3]))
            feature.update(user_information_vector(user))
            if annotation[2] == 4:
                bewertungen_0.append(0)
                features_0.append(feature)
            else:
                bewertungen_1.append(1)
                features_1.append(feature)

    number = 0
    if len(features_0) > len(features_1):
        number = len(features_1)
    else:
        number = len(features_0)
    for i in range(0,number):
        features.append(features_1[i])
        bewertungen.append(bewertungen_1[i])
        features.append(features_0[i])
        bewertungen.append(bewertungen_0[i])

    pickle.dump(features, open("resources/training_features.p", "wb"))
    pickle.dump(bewertungen, open("resources/training_features_annotations.p", "wb"))
    vec = DictVectorizer()
    feature_vectorized = vec.fit_transform(features)
    X = np.array(feature_vectorized.toarray())
    y = np.array(bewertungen)
    clf = svm.SVC(kernel='linear', C=0.1)
    scores = cross_validation.cross_val_score(clf, X, y, cv = 10)
    value = 0.0
    for s in scores:
        value+=s
    print(scores)
    print(value/len(scores))





