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