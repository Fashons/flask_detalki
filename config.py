import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'key1220__Botik__'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///computer_equipment.db'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory база для тестов
    WTF_CSRF_ENABLED = False  # Отключаем CSRF защиту для тестов
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,  # Добавляем тестовую конфигурацию
    'default': DevelopmentConfig
}