import sqlite3

DB = None
CONN = None

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Succesfully added student: %s %s" % (first_name, last_name)

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def get_project_by_title(title):
    query = """SELECT title, description FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """
Title: %s
Description: %s""" % (row[0], row[1])

def get_grade(student_github, project_title):
    query = """SELECT student_github, project_title, grade FROM Grades WHERE student_github = ? AND project_title = ?"""
    DB.execute(query,(student_github, project_title))
    row = DB.fetchone()
    print """%s grade on %s is %d""" % (row[0], row[1], row[2])

def add_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade) values (?, ?, ?)"""
    max_grade = int(max_grade)
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Succesfully added new project: %s %s %d" % (title, description, max_grade)

def add_grade(student_github, project_title, grade):
    query = """INSERT into Grades (student_github, project_title, grade) values (?, ?, ?)"""
    grade = int(grade)
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    print "Successfully added a grade of %d to %s on %s" % (grade, student_github, project_title)

def show_grades(student_github):
    query = """ SELECT student_github, project_title, grade FROM Grades WHERE student_github = ?"""
    DB.execute(query, (student_github,))
    grade_list = DB.fetchall()
    #return """Student github: %s""" % student_github
    list_of_projects = []
    for entry in grade_list:
        temp_project_dict = {}
        temp_project_dict[entry[1]] = (entry[2])
        list_of_projects.append(temp_project_dict)
    return list_of_projects

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "get_project":
            get_project_by_title(*args)
        elif command == "add_project":
            add_project(*args)
        elif command == "get_grade":
            get_grade (*args)
        elif command == "add_grade":
            add_grade(*args)
        elif command == "show_grades":
            show_grades (*args)

    CONN.close()

if __name__ == "__main__":
    main()
