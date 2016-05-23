# -*- coding: utf-8 -*-

from sklearn import svm
from sklearn.feature_extraction import DictVectorizer
from sklearn import cross_validation
import numpy as np
import pickle
import sys

#listen nötig für cross-feature-berechnungen
RESSORTS = ['Kultur','Bielefeld','Sport Bielefeld','Politik','Sport_Bund']
NORMALIZED_PAGES = ['1','2','3','4-5','6-7','8','9-16','17-24','25+']
NORMALIZED_AGES = ['bis30','30-35','35-40','40-45','45-50','50-60','60-70','groeßer70']
SEXES = ['m','f']
EDUCATIONS = ['Mittlere Reife','Hochschulabschluss','Abitur','Sonstiges']

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

#fuer die user-spezifischen Ressort Features
def normalize_user_ressort_ratings_to_dict(user_information):
    result = {}
    for i in range(0,5):
        result[RESSORTS[i]] = user_information[i+3]
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

def ressort_mapping(ressort):
    result = ''

    if ressort in ['Gütersloh','Bünde','Warburg','Herford','Löhne','Lübbecke','Höxter','Paderborn',
                   'Enger-Spenge','Bad Oeynhausen','Bielefeld','Schloss Holte', 'Beilagen']:
        result = 'Bielefeld'
    elif ressort in ['Sport Herford','Sport Bielefeld','Sport Bad Oeynhausen','Sport Paderborn','Sport Bünde',
                     'Sport Lübbecke','Sport Schloß Holte','Sport Höxter','Sport Gütersloh']:
        result = 'Sport Bielefeld'
    elif ressort == 'Kultur':
        result = 'Kultur'
    elif result == 'Politik':
        result = 'Politik'
    elif result == 'Sport_Bund':
        result = 'Sport_Bund'

    return result

#fuer vergleich von interessen mit titel oder text
def compare_string_to_interests(string,interest_list, mode = 'prior_title'):
    result = {}
    for interest in interest_list:
        #todo hier besser splitten als mit space
        for word in string.split():
            if interest.lower() in word.lower():
                result[mode + '_interest'] = 1
    return result

#fuer die crossfeatures mit ressort und page_normalized
def compute_cross_features(user_age, user_sex, user_education, article_page, article_ressort):

    cf_age_ressort = {}
    cf_sex_ressort = {}
    cf_edu_ressort = {}

    for ressort in RESSORTS:

        if ressort_mapping(article_ressort) == ressort:

            for age in NORMALIZED_AGES:
                feature = '%s_%s' % (ressort,age)
                if normalize_age(user_age) == age:
                    cf_age_ressort[feature] = 1
                else:
                    cf_age_ressort[feature] = 0
            for sex in SEXES:
                feature = '%s_%s' % (ressort,sex)
                if user_sex == sex:
                    cf_sex_ressort[feature] = 1
                else:
                    cf_sex_ressort[feature] = 0
            for edu in EDUCATIONS:
                feature = '%s_%s' % (ressort,edu)
                if user_education == edu:
                    cf_edu_ressort[feature] = 1
                else:
                    cf_edu_ressort[feature] = 0

        else:

            for age in NORMALIZED_AGES:
                feature = "%s_%s" % (ressort,age)
                cf_age_ressort[feature] = 0
            for sex in SEXES:
                feature = "%s_%s" % (ressort,sex)
                cf_sex_ressort[feature] = 0
            for edu in EDUCATIONS:
                feature = "%s_%s" % (ressort,edu)
                cf_edu_ressort[feature] = 0


    cf_age_page = {}
    cf_sex_page = {}
    cf_edu_page = {}

    for normalized_page in NORMALIZED_PAGES:

        if normalize_pages(article_page) == normalized_page:

            for age in NORMALIZED_AGES:
                feature = '%s_%s' % (normalized_page,age)
                if normalize_age(user_age) == age:
                    cf_age_page[feature] = 1
                else:
                    cf_age_page[feature] = 0
            for sex in SEXES:
                feature = '%s_%s' % (normalized_page,sex)
                if user_sex == sex:
                    cf_sex_page[feature] = 1
                else:
                    cf_sex_page[feature] = 0
            for edu in EDUCATIONS:
                feature = '%s_%s' % (normalized_page,edu)
                if user_education == edu:
                    cf_edu_page[feature] = 1
                else:
                    cf_edu_page[feature] = 0

        else:

            for age in NORMALIZED_AGES:
                feature = "%s_%s" % (normalized_page,age)
                cf_age_page[feature] = 0
            for sex in SEXES:
                feature = "%s_%s" % (normalized_page,sex)
                cf_sex_page[feature] = 0
            for edu in EDUCATIONS:
                feature = "%s_%s" % (normalized_page,edu)
                cf_edu_page[feature] = 0

    return cf_age_ressort,cf_sex_ressort,cf_edu_ressort,cf_age_page,cf_sex_page,cf_edu_page

#User X findet Ressort Y gut und Artikel Z ist aus Ressort Y
def user_specific_ressort_ratings(ressort_ratings_user, ressort_artikel, threshold = 3):
    result = {}

    for key in ressort_ratings_user:
        dict_key = "ressort_specific_%s" % key
        if key == ressort_artikel and ressort_ratings_user[key] >= threshold:
            result[dict_key] = 1
        else:
            result[dict_key] = 0

    return result

#User X findet Ressort Y mit Wertung Z gut und Artikel ist aus Ressort Y
def user_specific_ressort_explicit_ratings(ressort_ratings_user,ressort_artikel):
    result = {}

    for ressort in ressort_ratings_user.keys():
        feature_name = 'user_specific_ressort_rating_' + ressort +'_'
        for j in range(1,6):
            feature_name += '%d' % j
            if ressort_ratings_user[ressort] == j and ressort_artikel == ressort:
                result[feature_name] = 1
            else:
                result[feature_name] = 0

    return result


