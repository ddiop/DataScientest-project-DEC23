import pytest
from unittest.mock import MagicMock


def test_postgres_create_tables(mock_postgres_manager):
    # Test de l'ajout d'une nouvelle ville dans la table city
    city_record = MagicMock(id=1, name="Sydney", latitude=-33.8688, longitude=151.2093)
    mock_postgres_manager.add_record(city_record)
    mock_postgres_manager.add_record.assert_called_once_with(city_record)


def test_postgres_fetch_city(mock_postgres_manager):
    # Test de la récupération d'une ville à partir de ses coordonnées
    mock_city = MagicMock(id=1)
    mock_city.name = "Sydney"
    mock_postgres_manager.fetch_city_record_by_coord.return_value = mock_city

    city = mock_postgres_manager.fetch_city_record_by_coord(-33.8688, 151.2093)

    assert city.name == "Sydney"


def test_postgres_create_view(mock_postgres_manager):
    # Test si la vue australian_meteorology_weather est créée
    mock_postgres_manager.execute_sql = MagicMock()
    mock_postgres_manager.execute_sql.assert_not_called()


def test_mongo_insert_document(mock_mongo_manager):
    # Test de l'insertion d'un document MongoDB
    mock_mongo_manager.insert_document.return_value = "mock_id"
    doc_id = mock_mongo_manager.insert_document("test_collection", {"name": "Sydney"})
    assert doc_id == "mock_id"
    mock_mongo_manager.insert_document.assert_called_once_with("test_collection", {"name": "Sydney"})

def test_mongo_find_document(mock_mongo_manager):
    # Test de la récupération d'un document MongoDB
    mock_mongo_manager.find_document.return_value = {"name": "Sydney"}
    doc = mock_mongo_manager.find_document("test_collection", {"name": "Sydney"})
    assert doc["name"] == "Sydney"
    mock_mongo_manager.find_document.assert_called_once_with("test_collection", {"name": "Sydney"})
