import json
import time
import requests
import mal


def query_review(variables):
    # Here we define our query as a multi-line string
    query = '''
    query ($id: Int) { # Define which variables will be used in the query (id)
      Review (id: $id, mediaType: ANIME) {
        id
        summary
        body
        score
      }
    }
    '''

    url = 'https://graphql.anilist.co'

    # Make the HTTP Api request
    response = requests.post(url, json={'query': query, 'variables': variables})

    response.raise_for_status()
    data = response.json()
    response.close()

    return data


def save_reviews_to_json(username):
    mal_ids = mal.get_anime_ids(username)

    query = '''
    query ($id: Int) { # Define which variables will be used in the query (id)
      Media (idMal: $id, type: ANIME) {
        id
        reviews {
            nodes {
                id
                summary
                body
                score
            }
        }
      }
    }
    '''

    url = 'https://graphql.anilist.co'

    reviews = []
    for mal_id in mal_ids:
        variables = {
            'id': mal_id
        }

        # Make the HTTP Api request
        response = requests.post(url, json={'query': query, 'variables': variables})

        response.raise_for_status()
        data = response.json()
        response.close()

        reviews.append(data)

        time.sleep(1)

    # grab only the necessary info
    nodes = [review['data']['Media']['reviews']['nodes'] for review in reviews]
    flat = [item for sublist in nodes for item in sublist]

    # save to json file
    with open("reviews.json", "w") as output:
        json.dump(flat, output)
