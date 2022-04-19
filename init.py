
import mysql.connector


config = {
    'user': 'root',
    'password': 'Parola123',
    'host': '34.65.13.178',
    'database': 'traveler'
}
cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor()
# cursor.execute("DROP TABLE IF EXISTS messages")
# cursor.execute("CREATE TABLE messages ("
#                "id INT(6) AUTO_INCREMENT PRIMARY KEY,"
#                "created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
#                "lang VARCHAR(200) NOT NULL,"
#                "country VARCHAR(200) NOT NULL,"
#                "person VARCHAR(200) NOT NULL,"
#                "message VARCHAR(200) NOT NULL )")
#
# cnxn.commit()  # this commits changes to the database
#query = ("INSERT INTO messages (lang,country,person,message) VALUES (\"test\",\"test\",\"test\",\"test\")")
cursor.execute('DELETE FROM messages')
cnxn.commit()

cursor.execute("SELECT * FROM messages")
out = cursor.fetchall()
for row in out:
    print(row)
print("ok")