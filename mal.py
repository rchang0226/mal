import json
import requests
import secrets

CLIENT_ID = 'cbadc00b08bcef5877d7504b85f6e35e'
CLIENT_SECRET = 'YOUR CLIENT SECRET'


# 1. Generate a new Code Verifier / Code Challenge.
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]


# 2. Print the URL needed to authorise your application.
def print_new_authorisation_url(code_challenge: str):
    global CLIENT_ID

    url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={CLIENT_ID}&code_challenge={code_challenge}'
    print(f'Authorise your application by clicking here: {url}\n')


# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token(authorisation_code: str, code_verifier: str) -> dict:
    global CLIENT_ID, CLIENT_SECRET

    url = 'https://myanimelist.net/v1/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        # 'client_secret': CLIENT_SECRET,
        'code': authorisation_code,
        'code_verifier': code_verifier,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the request contains errors

    token = response.json()
    response.close()
    print('Token generated successfully!')

    with open('token.json', 'w') as file:
        json.dump(token, file, indent=4)
        print('Token saved in "token.json"')

    return token


# 4. Test the API by requesting your profile information
def print_user_info(access_token: str):
    url = 'https://api.myanimelist.net/v2/users/@me'
    response = requests.get(url, headers={
        'Authorization': f'Bearer {access_token}'
    })

    response.raise_for_status()
    user = response.json()
    response.close()

    print(f"\n>>> Greetings {user['name']}! <<<")


# Runs #1-4 from above
def run_one_through_four():
    code_verifier = code_challenge = get_new_code_verifier()
    print_new_authorisation_url(code_challenge)

    authorisation_code = input('Copy-paste the Authorisation Code: ').strip()
    token = generate_new_token(authorisation_code, code_verifier)

    print_user_info(token['access_token'])


def get_anime_titles(user):
    url = f'https://api.myanimelist.net/v2/users/{user}/animelist?status=completed&limit=100'
    response = requests.get(url, headers={
        'Authorization': f'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImNjY2VhNTg0OTlkMjAwZTRiMjQ5ZTlkYTA5NjhhZGU0ODA5YWM5ZTA1MzNjZDBiNjU3NWZjZDc1MGJlYTAyMGEzNmQ4N2U2NTMwODdmZjgxIn0.eyJhdWQiOiJjYmFkYzAwYjA4YmNlZjU4NzdkNzUwNGI4NWY2ZTM1ZSIsImp0aSI6ImNjY2VhNTg0OTlkMjAwZTRiMjQ5ZTlkYTA5NjhhZGU0ODA5YWM5ZTA1MzNjZDBiNjU3NWZjZDc1MGJlYTAyMGEzNmQ4N2U2NTMwODdmZjgxIiwiaWF0IjoxNjU3MjQ4ODIwLCJuYmYiOjE2NTcyNDg4MjAsImV4cCI6MTY1OTkyNzIyMCwic3ViIjoiODMwOTQzNSIsInNjb3BlcyI6W119.pbHU2gssDOjERlXIEcO-uxpOuCykx-zzdXRSK45jNdZ3pDFXEZ5o8WcyGR4EXJiNY1WP_rogvES-sjgUAfVoM4ZuesrkgWUcTNQGVvGaJlH5pu6k4w1peDZMCkCLxFvgNsMue38MOOT5hP3IWNRYDVk7iMy3mJnRbeJTEhrhMuPdvOO30IdKws1SFFphCj9iG_aG5pibZ9QucXNyoLMrUPBsLLf-gZN5SKddr8yroqyS_Gv7fa7bnCmPdNaVB-4I9s91fPIfbUI65fKGR4oJITfUus-RiyUuyZQ-p9U-351ettNRk_bxCXyonT4ODVAxbgyw9kUAjXmKCtgmz3rTgg'
    })

    response.raise_for_status()
    data = response.json()
    response.close()

    titles = []

    for node in data['data']:
        anime = node['node']
        title = anime['title']
        titles.append(title)

    return titles


