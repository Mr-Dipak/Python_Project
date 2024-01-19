class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://DIPAK\\SQLEXPRESS/PYTHONPROJECT?driver=ODBC+Driver+17+for+SQL+Server'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key_here'
