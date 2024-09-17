import pytest
from unittest.mock import MagicMock, patch
from database.postgresql_functools import PostgresManager


@pytest.fixture
def mock_postgres_manager():
    """Fixture pour mocker PostgresManager."""
    with patch('database.postgresql_functools.PostgresManager') as MockPostgresManager:
        mock_instance = MockPostgresManager.return_value

        # Mock des méthodes pour simuler l'ajout, la récupération et la suppression des données
        mock_instance.add_record = MagicMock()
        mock_instance.fetch_record = MagicMock()
        mock_instance.fetch_all_records = MagicMock()
        mock_instance.delete_record = MagicMock()
        mock_instance.fetch_city_record_by_coord = MagicMock()

        yield mock_instance


@pytest.fixture
def mock_mongo_manager():
    """Fixture pour mocker MongoDBManager."""
    with patch('database.mongodb_functools.MongoDBManager') as MockMongoDBManager:
        mock_instance = MockMongoDBManager.return_value

        # Mock des méthodes pour simuler l'insertion et la récupération des documents
        mock_instance.insert_document = MagicMock()
        mock_instance.find_document = MagicMock()
        mock_instance.delete_document = MagicMock()

        yield mock_instance
