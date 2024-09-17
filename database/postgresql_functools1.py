import psycopg2

if __name__ == "__main__":
    # Configuration de la connexion
    conn = psycopg2.connect(
        host="172.21.0.4",  # Adresse IP du conteneur PostgreSQL
        database="airflow",  # Nom de la base de données
        user="airflow",  # Nom d'utilisateur
        password="airflow"  # Mot de passe
    )

    # Création du curseur
    cursor = conn.cursor()

    # Requête d'insertion d'une ville
    insert_query = """
    INSERT INTO city (name, population, country)
    VALUES (%s, %s, %s)
    RETURNING id;
    """

    # Valeurs de la ville à insérer
    city_data = ('Paris', 2148000, 'France')

    # Exécution de la requête
    cursor.execute(insert_query, city_data)

    # Récupération de l'ID généré
    city_id = cursor.fetchone()[0]
    print(f"City inserted with ID: {city_id}")

    # Validation des modifications
    conn.commit()

    # Fermeture de la connexion
    cursor.close()
    conn.close()



