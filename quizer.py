import os
import sys
import psycopg2
import re
from configparser import ConfigParser

# def addGrade(testNum, name, grade):
#    toBeWritten = "Name: " + name + ' Test:' + str(testNum) + ' Grade: ' + str(grade) + '\n'
#    fileOfTests = open("grades.txt", "a")
#    fileOfTests.write(toBeWritten)
#    fileOfTests.close()

# Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")
dbinfo = config_object["DBINFO"]

h = dbinfo["host"]
p = dbinfo["port"]
usr = dbinfo["user"]
pw = dbinfo["password"]
db = dbinfo["database"]

con = psycopg2.connect(host=h,
                       port=p,
                       user=usr,
                       password=pw,
                       database=db)

# Get a database cursor
cur = con.cursor()


def addTest():
    testName = input('Test Name:')
    questions = ''
    answers = ''
    qA = ''
    allQa = []
    anyMore = 'yes'

    sqlInsert = f'INSERT INTO tests (test) values(\'{testName}\')'
    cur.execute(sqlInsert)
    con.commit();

    cur.execute(f'select id from tests where test = \'{testName}\'')
    testId = cur.fetchone()

    while anyMore == 'yes':

        questions = input('What is the question?')
        answers = (input('What is the answer?'))
        sqlInsert = f'INSERT INTO QandA (question, answer, testid) values(\'{questions}\', \'{answers}\', \'{testId[0]}\') '
        cur.execute(sqlInsert)
        con.commit();

        # if len(allQa) > 0:
        #   qA = ',' + questions + '-' + answers
        # else:
        #   qA = questions + '-' + answers
        # allQa.append(qA)

        anymore = input('Anymore Questions?')
        if anymore == 'no':
            break
    # toBeWritten = '' + ''.join(allQa) + '\n'
    # fileOfTests = open("tests.txt", "a")
    # fileOfTests.write(toBeWritten)
    # fileOfTests.close()

    main()


def takeTest(user):
    numCorrect = 0
    questions = []
    answers = []

    testName = input('Test Name:')
    cur.execute(f'select id from tests where test = \'{testName}\'')
    testId = cur.fetchone()
    cur.execute(f'select question from qanda where testid = \'{testId[0]}\'')
    questions = cur.fetchall()
    cur.execute(f'select answer from qanda where testid = \'{testId[0]}\'')
    answers = cur.fetchall()
    numCorrect = 0
    for i in range(0, len(questions), 1):
        print('Question', i + 1)
        userAnswer = input(questions[i][0])
        if userAnswer.lower() == answers[i][0].strip().lower():
            numCorrect += 1

    grade = (numCorrect / len(questions)) * 100
    print(f'Grade: {grade}')  # Calculates current score based on number of questions.
    sqlInsert = f'INSERT INTO grades (name, grade, testID, date) values(\'{user}\', \'{grade}\', \'{testId[0]}\',current_timestamp)'

    cur.execute(sqlInsert)
    con.commit();

    ################Originally saved to txt file.
    # fileOfTests = open('tests.txt', 'r')  ##opens file with all tests
    # tests = fileOfTests.readlines()  ## reads one line(specific test)
    # name = input('Student Name:')
    # selection = int(input('Which test would you like to take?'))
    # specificTest = tests[selection - 1]
    # allQuestions = specificTest.split(',')  ## seperates test questions
    # for i in range(len(allQuestions)):  ##adds all questions and answers to appropriate fields
    #    qA = allQuestions[i].split('-')
    #    questions.append(qA[0])
    #    answers.append(qA[1])
    # for i in range(len(questions)):
    #    print('Question', i + 1)
    #    userAnswer = input(questions[i])
    #    answerCheck = answers[i].strip()
    #    if (userAnswer.lower() == answerCheck.lower()):
    #        numCorrect += 1

    # print('Grade:')
    # grade = (numCorrect / len(questions)) * 100
    # print(grade)  ##Calculates current score based on number of questions.
    # addGrade(selection, name, grade)
    # fileOfTests.close()
    ###############

    main(user)


def viewTests(userName):
    cur.execute('select qanda.testid as Test_id, tests.test as Test, qanda.question as Questions, '
                'qanda.answer as Answers from tests inner join qanda on tests.id = qanda.testid')
    allQuizes = cur.fetchall()
    print('Number, Test, Question, Answer')
    for i in range(0, len(allQuizes), 1):
        print(allQuizes[i])

    # count = 0
    # fileOfTests = open('tests.txt', 'r')  ##opens file with all tests
    # for line in fileOfTests:
    #    count += 1
    #    print('Quiz #', count, '-->', line)
    # fileOfTests.close()

    main(userName)


# Needs to be changed to database#######################
def deleteTest():
    count = 0
    fileOfTests = open('tests.txt', 'r')  ##opens file with all tests
    for line in fileOfTests:
        count += 1
        print('Quiz #', count, '-->', line)
    fileOfTests.close()
    reading = []
    fileOfTests = open('tests.txt', 'r')  ##opens file with all tests
    for line in fileOfTests:
        reading.append(line)
    fileOfTests.close()
    selection = int(input('Which quiz would you like to delete?'))
    reading.pop(selection - 1)
    fileOfTests = open("tests.txt", "w")
    for item in reading:
        fileOfTests.write("%s" % item)
    fileOfTests.close()
    main(userName)


##############################################

def viewGrades():
    cur.execute(
        'select tests.test, grades.name, grades.grade, grades.date from tests inner join grades on tests.id = grades.testid')
    allQuizes = cur.fetchall()
    print('Test, Name, Grade, Date')
    for i in range(0, len(allQuizes), 1):
        print(allQuizes[i])

    # a_file = open("grades.txt")
    # lines = a_file.readlines()
    # for line in lines:
    #    print(line, '')

    main(userName)


# Still needs work##############################
def printGrades():
    cur.execute(
        'select tests.test, grades.name, grades.grade, grades.date from tests inner join grades on tests.id = grades.testid')
    allQuizes = cur.fetchall()

    header = [i[0] for i in allQuizes]
    print(header)
    # cur.copy_to(sys.stdout, 'table', sep='\t', null='\n')

    main(userName)


################################################

def main(user):
    print('1) Available Quizes')
    print('2) Take Quiz')
    print('3) Add Quiz')
    print('4) Delete Quiz')
    print('5) View Grades')
    print('p) Print Grades')
    print('e) Exit')
    choice = input('Please select from the menu:')
    if choice == '1':
        viewTests(user)
    if choice == '2':
        takeTest(user)
    if choice == '3':
        addTest()
    if choice == '4':
        deleteTest()
    if choice == '5':
        viewGrades()
    if choice == 'p':
        printGrades()
    if choice == 'e':
        exit()
    else:
        main()


userName = input('Name:')
main(userName)
cur.close()
con.close()
