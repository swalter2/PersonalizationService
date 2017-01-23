import json

from service import service

# js = json.dumps({'personId':1})
# print(js)


def get_scores_for_user(personId):
    print("Retrieving Scores for User {}...".format(personId))
    with service.test_client() as client:
        answer = client.post("/servicePersonalization",
                             data=json.dumps({'personid':personId}),
                           content_type='application/json')
        print("Finished retrieving scores!")
        return answer.data.decode("utf-8")

def get_article_data_for_date(date_str):
    print("Retrieving Article Data for {}...".format(date_str))
    with service.test_client() as client:
        answer = client.post("/serviceArticles",
                             data=json.dumps({'datum':'09052016'}),
                           content_type='application/json')
        print("Finished Retrieving Article Data!")
        return answer.data.decode('utf-8')


for i in range(1,10):
    data = json.loads(get_scores_for_user(i))
    print(data)
    for artikel in list(data):
        for artikelId in list(data['artikel']):
            print("{:<10}{:<40}{:>10.2f}".format(i,artikelId,data['artikel'][artikelId]['score']))
        # print(articleId)