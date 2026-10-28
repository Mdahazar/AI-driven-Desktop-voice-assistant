import speech_recognition as sr
import pyttsx3
import time

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.microphone = None
        self.mic_available = False
        
        # Configure TTS
        voices = self.tts_engine.getProperty('voices')
        if len(voices) > 1:
            self.tts_engine.setProperty('voice', voices[1].id)
        self.tts_engine.setProperty('rate', 160)
        self.tts_engine.setProperty('volume', 0.8)
        
        self._setup_microphone()
    
    def _setup_microphone(self):
        """Setup microphone"""
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            self.mic_available = True
            print("✅ Microphone ready!")
        except Exception as e:
            print(f"❌ Microphone setup failed: {e}")
            self.mic_available = False
    
    def listen(self):
        """Listen for voice input"""
        if not self.mic_available:
            return self._get_text_input()
        
        try:
            print("\n🎤 Listening...", end="", flush=True)
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=6)
            
            print(" processing...", end="", flush=True)
            text = self.recognizer.recognize_google(audio).lower()
            print(f" heard: '{text}'")
            return text
            
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            print(" couldn't understand")
            return ""
        except Exception as e:
            print(f" error: {e}")
            return self._get_text_input()
    
    def _get_text_input(self):
        """Fallback to text input"""
        try:
            text = input("\n💬 Type command: ").strip()
            return text.lower() if text else ""
        except:
            return "exit"
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"🗣️ Sara: {text}")
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"⚠️ TTS Error: {e}")
    
    def is_wake_word(self, text):
        """Check for wake word"""
        if not text:
            return False
            
        wake_words = ['sara', 'sarah', 'sera', 'serah', 'sira']
        phrases = ['hi sara', 'hey sara', 'hello sara', 'okay sara', 'wake up']
        
        text_lower = text.lower()
        for phrase in phrases:
            if phrase in text_lower:
                return True
        for word in wake_words:
            if word in text_lower:
                return True
        return False
    
    def is_exit_command(self, text):
        """Check exit commands - ONLY exact match for 'sara exit'"""
        if not text:
            return False
        
        text_lower = text.lower().strip()
        return text_lower == 'sara exit'
    
    def is_sleep_command(self, text):
        """Check sleep commands"""
        if not text:
            return False
        sleep_commands = ['bye', 'goodbye', 'see you', 'sleep', 'go to sleep']
        return any(cmd in text.lower() for cmd in sleep_commands)