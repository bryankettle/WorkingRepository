import json
import os

url = r"H:\work test\AI_output\settings.json"

dict = {"settings": 
{
    "check": 1,
    "Help": 2,
    "me": 3,
}
}



class Json:
    def __init__(self, file_location):
        self.file_location = file_location
        if os.path.isfile(file_location):
            try:
                print("Json detected. Loading file.")
                with open(file_location, "r") as read_file:
                    self.database = json.load(read_file)
            except:
                print("loading failed. Check the settings.json file")
                exit()
        else:
            print("Json not detected. Creating file.")
            try:
                folderDir = file_location.split("\\")[:-1]
                folderDir = "\\".join(folderDir)

                if not os.path.isdir(folderDir):
                    os.makedirs(folderDir)
                
                with open(self.file_location, "w") as write_file:
                    json.dump({}, write_file, sort_keys = True, indent = 4)
            except:
                print("Failed to create Json. Please check if the folder is accessible")

    def write_file(self,data):
        try:
            print("Writing to database.")
            with open(self.file_location, "r") as read_file:
                self.database = json.load(read_file)

            #self.database.update(data)
            #self.database["settings"].append(data) = ... write code here
            

            with open(self.file_location, "w") as write_file:
                json.dump(self.database, write_file, sort_keys = True, indent = 4)
        except:
            print("failed to write to the database.")


    def write_file(self,data, key):
        try:
            print("Writing to database.")
            with open(self.file_location, "r") as read_file:
                self.database = json.load(read_file)

            #self.database[key[0]][key[1]] = ... write code here

            with open(self.file_location, "w") as write_file:
                json.dump(self.database, write_file, sort_keys = True, indent = 4)

        except:
            print("failed to write to the database.")





   


class Check:
    def __init__(self, url):
        self.time_stamp = 0
        self.filename = url

    def folder(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self.time_stamp:
            self.time_stamp = stamp
            return True
            # File has changed, so do something...


'''

with open(url) as json_file:

with open("data_file.json", "w") as write_file:
    json.dump(data, write_file)
'''