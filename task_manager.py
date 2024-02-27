# This code use lists, dictionaries and functions 
# to develop task management system
# for a small business
#Notes: 
# The username and password to access the admin rights are; 
# username: admin
# password: password
#=====import neccesary libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # create the task components
    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)
        
#================================================================================================
# this sections consist of 5 functions that could be called depending on user choice
         
#======1st function > reg_user ===========        
# the following function is called when user want to register a new user
# this function allow new user to be added and write this into user.txt file       
def reg_user():  

    file = open("user.txt", "r")
    user_data = file.read().split("\n")
  
    username_password = {}  # dictionary to store added username and password
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password
    registered = False
    while not registered:
        new_username = input("Please enter the new username: ") # request new username from user    
        if new_username in username_password.keys():
             print("Sorry, that username is taken. Start again and try a different one.")
             continue
        else:
            # - Request input of new password once username is available 
            confirmed = False
            while not confirmed:
                new_password = input("Please enter a new password: ")

                 # - Request input of password confirmation.
                confirm_password = input("Please confirm the password: ")

                 # - Check if the new password and confirmed password are the same.
                if new_password == confirm_password:
            # - If they are the same, add them to the user.txt file,
                    capitalise_username = new_username.capitalize() # just for print below, not for file
                    print("\nNew user named " + capitalise_username+ " have been added")
                    username_password[new_username] = new_password
                    confirmed = True
                else:
                    print("\n password mismatch, please try again. ")           
            registered = True
    
   # when new username and password are both confirmed, 
   # new user is added, then writen to file below
            
    with open("user.txt", "w") as out_file:   
        user_data = []
        for k in username_password:
            user_data.append(f"{k};{username_password[k]}")
        out_file.write("\n".join(user_data))                      
    return()
    

#======2nd function > add_task ====================
def add_task():  #this function allow user to add new tasks to tasks.txt

    with open("user.txt", 'r') as user_file:
        """open file locally to deal situations when new 
            user created after file is opened globally is to be assigned a task """
        user_data = user_file.read().split("\n")

    # Convert to a dictionary to allow for username and passowrd in pairs
    # the username is the key and password the value in the dictionary
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False
    task_added =  False
    while not task_added: 
        task_username = input("Name of person task will be assigned to: ")
        if task_username not in username_password.keys(): # check if user exist in user.text 
            print("User does not exist. Please enter a valid username")
            
        else:
            task_title = input("Title of Task: ")
            task_description = input("Description of Task: ")
            while True:
                try:
                    task_due_date = input("Due date of task (YYYY-MM-DD): ")
                    due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                    break

                except ValueError:
                    print("Invalid datetime format. Please use the format specified")

            # Then get the current date.
            curr_date = date.today()
            ''' Add the data to the file task.txt and
                Include 'No' to indicate if the task is complete.'''
            new_task = {
                "username": task_username,
                "title": task_title,
                "description": task_description,
                "due_date": due_date_time,
                "assigned_date": curr_date,
                "completed": False   }
            # write new assigned task to task.txt below
            task_list.append(new_task)
            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No"
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n")    
                task_file.write("\n".join(task_list_to_write))
                print("Task successfully added.")
            task_added = True
    return()

#======3rd function > view_all ====================
def view_all(): # this function allow user to view all the tasks listed in tasks.txt 

    print("All the tasks listed in tasks.txt are as follow: ")
    for count, t in enumerate(task_list, 1): # enumerate used to number the tasks starting from 1
        disp_str = f"Task: \t\t\t {t['title']}\n"
        disp_str += f"Assigned to: \t\t {t['username']}\n"
        disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \t {t['description']}\n"
        disp_str += f"completed: \t\t {t['completed']}\n"
        print(count)
        print(disp_str)    
    return()

##======4th function > view_mine ====================
#this function allow user to view all tasks assigned to them in tasks.txt 
# user can also edit the file such as changing the due date, reassign a task or mark it as completed. 

