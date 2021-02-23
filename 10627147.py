import threading
import time
from multiprocessing import Process

def BubbleSort(arr):
    n = len( arr )
    for i in range( 0, n - 1 ):
        for j in range( i + 1, n ):
            if arr[i] > arr[j]:
                arr[i], arr[j] =arr[j], arr[i]
                
def Merge(a, p, q, r, a2, sort):
    for i in a2:
        a.append(i)
    stp1 = q - p + 1
    stp2 = r - q
    left = []
    right = []
    for i in range( stp1 ):
        left.append( a[p + i] )

    for j in range( stp2 ):
        right.append( a[q + j + 1] )
    i = j = 0
    for k in range( p, r + 1 ):
        if i < stp1 and j < stp2:
            if left[i] <= right[j]:
                a[k] = left[i]
                i += 1
            else:
                a[k] = right[j]
                j += 1
        elif i < stp1 and j >= stp2:
                a[k] = left[i]
                i += 1
        else:
            a[k] = right[j]
            j += 1
    sort.append(a)

        
def chunks(arr, k):
    tmp=[]
    arr=[int(x) for x in arr]
    n = int(len(arr)/ int(k))
    s=n*k
    for i in range(0, s, n):
        tmp.append(arr[i:i+n])
    if s!=0:
        for i in range(s, len(arr)):
            tmp[k-1].append(int(arr[i]))


    return tmp

def readfile():
    path = input()
    flag=True
    arr=[]
    options=[]
    with open(path) as f:
        for line in f.readlines():
  
            if line!='\n':
                if flag:
                    options.append(int(line[0]))
                    flag=False
                else:
                    flag=True
                    arr.append(line)
    all_arr=[]
    for i in arr:
        i=i.split()
        tmp=[]
        for m in i:
            tmp.append(int(m))
        all_arr.append(tmp)
    return options, all_arr, path


arr=[]
options, arr, fname=readfile()
j=0
file=open('output_'+fname,'w')

for i in options:
    if i!=1:
        cut=int(input('切成幾份:'))
    if i==1:
        tStart = time.time()
        BubbleSort(arr[j])
        tEnd = time.time()
        print('sorted:')
        for x in arr[j]:
            print(x,end=' ')
        print('\n'+'CPU time:',tEnd - tStart)
        file.writelines('sorted:'+'\n'+' '.join([str(x) for x in arr[j]])+"\n")
        file.writelines('CPU time:'+str(tEnd - tStart)+"\n")
    elif i==2:
        arrlist=chunks(arr[j], cut)
        threads = []
        sort=[]
        tStart = time.time()
        for m in range(cut):
            threads.append(threading.Thread(target = BubbleSort(arrlist[m]), args = (m,)))
            threads[m].start()
        for m in range(cut):
            threads[m].join()

        while len(arrlist)!=1:
            threads = []
            for m in range(0,len(arrlist),2):
                if m==len(arrlist)-1:
                    sort.append(arrlist[m])
                else:
                    threads.append(threading.Thread(target = Merge(arrlist[m], 0, len(arrlist[m])-1,len(arrlist[m+1])+len(arrlist[m])-1,arrlist[m+1],sort), args = (m,)))
                    threads[len(threads)-1].start()                    
          
            for m in range(0,len(threads)):
                threads[m].join()
                arrlist=sort
                sort=[]
                break
            
        tEnd = time.time()
        print('sorted:')
        for x in arrlist[0]:
            print(x,end=' ')
        file.writelines('sorted:'+'\n'+' '.join([str(x) for x in arrlist[0]])+"\n")

        print('\n'+'CPU time:',tEnd - tStart)
        file.writelines('CPU time:'+str(tEnd - tStart)+"\n")   
    elif i==3:
        arrlist=chunks(arr[j], cut)
        processes = []
        sort=[]
        tStart = time.time()
        for m in range(cut):
            processes.append(Process(target = BubbleSort(arrlist[m]), args = (m,)))
            processes[m].start()
        for m in range(cut):
            processes[m].join()

        while len(arrlist)!=1:
            processes = []
            for m in range(0,len(arrlist),2):
                if m==len(arrlist)-1:
                    sort.append(arrlist[m])
                else:
                    processes.append(Process(target = Merge(arrlist[m], 0, len(arrlist[m])-1,len(arrlist[m+1])+len(arrlist[m])-1,arrlist[m+1],sort), args = (m,)))
                    processes[len(processes)-1].start()                    
          
            for m in range(0,len(processes)):
                processes[m].join()
                arrlist=sort
                sort=[]
                break
        tEnd = time.time()
        print('sorted:')
        for x in arrlist[0]:
            print(x,end=' ')
        file.writelines('sorted:'+'\n'+' '.join([str(x) for x in arrlist[0]])+"\n")
        print('\n'+'CPU time:',tEnd - tStart)
        file.writelines('CPU time:'+str(tEnd - tStart)+"\n") 
    elif i==4:
        sort=[]
        arrlist=chunks(arr[j], cut)
        tStart = time.time()
        p_one = Process(target=BubbleSort(arrlist[0]))
        p_one.start()
        for m in range(1,cut):
            p_one.join()
            p_one.target=BubbleSort(arrlist[m])
        p_one.join()
        
        while len(arrlist)!=1:
            for m in range(0,len(arrlist),2):
                if m==len(arrlist)-1:
                    sort.append(arrlist[m])
                else:
                    p_one.target = Merge(arrlist[m], 0, len(arrlist[m])-1,len(arrlist[m+1])+len(arrlist[m])-1,arrlist[m+1],sort)

            p_one.join()
            arrlist=sort
            sort=[]
        tEnd = time.time()
        print('sorted:')
        for x in arrlist[0]:
            print(x,end=' ')
        file.writelines('sorted:'+'\n'+' '.join([str(x) for x in arrlist[0]])+"\n")
        print('\n'+'CPU time:',tEnd - tStart)
        file.writelines('CPU time:'+str(tEnd - tStart)+"\n")           
    else:
        print('error option')
    j+=1
file.close()