def get_list_intersection(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    return set1.intersection(set2)


def get_anime_ids(user):
    url = f'https://api.myanimelist.net/v2/users/{user}/animelist?status=completed&limit=100'
    response = requests.get(url, headers={
        'Authorization': f'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImNjY2VhNTg0OTlkMjAwZTRiMjQ5ZTlkYTA5NjhhZGU0ODA5YWM5ZTA1MzNjZDBiNjU3NWZjZDc1MGJlYTAyMGEzNmQ4N2U2NTMwODdmZjgxIn0.eyJhdWQiOiJjYmFkYzAwYjA4YmNlZjU4NzdkNzUwNGI4NWY2ZTM1ZSIsImp0aSI6ImNjY2VhNTg0OTlkMjAwZTRiMjQ5ZTlkYTA5NjhhZGU0ODA5YWM5ZTA1MzNjZDBiNjU3NWZjZDc1MGJlYTAyMGEzNmQ4N2U2NTMwODdmZjgxIiwiaWF0IjoxNjU3MjQ4ODIwLCJuYmYiOjE2NTcyNDg4MjAsImV4cCI6MTY1OTkyNzIyMCwic3ViIjoiODMwOTQzNSIsInNjb3BlcyI6W119.pbHU2gssDOjERlXIEcO-uxpOuCykx-zzdXRSK45jNdZ3pDFXEZ5o8WcyGR4EXJiNY1WP_rogvES-sjgUAfVoM4ZuesrkgWUcTNQGVvGaJlH5pu6k4w1peDZMCkCLxFvgNsMue38MOOT5hP3IWNRYDVk7iMy3mJnRbeJTEhrhMuPdvOO30IdKws1SFFphCj9iG_aG5pibZ9QucXNyoLMrUPBsLLf-gZN5SKddr8yroqyS_Gv7fa7bnCmPdNaVB-4I9s91fPIfbUI65fKGR4oJITfUus-RiyUuyZQ-p9U-351ettNRk_bxCXyonT4ODVAxbgyw9kUAjXmKCtgmz3rTgg'
    })

    response.raise_for_status()
    data = response.json()
    response.close()

    ids = []

    for node in data['data']:
        anime = node['node']
        id = anime['id']
        ids.append(id)

    return ids


def get_anime_synopses(user):
    synopses = []
    ids = get_anime_ids(user)
    for id in ids:
        url = f'https://api.myanimelist.net/v2/anime/{id}?fields=synopsis'
        response = requests.get(url, headers={
            'Authorization': f'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImNjY2VhNTg0OTlkMjAwZTRiMjQ5ZTlkYTA5NjhhZGU0ODA5YWM5ZTA1MzNjZDBiNjU3NWZjZDc1MGJlYTAyMGEzNmQ4N2U2NTMwODdmZjgxIn0.eyJhdWQiOiJjYmFkYzAwYjA4YmNlZjU4NzdkNzUwNGI4NWY2ZTM1ZSIsImp0aSI6ImNjY2VhNTg0OTlkMjAwZTRiMjQ5ZTlkYTA5NjhhZGU0ODA5YWM5ZTA1MzNjZDBiNjU3NWZjZDc1MGJlYTAyMGEzNmQ4N2U2NTMwODdmZjgxIiwiaWF0IjoxNjU3MjQ4ODIwLCJuYmYiOjE2NTcyNDg4MjAsImV4cCI6MTY1OTkyNzIyMCwic3ViIjoiODMwOTQzNSIsInNjb3BlcyI6W119.pbHU2gssDOjERlXIEcO-uxpOuCykx-zzdXRSK45jNdZ3pDFXEZ5o8WcyGR4EXJiNY1WP_rogvES-sjgUAfVoM4ZuesrkgWUcTNQGVvGaJlH5pu6k4w1peDZMCkCLxFvgNsMue38MOOT5hP3IWNRYDVk7iMy3mJnRbeJTEhrhMuPdvOO30IdKws1SFFphCj9iG_aG5pibZ9QucXNyoLMrUPBsLLf-gZN5SKddr8yroqyS_Gv7fa7bnCmPdNaVB-4I9s91fPIfbUI65fKGR4oJITfUus-RiyUuyZQ-p9U-351ettNRk_bxCXyonT4ODVAxbgyw9kUAjXmKCtgmz3rTgg'
        })

        response.raise_for_status()
        data = response.json()
        response.close()

        synopses.append(data['synopsis'])

    return synopses


def get_anime_score_means(user):
    scores = []
    ids = get_anime_ids(user)
    for id in ids:
        url = f'https://api.myanimelist.net/v2/anime/{id}?fields=synopsis,mean'
        response = requests.get(url, headers={
            'Authorization': f'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImNjY2VhNTg0OTlkMjAwZTRiMjQ5ZTlkYTA5NjhhZGU0ODA5YWM5ZTA1MzNjZDBiNjU3NWZjZDc1MGJlYTAyMGEzNmQ4N2U2NTMwODdmZjgxIn0.eyJhdWQiOiJjYmFkYzAwYjA4YmNlZjU4NzdkNzUwNGI4NWY2ZTM1ZSIsImp0aSI6ImNjY2VhNTg0OTlkMjAwZTRiMjQ5ZTlkYTA5NjhhZGU0ODA5YWM5ZTA1MzNjZDBiNjU3NWZjZDc1MGJlYTAyMGEzNmQ4N2U2NTMwODdmZjgxIiwiaWF0IjoxNjU3MjQ4ODIwLCJuYmYiOjE2NTcyNDg4MjAsImV4cCI6MTY1OTkyNzIyMCwic3ViIjoiODMwOTQzNSIsInNjb3BlcyI6W119.pbHU2gssDOjERlXIEcO-uxpOuCykx-zzdXRSK45jNdZ3pDFXEZ5o8WcyGR4EXJiNY1WP_rogvES-sjgUAfVoM4ZuesrkgWUcTNQGVvGaJlH5pu6k4w1peDZMCkCLxFvgNsMue38MOOT5hP3IWNRYDVk7iMy3mJnRbeJTEhrhMuPdvOO30IdKws1SFFphCj9iG_aG5pibZ9QucXNyoLMrUPBsLLf-gZN5SKddr8yroqyS_Gv7fa7bnCmPdNaVB-4I9s91fPIfbUI65fKGR4oJITfUus-RiyUuyZQ-p9U-351ettNRk_bxCXyonT4ODVAxbgyw9kUAjXmKCtgmz3rTgg'
        })

        response.raise_for_status()
        data = response.json()
        response.close()

        scores.append(data['mean'])

    return scores
