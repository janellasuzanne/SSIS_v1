import tkinter as tk
from tkinter import ttk, messagebox
import operator

class SSIS_ver1(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Simple Student Information System v2')

        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set the window dimensions
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenheight()

        # Calculate the position to center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window position
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # self.geometry('720x480')
        self.bind('<Control-KeyPress-w>', lambda event: self.quit())

        # entities
        self.student = 'STUDENT'
        self.course = 'COURSE'

        self.code_var = tk.StringVar(value='Enter Course Code')
        self.desc_var = tk.StringVar(value='Enter Course Description')
        self.id_var = tk.StringVar(value='Enter ID Number')
        self.first_var = tk.StringVar(value='Enter First Name')
        self.last_var = tk.StringVar(value='Enter Last Name')
        self.year_var = tk.StringVar(value='Select Year Level')
        self.gender_var = tk.StringVar(value='Select Gender')
        self.search_var = tk.StringVar(value='All')
        self.search_entry_var = tk.StringVar(value='Search here...')

        # frames
        self.entities_frame = tk.LabelFrame(self, relief='sunken')
        self.search_frame = tk.Frame(self, relief='sunken')

        # entities elements
        self.student_button = tk.Button(
            self.entities_frame,
            text=self.student,
            width=25,
            command=lambda: self.tab_selection(self.student)
        )
        self.course_button = tk.Button(
            self.entities_frame,
            text=self.course,
            width=25,
            command=lambda: self.tab_selection(self.course)
        )

        # search elements
        self.search_combobox = ttk.Combobox(
            self.search_frame,
            textvariable=self.search_var,
            width=20,
            state='readonly'
        )
        self.search_entry = tk.Entry(
            self.search_frame,
            textvariable=self.search_entry_var,
            width=80
        )

        # show_list button
        self.show_list = tk.Button(
            self,
            text='Show List',
            command=lambda: self.refresh_list(self.entity)
        )

        self.treeview = ttk.Treeview(self, show='headings')
        self.treeview.bind('<Double-Button-1>', self.get_info)

        # add button
        self.add = tk.Button(
            self,
            text='Add',
            relief='raised',
            command=lambda: self.create(self.entity)
        )

        # LAYOUT
        # frames
        self.entities_frame.pack(fill='x', padx=5, pady=10)
        self.search_frame.pack(fill='x', padx=5, pady=5)

        self.student_button.pack(side='left', expand=True, pady=5)
        self.course_button.pack(side='left', expand=True, pady=5)
        self.search_combobox.pack(side='left', expand=True)
        self.search_entry.pack(side='left', expand=True)
        self.show_list.pack(fill='x')
        self.treeview.pack(fill='x', expand=True, padx=30, pady=10)
        self.add.pack(fill='x', padx=10, pady=10)

        self.entity = self.student
        self.refresh_list(self.student)

        self.mainloop()

    def tab_selection(self, entity):
        if entity == self.student:
            self.entity = self.student
        elif entity == self.course:
            self.entity = self.course
        self.search_var.set('All')
        self.refresh_list(self.entity)

    def refresh_list(self, entity):
        self.entity = entity
        # Removes the previous data in the treeview
        if len(self.treeview.get_children()) > 0:
            self.treeview.delete(*self.treeview.get_children())

        if self.entity == self.student:
            self.treeview['columns'] = ('ID', 'Name', 'Course', 'Year Level')
            self.treeview.column("ID", width=5)
            self.treeview.column("Name", width=30)
            self.treeview.column("Course", width=10)
            self.treeview.column("Year Level", width=10)

            self.treeview.heading("ID", text="Student ID")
            self.treeview.heading("Name", text="Student Name")
            self.treeview.heading("Course", text="Course")
            self.treeview.heading("Year Level", text="Year Level")

            students = self.read_students_from_file()
            for student in students:
                self.treeview.insert('', tk.END, values=(student['id'], f'{student["first_name"]} {student["last_name"]}', student['course'], student['year_level']))
        else:

            self.treeview['columns'] = ('Code', 'Desc')
            self.treeview.column("Code", width=5)
            self.treeview.column("Desc", width=30)

            self.treeview.heading("Code", text="Course Code")
            self.treeview.heading("Desc", text="Course Description")

            courses = self.read_courses_from_file()
            for course in courses:
                self.treeview.insert('', tk.END, values=(course['code'], course['description']))

        # Updates the available search filters
        self.search_combo_update()
        
        self.search_items()

    def read_students_from_file(self):
        students = []
        with open('students.txt', 'r') as file:
            for line in file:
                id, first_name, last_name, course, year_level, gender = line.strip().split(',')
                student = {
                    'id': id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'course': course,
                    'year_level': year_level,
                    'gender': gender
                }
                students.append(student)
        return students

    def read_courses_from_file(self):
        courses = []
        with open('courses.txt', 'r') as file:
            for line in file:
                code, description = line.strip().split(',')
                course = {'code': code, 'description': description}
                courses.append(course)
        return courses

    def search_combo_update(self):
        if self.entity == self.student:
            self.search_combobox['values'] = ('All', 'ID', 'Last Name', 'Course')
        elif self.entity == self.course:
            self.search_combobox['values'] = ('All', 'Course Code')

    def search_items(self):
        search_criteria = self.search_var.get()
        search_text = self.search_entry_var.get()

        if self.entity == self.student:
            if search_criteria == 'All':
                students = self.read_students_from_file()
                filtered_students = students
            elif search_criteria == 'ID':
                students = self.read_students_from_file()
                filtered_students = [student for student in students if student['id'] == search_text]
            elif search_criteria == 'Last Name':
                students = self.read_students_from_file()
                filtered_students = [student for student in students if student['last_name'].lower() == search_text.lower()]
            elif search_criteria == 'Course':
                students = self.read_students_from_file()
                filtered_students = [student for student in students if student['course'].lower() == search_text.lower()]

            # Display the filtered students in the treeview
            self.treeview.delete(*self.treeview.get_children())
            for student in filtered_students:
                self.treeview.insert('', tk.END, values=(student['id'], f'{student["first_name"]} {student["last_name"]}', student['course'], student['year_level']))

        elif self.entity == self.course:
            if search_criteria == 'All':
                courses = self.read_courses_from_file()
                filtered_courses = courses
            elif search_criteria == 'Course Code':
                courses = self.read_courses_from_file()
                filtered_courses = [course for course in courses if course['code'].lower() == search_text.lower()]

            # Display the filtered courses in the treeview
            self.treeview.delete(*self.treeview.get_children())
            for course in filtered_courses:
                self.treeview.insert('', tk.END, values=(course['code'], course['description']))
        

    def create(self, entity):
        # toplevel
        self.create_toplevel = tk.Toplevel(self)
        self.create_toplevel.title('Information')
        self.create_toplevel.geometry('500x350')
        self.create_toplevel.resizable(False, False)
        self.create_toplevel.bind('<Control-KeyPress-w>', lambda event: self.create_toplevel.destroy())

        # WIDGETS
        # frames 
        self.info_field = tk.LabelFrame(self.create_toplevel, relief='sunken')
        self.labels_frame = tk.Frame(self.info_field)
        self.entries_frame = tk.Frame(self.info_field)
        self.actions_frame = tk.Frame(self.create_toplevel)

        # actions elements
        self.submit = tk.Button(self.actions_frame, text='Submit', command=self.submit_item)
        self.cancel = tk.Button(self.actions_frame, text='Cancel', command=lambda: self.create_toplevel.destroy())

        # LAYOUT
        # frames
        self.info_field.pack(fill='x', pady=20)
        self.actions_frame.pack(fill='x', side='bottom', pady=10)
        
        # info frame sub-frames
        self.labels_frame.pack(side='left', expand=True, pady=10)
        self.entries_frame.pack(side='left', expand=True, pady=10)

        # actions element
        self.submit.pack(fill='x', padx=10, pady=5)
        self.cancel.pack(fill='x', padx=10, pady=5)

        if entity == self.course:
            self.code_label = tk.Label(self.labels_frame, text='COURSE CODE:')
            self.desc_label = tk.Label(self.labels_frame, text='COURSE DESCRIPTION:')

            self.code_entry = tk.Entry(
                self.entries_frame,
                textvariable=self.code_var,
                width=45
            )
            self.desc_entry = tk.Entry(
                self.entries_frame,
                textvariable=self.desc_var,
                width=45
            )

            self.code_label.pack(anchor='w', pady=2)
            self.desc_label.pack(anchor='w', pady=2)
            self.code_entry.pack(pady=2)
            self.desc_entry.pack(pady=2)

        if entity == self.student:
            self.student_id_label = tk.Label(self.labels_frame, text='STUDENT ID:')
            self.first_name_label = tk.Label(self.labels_frame, text='FIRST NAME:')
            self.last_name_label = tk.Label(self.labels_frame, text='LAST NAME:')
            self.course_label = tk.Label(self.labels_frame, text='COURSE:')
            self.year_level_label = tk.Label(self.labels_frame, text='YEAR LEVEL:')
            self.gender = tk.Label(self.labels_frame, text='GENDER:')

            self.student_id_entry = tk.Entry(
                self.entries_frame,
                textvariable=self.id_var,
                width=45
            )

            self.first_name_entry = tk.Entry(
                self.entries_frame,
                textvariable=self.first_var,
                width=45
            )

            self.last_name_entry = tk.Entry(
                self.entries_frame,
                textvariable=self.last_var,
                width=45
            )

            self.course_combobox = ttk.Combobox(
                self.entries_frame,
                textvariable=self.code_var,
                width=45,
                state='readonly'
            )
            courses = self.read_courses_from_file()
            self.course_combobox['values'] = [course['code'] for course in courses]

            self.year_level_combobox = ttk.Combobox(
                self.entries_frame,
                values=('1st Year', '2nd Year', '3rd Year', '4th Year'),
                textvariable=self.year_var,
                width=45,
                state='readonly'
            )

            self.gender_combobox = ttk.Combobox(
                self.entries_frame,
                values=('Male', 'Female'),
                textvariable=self.gender_var,
                width=45,
                state='readonly'
            )

            self.student_id_label.pack(anchor='w', pady=2)
            self.first_name_label.pack(anchor='w', pady=2)
            self.last_name_label.pack(anchor='w', pady=2)
            self.course_label.pack(anchor='w', pady=2)
            self.year_level_label.pack(anchor='w', pady=2)
            self.gender.pack(anchor='w', pady=2)

            self.student_id_entry.pack(pady=2)
            self.first_name_entry.pack(pady=2)
            self.last_name_entry.pack(pady=2)
            self.course_combobox.pack(pady=2)
            self.year_level_combobox.pack(pady=2)
            self.gender_combobox.pack(pady=2)

    def submit_item(self):
        if self.entity == self.course:
            course = {
                'code': self.code_var.get(),
                'description': self.desc_var.get()
            }

            # Check if course code already exists
            if self.is_duplicate_course_code(course['code']):
                messagebox.showerror('Error', 'Duplicate COURSE!')
                return

            self.write_course_to_file(course)

        elif self.entity == self.student:
            student = {
                'id': self.id_var.get(),
                'first_name': self.first_var.get(),
                'last_name': self.last_var.get(),
                'course': self.code_var.get(),
                'year_level': self.year_var.get(),
                'gender': self.gender_var.get()
            }

            # Check if student ID already exists
            if self.is_duplicate_student_id(student['id']):
                messagebox.showerror('Error', 'Duplicate STUDENT ID!')
                return

            self.write_student_to_file(student)

        messagebox.showinfo('Registration Successful!', f'{self.entity} successfully registered!')
        self.refresh_list(self.entity)
        self.create_toplevel.destroy()

    def is_duplicate_course_code(self, code, exclude=None):
        courses = self.read_courses_from_file()
        for course in courses:
            if course['code'] == code and course['code'] != exclude:
                return True
        return False

    def is_duplicate_student_id(self, id, exclude=None):
        students = self.read_students_from_file()
        for student in students:
            if student['id'] == id and student['id'] != exclude:
                return True
        return False

    def write_course_to_file(self, course):
        with open('courses.txt', 'a') as file:
            file.write(f"{course['code']},{course['description']}\n")

    def write_student_to_file(self, student):
        with open('students.txt', 'a') as file:
            file.write(
                f"{student['id']},{student['first_name']},{student['last_name']},{student['course']},"
                f"{student['year_level']},{student['gender']}\n"
            )

    def get_info(self, event):
        item = self.treeview.focus()
        info = self.treeview.item(item, 'values')
        
        # WIDGETS
        # toplevel
        self.info_toplevel = tk.Toplevel(self)
        self.info_toplevel.title('Information')
        self.info_toplevel.geometry('500x300')
        self.info_toplevel.resizable(False, False)
        self.info_toplevel.bind('<Control-KeyPress-w>', lambda event: self.info_toplevel.destroy())

            # frames
        self.info_field = tk.LabelFrame(self.info_toplevel, relief='sunken')
        self.labels_frame = tk.Frame(self.info_field)
        self.entries_frame = tk.Frame(self.info_field)

        self.actions_frame = tk.Frame(self.info_toplevel)

        if self.entity == self.course:
            self.code_var.set(info[0])
            self.desc_var.set(info[1])
            # WIDGETS
            # labels
            self.code_label = tk.Label(self.labels_frame, text='COURSE CODE:')
            self.desc_label = tk.Label(self.labels_frame, text='COURSE DESCRIPTION:')

            # entries
            self.code_entry = tk.Entry(
                self.entries_frame,
                textvariable=self.code_var,
                width=45,
                state='disable')
            self.desc_entry = tk.Entry(
                self.entries_frame,
                textvariable=self.desc_var,
                width=45,
                state='disable')

            # LAYOUT
                # labels
            self.code_label.pack(anchor='w', pady=2)
            self.desc_label.pack(anchor='w', pady=2)
            
                # entries
            self.code_entry.pack(pady=2)
            self.desc_entry.pack(pady=2)

            self.editables = (self.code_entry, self.desc_entry)
            self.key = info[0]

        elif self.entity == self.student:
            with open('students.txt', 'r') as file:
                for line in file:
                    student_list = line.strip().split(',')
                    if student_list[0] == info[0]:
                        self.id_var.set(student_list[0])
                        self.first_var.set(student_list[1])
                        self.last_var.set(student_list[2])
                        self.code_var.set(student_list[3])
                        self.year_var.set(student_list[4])
                        self.gender_var.set(student_list[5])
                        print(student_list)

                        break

            # WIDGETS
                # labels
            self.student_id_label = tk.Label(self.labels_frame, text='STUDENT ID:')
            self.first_name_label = tk.Label(self.labels_frame, text='FIRST NAME:')
            self.last_name_label = tk.Label(self.labels_frame, text='LAST NAME:')
            self.course_label = tk.Label(self.labels_frame, text='COURSE:')
            self.year_level_label = tk.Label(self.labels_frame, text='YEAR LEVEL:')
            self.gender = tk.Label(self.labels_frame, text='GENDER:')

                # entries
            self.student_id_entry = tk.Entry(
                self.entries_frame, 
                textvariable=self.id_var,
                width=45,
                state='disable')
            self.first_name_entry = tk.Entry(
                self.entries_frame, 
                textvariable=self.first_var,
                width=45,
                state='disable')
            self.last_name_entry = tk.Entry(
                self.entries_frame, 
                textvariable=self.last_var,
                width=45,
                state='disable')

            self.course_combobox = ttk.Combobox(
                self.entries_frame, 
                textvariable=self.code_var,
                width=45,
                state='disable')

            # fetch available courses
            courses = []
            with open('courses.txt', 'r') as file:
                for line in file:
                    course_info = line.strip().split(',')
                    courses.append(course_info[0])
            self.course_combobox['values'] = courses

            self.year_level_combobox = ttk.Combobox(
                self.entries_frame, 
                values=('1st Year', '2nd Year', '3rd Year', '4th year'),
                textvariable=self.year_var,
                width=45,
                state='disable')

            self.gender_combobox = ttk.Combobox(
                self.entries_frame, 
                values=('Male', 'Female'),
                textvariable=self.gender_var,
                width=45,
                state='disable')

            # LAYOUT
                # labels
            self.student_id_label.pack(anchor='w', pady=2)
            self.first_name_label.pack(anchor='w', pady=2)
            self.last_name_label.pack(anchor='w', pady=2)
            self.course_label.pack(anchor='w', pady=2)
            self.year_level_label.pack(anchor='w', pady=2)
            self.gender.pack(anchor='w', pady=2)
                # entries
            self.student_id_entry.pack(pady=2)
            self.first_name_entry.pack(pady=2)
            self.last_name_entry.pack(pady=2)
            self.course_combobox.pack(pady=2)
            self.year_level_combobox.pack(pady=2)
            self.gender_combobox.pack(pady=2)
        
            self.editables = (self.course_combobox, self.year_level_combobox, self.gender_combobox)
            self.key = info[0]

            # actions_frame elementS
        self.edit = tk.Button(self.actions_frame, text='Edit', width=20, command=lambda: self.edit_entries(self.editables))
        self.update = tk.Button(self.actions_frame, text='Update', width=20, command=lambda: self.update_item(self.key))
        self.delete = tk.Button(self.actions_frame, text='Delete', width=20, command=lambda: self.delete_item(self.info_toplevel))

        # LAYOUT
            # frames
        self.info_field.pack(fill='x', pady=20)
        self.labels_frame.pack(side='left', expand=True, pady=10)
        self.entries_frame.pack(side='left', expand=True, pady=10)

            # actions layout
        self.actions_frame.pack(side='bottom', fill='x', padx=20, pady=10)

            # actions elements
        self.edit.pack(side='left', expand=True)
        self.update.pack(side='left', expand=True)
        self.delete.pack(side='left', expand=True)

    def edit_entries(self, editables):
        if self.entity == self.course:
            for editable in editables:
                editable['state'] = 'normal'
        if self.entity == self.student:
            for editable in editables:
                editable['state'] = 'readonly'

    def update_item(self, key):
        if self.entity == self.course:
            updated_course = {
                'code': self.code_var.get(),
                'description': self.desc_var.get()
            }

            # Check if course code already exists (excluding the current course)
            if self.is_duplicate_course_code(updated_course['code'], exclude=key):
                messagebox.showerror('Error', 'Duplicate COURSE!')
                return

            students = []

            with open('students.txt', 'r') as file:
                for line in file:
                    student_info = line.strip().split(',')
                    if student_info[3] == key:
                        student_info[3] = updated_course['code']
                    students.append({
                        'id': student_info[0],
                        'first_name': student_info[1],
                        'last_name': student_info[2],
                        'course': student_info[3],
                        'year_level': student_info[4],
                        'gender': student_info[5]
                    })

            self.write_students_to_file(students)

            courses = self.read_courses_from_file()
            for i, course in enumerate(courses):
                if course['code'] == key:
                    courses[i] = updated_course

            self.write_courses_to_file(courses)

        if self.entity == self.student:
            updated_student = {
                'id': self.id_var.get(),
                'first_name': self.first_var.get(),
                'last_name': self.last_var.get(),
                'course': self.code_var.get(),
                'year_level': self.year_var.get(),
                'gender': self.gender_var.get()
            }

            students = self.read_students_from_file()
            for i, student in enumerate(students):
                if student['id'] == key:
                    students[i] = updated_student

            self.write_students_to_file(students)

            courses = self.read_courses_from_file()
            for course in courses:
                if course['code'] == key:
                    course['code'] = updated_student['course']

            self.write_courses_to_file(courses)

        messagebox.showinfo('Update Successful', 'Information Updated!')
        self.refresh_list(self.entity)
        self.info_toplevel.destroy()

    def delete_item(self, toplevel):
        confirm = False

        if self.entity == self.course:
            studentsInCourse = []
            with open('students.txt', 'r') as file:
                for line in file:
                    student_info = line.strip().split(',')
                    if student_info[3] == self.code_var.get():
                        studentsInCourse.append(student_info)

            if len(studentsInCourse) > 0:
                answer = messagebox.askokcancel(
                    "Warning",
                    f"Students are currently enrolled in this {self.entity}.\nDo you still want to DELETE this {self.entity}?\n\n\n(If the course is deleted, all currently enrolled students will not belong to any courses.)"
                )
                if answer:
                    confirm = True
            else:
                answer = messagebox.askyesno(
                    'Confirm Deletion',
                    f"Are you sure you want to DELETE THIS {self.entity}?\n\nCOURSE CODE: \t\t{self.code_var.get()}\n\nCOURSE DESCRIPTION: \t{self.desc_var.get()}"
                )
                if answer:
                    confirm = True

            if confirm:
                messagebox.showinfo('DELETION CONFIRMED', f'{self.entity} successfully deleted')

                # Delete the course from the courses file
                courses = self.read_courses_from_file()
                updated_courses = [course for course in courses if course['code'] != self.code_var.get()]
                self.write_courses_to_file(updated_courses)

                # Update the student records in the students file
                updated_students = []
                with open('students.txt', 'r') as file:
                    for line in file:
                        student_info = line.strip().split(',')
                        if student_info[3] == self.code_var.get():
                            student_info[3] = 'None'
                        updated_students.append({
                            'id': student_info[0],
                            'first_name': student_info[1],
                            'last_name': student_info[2],
                            'course': student_info[3],
                            'year_level': student_info[4],
                            'gender': student_info[5]
                    })

                self.write_students_to_file(updated_students)

        if self.entity == self.student:
            answer = messagebox.askyesno(
                'Confirm Deletion',
                f'Are you sure you want to DELETE THIS {self.entity}?\n\nSTUDENT ID:\t{self.id_var.get()}\n\nNAME: \t\t{self.first_var.get()} {self.last_var.get()}\n\nCOURSE: \t{self.code_var.get()}\n\nYEAR LEVEL: \t{self.year_var.get()}\n\nGENDER: \t{self.gender_var.get()}'
            )

            if answer:
                messagebox.showinfo('DELETION CONFIRMED', f'{self.entity} successfully deleted')
                confirm = True

                # Delete the student from the students file
                students = self.read_students_from_file()
                updated_students = [student for student in students if student['id'] != self.id_var.get()]
                self.write_students_to_file(updated_students)

        # Updates the list in the treeview after deletion
        if confirm:
            toplevel.destroy()
            self.refresh_list(self.entity)
        else:
            toplevel.destroy()

    def read_courses_from_file(self):
        courses = []
        with open('courses.txt', 'r') as file:
            for line in file:
                code, description = line.strip().split(',')
                course = {'code': code, 'description': description}
                courses.append(course)
        return courses

    def write_courses_to_file(self, courses):
        with open('courses.txt', 'w') as file:
            for course in courses:
                file.write(f"{course['code']},{course['description']}\n")

    def read_students_from_file(self):
        students = []
        with open('students.txt', 'r') as file:
            for line in file:
                id, first_name, last_name, course, year_level, gender = line.strip().split(',')
                student = {
                    'id': id,
                    'first_name': first_name,
                    'last_name': last_name,
                    'course': course,
                    'year_level': year_level,
                    'gender': gender
                }
                students.append(student)
        return students

    def write_students_to_file(self, students):
        with open('students.txt', 'w') as file:
            for student in students:
                file.write(
                    f"{student['id']},{student['first_name']},{student['last_name']},{student['course']},"
                    f"{student['year_level']},{student['gender']}\n"
                )

SSIS_ver1()
