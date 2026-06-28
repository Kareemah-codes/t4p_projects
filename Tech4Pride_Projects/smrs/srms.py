#Modules
import os
import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

#GLOBAL
class_data = ""
folder_path =""

def load_file():
    """Loads existing class file"""
    folder_name = input('What class are you looking for?')
    term= input('What term?')

    global folder_path
    folder_path =f"{folder_name}/term{term}.json"
    with open(folder_path,"r") as file:
       global class_data
       class_data= json.load(file)

def write_file():
    global folder_path
    with open(folder_path,'w') as f:
        global class_data
        class_data= json.dumps(class_data, indent=2)
        f.write(class_data)

def setup_class():
    """Setup's up a class by creating a folder with a json file inside"""
    class_label = input('Enter class name')
    term = int(input('Enter term(1,2 or )3'))
    subjects = []
    no_subjects = int(input('What number of subjects do the students take?'))

    for i in range(no_subjects):
        subject = input(f'Enter subject {i+1}')
        subjects.append(subject)

    no_students = int(input('What is the number of students'))
    if no_students >200:
        print('Maximum of 200 students allowed')

    passing_threshold = int(input("What is the passing threshold for this class[default=>50%]") or 50) 

    max_no_failures = int(input('What is the max number of failures to be promoted?'))
    form_teacher = input('Enter the Class Teacher\'s name ')

    class_enitity = {
        "name": class_label,
        "term": term,
        "form teacher":form_teacher,
        "no_students":no_students,
        "subjects": subjects,
        "students":[]
    }

    folder_name = f"{class_label}"

    #creating the folder
    try:
        os.mkdir(folder_name)
        print(f"Class folder : {folder_name} created successfully")
    except:
        print("Error")

    #creating the json file
    with open(f"{folder_name}/term{term}.json",'a') as f:
        global class_data
        class_data= json.dumps(class_enitity)
        f.write(class_data)


def add_student():

    """Adds student to created or existing json file"""
    
    name = input('Enter student name')
    id = input('Enter student ID')

    student ={
        "id": id,
        "name": name        
    }
    global class_data
    class_data["students"].append(student)
    write_file()

def update_marks():
    """Updates or enters marks for student"""
    
    id = input('Enter student ID')

    for student in class_data["students"]:
        if student["id"] == id:
            print(f"{student["name"]}'s Current Scores \n {student["scores"]}\n Enter the score update for each subject")

            for subject, current_score in student["scores"].items():
                new_score = int(input(f"{subject} (current: {current_score}): "))
                student["scores"][subject] = new_score 
            break
            
        # else:
        #     print(f"Student with {id} does not exist")
    write_file()

def display_student_result():
    id = input('Enter Student ID: ')

    for student in class_data["students"]:
        if student["id"] == id:

           
            console = Console()
            table = Table()
            table.add_column("Subject")
            table.add_column("Max")
            table.add_column("Score")

            
            for subject, current_score in student["scores"].items():
                table.add_row(subject, "100", str(current_score))

            console.print(f"""
═══════════════════════════════════════════════════════════
CLASS: {class_data["class_name"]}          TERM: {class_data["term"]}
═══════════════════════════════════════════════════════════
Name    : {student["name"]}         Student ID : {student["id"]}
Gender  : {student["gender"]}       DOB        : {student["dob"]}
═══════════════════════════════════════════════════════════
            """)

            console.print(table)

            console.print(f"""
═══════════════════════════════════════════════════════════
Class Rank  : {student["rank"]} out of {len(class_data["students"])}
Status      : {student["status"]}
Form Teacher: {class_data["form_teacher"]}
═══════════════════════════════════════════════════════════
            """)

            break 

    else:
        print(f"Student with ID {id} does not exist")

def display_class_result():
    console = Console()
    table = Table()
    table.add_column("Rank")
    table.add_column("Name")   

    for subject in class_data["subjects"]:
        table.add_column(subject["name"])

    table.add_column("Total")

    for student in class_data["students"]:
        scores = [str(score) for score in student["scores"].values()] 
        table.add_row(str(student["rank"]), student["name"], *scores, str(student["total"]))

    console.print(table)
 
def search_student():
    id = input('Enter student ID ')

    for student in class_data["students"]:
        if student["id"] == id:
            print(f"{student["name"]}'s Details \n")
            print(student)

def delete_student():
    id = input('Enter student ID ')

    for student in class_data["students"]:
        if student["id"] == id:
            print(f"{student["name"]}'s Details \n {student}")
            delete_confirm = input("Delete the above student's details?(y/n)")

            if delete_confirm.lower() == 'y':
                class_data["students"].remove(student)
                write_file()
                print('Deletion successful')
            elif delete_confirm.lower() =='n':
                pass
            else:
                print('Input correct character(y/n)')




def init_class():
    """Initializes program"""
    print('Welcome to the Student Result Manager')
    response = input("Are you loading an existing class(Y) OR setting up a class(N)")
    if response.lower() == 'y':
        load_file()
        delete_student()
    elif response.lower()== 'n':
        setup_class()
    else:
        print('Error,select Y or N')

init_class()



    







