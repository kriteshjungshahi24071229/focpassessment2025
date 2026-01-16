import os

# Ensure required files exist
def setup_files():
    for file in ["users.txt", "grades.txt", "eca.txt", "passwords.txt"]:
        if not os.path.exists(file):
            with open(file, "w") as f:
                if file == "users.txt":
                    f.write("admin1,Admin User,admin\n")
                elif file == "passwords.txt":
                    f.write("admin1,adminpass\n")

class User:
    def __init__(self, user_id, name, role):
        self.user_id = user_id
        self.name = name
        self.role = role

class Student(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name, "student")

    def menu(self):
        while True:
            print("\nStudent Menu")
            print("1. View Grades\n2. View ECA\n3. Update Profile\n4. Logout")
            choice = input("Select: ")
            if choice == '1':
                self.view_grades()
            elif choice == '2':
                self.view_eca()
            elif choice == '3':
                self.update_profile()
            elif choice == '4':
                break

    def view_grades(self):
        try:
            with open("grades.txt", "r") as f:
                for line in f:
                    if line.startswith(self.user_id):
                        print("Grades:", line.strip().split(',')[1:])
                        return
            print("No grades found.")
        except FileNotFoundError:
            print("Grades file not found.")

    def view_eca(self):
        try:
            with open("eca.txt", "r") as f:
                for line in f:
                    if line.startswith(self.user_id):
                        print("ECA Participation:", line.strip().split(',')[1:])
                        return
            print("No ECA record found.")
        except FileNotFoundError:
            print("ECA file not found.")

    def update_profile(self):
        new_name = input("Enter new name: ")
        with open("users.txt", "r") as f:
            lines = f.readlines()
        with open("users.txt", "w") as f:
            for line in lines:
                if line.startswith(self.user_id):
                    f.write(f"{self.user_id},{new_name},student\n")
                else:
                    f.write(line)
        print("Profile updated.")

class Admin(User):
    def __init__(self, user_id, name):
        super().__init__(user_id, name, "admin")

    def menu(self):
        while True:
            print("\nAdmin Menu")
            print("1. Add User\n2. Modify User\n3. Delete User\n4. Generate Insights\n5. Enter/Update Grades\n6. Logout")

            choice = input("Select: ")
            if choice == '1':
                self.add_user()
            elif choice == '2':
                self.modify_user()
            elif choice == '3':
                self.delete_user()
            elif choice == '4':
                self.generate_insights()
            elif choice == '5':
                self.enter_or_update_grades()
            elif choice == '6':
                break

    def add_user(self):
        user_id = input("User ID: ")
        name = input("Name: ")
        role = input("Role (admin/student): ")
        password = input("Password: ")

        if self.user_exists(user_id):
            print("User ID already exists.")
            return

        with open("users.txt", "a") as u, open("passwords.txt", "a") as p:
            u.write(f"{user_id},{name},{role}\n")
            p.write(f"{user_id},{password}\n")
        print("User added.")

    def user_exists(self, user_id):
        with open("users.txt") as f:
            return any(line.startswith(user_id + ",") for line in f)

    def modify_user(self):
        user_id = input("User ID to modify: ")
        if not self.user_exists(user_id):
            print("User not found.")
            return
        new_name = input("New name: ")
        with open("users.txt", "r") as f:
            lines = f.readlines()
        with open("users.txt", "w") as f:
            for line in lines:
                parts = line.strip().split(',')
                if parts[0] == user_id:
                    f.write(f"{user_id},{new_name},{parts[2]}\n")
                else:
                    f.write(line)
        print("User modified.")

    def delete_user(self):
        user_id = input("User ID to delete: ")
        for file in ["users.txt", "grades.txt", "eca.txt", "passwords.txt"]:
            with open(file, "r") as f:
                lines = f.readlines()
            with open(file, "w") as f:
                for line in lines:
                    if not line.startswith(user_id + ","):
                        f.write(line)
        print("User deleted.")

    def generate_insights(self):
        subjects = ["Math", "Science", "English", "History", "Art"]
        totals = [0]*5
        count = 0

        with open("grades.txt") as f:
            for line in f:
                grades = list(map(int, line.strip().split(',')[1:]))
                totals = [x + y for x, y in zip(totals, grades)]
                count += 1

        print("\nAverage Grades:")
        for sub, total in zip(subjects, totals):
            print(f"{sub}: {total / count:.2f}" if count else f"{sub}: N/A")

    def enter_or_update_grades(self):
        student_id = input("Student ID: ")
        if not self.user_exists(student_id):
            print("Student not found.")
            return

        print("Enter marks for the following subjects:")
        subjects = ["Math", "Science", "English", "History", "Art"]
        try:
            grades = [int(input(f"{subject}: ")) for subject in subjects]
        except ValueError:
            print("Invalid input. Please enter numeric grades.")
            return

        updated = False
        lines = []
        if os.path.exists("grades.txt"):
            with open("grades.txt", "r") as f:
                lines = f.readlines()

        with open("grades.txt", "w") as f:
            for line in lines:
                if line.startswith(student_id + ","):
                    f.write(f"{student_id},{','.join(map(str, grades))}\n")
                    updated = True
                else:
                    f.write(line)
            if not updated:
                f.write(f"{student_id},{','.join(map(str, grades))}\n")

        print("Grades saved successfully.")

def login():
    username = input("Username: ")
    password = input("Password: ")

    try:
        with open("passwords.txt") as f:
            creds = dict(line.strip().split(',') for line in f)

        if creds.get(username) == password:
            with open("users.txt") as f:
                for line in f:
                    uid, name, role = line.strip().split(',')
                    if uid == username:
                        return Admin(uid, name) if role == 'admin' else Student(uid, name)
    except FileNotFoundError:
        print("User data files missing.")

    print("Login failed.")
    return None

def main():
    setup_files()
    while True:
        print("\n1. Login as Admin\n2. Login as Student\n3. Exit")
        option = input("Select: ")

        if option in ('1', '2'):
            user = login()
            if user:
                user.menu()
        elif option == '3':
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    main()