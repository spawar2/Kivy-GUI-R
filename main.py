from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase



class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen): 
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def analysis(self):
        sm.current = "login"

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created
        '''
        import cv2
        import matplotlib.pyplot as plt
        import cvlib as cv
        import os
        from cvlib.object_detection import draw_bbox
        import numpy as np
        import time
        os.chdir('/Users/yalegenomecenter/Desktop/vehicle_counting_tensorflow-master/Revision 03_08_2020/images')
        vid = cv2.VideoCapture('/Users/yalegenomecenter/Desktop/vehicle_counting_tensorflow-master/Revision 03_08_2020/images/Road traffic video for object recognition.mp4')
        index = 0
        while(True):
            ret, frame = vid.read()
            if not ret: 
                break
                print('Video ended unexpectedly..')
            name2 = 'frame' + str(index) + '.jpg'
            print ('Creating...' + name2)
            cv2.imwrite(name2, frame)
            print(name2)    
            im = cv2.imread(name2)
            bbox, label, conf = cv.detect_common_objects(im)
            output_image = draw_bbox(im, bbox, label, conf)
            print('Number of cars in the image is '+ str(label.count('car')))
            print('Number of trains in the image is '+ str(label.count('train')))
            print('Number of trucks in the image is '+ str(label.count('truck')))
            car = str(label.count('car'))
            train = str(label.count('train'))
            truck = str(label.count('truck'))
            total = [int(car),int(train),int(truck)]
            print('Total number of cars parked is ' + str(sum(total)))
            #cv2.imshow("Frame", output_image)
            cv2.waitKey(200)
            index += 1
            time.sleep(15)
            for file in os.listdir('.'):
                if file.endswith('.jpg'):
                    os.remove(file) 
            '''
class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(name="create"),MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
