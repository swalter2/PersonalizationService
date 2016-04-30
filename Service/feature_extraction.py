# -*- coding: utf-8 -*-
from nltk import word_tokenize
import general
import numpy as np

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

#normalisiert seiten auf die von philipp recherchierten bereiche
def normalize_pages(self):
    dict = {'1':0,'2':0,'3':0,'4-5':0,'6-7':0,'8':0,'9-16':0,'17-24':0,'25+':0}
    if self.page == 1:
        dict['1'] = 1
    elif self.page == 2:
        dict['2'] = 1
    elif self.page == 3:
        dict['3'] = 1
    elif self.page < 6:
        dict['4-5'] = 1
    elif self.page < 8:
        dict['6-7'] = 1
    elif self.page == 8:
        dict['8'] = 1
    elif self.page < 17:
        dict['9-16'] = 1
    elif self.page < 25:
        dict['17-24'] = 1
    else:
        dict['25+'] = 1
    return dict



#fuer die crossfeatures
def compute_cross_features(user_age,user_sex,user_education,article_ressort,article_normalized_page,
                           ressort_list,pages_list,age_list,sexes_list,edu_list):
    cf_age_ressort = {}
    cf_sex_ressort = {}
    cf_edu_ressort = {}

    for ressort in ressort_list:

        if article_ressort == ressort:

            for age in age_list:
                feature = '%s_%s' % (ressort,age)
                if user_age == age:
                    cf_age_ressort[feature] = 1
                else:
                    cf_age_ressort[feature] = 0
            for sex in sexes_list:
                feature = '%s_%s' % (ressort,sex)
                if user_sex == sex:
                    cf_sex_ressort[feature] = 1
                else:
                    cf_sex_ressort[feature] = 0
            for edu in edu_list:
                feature = '%s_%s' % (ressort,edu)
                if user_education == edu:
                    cf_edu_ressort[feature] = 1
                else:
                    cf_edu_ressort[feature] = 0

        else:

            for age in age_list:
                feature = "%s_%s" % (ressort,age)
                cf_age_ressort[feature] = 0
            for sex in sexes_list:
                feature = "%s_%s" % (ressort,sex)
                cf_sex_ressort[feature] = 0
            for edu in edu_list:
                feature = "%s_%s" % (ressort,edu)
                cf_edu_ressort[feature] = 0

    cf_age_page = {}
    cf_sex_page = {}
    cf_edu_page = {}

    for normalized_page in pages_list:

        if article_normalized_page == normalized_page:

            for age in age_list:
                feature = '%s_%s' % (normalized_page,age)
                if user_age == age:
                    cf_age_page[feature] = 1
                else:
                    cf_age_page[feature] = 0
            for sex in sexes_list:
                feature = '%s_%s' % (normalized_page,sex)
                if user_sex == sex:
                    cf_sex_page[feature] = 1
                else:
                    cf_sex_page[feature] = 0
            for edu in edu_list:
                feature = '%s_%s' % (normalized_page,edu)
                if user_education == edu:
                    cf_edu_page[feature] = 1
                else:
                    cf_edu_page[feature] = 0

        else:

            for age in age_list:
                feature = "%s_%s" % (normalized_page,age)
                cf_age_page[feature] = 0
            for sex in sexes_list:
                feature = "%s_%s" % (normalized_page,sex)
                cf_sex_page[feature] = 0
            for edu in edu_list:
                feature = "%s_%s" % (normalized_page,edu)
                cf_edu_page[feature] = 0

    return cf_age_ressort,cf_sex_ressort,cf_edu_ressort,cf_age_page,cf_sex_page,cf_edu_page

