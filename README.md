# btc-balance-check-using-thread-and-processes
This code check the btc balance concurrently from api , basically here a thread read a file and puts it to a queue then we have processes which will use the api to return the balance and then put it to another queue and a thread will be writing the results to another file in the format "address=balance"




any tip is appreciated



