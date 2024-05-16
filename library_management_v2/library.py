import random
import string
import os


class Library:
    def __init__(self, file_path):
        self.rentals_dict = {}
        self.student_dict = {}
        self.book_dict = {}
        self.book_file_path = file_path
        self.load_books()
        self.load_students()
        self.load_rentals()
        self.last_book_id = max(self.book_dict.keys(), default=0)
        # create txt files
        for filename in ["library_data.txt", "rentals.txt", "students.txt"]:
            if not os.path.isfile(filename):
                open(filename, "w").close()

    def load_books(self):
        try:
            # open file
            with open("library_data.txt", 'r') as file:
                lines = file.readlines()
                for line in lines:
                    book_id, name, author, quantity = line.strip().split(',')
                    # create a dictionary in book_dict w/ book_id as key
                    book_id = int(book_id)
                    self.book_dict[book_id] = {"name": name, "author": author, "quantity": int(quantity)}
        except FileNotFoundError:
            self.book_dict = {}

    def save_books(self):
        with open("library_data.txt", 'w') as file:
            # goes through each key value pair in the book_dict
            for book_id, info in self.book_dict.items():
                # write line to the file with the book information
                file.write(f"{book_id},{info['name']},{info['author']},{info['quantity']}\n")

    def new_book(self, name, author, quantity):
        author = author.strip()
        name = name.strip()
        # increment book id to generate unique id
        self.last_book_id += 1
        book_id = self.last_book_id

        # check if there is an existing book
        existing_book = next((id for id, book in self.book_dict.items() if book['name'].lower() == name.lower()), None)
        if existing_book:
            # increase quantity by its quantity
            self.book_dict[existing_book]['quantity'] += int(quantity)
            print(
                f"Quantity of book '{name}' by {author} (ID: {existing_book}) increased to "
                f"{self.book_dict[existing_book]['quantity']}.")
        else:
            # if no existing book then add a new entry to book_dict
            self.book_dict[book_id] = {"name": name, "author": author, "quantity": int(quantity)}
            print(f"Book '{name}' by {author} (ID: {book_id}) added successfully with quantity {quantity}.")
        self.save_books()

    def remove_book(self, book_id):
        # check id the book_id exists in the book_dict
        if book_id in self.book_dict:
            # retrieve information from book_dict
            book_title = self.book_dict[book_id]['name']
            current_quantity = int(self.book_dict[book_id]['quantity'])
            try:
                quantity_to_remove = int(input(
                    f"Enter the quantity of '{book_title}' with ID '{book_id}' to remove "
                    f"(currently {current_quantity}): "))
                if 0 < quantity_to_remove <= current_quantity:
                    if quantity_to_remove == current_quantity:
                        del self.book_dict[book_id]
                    else:
                        self.book_dict[book_id]['quantity'] -= quantity_to_remove
                    print(
                        f"{quantity_to_remove} copies of book '{book_title}' with ID '{book_id}' removed successfully.")
                    self.save_books()
                else:
                    print("Invalid quantity. Please enter a valid quantity.")
            except ValueError:
                print("Invalid quantity. Please enter a valid number.")
        else:
            print("Book not found in the library.")

    def binary_search_books(self, book_id):
        book_id = int(book_id)
        # sort dictionary
        sorted_keys = sorted(self.book_dict.keys())
        low = 0
        high = len(sorted_keys) - 1

        while low <= high:
            mid = (low + high) // 2
            if sorted_keys[mid] == book_id:
                return self.book_dict[book_id]
            elif sorted_keys[mid] < book_id:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def search_book(self, book_id):
        # utilize binary search to look up book_id
        book = self.binary_search_books(book_id)
        if book != -1:
            print(f"Book '{book['name']}' by {book['author']}, Quantity: {book['quantity']}")
        else:
            print("Book not found in the library.")

    def print_books(self):
        print("Books in the library:")
        if self.book_dict:
            for book_id, info in sorted(self.book_dict.items()):
                print(f"Book ID: {book_id}, Name: '{info['name']}' by {info['author']}, Quantity: {info['quantity']}")
        else:
            print("No books in the library.")

    def load_students(self):
        try:
            with open("students.txt", 'r') as file:
                lines = file.readlines()
                # iterate each line in file
                for line in lines:
                    if ',' in line:
                        name, student_id = line.strip().split(',')
                        # add students name and id to the student_dict
                        self.student_dict[student_id] = name
        except FileNotFoundError:
            self.student_dict = {}

    def save_students(self):
        with open("students.txt", 'w') as file:
            # iterate over each key value pair in the student_dict
            for student_id, name in self.student_dict.items():
                # write a line to the file w/ student information
                file.write(f"{name},{student_id}\n")

    def add_student(self, name, student_id):
        name = name.strip()
        student_id = str(student_id)
        # check if student exists in the student_dict
        if student_id in self.student_dict:
            print(
                f"Student with ID '{student_id}' already exists in the list with name "
                f"'{self.student_dict[student_id]}'.")
        else:
            # add student to the student_dict
            self.student_dict[student_id] = name
            print(f"Student '{name}' with ID '{student_id}' added successfully.")
            self.save_students()

    def delete_student(self, name, student_id):
        name = name.strip()
        student_id = str(student_id)

        # check if given student name and id exists in the student_dict
        if self.student_dict.get(student_id) == name:
            # remove from student_dict
            del self.student_dict[student_id]
            print(f"Student '{name}' with ID '{student_id}' removed successfully.")
            self.save_students()
        else:
            print(f"Student with name '{name}' and ID '{student_id}' not found in the database.")

    def binary_search_students(self, name):
        # sort list by student name in lowercase
        sorted_students = sorted(self.student_dict.items(), key=lambda x: x[1].lower())
        low = 0
        high = len(sorted_students) - 1
        # storing the range of matching names
        start_index = -1
        end_index = -1

        while low <= high:
            mid = (low + high) // 2
            if sorted_students[mid][1].lower() == name.lower():
                start_index = mid
                end_index = mid
                while start_index > 0 and sorted_students[start_index - 1][1].lower() == name.lower():
                    start_index -= 1
                while (end_index < len(sorted_students) - 1 and
                       sorted_students[end_index + 1][1].lower() == name.lower()):
                    end_index += 1
                return start_index, end_index
            elif sorted_students[mid][1].lower() < name.lower():
                low = mid + 1
            else:
                high = mid - 1
        return start_index, end_index

    def search_student_by_name(self, name):
        name = name.strip()
        start_index, end_index = self.binary_search_students(name)
        sorted_students = sorted(self.student_dict.items(), key=lambda x: x[1].lower())

        if start_index != -1 and end_index != -1:
            print(f"Students with the name '{name}':")
            for keys in range(start_index, end_index + 1):
                print(f"Student Name: {sorted_students[keys][1]}, Student ID: {sorted_students[keys][0]}")
        else:
            print("Student not found.")

    def display_students(self):
        if not self.student_dict:
            print("No students in the database.")
            return

        print("Students in the database (sorted by ID):")
        for student_id, name in sorted(self.student_dict.items()):
            print(f"Name: {name}, ID: {student_id}")

    def load_rentals(self):
        try:
            with open("rentals.txt", 'r') as file:
                lines = file.readlines()
                self.rentals_dict = {}
                for line in lines:
                    data = line.strip().split(',')
                    if len(data) == 3:
                        # extract data
                        student_name, student_id, book_id = data
                        student_id = str(student_id)
                        book_id = int(book_id)
                        # check if the rental already exist in the dictionary
                        if (student_name, student_id) in self.rentals_dict:
                            # append the book id to the existing list of rentals
                            self.rentals_dict[(student_name, student_id)].append(book_id)
                        else:
                            # if not create a new entry in the dictionary w/ student
                            self.rentals_dict[(student_name, student_id)] = [book_id]
                    else:
                        print(f"Ignoring line in rentals file: {line.strip()}. It does not contain valid data.")
        except FileNotFoundError:
            self.rentals_dict = {}

    def save_rentals(self):
        with open("rentals.txt", 'w') as file:
            # iterate over each rental entry in the rental_dict
            for student_key, book_ids in self.rentals_dict.items():
                # extract the student name and ID from the dictionary key
                student_name, student_id = student_key
                # write a line for each rental entry w/ the information
                for book_id in book_ids:
                    file.write(f"{student_name},{student_id},{book_id}\n")

    def add_rental(self, student_name, student_id, book_id):
        student_name = student_name.strip()
        student_id = str(student_id)
        book_id = int(book_id)

        # check if book w/ the given ID exists in the library
        if book_id not in self.book_dict:
            print(f"Book with ID '{book_id}' not found in the library.")
            return

        # gather information from book_dict
        book = self.book_dict[book_id]
        book_quantity = int(book['quantity'])

        # check if the student w/ the given ID exists in the database
        if student_id not in self.student_dict:
            print("Student not found in the database.")
            return

        # check if book is available
        if book_quantity > 0:
            if (student_name, student_id) not in self.rentals_dict:
                self.rentals_dict[(student_name, student_id)] = set()
            elif isinstance(self.rentals_dict[(student_name, student_id)], list):
                self.rentals_dict[(student_name, student_id)] = set(self.rentals_dict[(student_name, student_id)])
            self.rentals_dict[(student_name, student_id)].add(book_id)
            book_quantity -= 1
            self.book_dict[book_id]['quantity'] = book_quantity
            self.save_rentals()
            self.save_books()
            print(
                f"Book '{book['name']}' with ID '{book_id}' rented to student '{student_name}' "
                f"with ID '{student_id}'.")
        else:
            print("Book is out of stock.")

    def return_rental(self, student_name, student_id, book_id):
        student_name = student_name.strip()
        student_id = str(student_id)
        book_id = int(book_id)
        # check if there is a matching rental for provided details
        if (student_name, student_id) in self.rentals_dict:
            if book_id in self.rentals_dict[(student_name, student_id)]:
                # remove the book from the rental list for the student
                self.rentals_dict[(student_name, student_id)].remove(book_id)
                # check if book exists in the library
                if book_id in self.book_dict:
                    # increase its quantity
                    self.book_dict[book_id]['quantity'] = int(self.book_dict[book_id]['quantity']) + 1
                    self.save_rentals()
                    self.save_books()
                    print(f"Book with ID '{book_id}' returned by student '{student_name}' with ID '{student_id}'.")
                    return
                else:
                    print(f"Book with ID '{book_id}' not found in the library.")
                    return
        print("No matching rental found for the provided student and book details.")

    def binary_search_rentals(self, student_id):
        student_id = str(student_id)
        # sort rental dictionary by student_id
        sorted_rentals = sorted(self.rentals_dict.keys(), key=lambda x: x[1])
        low = 0
        high = len(sorted_rentals) - 1

        while low <= high:
            mid = (low + high) // 2
            if sorted_rentals[mid][1] == student_id:
                return mid
            elif sorted_rentals[mid][1] < student_id:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def search_rentals(self, student_id):
        student_id = str(student_id)
        sorted_rentals = sorted(self.rentals_dict.keys(), key=lambda x: x[1])
        rental = self.binary_search_rentals(student_id)

        if rental != -1:
            print(f"Rentals for the student with ID '{student_id}':")
            for book_id in self.rentals_dict[sorted_rentals[rental]]:
                book_info = self.book_dict.get(book_id, {})
                print(f"Book ID: {book_id}, Book Title: {book_info.get('name', 'Unknown')}, "
                      f"Author: {book_info.get('author', 'Unknown')}, Quantity: {book_info.get('quantity', 0)}")
        else:
            print(f"No rentals found for the student with ID '{student_id}'.")

    def display_rentals(self):
        if not self.rentals_dict:
            print("No rentals in the database.")
            return

        print("Rentals in the database:")
        for student_info, book_ids in self.rentals_dict.items():
            student_name, student_id = student_info
            student_name = self.student_dict.get(student_id, student_name)
            for book_id in book_ids:
                book_title = self.book_dict.get(book_id, {}).get('name', "Unknown")
                print(
                    f"Student Name: {student_name}, Student ID: {student_id}, "
                    f"Book ID: {book_id}, Book Title: {book_title}")

    def generate_books(self, num_books):
        for _ in range(num_books):
            title = ''.join(random.choices(string.ascii_letters, k=random.randint(5, 15)))
            author = ''.join(random.choices(string.ascii_letters, k=random.randint(5, 15)))
            quantity = random.randint(1, 100)
            self.new_book(title, author, quantity)

    def generate_students(self, num_students):
        for _ in range(num_students):
            name_length = random.randint(5, 12)
            name = ''.join(random.choices(string.ascii_letters, k=name_length))
            student_id = ''.join(random.choices(string.digits, k=7))
            self.add_student(name, student_id)


