from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatButton,MDRaisedButton,MDFillRoundFlatButton
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import AsyncImage
from kivy.core.text import LabelBase
import datetime
import requests
from secret import api_key
import json
import converter

#Unicode to Bijoy converter
def u2a(string):
    uniconverter = converter.Unicode()
    return uniconverter.convertUnicodeToBijoy(string)



#Installing custom fonts
LabelBase.register(name='Sutonny',fn_regular='SutonnyMJ.ttf')

class ANID(MDApp):

    def build(self):
        self.title = "APINID Project"
        self.screen = Screen()
        #Private variables
        self.current_date = None
    
        #Head title
        self.head = MDLabel(text='APINID Visual Implementation',font_style='H5',pos_hint={'center_x':0.5,'center_y':0.9},bold=True,halign='center',theme_text_color='Custom',text_color='#2e8b57')
        #NID number input field
        self.nid = MDTextField(hint_text='Enter NID Number',input_filter='int',pos_hint={'center_x':0.5,'center_y':0.8},size_hint=(0.8,None))
        #NID verify button
        self.check = MDRoundFlatButton(text='Check',pos_hint={'center_x':0.5,'center_y':0.6},size_hint=(0.5,None))
        #Date picker
        self.date_field = MDTextField(hint_text='Select date of birth(yyyy-mm-dd)',pos_hint={'center_x':0.5,'center_y':0.7},size_hint=(0.8,None))
        self.photo_label = MDLabel(text='Photo of the card holder.',halign='center',pos_hint={'center_x':0.5,'center_y':0.5})
        #Image Insert
        self.web_image = AsyncImage(source='https://www.w3schools.com/tags/img_girl.jpg',pos_hint={'center_x':0.5,'center_y':0.3},size_hint=(0.3,0.3))
        #Card Holder Name
        self.holder_name = MDFillRoundFlatButton(text='',font_name='Sutonny',pos_hint={'center_x':0.5,'center_y':0.1})
        #Credit
        self.credit_text = MDLabel(text='Developed by Sabbirbbs',halign='center',pos_hint={'center_x':0.5,'center_y':0.04})
        #Binding key press function
        self.check.bind(on_press=self.checknid)
        #Alert dialog
        self.dialog = MDDialog(text="The NID card is valid")
        

        #Adding elements to screen
        self.screen.add_widget(self.head)
        self.screen.add_widget(self.nid)
        self.screen.add_widget(self.check)
        self.screen.add_widget(self.date_field)

        return self.screen

    #Fucntion to be executed when NID check button clicked
    def checknid(self,instance):
        self.current_date = self.date_field.text
        if self.current_date and self.nid.text:
            self.check.text = "Wait..."
            self.screen.remove_widget(self.photo_label)
            self.screen.remove_widget(self.web_image)
            self.screen.remove_widget(self.holder_name)
            self.screen.remove_widget(self.credit_text)
            self.nid_number = self.nid.text
            self.dob = self.date_field.text
            self.nid_data = self.gather_nidinfo(self.nid_number,self.dob)
            #Showing result according to api returned data
            if self.nid_data['status'] == 'success':
                self.web_image.source = self.nid_data['data']['photo']
                self.holder_name.text = u2a(self.nid_data['data']['name'])
                self.screen.add_widget(self.photo_label)
                self.screen.add_widget(self.web_image)
                self.screen.add_widget(self.holder_name)
                self.screen.add_widget(self.credit_text)
            elif self.nid_data['status'] == 'valid':
                #Alert dialog
                self.dialog = MDDialog(text='The NID Card is valid but unable to fetch data.').open()            
            else:
                #Alert dialog
                self.dialog = MDDialog(text=str(self.nid_data['data'])).open()
                
            self.nid.text = ""
            self.current_date = None
            self.check.text = "Check Another"
            self.date_field.text = ""
        else:
            self.dialog = MDDialog(text="You must enter NID number & select DOB.").open()
        


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
            return {'status':'error','data':'It\'s seems you entered invalid NID data.'}

    

ANID().run()


