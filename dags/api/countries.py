import requests


def get_api_data(url):
    try:
        response = requests.get(url)
        # Vérifiez si la requête a réussi (code de statut 200)
        if response.status_code == 200:
            # Convertissez la réponse JSON en un dictionnaire Python
            data = response.json()
            return data
        else:
            print("La requête a échoué avec le code de statut:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Une erreur s'est produite lors de la requête :", e)
        return None
