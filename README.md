# btc-balance-check-using-thread-and-processes
This code check the btc balance concurrently from api , basically here a thread read a file and puts it to a queue then we have processes which will use the api to return the balance and then put it to another queue and a thread will be writing the results to another file in the format "address=balance"

I think batching multiple addresses will be good instead of each query considering all the api's have rate limits

u may consider using my other webscraper instead of this

note: be carefull to add timeout or else you will be banned from some api 

issues : memory leak







