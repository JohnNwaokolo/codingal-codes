class employee :
    name= input("enter your name: ")

    def __init__(self):
      print ("Hi, my name is", self.name)
    
    def __del__(self):
        print("I have succesfully deleted the employee object")

ob = employee()
name = ob.name
del ob