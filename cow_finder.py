import csv
import random
import tkinter as tk
from tkinter import messagebox

# ธรรมนูญ เรืองทับ 65050387

# Model
class Cow:
    def __init__(self, id, age_years=0, age_months=0, udders=0):
        self.id = id
        self.age_years = age_years
        self.age_months = age_months
        self.udders = udders

    def is_goat(self):
        # ถ้าไม่มีอายุและเต้านมให้ถือว่าเป็นแพะ
        return self.age_years == 0 and self.age_months == 0 and self.udders == 0

    def milk_production(self):
        # น้ำนม = อายุปี + อายุเดือน
        return self.age_years + self.age_months

class CowDatabase:
    def __init__(self, file_name):
        self.file_name = file_name
        self.cows = self.load_cows()

    def load_cows(self):
        cows = []
        try:
            with open(self.file_name, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    age_years = int(row['age_years']) if row['age_years'] else 0
                    age_months = int(row['age_months']) if row['age_months'] else 0
                    udders = int(row['udders']) if row['udders'] else 0
                    cow = Cow(row['id'], age_years, age_months, udders)
                    cows.append(cow)
        except FileNotFoundError:
            print(f"File {self.file_name} not found.")
        return cows

    def save_cows(self):
        with open(self.file_name, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'age_years', 'age_months', 'udders'])
            writer.writeheader()
            for cow in self.cows:
                writer.writerow({
                    'id': cow.id,
                    'age_years': cow.age_years if cow.age_years != 0 else '',
                    'age_months': cow.age_months if cow.age_months != 0 else '',
                    'udders': cow.udders if cow.udders != 0 else ''
                })

    def find_cow_by_id(self, cow_id):
        for cow in self.cows:
            if cow.id == cow_id:
                return cow
        return None

# View
class CowView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root
        self.root.title("Cow Strike")
        self.root.geometry("400x400")
        self.root.configure(background='orchid2')
        
        # Create a main frame
        self.main_frame = tk.Frame(root,bg="orchid2")
        self.main_frame.pack(expand=True)

        # สร้างอินพุตสำหรับรับรหัสวัว
        self.label = tk.Label(self.main_frame, text="Enter Cow ID:")
        self.label.pack(pady=5)

        self.entry = tk.Entry(self.main_frame)
        self.entry.pack(pady=5)

        self.submit_button = tk.Button(self.main_frame, text="Submit", command=self.submit)
        self.submit_button.pack(pady=5)

        self.kick_button = tk.Button(self.main_frame, text="Kick the Goat", command=self.kick_goat)
        self.kick_button.pack(pady=5)

        # Frame for result labels
        self.result_frame = tk.Frame(self.main_frame)
        self.result_frame.pack(pady=10, fill=tk.X)

        # Label สำหรับแสดงผลลัพธ์ของวัว
        self.cow_result_label = tk.Label(self.result_frame, text="Cow Result:", anchor="w")
        self.cow_result_label.pack(fill=tk.X)

        # Label สำหรับแสดงผลลัพธ์ของแพะ
        self.goat_result_label = tk.Label(self.result_frame, text="Goat Result:", anchor="w")
        self.goat_result_label.pack(fill=tk.X, pady=(15, 0))
        

    def submit(self):
        cow_id = self.entry.get()
        self.controller.handle_cow_submission(cow_id)

    def kick_goat(self):
        self.controller.handle_goat_kick()

    def display_cow_result(self, result):
        self.cow_result_label.config(text=f"Cow Result: {result}")

    def display_goat_result(self, result):
        self.goat_result_label.config(text=f"Goat Result: {result}")

# Controller
class CowController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_cow_submission(self, cow_id):
        cow = self.model.find_cow_by_id(cow_id)
        
        # มีครบ 8 ตัว หรือไม่
        if len(cow_id) != 8:
            return self.view.display_cow_result(f"Syntax Error! ID should be 8 number")
        
        # ขึ้นต้นด้วย 0 หรือไม่
        if cow_id.startswith("0"):
            return self.view.display_cow_result(f"Syntax Error! ID should not start with 0")
        
        # เป็นตัวเลขทั้งหมด หรือไม่
        if not cow_id.isdigit():
            return self.view.display_cow_result(f"Syntax Error! ID should be all number")
        
        # ตรวจสอบกับฐานข้อมูล
        if cow is None:
            self.view.display_cow_result(f"Error: No cow or goat found with ID: {cow_id}")
            
        else:
            if cow.is_goat():
                self.view.display_goat_result("Goat detected! Press 'Kick the Goat' to remove it.")
            else:
                if cow.udders == 4:
                    milk = cow.milk_production()
                    if random.randint(1, 100) <= 5:  # 5% chance to lose 1 udder 
                        cow.udders = 3
                        self.view.display_cow_result(f"Cow ID: {cow_id} \nCow Age : {cow.age_years} years {cow.age_months} months \nCow Udder: {cow.udders}  \nproduced {milk} liters of milk, but it lost 1 udder!")
                    else:
                        self.view.display_cow_result(f"Cow ID: {cow_id} \nCow Age : {cow.age_years} years {cow.age_months} months \nCow Udder: {cow.udders} \nproduced {milk} liters of milk.")
                elif cow.udders == 3:
                    if random.randint(1, 100) <= 20:  # 20% chance to regain 1 udder
                        cow.udders = 4
                        self.view.display_cow_result(f"Cow ID: {cow_id} has regained 1 udder and now has 4 udders.")
                    else:
                        self.view.display_cow_result(f"Cow ID: {cow_id} cannot be milked (only 3 udders).")
                self.model.save_cows()

    def handle_goat_kick(self):
        self.view.display_goat_result("Goat kicked out successfully!")


# Main
if __name__ == "__main__":
    root = tk.Tk()
    
    model = CowDatabase("database.csv")
    view = CowView(root, None)
    controller = CowController(model, view)
    view.controller = controller
    root.mainloop()
