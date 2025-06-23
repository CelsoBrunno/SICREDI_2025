from app.db.db_connection import get_db_connection
conn = get_db_connection()
conn.execute("UPDATE usuarios SET cargo='A' WHERE email=?", ('analista@gmail.com',))
conn.commit()
conn.close()