def main():
    file_path = "library_data.txt"
    library = Library(file_path)
    # library.generate_books(10000)
    # library.generate_students(10000)

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Search Book")
        print("4. Display Books")
        print("5. Add Student")
        print("6. Delete Student")
        print("7. Search Student")
        print("8. Display Students")
        print("9. Rent Book")
        print("10. Return Book")
        print("11. Search Rentals")
        print("12. Display Rentals")
        print("0. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter book name: ")
            author = input("Enter book author: ")
            quantity = (input("Enter book quantity: "))
            if not author.strip().replace('-', '').replace(' ', '').isalpha():
                print(
                    "Invalid author name. Author name should only contain alphabetic characters, "
                    "hyphens, and spaces between words.")
                continue
            if isinstance(quantity, str):
                try:
                    quantity = int(quantity)
                except ValueError:
                    print("Invalid input for quantity. Please enter a valid integer.")
                    continue
            library.new_book(name, author, quantity)
        elif choice == "2":
            book_id = (input("Enter book ID to remove: "))
            if isinstance(book_id, str):
                try:
                    book_id = int(book_id)
                except ValueError:
                    print("Invalid input. Please enter valid Book ID (numbers).")
                    continue
            library.remove_book(book_id)
        elif choice == "3":
            book_id = (input("Enter book ID to search: "))
            if isinstance(book_id, str):
                try:
                    book_id = int(book_id)
                except ValueError:
                    print("Invalid input for book ID. Please enter a valid integer.")
                    continue
            library.search_book(book_id)
        elif choice == "4":
            library.print_books()
        elif choice == "5":
            name = input("Enter student name: ")
            student_id = input("Enter student ID: ")
            name = name.strip()
            if isinstance(student_id, str):
                try:
                    student_id = int(student_id)
                except ValueError:
                    print("Invalid input for student ID. Please enter a valid integer.")
                    continue
            library.add_student(name, student_id)
        elif choice == "6":
            name = input("Enter student name: ")
            student_id = input("Enter student ID: ")
            if isinstance(student_id, str):
                try:
                    student_id = int(student_id)
                except ValueError:
                    print("Invalid input for student ID. Please enter a valid integer.")
                    continue
            library.delete_student(name, student_id)
        elif choice == "7":
            name = input("Enter student name to search: ")
            library.search_student_by_name(name)
        elif choice == "8":
            library.display_students()
        elif choice == "9":
            name = input("Enter student name: ")
            student_id = input("Enter student ID: ")
            book_id = input("Enter book ID to rent: ")
            name = name.strip()
            if isinstance(student_id, str) and isinstance(book_id, str):
                try:
                    student_id = int(student_id)
                    book_id = int(book_id)
                except ValueError:
                    print("Invalid input for student ID or book ID. Please enter valid integers.")
                    continue
            library.add_rental(name, student_id, book_id)
        elif choice == "10":
            name = input("Enter student name: ")
            student_id = input("Enter student ID: ")
            book_id = input("Enter book ID to return: ")
            name = name.strip()
            if isinstance(student_id, str) and isinstance(book_id, str):
                try:
                    student_id = int(student_id)
                    book_id = int(book_id)
                except ValueError:
                    print("Invalid input for student ID or book ID. Please enter valid integers.")
                    continue
            library.return_rental(name, student_id, book_id)
        elif choice == "11":
            student_id = input("Enter student ID to search rentals: ")
            if isinstance(student_id, str):
                try:
                    student_id = int(student_id)
                except ValueError:
                    print("Invalid input for student ID. Please enter a valid integer.")
                    continue
            library.search_rentals(student_id)
        elif choice == "12":
            library.display_rentals()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
