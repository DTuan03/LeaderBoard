import sqlite3

# Kết nối đến SQLite database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Truy vấn tất cả dữ liệu từ bảng 'students'
cursor.execute("SELECT * FROM students")

# cursor.execute("DROP TABLE students")

# Lấy tất cả kết quả truy vấn
rows = cursor.fetchall()

# In ra dữ liệu
for row in rows:
    print(row)

# Đóng kết nối
conn.close()
