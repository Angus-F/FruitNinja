
#!/usr/bin/python
#coding=utf-8
import random 
import time
    
def main(pos):
    index=1000
    while index>0:
        index-=1
        time.sleep(0.1)
        print('subprocess',pos[0])

if __name__ == '__main__':
    main()