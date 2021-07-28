import os


## 
def main():
    i =1
    
    for filename in os.listdir("bottle2"):
        dst = str(i)+".jpg"
        src = "bottle2/"+filename
        dst = "bottle2/"+dst
        os.rename(src,dst)
        
        i+=1

if __name__ == '__main__':
    main()