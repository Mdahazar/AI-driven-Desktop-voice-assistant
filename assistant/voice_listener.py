import speech_recognition as sr
import threading

class VoiceListener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self._adjust_for_ambient_noise()
        
    def _adjust_for_ambient_noise(self):
        """Adjust the recognizer for ambient noise"""
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("Ambient noise adjustment complete.")
    
    def listen(self):
        """Listen for voice input and return transcribed text"""
        try:
            with self.microphone as source:
                print("\n🎤 Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("🔄 Processing...")
            text = self.recognizer.recognize_google(audio).lower()
            return text
            
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None