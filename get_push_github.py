#!/usr/bin/env python3
import requests
import time
from datetime import datetime
import pytz
from babel import Locale
from babel.dates import format_datetime

def translate_to_france_hour(date_str: str): 
    # Conversion en objet datetime en UTC
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    date_obj = date_obj.replace(tzinfo=pytz.UTC)  # On définit que l'heure est en UTC

    # Conversion en heure française
    timezone_fr = pytz.timezone("Europe/Paris")
    date_obj_fr = date_obj.astimezone(timezone_fr)

    # Utilisation de Babel pour formater la date en français
    formatted_date = format_datetime(date_obj_fr, format="d MMMM yyyy à HH:mm", locale="fr_FR")
    return (formatted_date)


def get_list_commit(github_token: str, owner: str, repo: str): #récupère la liste des commit
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    return response

def check_list_commit(response: requests.Response): # vérifie si la liste des commit a bien été récupérée
    if response.status_code == 200:
        return True
    else: 
        return ([response.status_code, response.text])

def check_new_push(repo: str, response: requests.Response, last_push_id: list): #vérifie s'il y a de nouveaux push

    commits = response.json()
    commit_id = commits[0]["node_id"]
    # Vérifie si ce commit est un nouveau push
    if (last_push_id == [""]):
        last_push_id[0] = commit_id
        print(last_push_id)
        return (False)
    if commit_id != last_push_id[0]:
        last_push_id[0] = commit_id
        commit_message = commits[0]["commit"]["message"]
        author = commits[0]["commit"]["author"]["name"]
        date = commits[0]["commit"]["author"]["date"]
        url = commits[0]["html_url"]
        print(f"📋 Nouveau commit par {author} le {translate_to_france_hour(date)} sur le repository {repo}:\n\n {commit_message}\n\nCliquez sur l'Url pour voir le dernier commit: {url}")
        # Ici, tu peux aussi appeler une fonction pour envoyer le message sur Discord
        return (f"📋 Nouveau commit par {author} le {translate_to_france_hour(date)} sur le repository {repo}:\n\n {commit_message}\n\nCliquez sur l'Url pour voir le dernier commit: {url}")
    else:
        return False

def loop_check_new_push(github_token: str, owner: str, repo: str, response: requests.Response): # Boucle pour vérifier périodiquement les nouveaux pushs
    github_token = "oupsie i removed it"  # Remplace par ton token GitHub personnel pour éviter les limitations
    owner = "ThibauDDDD" #le propriétaire du repository github
    repo = "Testrepository" # le nom du repository
    last_push_id = [""] # identifiant du dernier push détecté.
    while True:
        check_return = check_new_push(repo, get_list_commit(github_token, owner, repo), last_push_id)
        if (check_return != False):
            print(check_return)
        elif (check_return == False):
            print("Pas de nouveau push.")
        else:
            return()
        time.sleep(60)  # Vérifie toutes les 60 secondes

if __name__ == '__main__':
    loop_check_new_push("az", "de", "ed", requests.Response)