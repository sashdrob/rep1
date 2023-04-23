class Student:
    def __init__(self,full_name,group_number,progress):
        self.full_name=full_name
        self.group_number=group_number
        self.progress=progress
    def __str__(self):
        return self.full_name
    def prog(self):
        return self.progress
stud=[Student('Петя Иванов',21,[5,2,4]),Student('Вася Пупкин',31,[2,2,3,2]),Student('Денис Воронин',2,[5,5,5])]
stud_n=[]
prog=[]
for i in stud:
    stud_n.append(str(i))
for i in stud:
    if str(i.prog()).count('2')>0:
        prog.append(str(i))
print(sorted(stud_n))
print(sorted(prog))
