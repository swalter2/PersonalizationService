# -*- coding: utf-8 -*-
from nltk import word_tokenize

#fuer vergleich von interessen mit titel oder text
def compare_string_to_interests(string,interest_list, mode = 'prior_title'):
    result = {}
    for interest in interest_list:
        for word in word_tokenize(string):
            if word.lower() == interest.lower():
                result[mode + '_interest'] = 1
    return result

#fuer das prior feature mit den ressorts
def normalize_article_ressort_to_dict(article_ressort,ressort_list):
    result = {}
    for ressort in ressort_list:
        if article_ressort.lower() == ressort.lower():
            result[ressort] = 1
        else:
            result[ressort] = 0
    return result

#fuer die crossfeatures
def compute_cross_features(user_age,user_sex,user_education,article_ressort,ressort_list,article_normalized_page):
    cf_age_ressort = {}
    cf_sex_ressort = {}
    cf_edu_ressort = {}

    for ressort in ressort_list:
        pass
