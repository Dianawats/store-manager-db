from app import app
from app.db.dbmanager import DatabaseConnection

if __name__ == "__main__":
    dbUtils = DatabaseConnection()
    dbUtils.create_tables()
    app.run(debug=True)