#Config of Graphics driver
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatButton,MDRaisedButton,MDFillRoundFlatButton
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import AsyncImage
from kivy.core.text import LabelBase
from kivy.lang import Builder
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
LabelBase.register(name='Kalpurush_ANSI',fn_regular='fonts/kalpurush ANSI.ttf')
LabelBase.register(name='Shonar',fn_regular='fonts/Shonarb.ttf')
LabelBase.register(name='Vrinda',fn_regular='fonts/vrindab.ttf')
LabelBase.register(name='Kalpurush',fn_regular='fonts/kalpurush.ttf')

Image = """
Image:
    id: 'user_photo'
    source: 'favicon.ico'
    pos_hint: {'center_x':0.5,'center_y':0.3}
"""

class ANIDApp(MDApp):

    def build(self):
        self.title = "APINID Project"
        self.screen = Screen()

        #Head title
        self.head = MDLabel(text='APINID Visual Implementation',font_style='H5',pos_hint={'center_x':0.5,'center_y':0.9},bold=True,halign='center',theme_text_color='Custom',text_color='#2e8b57')
        #NID number input field
        self.nid = MDTextField(hint_text='Enter NID Number',input_filter='int',pos_hint={'center_x':0.5,'center_y':0.8},size_hint=(0.8,None))
        #NID verify button
        self.check = MDRoundFlatButton(text='Check',pos_hint={'center_x':0.5,'center_y':0.6})
        #Date picker
        self.date_field = MDRaisedButton(text='01/01/1991',pos_hint={'center_x':0.5,'center_y':0.7})
        self.photo_label = MDLabel(text='Photo of the card holder.',halign='center',pos_hint={'center_x':0.5,'center_y':0.5})
        #Image Insert
        #self.nid_photo = Builder.load_string(Image)
        self.web_image = AsyncImage(source='https://www.w3schools.com/tags/img_girl.jpg',pos_hint={'center_x':0.5,'center_y':0.3},size_hint=(0.3,0.3))
        #Card Holder Name
        self.holder_name = MDFillRoundFlatButton(text='',font_name='Kalpurush_ANSI',pos_hint={'center_x':0.5,'center_y':0.1})
        #Binding key press function
        self.date_field.bind(on_press=self.show_date)
        self.check.bind(on_press=self.checknid)
        #Alert dialog
        self.dialog = MDDialog(text="The NID card is valid")
        

        #Adding elements to screen
        self.screen.add_widget(self.head)
        self.screen.add_widget(self.nid)
        self.screen.add_widget(self.check)
        self.screen.add_widget(self.date_field)

        return self.screen

    #Show date picker
    def show_date(self,instance):
        date_box = MDDatePicker()
        date_box.bind(on_save=self.get_date,on_cancel=self.on_cancel)
        date_box.open()

    #Get date value from picker when ok clicked
    def get_date(self,instance,value,date_range):
        self.date_field.text = str(value)
        self.current_date = value

    #Dismiss date picker & save date value None
    def on_cancel(self,instance,value):
        self.current_date = None

    #Fucntion to be executed when NID check button clicked
    def checknid(self,instance):
        self.check.text = "Wait..."
        self.screen.remove_widget(self.photo_label)
        self.screen.remove_widget(self.web_image)
        self.screen.remove_widget(self.holder_name)
        self.nid_number = self.nid.text
        self.dob = f"{self.current_date.year}-{self.current_date.month}-{self.current_date.day}"
        self.nid_data = self.gather_nidinfo(self.nid_number,self.dob)
        print(str(self.nid_number)+str(self.dob))
        #Showing result according to api returned data
        if self.nid_data['status'] == 'success':
            self.web_image.source = self.nid_data['data']['photo']
            self.holder_name.text = u2a(self.nid_data['data']['name'])
            self.screen.add_widget(self.photo_label)
            self.screen.add_widget(self.web_image)
            self.screen.add_widget(self.holder_name)
        elif self.nid_data['status'] == 'valid':
            #Alert dialog
            self.dialog = MDDialog(text='The NID Card is valid but unable to fetch data.').open()            
        else:
            #Alert dialog
            self.dialog = MDDialog(text=str(self.nid_data['data'])).open()
            
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
            return {'status':'error','data':'Something went wrong.'}

    

if __name__  == '__main__':
    ANIDApp().run()


