import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3

# Thiết lập kết nối với Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Mở Google Sheet bằng URL
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1jSTFR5O8Vi1LYp-w02jFH_eqZtlc7W8-X5j8_H0D90k/edit?usp=sharing").sheet1

# Lấy giá trị dòng tiêu đề (row 1)
headers = sheet.row_values(1)

# Lấy dữ liệu và hiển thị
data = sheet.get_all_records(expected_headers=headers)

# Kết nối tới SQLite (hoặc tạo mới nếu chưa có)
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Tạo bảng nếu chưa có
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_code TEXT PRIMARY KEY NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    "1" TEXT,
    "2" TEXT,
    "3" TEXT,
    "4" TEXT,
    "5" TEXT,
    "6" TEXT,
    "7" TEXT,
    "8" TEXT,
    "9" TEXT,
    "10" TEXT,
    "11" TEXT,
    "12" TEXT,
    "13" TEXT,
    "14" TEXT,
    "15" TEXT,
    project_score TEXT
)
''')

# Loại bỏ dòng tiêu đề
data = data[1:]

# Chọn các cột và hàng cần thiết
for row in data:
    student_code = row['Mã sinh viên']
    first_name = row['Họ']
    last_name = row.get('Tên')
    roll_Call = [
        row.get('1', None),
        row.get('2', None),
        row.get('3', None),
        row.get('4', None),
        row.get('5', None),
        row.get('6', None),
        row.get('7', None),
        row.get('8', None),
        row.get('9', None),
        row.get('10', None),
        row.get('11', None),
        row.get('12', None),
        row.get('13', None),
        row.get('14', None),
        row.get('15', None)
    ]
    project_score = row.get('Điểm project', None)

    cursor.execute('''
    INSERT INTO students (
        student_code, first_name, last_name,
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", project_score
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (student_code, first_name, last_name, *roll_Call, project_score))

# Commit và đóng kết nối
conn.commit()
conn.close()
