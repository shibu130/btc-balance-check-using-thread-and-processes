import multiprocessing
from threading import Thread,current_thread

from time import perf_counter,sleep
import requests
from requests.exceptions import *
from  json.decoder import JSONDecodeError
#result
file_pointer=open("result.txt","a")

def balance(address):
    
    try:
        flag=0
        returnString=""
        api="https://chain.api.btc.com/v3/address/"
        # api2=""
        bal=requests.get(api+address, headers={"content-type":"application/json","Cookie":"acw_tc=0bc1a14415876248535402530e2d1b397e6e522345b9cad7922f886f7198eb"
        ,"Cache-Control":"no-cache","User-Agent":"User-Agent","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Connection":"keep-alive"}).json()['data']['balance']
        if(bal>0 or float(bal)>0):
        # print(True)
            # print(address+" has "+str(bal))
            bal=str(float(bal))

        
        # exit(0)
        else:
            # print(address+" has no balance")
            bal=0
    except JSONDecodeError:
                    print("address doesnt exist")
                    bal=0

    except Timeout :
                    #connection timed out 
                    bal=0
                    print("connection timeout")
    except ConnectionError:
                    bal=' connection error'
                    # dns failure connection refused
                    print("connection error")
    
    # if(flag==0):
    #     returnString=address+"="+str(float(bal))
    # else:
    #     returnString=address+"="+"didntwork"
    returnString=address+"="+str(bal)
    return returnString
   




def read_thread(q,fq):
    j=0
    with open("cain.txt","r") as  filep:
        for i in filep:
                # sleep(5)

               print("pushing {} item into queue".format(i.strip()))
               q.put(i.strip())
        else:
            
            q.put(None)#c1
            # sleep(1)
            q.put(None)#c2
            q.put(None) #c3
           
            
            q.put(None) #c4

            fq.put(None) #thread which does file write
            # q.put(None)
  




def consume(q,filewriteQueue):
    while(True):
        try:
            item=q.get()
            
            if(item==None):
                print(multiprocessing.current_process().name+" exited")
                break

            #balance api call'
            # balance("3")
            print(item.split("=")[0])
            
            rt=balance(item.split("=")[0]) #return item

            print(rt)

            



            print("process "+multiprocessing.current_process().name+" consumed "+item)

            filewriteQueue.put(rt)
            # print(filewriteQueue)

            print(rt+" added to the file write que")
            # sleep(5)

        except Exception:
                         
                         print("the api is returning null which is being written")



def read_and_write(fileQueue):
    while(True):
        item=fileQueue.get()

        if(item==None):
            print(current_thread().name+ " exited")
            break

        file_pointer.writelines(item+"\n")



               


if __name__ == "__main__":
    qu=multiprocessing.Queue(maxsize=5) #from file thread puts the line into the queue

    filewriteQueue=multiprocessing.Queue(maxsize=5) # queue for writing from file

    # file_pointer=open("brain-r.txt","w")


    P=Thread(name='p',target=read_thread,args=(qu,filewriteQueue)) #the thread i was refering to
    P.start()
 
    
    start=perf_counter() #just calaculate time
    C1=multiprocessing.Process(name='c1',target=consume,args=(qu,filewriteQueue,))
    C1.start()

    C2=multiprocessing.Process(name='c2',target=consume,args=(qu,filewriteQueue,))
    C2.start()

    C3=multiprocessing.Process(name='c3',target=consume,args=(qu,filewriteQueue,))
    C3.start()

    C4=multiprocessing.Process(name='c4',target=consume,args=(qu,filewriteQueue,))
    C4.start()

    filewriteThread=Thread(name='writerthread',target=read_and_write(filewriteQueue,))
    filewriteThread.start()
    # C4=Thread(name='filequeue',target=write_to_file,args=(filewriteQueue,file_pointer,))
    # C4.start()

    P.join()
    C1.join()
    C2.join()
    C3.join()
    C4.join()
    # qu.join()
    # filewriteQueue.join()
    print(P.is_alive())
    print(C1.is_alive())
    print(C2.is_alive())
    print(C3.is_alive())

    end=perf_counter()

    print(end-start)
    
