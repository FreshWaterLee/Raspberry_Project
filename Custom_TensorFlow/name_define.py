import os


## 
def main():
    i =1
    dirn = 'Tumbler'
    for filename in os.listdir(dirn):
        dst = str(i)+".jpg"
        src = dirn+"/"+filename
        dst = dirn+"/"+dst
        os.rename(src,dst)
        
        i+=1

if __name__ == '__main__':
    main()