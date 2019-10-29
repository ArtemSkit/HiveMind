

with open("Teacher.sql", 'r') as file:
    line = file.readline()
    with open("Teacher.txt", 'w') as ids:
        while line:
            ids.write(line.strip().split('(\'')[1].split('\'')[0] + '\n')
            line = file.readline()
