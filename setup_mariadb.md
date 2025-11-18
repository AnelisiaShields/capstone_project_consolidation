# MariaDB Setup Notes

1. Install MariaDB server.
2. Create database and user:
   ```sql
   CREATE DATABASE news_db;
   CREATE USER 'news_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON news_db.* TO 'news_user'@'localhost';
   FLUSH PRIVILEGES;
   ```
3. Install Python MySQL client:
   ```
   pip install mysqlclient
   ```
4. Update `news_project/settings.py` with DB credentials.
