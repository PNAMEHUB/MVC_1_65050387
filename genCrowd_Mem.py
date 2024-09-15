import csv
import random

# ฟังก์ชันสร้างรหัสวัว/แพะแบบสุ่ม
def generate_id():
    # สร้างรหัสความยาว 8 ตัว โดยรหัสไม่เริ่มด้วย 0 
    return str(random.randint(1, 9)) + ''.join([str(random.randint(0, 9)) for _ in range(7)])

# ฟังก์ชันสร้างข้อมูลวัว
def generate_cow():
    id = generate_id()
    age_years = random.randint(0, 10)  # อายุสุ่มตั้งแต่ 0 ถึง 10 ปี
    age_months = random.randint(0, 11)  # จำนวนเดือนในอายุ
    udders = random.choice([3, 4])  # จำนวนเต้านมสุ่ม 3 หรือ 4
    return {
        'id': id,
        'age_years': age_years,
        'age_months': age_months,
        'udders': udders
    }

# ฟังก์ชันสร้างข้อมูลแพะ
def generate_goat():
    id = generate_id()
    # แพะไม่มีข้อมูลอายุและเต้านม
    return {
        'id': id,
        'age_years': '',
        'age_months': '',
        'udders': ''
    }

# ฟังก์ชันสร้างฐานข้อมูลและบันทึกลง CSV วัว 20 แพะ 2
def generate_database(file_name, num_cows=20, num_goats=2):
    with open(file_name, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'age_years', 'age_months', 'udders'])
        writer.writeheader()

        # สร้างข้อมูลวัว
        for _ in range(num_cows):
            cow = generate_cow()
            writer.writerow(cow)

        # สร้างข้อมูลแพะ
        for _ in range(num_goats):
            goat = generate_goat()
            writer.writerow(goat)

if __name__ == "__main__":
    # เรียกใช้งานฟังก์ชันเพื่อสร้างฐานข้อมูลในไฟล์ 'database.csv'
    generate_database("database.csv")
    print("Generated database.csv with cows and goats.")
