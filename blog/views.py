from django.shortcuts import render
from .models import Task
from django.contrib.auth.models import *
from django.utils import timezone
from django.http import HttpResponse
from .forms import ContactForm
import random
import os
def post_list(request):
    allowed_tasks = []
    for i in Task.objects.all():
        if not request.user.is_anonymous:
            if request.user.get_short_name() == i.school:
                allowed_tasks.append(i.id)
            
    tasks = Task.objects.filter(id__in=allowed_tasks)
    return render(request, 'blog/post_list.html', {'tasks':tasks})

        
def login(request):
    return render(request, 'blog/login.html')

def task(request, id):
    allowed_task = []
    for i in Task.objects.all():
        if i.id == id:
            allowed_task.append(i.id)
    tasks = Task.objects.filter(id__in=allowed_task)
    return render(request, 'blog/task.html', {'tasks':tasks})

def task_submit(request, id):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            for i in Task.objects.all():
                if i.id == id:
                    expectedoutput = i.output
                    endinput = i.input
                    keywords = i.keyterms
            
            bad_chars="[]',"
            endinput_list = []
            ichars = []
            for i in range(len(endinput)-2):
                if not endinput[i+2] == ",":
                    ichars.append(endinput[i+2])
                else:
                    ichars.append("END")
            iword = ""
            for i in range(len(ichars)):
                if ichars[i] != "END":
                    iword = str(iword)+str(ichars[i])
                else:
                    endinput_list.append(iword)
                    iword = ""
            keywords_list =[]
            kword = ""
            for i in range(len(keywords)-2):
                if not keywords[i+2] == ",":
                    kword = str(kword)+str(keywords[i+2])
                else:
                    keywords_list.append(kword)
                    kword = ""

            code = request.POST.get('code')
            submit = []
            a_submit = []
            stat_input = 0
            submitappend = ""
            for x in range(len(code)):
                if code[x] == ";":
                    submit.append(submitappend)
                    submitappend = ""
                else:
                    submitappend = str(submitappend)+str(code[x])
                                
            a_submit = []
            output = 0
            received_input=0
            stat_input = 0
            outputvar1 = random.randint(1000,10000)
            outputvar = "a"+str(outputvar1)
            keywords_received = 0
            for i in range(len(submit)):
                if submit[i].find("print(") != -1:
                    code = submit[i]
                    find = submit[i].find("print(")
                    value = code[find+6:-1]
                    if output > 0:
                        a_submit.append(code[:find]+str(outputvar)+".append("+str(value)+")")
                        if keywords_received < len(keywords_list):
                            if submit[i].find(keywords_list[keywords_received]) != -1:
                                keywords_received += 1
                            
                    else:
                        a_submit.append(code[:find]+str(outputvar)+" = ["+str(value)+"]")
                        output+=1
                        if keywords_received < len(keywords_list):
                            if submit[i].find(keywords_list[keywords_received]) != -1:
                                keywords_received += 1
                elif submit[i].find("input(") != -1:
                    code = submit[i]
                    find = submit[i].find("input(")
                    value = code[:find-1]
                    a_submit.append(value+str(endinput_list[stat_input]))
                    stat_input += 1
                    received_input += 1
                    if keywords_received < len(keywords_list):
                        if submit[i].find(keywords_list[keywords_received]) != -1:
                            keywords_received += 1
                else:
                    a_submit.append(submit[i])
                    if keywords_received < len(keywords_list):
                        if submit[i].find(keywords_list[keywords_received]) != -1:
                            keywords_received += 1

            file = open("mark.py", "w")
            file.write(a_submit[0])
            file.close()
            for i in range(len(a_submit)-1):
                file = open("mark.py", "a")
                file.write('\n'+a_submit[i+1])
                file.close()
            file1 = open("mark.py", "a")
            file1.write('\n'+"with open(\"output.txt\", \"w\") as f:")
            file1.close()
            file2 = open("mark.py", "a")
            file2.write('\n'+"  "+"f.write(str("+str(outputvar)+"))")
            file2.close()
            print("Test program created!")
            print(os.system('mark.py'))
            print("Attempting to gather output data...")
            if os.path.exists('./output.txt'):
                r = open("output.txt")
                print("Gathered successfully!")
                char = []
                char1 = []
                insertend = False
                insertend1 = False
                words = []
                words1 = []
                word = ""
                word1 = ""
                for i in range(len(r.read())):
                    r = open("output.txt")
                    if bad_chars.find(r.read()[i]) == -1:
                        r = open("output.txt")
                        char.append(r.read()[i])
                        r = open("output.txt")
                        insertend = True
                    elif insertend == True:
                        insertend = False
                        char.append("END")
                for i in range(len(char)):
                    if char[i] != "END":
                        word = word+char[i]
                    else:
                        words.append(word)
                        word = ""
                

                for i in range(len(expectedoutput)-2):
                    
                    if not expectedoutput[i+2] == ",":
                        char1.append(expectedoutput[i+2])
                    elif expectedoutput[i+2] == ",":
                        char1.append("END")
                for i in range(len(char1)):
                    if char1[i] != "END":
                        word1 = word1+char1[i]
                    else:
                        words1.append(word1)
                        word1 = ""
                mark = 0
                total_marks = (len(words1))+len(endinput_list)+len(keywords_list)
                try:
                    for i in range(len(words1)):
                        if words1[i].upper() == words[i].upper():
                            mark+=1
                        elif words[i].upper().find(words1[i].upper()) != -1:
                            mark+=1
                except IndexError:
                    print("Hi")
                if received_input == len(endinput_list):
                        mark+=received_input
                mark += keywords_received
                r.close()
                os.remove("mark.py")
                os.remove("output.txt")
                username= request.user.get_username()
                for i in Task.objects.all():
                    if i.id == id:
                        i.students = str(i.students)+str(request.user.get_username())
                        i.marks = str(i.marks)+str(mark)
                        i.save()
                return HttpResponse("<html><head><style>#header /*Styles for Header*/{padding: 15px;color: #ffffff;font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 24px;background-color: #00ddff;}#main {font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 18px;}#button {background-color: white;color: black;border: 2px #e7e7e7;font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;border-radius: 5px;}#button:hover {background-color: #e7e7e7; color: black;font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;}#button1 {background-color: white;color: black;border: 2px solid #e7e7e7;width=\"50%\"font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;border-radius: 5px;}#button1:hover {background-color: #e7e7e7; color: black;width=\"50%\"font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 20px;}#title {font-family: \"Trebuchet MS\", Helvetica, sans-serif;font-size: 24px;}</style><title>MARKER</title></head><body><div><center><a href=\"/\"><h1 id=\"header\">MARKER</h1></a></center></div><center><p id=\"main\">Your mark is "+str(mark)+" out of "+str(total_marks)+"</p><br><a href=\"/\" id=\"button\">Click here to return back to the home page</a>")
                
            else:
                print("Hi")
    else:
        form = ContactForm()
    return render(request, 'blog/task_submit.html', {'form':form})