def view_mine(): 
    with open("tasks.txt", 'r') as task_file:

        for count, t in enumerate(task_list, start=1): #looping through the tasks and 
            #using enumurate to number tasks so that users can see task number from 1 to number of tasks   
           
            if t['username'] == curr_user:      
                  
                disp_str = f"Task: \t\t {t['title']}\n"
                disp_str += f"Assigned to: \t\t {t['username']}\n"
                disp_str += f"Date Assigned: \t\t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_str += f"Task Description: \t {t['description']}\n"
                disp_str += f"completed: \t\t {t['completed']}\n"
                
                print(count, disp_str)
    return_menu = False
    while not return_menu:              
        i =int(input("Please select a task numbers or select -1 to return to main menu: \n ")) 
        if i == -1:
            print("You have chosen to return to main menu: \n ")
            return_menu = True
            
        elif i == count:
            print("You have selected task " + str(i))
            i = i - 1 # i = i-1 since the index starts from zero and not 1
            print(".......................................\n")
            user_choice = input("Select 1 to edit, 2 to mark task as completed, or -1 to return to main menu:\n")
                # variable user_choice store what the user want to do. i.e whether edit or mark as completed 
        
            if user_choice == "1":
                if task_list[i]['completed'] == False:
                    choice = input ("Choose 1 to edit assigned username or 2 for due date: \n")
                    if choice == "1":
                        new_user = input("Enter new username: ")
                        task_list[i]['username'] = new_user
                        print("The task have been succesfully reassigned to: " + new_user.capitalize())
                        
                    elif choice == "2":
                        new_date = input("Enter new due date (YYYY-MM-DD): ")
                        task_list[i]['due_date'] =  datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                        print(new_date)
                        print("The task due date have been updated to: " + new_date)
                    
                    else:
                        print("Invalid choice, choose 1 to edit assigned username or 2 for due date: \n")
                else:
                    print("Sorry:Task can only be edited if it is uncompleted ") 
                    
            elif user_choice == "2":
                task_list[i]['completed'] = "Yes"     
                print("\nThe task have been successfully marked as completed.")
            
            elif user_choice == "-1":
                return_menu = True

            else:
                print("Invalid selection, please try again: ")
        else:
            print("Invalid selection, please try again: ")
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
    
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]

            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    
    return()           
# ####################5th function > generate_report#################################

def generate_report():
    
    #This section of the function deals with task_overview report
    with open("task_overview.txt",'w') as file: # To clear the data in the task_overview.txt 
        pass                                    # report needs to be new everytime it is generated 

    # defining relevant local variables for task_overview
    total_tasks = len(task_list)
    task_number_completed = 0
    task_number_uncompleted = 0
    task_uncompleted_overdue = 0
    task_percentage_incomplete = 0
    task_percentage_overdue = 0
    new_task_overview = {}

    #Loop through each task and update the variables for each task.
    for x in range(0, len(task_list)):
        if task_list[x]['completed'] == True:
            task_number_completed += 1
        elif task_list[x]['completed'] == False:
            task_number_uncompleted += 1

        d = task_list[x]['due_date']  #variable d to get the due date for each task
        if task_list[x]['completed'] == False:
           if datetime.date(datetime.now()) > d.date():  #compare due date to the present date time 
              task_uncompleted_overdue += 1
   
    # if else statements used below to avoid the division by zero error. 
    if task_number_uncompleted == 0:
        task_percentage_incomplete = 0
    else:
        task_percentage_incomplete = task_number_uncompleted/total_tasks*100
    if task_uncompleted_overdue == 0:
        task_percentage_overdue = 0
    else:
        task_percentage_overdue  = task_uncompleted_overdue/total_tasks*100


    #add all the output to a dictionary 
    new_task_overview = {  
                      "Total task": total_tasks, 
                      "Task completed": task_number_completed, 
                      "Task not completed": task_number_uncompleted,
                      "Task uncompleted & overdue": task_uncompleted_overdue, 
                      "Percentage tasks incomplete":round(task_percentage_incomplete, 2), #round the number to 2
                      "Percentage tasks overdue": round(task_percentage_overdue,2)}
    print("\n________________________")
    print("The Task Overview Report")
    print("________________________")
    for key, value in new_task_overview.items():
        print(key,"\n", value) # print the report for users before writing to a task_overview.txt
    
    if not os.path.exists(""):
        with open("task_overview.txt", "a+") as overview_file:
            #overview_file.write(str(new_task_overview)) 
            for key, value in new_task_overview.items():
                overview_file.write('%s:%s\n' % (key, str(value)))   
    

