from random import randint
rand_spisok_rating_chanse=[]
rand_spisok_rating=[]
for _ in range(35):
    rand_spisok_rating_chanse.append(randint(1,10))
    rand_spisok_rating.append(randint(8,9))
stroka=''
with open('rating.txt','w') as file:
    for i in rand_spisok_rating_chanse:
        stroka+=str(i)+';'
    file.write(stroka[:-1]+'\n')
    stroka=''
    for i in rand_spisok_rating:
        stroka+=str(i)+';'
    file.write(stroka[:-1])
    file.close()