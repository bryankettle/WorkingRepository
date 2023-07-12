import json
import shutil
from multiprocessing import Process,Lock
import os.path
import time
url = r"H:\work test\AI_output"
json_Location = url + "\\" + "test.json"



def process(file_lock,jsonss,data):
    for i, dat in enumerate(data):
        #time.sleep(2.25)
        with file_lock:
            print("lock obtained by process")
            jsonss.save_file(i + 1, "Banana","name")

class rawr:
    def __init__(self,json_Location):
        self.json_Location = json_Location
        self.datas = self.read_file()

    def read_file(self):
        with open(self.json_Location) as user_file:
            self.datas = json.loads(user_file.read())
            return self.datas

    def save_file(self,id,name,Pass):
        self.read_file()
        for data in self.datas:
            #print(data)
            #print(name)
            #print(Pass)
            if(data["id"] == id):
                data[Pass] = name

        with open(json_Location,"w") as user_file:
            json_object = json.dumps(self.datas, indent=4)
            user_file.write(json_object)

if __name__ == '__main__':
    file_lock = Lock()
    
    if(os.path.exists(json_Location)):
        jsonss = rawr(json_Location)
        data = jsonss.read_file()
        
    
    else:
        print("no json")
        data = []
        for i in range(1,100):
            file_contents = {
                "name": f"sathiyajith{i}",
                "id": i,
                "truth": True,
            }
            data.append(file_contents)
        with open(json_Location,"w") as user_file:
            json_object = json.dumps(data, indent=4)
            user_file.write(json_object)
            exit()
    
    p = Process(target=process, args=(file_lock,jsonss,data,))
    p.start()

    while True:
        for i, dat in enumerate(data):
            #time.sleep(1)
            with file_lock:
                print("lock obtained by main")
                jsonss.save_file(i+1,False,"truth")
            #file_lock.release()
            

        p.join()
        break
        
        

    

#conda activate yolov7
#cd /d "H:\work test"
