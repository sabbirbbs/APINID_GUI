#Config of Graphics driver
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatButton,MDRaisedButton
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.dialog import MDDialog
import datetime
import requests
from secret import api_key
import json


class ANIDApp(MDApp):

    def build(self):
        self.title = "APINID Project"
        screen = Screen()

        #Head title
        self.head = MDLabel(text='APINID Visual Implementation',font_style='H5',pos_hint={'center_x':0.5,'center_y':0.8},halign='center',theme_text_color='Custom',text_color=(0.5,0,0.5,1))
        #NID number input field
        self.nid = MDTextField(hint_text='Enter NID Number',input_filter='int',pos_hint={'center_x':0.5,'center_y':0.7},size_hint=(0.5,None))
        #NID verify button
        self.check = MDRoundFlatButton(text='Check',pos_hint={'center_x':0.5,'center_y':0.5})
        #Date picker
        self.date_field = MDRaisedButton(text='01/01/1991',pos_hint={'center_x':0.5,'center_y':0.6})
        #Binding key press function
        self.date_field.bind(on_press=self.show_date)
        self.check.bind(on_press=self.checknid)
        #Alert dialog
        self.dialog = MDDialog(text="The NID card is valid")
        

        #Adding elements to screen
        screen.add_widget(self.head)
        screen.add_widget(self.nid)
        screen.add_widget(self.check)
        screen.add_widget(self.date_field)

        return screen

    #Show date picker
    def show_date(self,instance):
        date_box = MDDatePicker()
        date_box.bind(on_save=self.get_date,on_cancel=self.on_cancel)
        date_box.open()

    #Get date value from picker when ok clicked
    def get_date(self,instance,value,date_range):
        self.date_field.text = str(value)
        self.current_date = str(value)

    #Dismiss date picker & save date value None
    def on_cancel(self,instance,value):
        self.current_date = None

    #Fucntion to be executed when NID check button clicked
    def checknid(self,instance):
        self.check.text = "Wait..."
        self.nid_data = self.gather_nidinfo('20006195209000074in','2000-12-27')
        #Showing result according to api returned data
        if self.nid_data['status'] in ['success','valid']:
            #Alert dialog
            self.dialog = MDDialog(text="The NID card is valid").open()
        else:
            #Alert dialog
            self.dialog = MDDialog(text="The NID card isn't valid").open()
            
        self.nid.text = ""
        self.current_date = None
        self.check.text = "Check Again"
        


    #Sending requests to NIDAPI to gather data
    def gather_nidinfo(self,nid,dob):
        try:
            response = requests.post(
                url = 'https://apinid.sabbirbbs.xyz/api/info',
                data = {
                    'nid': nid,
                    'dob': dob,
                    'secret': api_key
                }).text
            return json.loads(response)
        except Exception as error:
            return {'status':'error','data':error}

    

if __name__  == '__main__':
    ANIDApp().run()


