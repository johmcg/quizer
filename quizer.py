import os

def addGrade(testNum, name, grade):
    toBeWritten = "Name: "+name+' Test:'+str(testNum)+' Grade: '+str(grade) + '\n'
    fileOfTests = open("grades.txt", "a")
    fileOfTests.write(toBeWritten)
    fileOfTests.close()

def addTest():
    questions = ''
    answers = ''
    qA = ''
    allQa = []
    anyMore = 'yes'
    while anyMore == 'yes':
        questions=input('What is the question?')
        answers=(input('What is the answer?'))
        if len(allQa)>0:
            qA = ','+ questions + '-' + answers
        else:
            qA=questions+'-'+answers
        allQa.append(qA)
        anymore = input('Anymore Questions?')
        if anymore == 'no':
            break
    toBeWritten = '' + ''.join(allQa) + '\n'
    fileOfTests = open("tests.txt", "a")
    fileOfTests.write(toBeWritten)
    fileOfTests.close()
    main()

def takeTest():
    numCorrect = 0
    questions = []
    answers = []
    fileOfTests = open('tests.txt', 'r')##opens file with all tests
    tests = fileOfTests.readlines()## reads one line(specific test)
    name = input('Student Name:')
    selection = int(input('Which test would you like to take?'))
    specificTest = tests[selection-1]
    allQuestions = specificTest.split(',') ## seperates test questions
    for i in range(len(allQuestions)):##adds all questions and answers to appropriate fields
        qA = allQuestions[i].split('-')
        questions.append(qA[0])
        answers.append(qA[1])
    for i in range(len(questions)):
        print('Question', i+1)
        userAnswer = input(questions[i])
        answerCheck = answers[i].strip()
        if (userAnswer.lower() == answerCheck.lower()):
            numCorrect += 1

    print('Grade:')
    grade = (numCorrect/len(questions))*100
    print(grade) ##Calculates current score based on number of questions.
    addGrade(selection, name, grade)
    fileOfTests.close()
    main()

def viewTests():
    count = 0
    fileOfTests = open('tests.txt', 'r')##opens file with all tests
    for line in fileOfTests:
        count += 1
        print('Quiz #',count,'-->',line)
    fileOfTests.close()
    main()

def deleteTest():
    count = 0
    fileOfTests = open('tests.txt', 'r')##opens file with all tests
    for line in fileOfTests:
        count += 1
        print('Quiz #',count,'-->',line)
    fileOfTests.close()
    reading = []
    fileOfTests = open('tests.txt', 'r')##opens file with all tests
    for line in fileOfTests:
        reading.append(line)
    fileOfTests.close()
    selection=int(input('Which quiz would you like to delete?'))
    reading.pop(selection-1) 
    fileOfTests = open("tests.txt", "w")
    for item in reading:
        fileOfTests.write("%s" % item)
    fileOfTests.close()
    main()

def viewGrades():
    a_file = open("grades.txt")
    lines = a_file.readlines()
    for line in lines:
        print(line,'')
    main()


def printGrades():
    os.startfile("grades.txt", "print")
    main()


def main():
    print('1) Available Quizes')
    print('2) Take Quiz')
    print('3) Add Quiz')
    print('4) Delete Quiz')
    print('5) View Grades')
    print('p) Print Grades')
    print('e) Exit')
    choice = input('Please select from the menu:')
    if choice == '1':
        viewTests()
    if choice == '2':
        takeTest()
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

main()
