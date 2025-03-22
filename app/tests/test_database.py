from unittest.mock import patch
from app.database import init_db, get_db


@patch("app.database.Base.metadata.create_all")
def test_init_db(mock_create_all):
    init_db()
    mock_create_all.assert_called_once()


def test_get_db_yields_session():
    db_gen = get_db()
    db = next(db_gen)
    from sqlalchemy.orm import Session
    assert isinstance(db, Session)
    db_gen.close()