def compute_annotation_esa_comparison(article, user_annotations, mode='pos'):

    cos_sims = []

    user_annotations = []

    for article,annotation in user_annotations:
        if mode == 'pos':
            if annotation == 4:
                #Todo: esa_vectors für die zwei Artikel aus DB
                esa_vec_current_article = []
                esa_vec_article = []
                cos_sim = general.calcualtecos(esa_vec_current_article,esa_vec_article)
                cos_sims.append(cos_sim)

        #nur negativ bewertete artikel nutzen
        elif mode == 'neg':
            if annotation == 1:
                #Todo: esa_vectors für die zwei Artikel aus DB
                esa_vec_current_article = []
                esa_vec_article = []
                cos_sim = general.calcualtecos(esa_vec_current_article,esa_vec_article)
                cos_sims.append(cos_sim)


    return np.min(cos_sims),np.max(cos_sims),np.mean(cos_sims)

def compute_general_feature_dict(user_list, ressort_list,pages_list,age_list,sexes_list,edu_list):

    feature_vector = []

    for user in user_list:
        #Todo: aus Datenbank holen
        user_age = False
        user_sex = False
        user_education = False

        user_annotations = []

        for article, annotation in user_annotations:
            #Todo: aus Datenbank holen
            article_ressort = False
            article_normalized_page = normalize_pages(False)


            ressort_prior_dict = normalize_article_ressort_to_dict(article_ressort,ressort_list)

            cf_age_ressort, cf_sex_ressort, cf_edu_ressort, cf_age_page, cf_sex_page, cf_edu_page = compute_cross_features(
                user_age,user_sex,user_education,article_ressort,article_normalized_page,ressort_list,pages_list,age_list,sexes_list,edu_list
            )

            annotation_comparison_min_pos, annotation_comparison_max_pos, annotation_comparison_mean_pos = compute_annotation_esa_comparison(article,user_annotations)
            annotation_comparison_min_neg, annotation_comparison_max_neg, annotation_comparison_mean_neg = compute_annotation_esa_comparison(article,user_annotations)

            annotation_comparison_dict = {'comparison_min_pos':annotation_comparison_min_pos, 'comparison_max_pos':annotation_comparison_max_pos,
                                          'comparison_mean_pos':annotation_comparison_mean_pos,'comparison_min_neg':annotation_comparison_min_neg,
                                          'comparison_max_neg':annotation_comparison_max_neg, 'comparison_mean_neg':annotation_comparison_mean_neg}

            #weitere feature-extraction hier einfügen

            #features in einem Dict zusammenfassen
            feature_dict = {}

            feature_dict.update(ressort_prior_dict)
            feature_dict.update(cf_age_ressort)
            feature_dict.update(cf_sex_ressort)
            feature_dict.update(cf_edu_ressort)
            feature_dict.update(cf_age_page)
            feature_dict.update(cf_sex_page)
            feature_dict.update(cf_edu_page)
            feature_dict.update(annotation_comparison_dict)

            feature_vector.append(feature_dict)

    return feature_vector



####    AB HIER ESA FEATURES, voerst nicht relevant, da vom Service selbst schon implementiert     ########

#berechne cosinus-vergleich von artikel und user. berechne zusätzlich, ob score besser
# als der durchschnitt der aktuellen Ausgabe
def esa_comparison_interests_article(user, article):
    esa_score_dict, avg_result = compute_cosine_sim_current_issue_for_user(user)

    better_than_avg = False
    if esa_score_dict[article] > avg_result:
        better_than_avg = True

    return esa_score_dict[article],better_than_avg


#berechnet dict mit esa-scores für alle artikel einer Ausgabe bezogen auf einen user
#normalisiert diese scores durch den besten Score der ausgabe. Gibt
#außerdem den durchschnittlichen score der normalisierten Liste zurück
def compute_cosine_sim_current_issue_for_user(user):
    result = {}
    #TODO: esa_vektoren für artikel und user bereitstellen
    esa_vec_user = False

    #TODO: liste aller artikel der aktuellen ausgabe bereitstellen
    list_of_articles_in_current_issue = []

    for article in list_of_articles_in_current_issue:
        esa_vec_article = False
        result[article] = general.calcualtecos(esa_vec_user,esa_vec_article)

    max_score_current_issue_x_user = np.max(result.values())

    for article in result.keys():
        result[article] /= max_score_current_issue_x_user

    avg_score_current_issue_x_user = np.mean(result.values())

    return result, avg_score_current_issue_x_user



