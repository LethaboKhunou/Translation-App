from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from googletrans import Translator
import speech_recognition as sr
import pyttsx3

class TranslationApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10)
        
        self.input_text = TextInput(hint_text='Speak or Enter text to translate')
        self.output_text = TextInput(hint_text='Translation will appear here', readonly=True)
        
        # Language dropdown menu
        self.language_dropdown = DropDown()
        languages = ['en', 'fr', 'es', 'de']  # Example languages, you can add more
        for lang in languages:
            btn = Button(text=lang, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.language_dropdown.select(btn.text))
            self.language_dropdown.add_widget(btn)
        self.language_button = Button(text='Select Language')
        self.language_button.bind(on_release=self.language_dropdown.open)
        self.language_dropdown.bind(on_select=lambda instance, x: setattr(self.language_button, 'text', x))
        
        translate_button = Button(text='Translate', on_press=self.translate_text)
        voice_translate_button = Button(text='Voice Translate', on_press=self.listen_for_voice_input)
        speak_button = Button(text='Speak Translation', on_press=self.speak_translation)
        
        layout.add_widget(self.input_text)
        layout.add_widget(self.output_text)
        layout.add_widget(self.language_button)
        layout.add_widget(translate_button)
        layout.add_widget(voice_translate_button)
        layout.add_widget(speak_button)
        
        return layout
    
    def translate_text(self, instance):
        text_to_translate = self.input_text.text
        target_language = self.language_button.text  # Get the selected target language
        
        if text_to_translate and target_language:
            translator = Translator()
            translation = translator.translate(text_to_translate, dest=target_language)
            self.output_text.text = translation.text
        else:
            self.output_text.text = "Please enter text and select target language"

    def listen_for_voice_input(self, instance):
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)  # Set timeout to 5 seconds
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            self.input_text.text = text
        except sr.WaitTimeoutError:
            print("Timeout. No speech detected.")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        else:
            self.translate_text(None)  # Start translation automatically if voice input is recognized

    def speak_translation(self, instance):
        translated_text = self.output_text.text
        if translated_text:
            engine = pyttsx3.init()
            engine.say(translated_text)
            engine.runAndWait()
        else:
            print("No translation available to speak.")

if __name__ == '__main__':
    TranslationApp().run()
