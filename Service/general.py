# -*- coding: utf-8 -*-
import math

def combine_noun_adjectives(tags):
        output = ""
        tmp_output = ""
        for term, tag in tags:
            if "NN" in tag or "CD" in tag or "JJ" in tag or "NE" in tag or "FE" in tag:
                tmp_output += term + " "
            else:
                tmp_output = tmp_output.replace(" ", "_")
                output += tmp_output[:-1]+" "
                tmp_output = ""

        return output.lower()



def calcualtecos(vector1, vector2):
    #cos = skalar/(sqrt(norm_vec1)*sqrt(norm_vec2))

    #step1: create vector with all items in it
    vec1 = {}
    vec2 = {}
    for item in vector1:
        vec1[item] = 0.0
        vec2[item] = 0.0
    for item in vector2:
        vec1[item] = 0.0
        vec2[item] = 0.0

    #step2: fill vectors with actual values
    for item in vector1:
        vec1[item] = vector1[item]
    for item in vector2:
        vec2[item] = vector2[item]

    #step3: calculate scalar
    scalar = 0.0
    for item in vec1:
        scalar += vec1[item]*vec2[item]

    #step4: calculate norm
    norm_vec1 = 0.0
    for item in vec1:
        norm_vec1 += vec1[item]*vec1[item]
    norm_vec2 = 0.0
    for item in vec2:
        norm_vec2 += vec2[item]*vec2[item]

    if scalar == 0.0 or norm_vec1 == 0.0 or norm_vec2 == 0.0:
        return 0.0
    else:
        cos = scalar/(math.sqrt(norm_vec1)*math.sqrt(norm_vec2))
        return cos