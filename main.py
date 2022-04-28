import speech_recognition as sr    
import pyttsx3                     
import multiprocessing
import datetime                    
import pyjokes                     
import keyboard                    

from tkinter import * 
from PIL import Image, ImageTk
from playsound import playsound    

class VoiceAssist:
    '''
    Created for UZH HCI project as a demo for the Dina personal assistant.
    Started from https://www.instructables.com/How-to-Make-a-GUI-Virtual-Assistant/
    '''
    def __init__(self):
        self.name_file = open("user_name", "r")
        self.assistant_name = "Dina"
        self.user_name = self.name_file.read()

        self.engine = pyttsx3.init('sapi5')  
        self.engine.setProperty("rate", 180)
        voices = self.engine.getProperty('voices') 
        self.engine.setProperty('voice', voices[2].id)

        self.is_listening = False

        self.init_sounds()

        self.main_screen()

    def init_sounds(self):
        self.rain = multiprocessing.Process(target=playsound, args=("rain_sounds.wav",))
        self.meditate = multiprocessing.Process(target=playsound, args=("meditation.wav",))
        self.lullaby = multiprocessing.Process(target=playsound, args=("lullaby.wav",))
        self.story = multiprocessing.Process(target=playsound, args=("dino_story.wav",))
    
    def speak(self, text):
        self.engine.say(text)
        print(self.assistant_name + " : "  +  text)
        self.engine.runAndWait() 

    def greet_me(self):
        hour=datetime.datetime.now().hour

        if hour >= 0 and hour < 12:
            self.speak("Hello, Good Morning " + self.user_name)
        elif hour >= 12 and hour < 18:
            self.speak("Hello, Good Afternoon " + self.user_name)
        else:
            self.speak("Hello, Good Evening " + self.user_name)
        
        self.speak("How can I help you?")

    def get_audio(self): 
        r = sr.Recognizer() 
        audio = '' 
        text = ''

        with sr.Microphone() as source: 
            playsound("assistant_on.wav")
            print("Listening")
            self.label1.configure(image = self.img_2)
            self.label1.image = self.img_2 # keep a reference!
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, phrase_time_limit = 3) 
            playsound("assistant_off.wav")
            print("Done listening.") 
        try:
            text = r.recognize_google(audio, language ='en-US') 
            print('You: ' + ': ' + text)

        except Exception:
            pass
        
        self.label1.configure(image = self.img)
        self.label1.image = self.img # keep a reference!
        return text
            
    def date(self):
        now = datetime.datetime.now()
        month_name = now.month
        day_name = now.day
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        ordinalnames = [ '1st', '2nd', '3rd', ' 4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd','24rd', '25th', '26th', '27th', '28th', '29th', '30th', '31st'] 

        self.speak("Today is "+ month_names[month_name-1] +" " + ordinalnames[day_name-1] + '.')

    def play_sound(self, sound):
        if sound == "lullaby":
            self.lullaby.start()
        elif sound == "meditation":
            self.meditate.start()
        elif sound == "rain":
            self.rain.start()
        elif sound == "story":
            self.story.start()

    def stop_sound(self):
        for proc in [self.lullaby, self.meditate, self.rain, self.story]:
            try:
                proc.terminate()
                print("Stopping sounds")
                self.speak("Ok Stopping sound!")
            except:
                pass
        
        # Reinit sounds
        self.init_sounds()

    def process_audio(self):
        run = 1
        while run==1: 
            statement = self.get_audio().lower()
            results = ''
            run += 1

            if "hello" in statement or "hi" in statement or "hey" in statement:
                self.greet_me()               

            elif "goodbye" in statement or "shutdown" in statement or "turn off" in statement:
                self.speak('Your personal assistant demo is shutting down, have a nice day')
                screen.destroy()

            elif 'joke' in statement:
                self.speak(pyjokes.get_joke())  

            elif 'play rain' in statement:
                self.speak("I'm going to play soothing rain sounds")
                self.play_sound('rain')

            elif 'play lullaby' in statement:
                self.speak("Playing a sweet lullaby for your baby")
                self.play_sound('lullaby')
            
            elif 'play story' in statement:
                self.speak("Playing a story for your baby")
                self.play_sound('story')

            elif 'play meditation' in statement:
                self.speak("I hope this meditation helps you relax!")
                self.play_sound('meditation')
            
            elif 'night mode' in statement:
                self.speak("Goodnight " + self.user_name + " sleep well I will listen for \
                    your baby and alert you based on your settings")
            
            elif 'nap mode' in statement:
                self.speak("Nap time! When I hear your baby wake up I can give you tips on \
                    sleep training based on your settings")

            elif 'time' in statement:
                strTime=datetime.datetime.now().strftime("%H:%M:%S")
                self.speak(f"the time is {strTime}")

            elif 'date' in statement or 'day' in statement:
                self.date()

            elif 'who are you' in statement or 'what can you do' in statement:
                self.speak('I am ' + self.assistant_name + ' your personal assistant. I am programmed to help you and your baby have higher quality sleep.') 

            elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
                self.speak("I was built by Mommify")

            elif statement == "":
                self.speak("Sorry I didn't catch that, can you repeat it?")
            
            elif statement == "stop sounds":
                self.speak("Ok stopping the sounds now!")
            
            else:
                self.speak("I don't know that yet, but I'm still learning")
            
            self.speak(results)

    def change_name(self):
        name_info = name.get()
        file=open("user_name", "w")
        file.write(name_info)
        file.close()
        settings_screen.destroy()
        screen.destroy()

    def change_name_window(self):
        global settings_screen
        global name
        settings_screen = Toplevel(screen)
        settings_screen.title("Settings")
        settings_screen.geometry("300x300")
        settings_screen.iconbitmap('app_icon.ico')
    
        name = StringVar()

        current_label = Label(settings_screen, text = "Your name: "+ self.user_name)
        current_label.pack()

        enter_label = Label(settings_screen, text = "To change the name please enter a new name below.") 
        enter_label.pack(pady=10)   
        
        Name_label = Label(settings_screen, text = "Name")
        Name_label.pack(pady=10)
        
        name_entry = Entry(settings_screen, textvariable = name)
        name_entry.pack()

        change_name_button = Button(settings_screen, text = "Ok", width = 10, height = 1, command = self.change_name)
        change_name_button.pack(pady=10)

    def info(self):
        info_screen = Toplevel(screen)
        info_screen.title("Info")

        creator_label = Label(info_screen,text = "Momify")
        creator_label.pack()

    def main_screen(self):
        if __name__ == '__main__':
            global screen
            screen = Tk()
            screen.title(self.assistant_name)
            screen.geometry("500x500")
            
            icon = Image.open("bear_icon.png")
            icon = ImageTk.PhotoImage(icon)
            screen.iconphoto(False, icon)

            name_label = Label(text = f"Momify Dina Demo", width = 300, font = ("Calibri", 13))
            name_label.pack()

            image = Image.open("bear.png")
            resize_image = image.resize((450, 450))

            image_2 = Image.open("bear_listening.png")
            resize_image_2 = image_2.resize((450, 450))

            self.img = ImageTk.PhotoImage(resize_image)
            self.img_2 = ImageTk.PhotoImage(resize_image_2)

            self.label1 = Label(image=self.img)
            self.label1.image = self.img
            self.label1.pack()

            button_img = Image.open("bear_icon.png")
            resize_button_img = button_img.resize((50, 40))
            resize_button_img = ImageTk.PhotoImage(resize_button_img)
            microphone_button = Button(image=resize_button_img, command = self.process_audio)
            microphone_button.pack(pady=10)

            settings_photo = PhotoImage(file = "settings.png")
            settings_button = Button(image=settings_photo, command = self.change_name_window)
            settings_button.pack(pady=10)
            
            info_button = Button(text ="Info", command = self.info)
            info_button.pack(pady=10)

            # keyboard shortcuts to start listening for audio
            keyboard.add_hotkey("l", self.process_audio)

            # keyboard shortcut to stop sounds playing
            keyboard.add_hotkey("enter", self.stop_sound)

            screen.mainloop()


try:
    start = VoiceAssist()
except Exception as e:
    print(e)