from recommendation.storage.db.models import SessionLocal


def get_db():
    """
    Генератор для получения сессии базы данных.

    Эта функция создает и возвращает сессию базы данных с помощью `SessionLocal`.
    После завершения работы с сессией, она автоматически закрывается, даже если в процессе возникли исключения.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
