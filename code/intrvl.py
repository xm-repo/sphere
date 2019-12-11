import re
import json
import numpy as np
import intervals as I

intv_7 = I.open(I.inf, -I.inf)
intv_8 = I.open(I.inf, -I.inf)
intv_9 = I.open(I.inf, -I.inf)

f = open('colorings.txt', 'r')

for l in f:
    l = (' '.join(l.split(' '))).split()
    
    if len(l) == 0:
        continue

    c = int(l[1])
    a = float(l[2])
    b = float(l[3])

    if c == 7:
        intv_7 = intv_7 | I.open(a, b)
    elif c == 8:
        intv_8 = intv_8 | I.open(a, b)
    elif c == 9:
        intv_9 = intv_9 | I.open(a, b)

print('7')
print(intv_7)
print('8')
print(intv_8)
print('9')
print(intv_9)

for ii in list(intv_7):
    print('\\draw[thickest] ({},4) -- ({},4);'.format(5*ii.lower, 5*ii.upper))

for ii in list(intv_8):
    print('\\draw[thickest] ({},2) -- ({},2);'.format(5*ii.lower, 5*ii.upper))

for ii in list(intv_9):
    print('\\draw[thickest] ({},0) -- ({},0);'.format(5*ii.lower, 5*ii.upper))

'''    
    if l[0] == '37.xyz':
        continue

    name = int(l[0].replace('.xyz', ' '))
    d0 = float(l[2]) #d0
    d1 = float(l[3]) #d1

    if d1 / d0 < 1:
        continue
    
    intv_all = intv_all | I.open(1/d1, 1/d0)

    if name in chroma7:
        intv_7 = intv_7 | I.open(np.round(1/d1, 3), np.round(1/d0, 3))
    elif name in chroma8:
        intv_8 = intv_8 | I.open(np.round(1/d1, 3), np.round(1/d0, 3))
    else:
        intv_9 = intv_9 | I.open(np.round(1/d1, 3), np.round(1/d0, 3))

print('all')
print(intv_all)
print('7')
print(intv_7)
print('8')
print(intv_8)
print('9')
print(intv_9)

intv_9 = (intv_9 - intv_8) - intv_7
intv_8 = (intv_8 - intv_7)


for ii in list(intv_7):
    print('\\draw[thickest] ({},4) -- ({},4);'.format(5*ii.lower, 5*ii.upper))

for ii in list(intv_8):
    print('\\draw[thickest] ({},2) -- ({},2);'.format(5*ii.lower, 5*ii.upper))

for ii in list(intv_9):
    print('\\draw[thickest] ({},0) -- ({},0);'.format(5*ii.lower, 5*ii.upper))    

'''

'''
f2 = open('C:\\Users\\IM\\Desktop\\conf\\thomson\\diams1.txt', 'r')

d = dict()
for l in f2:
    arr = l.split(' ')  
    N = arr[0].replace('.xyz', '')
    theta1 = float(arr[5])
    theta2 = float(arr[6])
    d[N] = np.round(theta2, 3)

data = json.load(open('C:\\Users\\IM\\Desktop\\conf\\thomson\\thomson\\wiki_table.txt'))

for k in data.keys():
    data[k]['theta2'] = 0

for k in d.keys():
    data[k]['theta2'] = d[k]

with open('C:\\Users\\IM\\Desktop\\conf\\thomson\\thomson\\wiki_table.txt', 'w') as f:
  json.dump(data, f, ensure_ascii=False)
    #for v in values[-12:]:
#       if v.isdigit():

#for p in d:
#   print(data[p]['theta'])
#   data['12']['theta2'] = d[12]
#   break
'''



'''
data = json.load(open('C:\\Users\\IM\\Desktop\\conf\\thomson\\temp.txt'))


d = dict()

for p in data:
    values = list(p.values())

    if len(values) == 15:
        N = int(values[0])
        values2 = [int(v) if v.isdigit() else 0 for v in values[-11:-2]]
        values2.append(float(values[-2][:-2]))
        ' '.join(map(str, values2))
    else:
        N = int(values[0])
        values2 = [int(v) if v.isdigit() else 0 for v in values[-10:-1]]
        values2.append(float(values[-1][:-2]))
        ' '.join(map(str, values2))
    
    dd = dict()
    dd['v3'] = values2[0]
    dd['v4'] = values2[1]
    dd['v5'] = values2[2]
    dd['v6'] = values2[3]
    dd['v7'] = values2[4]
    dd['v8'] = values2[5]
    dd['e'] = values2[6]
    dd['f3'] = values2[7]
    dd['f4'] = values2[8]
    dd['theta'] = values2[9]
    d[N] = dd

    print(dd)

with open('C:\\Users\\IM\\Desktop\\conf\\thomson\\temp2.txt', 'w') as f:
  json.dump(d, f, ensure_ascii=False)
    #for v in values[-12:]:
#       if v.isdigit():

    #break
'''


'''
f1 = open('C:\\Users\\IM\\Desktop\\conf\\thomson\\page.txt')
import re
import requests

f2 = open('C:\\Users\\IM\\Desktop\\conf\\thomson\\page2.txt', 'w')

s = set()
for l in f1:    
    for ll in re.findall(r'\d+\.xyz', l):
        s.add(ll)

for ll in s:
    #f2.write(ll + '\n')
    url = "http://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/xyz/" + ll
    response = requests.get(url, stream=True)

    with open('C:\\Users\\IM\\Desktop\\conf\\thomson\\sol1\\' + ll, "wb") as handle:
        for data in response.iter_content():
            handle.write(data)


        #'http://www-wales.ch.cam.ac.uk/~wales/CCD/Thomson/xyz/167.xyz'
'''        