################################################################
#This section of the function deals with user_overiew report
    with open("user_overview.txt",'w') as file: # To clear the data in the user_overview.txt 
        pass                                    # report needs to be new everytime it is generated 
    # relevant variables defined below
    user_task_no = 0
    percentage_assigned = 0
    user_complete = 0
    user_incomplete = 0
    percentage_completed = 0
    percentage_incompleted = 0
    user_overdue = 0
    user_percentage_overdue = 0
    count = 0
    user_in_taskmanager = 0
    # loop below used to determine the number of users that are tracked in task manager
    for username in username_password.keys():   
        for line in task_data:
            x = list(line.split(";"))
            if username == x[0]:
               count +=1
        
        if count != 0:
            user_in_taskmanager +=1
        count = 0
   
    user_tracked =f"User registed in Task_manager; {user_in_taskmanager}"
    task_generated =f"Task generated and tracked in Task_manager; {total_tasks}"
    print("________________________")
    print("The User Overview Report")
    print("________________________")
    print(user_tracked)
    print(task_generated)
    if not os.path.exists(""):
        with open("user_overview.txt", "a+") as overview_file:
            overview_file.write(user_tracked) 
            overview_file.write("\n")
            overview_file.write(task_generated) 
            overview_file.write("\n")            
    # loop below used to determine the task information for each user
    for username in username_password.keys(): 
        for t in task_list:
            v = t['due_date']
            if username == t['username']:
                user_task_no += 1
                if t['completed'] == True:
                    user_complete += 1
                elif t['completed'] == False:
                    user_incomplete += 1                  
                    if datetime.date(datetime.now()) > v.date():
                      user_overdue += 1
        if user_task_no == 0:
            percentage_assigned = 0
        else:
            percentage_assigned = round(user_task_no/total_tasks*100, 2)
        if user_incomplete == 0:
            percentage_incompleted = 0
        else: 
            percentage_incompleted = round(user_incomplete/user_task_no*100, 2)
            percentage_completed = 100 - percentage_incompleted
        if user_overdue == 0:
            user_percentage_overdue = 0
        else:
            user_percentage_overdue = round(user_overdue/user_task_no*100, 2)
            
        print("..................................")
        print("user: " + username)
        print("assigned: " + str(user_task_no))
        print("Percentage assigned: " + str(percentage_assigned))
        print("percentage completed: "  + str(percentage_completed)) 
        print("percentage incompleted: "  + str(percentage_incompleted))
        print("Percentage overdue: "  + str(user_percentage_overdue)) 
         

        new_taskoverview = {"user": username, 
        "assigned" :str(user_task_no),
        "Percentage assigned" :str(percentage_assigned),
        "Percentage completed": str(percentage_completed),
        "Percentage uncompleted":str(percentage_incompleted),
        "Percentage overdue":  str(user_percentage_overdue)  }
        cap_list = []   
        cap_list.append(new_taskoverview) 

        # write the user report to file
        with open("user_overview.txt", "a+") as overview_file: # each user report is appended once generated fro the loop
            overview_file.write(str(new_taskoverview)) 
            overview_file.write("\n") 
        
        # reset all variables to zero for use in the loop for new user 
        user_task_no = 0
        percentage_assigned = 0
        user_complete = 0
        user_incomplete = 0
        percentage_completed = 0
        percentage_incompleted = 0
        user_overdue = 0
        user_percentage_overdue = 0

    return()

################################################
def display_statistics():
    
    num_users = len(username_password.keys())
    num_tasks = len(task_list)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")    
    return()


##################################################################################################
#====Login Section====
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary to allow for username and passowrd in pairs
# the username is the key and password the value in the dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

#======================Menu section================================================================
#print("\n===============Main Menu===========================")
exit = False
while not exit: 
    menu = input('''\n==========Main Menu==========\nSelect one of the following Options below:
    r - Register a user
    a - Add a task
    va - View all tasks
    vm - View my task
    gr - generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()
    if menu == 'r':
        registering = reg_user()
    elif menu == 'a':
        tasking = add_task()
    elif menu == 'va':
        viewing = view_all()
    elif menu == "vm":
        viewmy = view_mine()
    elif menu == "gr": 
        if curr_user == 'admin': 
            genreport = generate_report()
        else:
            print("You cannot generate report as you have no admin rights")
    elif menu == 'ds': 
        if curr_user == 'admin': 
            displaystat = display_statistics()
        else:
            print("You cannot display statistics as you have no admin rights")     
    elif menu == 'e':
        print("Thank you and goodbye")
        exit = True
    else:
        print("You did not choose a right option, please start again ")

