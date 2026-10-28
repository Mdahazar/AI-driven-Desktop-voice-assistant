import threading
import time
from voice_engine import VoiceEngine
from popup_gui import SaraPopup
from system_monitor import SystemMonitor
from web_search import WebSearch
from file_manager import FileManager
from reminder_system import ReminderSystem
from email_sender import EmailSender
from music_player import MusicPlayer
from note_taker import NoteTaker
from whatsapp_sender import WhatsAppSender
import sys
from datetime import datetime
import re
import requests
import json

class SaraAssistant:
    def __init__(self):
        print("🚀 Starting Sara AI Assistant...")
        self.voice_engine = VoiceEngine()
        self.popup = SaraPopup()
        self.system_monitor = SystemMonitor()
        self.web_search = WebSearch()
        self.file_manager = FileManager()
        self.reminder_system = ReminderSystem()
        self.email_sender = EmailSender()
        self.music_player = MusicPlayer("E:\\sara-data\\music")
        self.note_taker = NoteTaker("E:\\sara-data")
        self.whatsapp_sender = WhatsAppSender()
        self.running = True
        self.assistant_active = False
        self.search_mode_active = False
        self.commands_list = self._get_commands_list()
    
    def _get_commands_list(self):
        """Return list of all available commands"""
        return """
🎯 AVAILABLE COMMANDS:

🤖 BASIC:
• "Hi Sara" / "Hello Sara" - Wake up
• "Bye" / "Goodbye" - Sleep (minimizes)
• "Sara exit" - Shutdown
• "What can you do?" - Help
• "Sara activate search" - AI Search Mode (DeepSeek)

🧮 MATH CALCULATIONS:
• "Calculate 15 + 20" - Basic math
• "What is 100 minus 25" - Subtraction  
• "How much is 8 times 7" - Multiplication
• "Solve 50 divided by 2" - Division
• "15 plus 20" / "30 minus 10" - Quick math
• "8 times 9" / "100 divided by 4" - Operations
• "2 into 5" / "2 x 5" / "2 multiply 5" - Multiplication

🕒 TIME:
• "What time is it?" - Current time
• "What's today's date?" - Current date

💻 SYSTEM:
• "System info" - System information
• "Battery status" - Battery level
• "Storage info" - Disk usage

🌐 WEB & YOUTUBE:
• "Search Wikipedia [topic]" - Wikipedia search
• "Search web [query]" - Web search
• "Youtube [song/video]" - Play on YouTube
• "Watch [video]" - Play on YouTube
• "Video [name]" - Play on YouTube

📱 WHATSAPP:
• "Send message" - Send WhatsApp message
• "Send message to [name]" - Quick send
• "Add contact [name] number [number]" - Save contact
• "List contacts" - Show saved contacts

📁 FILES:
• "Open [app]" - Open application
• "Open folder [name]" - Open folder
• "Close [app]" - Close application
• "Take screenshot" - Capture screen

💡 BRIGHTNESS:
• "Brightness up" - Increase brightness
• "Brightness down" - Decrease brightness
• "Set brightness to [number]" - Set level

📝 NOTES:
• "Write note" - Start recording
• "Save note" - Save note
• "List notes" - Show notes

⏰ REMINDERS:
• "Set reminder [message] in [X] minutes" - Set reminder

🎵 MUSIC:
• "Play music" - Play from collection
• "Stop music" - Stop music
• "Volume up/down" - Adjust volume
        """
    
    def _query_deepseek(self, prompt):
        """Query DeepSeek model via Ollama with better timeout handling"""
        try:
            # Ollama API endpoint
            url = "http://localhost:11434/api/generate"
            
            # Use your exact model name with optimized settings
            payload = {
                "model": "deepseek-r1:7b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                    "num_predict": 500  # Limit response length for faster responses
                }
            }
            
            # Send request to Ollama with longer timeout for complex queries
            response = requests.post(url, json=payload, timeout=120)  # 2 minutes for generation
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', 'No response from AI')
                
                # Truncate very long responses
                if len(response_text) > 1500:
                    response_text = response_text[:1500] + "\n\n... (response truncated for speed)"
                
                return response_text
            else:
                return f"❌ Error from Ollama: {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return "❌ Cannot connect to Ollama. Please make sure Ollama is running."
        except requests.exceptions.Timeout:
            return "❌ Ollama is taking too long to respond. The model might be overloaded or your question is too complex.\n\n💡 Try asking simpler questions or use web search for faster results."
        except Exception as e:
            return f"❌ Error querying DeepSeek: {str(e)}"
    
    def _query_fallback_ai(self, prompt):
        """Fallback AI for when DeepSeek is too slow"""
        try:
            # Simple fallback response
            return f"🔍 [AI Search - Fallback Mode]\n\nDeepSeek is taking too long for this query.\n\n💡 Suggestions:\n• Ask simpler, shorter questions\n• Use web search for factual information\n• Try 'Can you' commands for quick tasks\n\nYour question: '{prompt}'\n\nTry rephrasing with fewer words for faster response."
        except:
            return "❌ AI service unavailable. Please try a simpler question or use web search."
    
    def _activate_search_mode(self):
        """Activate AI search mode"""
        print("🔍 Activating AI Search Mode...")
        self.search_mode_active = True
        
        search_msg = "🔍 AI SEARCH MODE ACTIVATED\n\nI'm now connected to DeepSeek R1 7B AI.\n💡 For faster responses, ask simpler questions.\n💡 Complex code generation may take time.\n\n💡 Special commands:\n• 'Can you [command]' - One-time normal command\n• 'Thank you Sara' - Return to normal mode"
        
        self._update_popup(search_msg)
        return search_msg, "AI Search mode activated. For faster responses, ask simpler questions!"
    
    def _deactivate_search_mode(self):
        """Deactivate AI search mode and return to normal"""
        print("🔍 Deactivating AI Search Mode...")
        self.search_mode_active = False
        return "🔄 Returning to normal mode. All features are now available again.", "Returning to normal mode"
    
    def _process_normal_command_in_search_mode(self, command):
        """Process one normal command while in search mode"""
        cmd = command.lower().replace('can you', '').strip()
        
        response = ""
        tts_text = ""
        
        # Open folder command
        if cmd.startswith('open folder'):
            folder_name = cmd.replace('open folder', '').strip()
            if folder_name:
                response = self.file_manager.open_folder(folder_name)
                tts_text = f"Opening folder {folder_name}"
            else:
                response = "Please specify folder name"
                tts_text = "Please specify folder name"
        
        # Open application command
        elif cmd.startswith('open ') and not cmd.startswith('open folder'):
            app_name = cmd.replace('open', '').strip()
            if app_name:
                response = self.file_manager.open_application(app_name)
                tts_text = f"Opening {app_name}"
            else:
                response = "Please specify what to open"
                tts_text = "Please specify what to open"
        
        # Close application command
        elif cmd.startswith('close '):
            app_name = cmd.replace('close', '').strip()
            if app_name:
                response = self.file_manager.close_application(app_name)
                tts_text = f"Closing {app_name}"
            else:
                response = "Please specify application"
                tts_text = "Please specify application"
        
        # Music Control Commands
        elif any(word in cmd for word in ['play music', 'start music']):
            response = self.music_player.play_music()
            tts_text = "Playing music"
        
        elif any(word in cmd for word in ['stop music', 'end music']):
            response = self.music_player.stop_music()
            tts_text = "Music stopped"
        
        elif any(word in cmd for word in ['pause music']):
            response = self.music_player.pause_music()
            tts_text = "Music paused"
        
        elif any(word in cmd for word in ['resume music', 'continue music']):
            response = self.music_player.unpause_music()
            tts_text = "Music resumed"
        
        # Brightness Control Commands
        elif cmd.startswith('brightness up'):
            try:
                parts = cmd.split()
                points = 1
                if len(parts) > 2:
                    points = int(parts[2])
                response = self.file_manager.increase_brightness(points)
                tts_text = f"Brightness up {points}"
            except:
                response = self.file_manager.increase_brightness(1)
                tts_text = "Brightness increased"
        
        elif cmd.startswith('brightness down'):
            try:
                parts = cmd.split()
                points = 1
                if len(parts) > 2:
                    points = int(parts[2])
                response = self.file_manager.decrease_brightness(points)
                tts_text = f"Brightness down {points}"
            except:
                response = self.file_manager.decrease_brightness(1)
                tts_text = "Brightness decreased"
        
        elif cmd.startswith('set brightness to'):
            try:
                level = int(cmd.replace('set brightness to', '').strip())
                response = self.file_manager.set_brightness(level)
                tts_text = f"Brightness set to {level}"
            except:
                response = "Please specify brightness level 0-100"
                tts_text = "Please specify level 0-100"
        
        # Screenshot command
        elif any(word in cmd for word in ['screenshot', 'take screenshot']):
            response = self.file_manager.take_screenshot()
            tts_text = "Screenshot taken"
        
        # Time and date
        elif any(word in cmd for word in ['time', 'what time']):
            current_time = datetime.now().strftime("%I:%M %p")
            response = f"🕒 {current_time}"
            tts_text = f"The time is {current_time}"
        
        elif any(word in cmd for word in ['date', 'today date']):
            current_date = datetime.now().strftime("%B %d, %Y")
            response = f"📅 {current_date}"
            tts_text = f"Today is {current_date}"
        
        # Default for unknown "can you" commands
        else:
            response = "❌ I can't perform that specific action in search mode. Please ask a general question instead."
            tts_text = "Cannot perform that action in search mode"
        
        return response, tts_text
    
    def _handle_math_calculation(self, command):
        """Handle mathematical calculations"""
        try:
            # Clean the command and extract the math expression
            math_phrases = [
                'calculate', 'what is', 'how much is', 'solve', 'math',
                'compute', 'tell me what is', 'give me the answer for'
            ]
            
            # Remove common phrases to get the pure math expression
            clean_cmd = command
            for phrase in math_phrases:
                clean_cmd = clean_cmd.replace(phrase, '').strip()
            
            # Replace spoken words with mathematical operators
            operator_replacements = {
                'plus': '+',
                'minus': '-',
                'times': '*',
                'multiply by': '*',
                'multiplied by': '*',
                'multiply': '*',
                'into': '*',
                'multiple of': '*',
                'x': '*',
                'divide by': '/',
                'divided by': '/',
                'over': '/',
                'to the power of': '**',
                'squared': '**2',
                'cubed': '**3',
                'modulo': '%',
                'percent': '/100',
                'point': '.',
                'add': '+',
                'subtract': '-',
                'product of': '*'
            }
            
            # Replace spoken operators with symbols
            math_expression = clean_cmd
            for spoken, symbol in operator_replacements.items():
                math_expression = math_expression.replace(spoken, symbol)
            
            # Remove any extra words and keep only numbers and operators
            math_expression = re.sub(r'[^\d\+\-\*\/\.\(\)\s]', '', math_expression)
            math_expression = math_expression.strip()
            
            if not math_expression:
                return "❌ Please provide a valid math expression", "Please provide a valid math expression"
            
            # Safety check - only allow basic math operations
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in math_expression):
                return "❌ Only basic math operations are allowed for safety", "Only basic math operations allowed"
            
            # Evaluate the expression safely
            try:
                result = eval(math_expression)
                
                # Format the result
                if isinstance(result, (int, float)):
                    if result == int(result):
                        result = int(result)
                    
                    response = f"🧮 Calculation:\n{math_expression} = {result}"
                    tts_text = f"The answer is {result}"
                    
                    # Add explanation for common operations
                    if '+' in math_expression:
                        parts = math_expression.split('+')
                        if len(parts) == 2:
                            response += f"\n\n📝 {parts[0].strip()} plus {parts[1].strip()} equals {result}"
                    elif '-' in math_expression:
                        parts = math_expression.split('-')
                        if len(parts) == 2:
                            response += f"\n\n📝 {parts[0].strip()} minus {parts[1].strip()} equals {result}"
                    elif '*' in math_expression:
                        parts = math_expression.split('*')
                        if len(parts) == 2:
                            response += f"\n\n📝 {parts[0].strip()} times {parts[1].strip()} equals {result}"
                    elif '/' in math_expression:
                        parts = math_expression.split('/')
                        if len(parts) == 2:
                            response += f"\n\n📝 {parts[0].strip()} divided by {parts[1].strip()} equals {result}"
                    
                    return response, tts_text
                else:
                    return "❌ Could not calculate the result", "Calculation error"
                    
            except ZeroDivisionError:
                return "❌ Cannot divide by zero", "Cannot divide by zero"
            except:
                return "❌ Invalid math expression", "Invalid math expression"
                
        except Exception as e:
            return f"❌ Math calculation error: {e}", "Math calculation error"
    
    def run(self):
        """Main assistant loop"""
        print("\n" + "="*50)
        print("🤖 SARA AI ASSISTANT")
        print("💡 Say 'Hi Sara' to begin")
        print("🔍 Say 'Sara activate search' for AI Search Mode")
        print("⏹️  Say 'Sara exit' to shutdown")
        print("="*50)
        
        # Start in sleep mode (listening for wake word)
        print("💤 Sleeping - Listening for 'Hi Sara'...")
        
        try:
            while self.running:
                text = self.voice_engine.listen()
                
                if text:
                    print(f"👤 User: {text}")
                    
                    # Check for exit command first
                    if self.voice_engine.is_exit_command(text):
                        self._handle_exit()
                        break
                    
                    # Check for wake word when assistant is sleeping
                    if not self.assistant_active and self.voice_engine.is_wake_word(text):
                        self.activate_assistant()
                        continue
                    
                    # Check for sleep command when assistant is active
                    if self.assistant_active and self.voice_engine.is_sleep_command(text):
                        self._handle_sleep()
                        continue
                    
                    # Process commands only when assistant is active
                    if self.assistant_active and text.strip():
                        self.process_command(text)
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            self.stop_completely()
    
    def activate_assistant(self):
        """Activate assistant - show popup and start processing commands"""
        print("🔔 Activating Sara AI...")
        self.assistant_active = True
        
        # Show popup
        if not self.popup.is_open:
            popup_thread = threading.Thread(target=self.popup.show_popup)
            popup_thread.daemon = True
            popup_thread.start()
            time.sleep(0.5)
        
        greeting = self._get_time_greeting()
        welcome_msg = f"{greeting}\n\nReady to assist you."
        
        self._update_popup(welcome_msg)
        self.voice_engine.speak(f"{greeting.split('!')[0]}! How can I help you?")
        
        print("🎯 Sara AI activated - Ready for commands!")
    
    def _get_time_greeting(self):
        """Get appropriate greeting based on time"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "☀️ Good morning!"
        elif 12 <= hour < 17:
            return "🌞 Good afternoon!"
        elif 17 <= hour < 21:
            return "🌇 Good evening!"
        else:
            return "🌙 Good night!"
    
    def process_command(self, command):
        """Process all types of commands"""
        print(f"🔧 Processing: {command}")
        cmd = command.lower()
        
        response = ""
        tts_text = ""
        
        # SEARCH MODE ACTIVATION - Must be exact "sara activate search"
        if cmd == 'sara activate search':
            if not self.search_mode_active:
                response, tts_text = self._activate_search_mode()
            else:
                response = "🔍 Search mode is already active!"
                tts_text = "Search mode already active"
        
        # SEARCH MODE EXIT - "thank you sara"
        elif self.search_mode_active and 'thank you sara' in cmd:
            response, tts_text = self._deactivate_search_mode()
        
        # SEARCH MODE: "Can you" commands (one-time normal commands)
        elif self.search_mode_active and cmd.startswith('can you'):
            print("🔍 Processing one-time normal command in search mode...")
            response, tts_text = self._process_normal_command_in_search_mode(command)
        
        # SEARCH MODE: All other queries go to DeepSeek
        elif self.search_mode_active:
            print("🔍 Processing in AI Search Mode...")
            
            # Show "processing" message
            processing_msg = "⏳ Processing your question with DeepSeek AI...\nThis may take a moment for complex queries."
            self._update_popup(processing_msg)
            self.voice_engine.speak("Processing your question")
            
            # Try DeepSeek first
            response = self._query_deepseek(command)
            
            # If timeout or error, use fallback
            if "timeout" in response.lower() or "error" in response.lower() or "❌" in response:
                response = self._query_fallback_ai(command)
            
            tts_text = "Here's what I found"
        
        # NORMAL MODE PROCESSING (only if not in search mode)
        elif not self.search_mode_active:
            # WhatsApp message flow
            if self.whatsapp_sender.waiting_for_contact:
                response = self.whatsapp_sender.set_contact(command)
                tts_text = "What message do you want to send?"
            
            elif self.whatsapp_sender.waiting_for_message:
                response = self.whatsapp_sender.set_message(command)
                tts_text = "Message ready. Say 'send' to send or 'cancel' to cancel."
            
            elif self.whatsapp_sender.ready_to_send and 'send' in cmd:
                response = self.whatsapp_sender.send_message()
                tts_text = "Sending message"
            
            elif self.whatsapp_sender.ready_to_send and 'cancel' in cmd:
                response = self.whatsapp_sender.cancel_message()
                tts_text = "Message cancelled"
            
            # If waiting for note filename, save note with given name
            elif self.note_taker.waiting_for_filename:
                response = self.note_taker.save_note_with_name(command)
                tts_text = f"Note saved as {command}"
            
            # MATHEMATICAL CALCULATIONS
            elif any(word in cmd for word in ['calculate', 'what is', 'how much is', 'solve', 'math', 'plus', 'minus', 'times', 'divided by', 'multiply', 'add', 'subtract', 'into', 'multiple', 'x']):
                response, tts_text = self._handle_math_calculation(cmd)
            
            # YouTube commands (must come before music commands)
            elif any(cmd.startswith(prefix) for prefix in ['youtube', 'watch', 'video']):
                if cmd.startswith('youtube'):
                    query = cmd.replace('youtube', '').strip()
                elif cmd.startswith('watch'):
                    query = cmd.replace('watch', '').strip()
                elif cmd.startswith('video'):
                    query = cmd.replace('video', '').strip()
                
                if query:
                    response = self.web_search.play_youtube(query)
                    tts_text = f"Playing {query} on YouTube"
                else:
                    response = "Please specify what to play on YouTube"
                    tts_text = "Please specify what to play"
        
            # WhatsApp commands
            elif cmd.startswith('send message to'):
                contact = cmd.replace('send message to', '').strip()
                if contact:
                    response = self.whatsapp_sender.set_contact(contact)
                    tts_text = f"Message to {contact}. What's the message?"
                else:
                    response = "Please specify contact name"
                    tts_text = "Please specify contact"
            
            elif cmd == 'send message':
                response = self.whatsapp_sender.start_message()
                tts_text = "Who do you want to send message to?"
            
            # Add contact command
            elif cmd.startswith('add contact'):
                try:
                    parts = cmd.replace('add contact', '').strip().split(' number ')
                    if len(parts) == 2:
                        name = parts[0].strip()
                        number = parts[1].strip()
                        response = self.whatsapp_sender.add_contact(name, number)
                        tts_text = f"Contact {name} added"
                    else:
                        response = "Usage: Add contact [name] number [phone number]"
                        tts_text = "Please specify name and number"
                except:
                    response = "Usage: Add contact [name] number [phone number]"
                    tts_text = "Please specify name and number"
            
            elif cmd == 'list contacts':
                response = self.whatsapp_sender.list_contacts()
                tts_text = "Your contacts"
            
            # Open folder command
            elif cmd.startswith('open folder'):
                folder_name = cmd.replace('open folder', '').strip()
                if folder_name:
                    response = self.file_manager.open_folder(folder_name)
                    tts_text = f"Opening folder {folder_name}"
                else:
                    response = "Please specify folder name"
                    tts_text = "Please specify folder name"
            
            # Brightness Control Commands
            elif cmd.startswith('brightness up'):
                try:
                    parts = cmd.split()
                    points = 1
                    if len(parts) > 2:
                        points = int(parts[2])
                    response = self.file_manager.increase_brightness(points)
                    tts_text = f"Brightness up {points}"
                except:
                    response = self.file_manager.increase_brightness(1)
                    tts_text = "Brightness increased"
            
            elif cmd.startswith('brightness down'):
                try:
                    parts = cmd.split()
                    points = 1
                    if len(parts) > 2:
                        points = int(parts[2])
                    response = self.file_manager.decrease_brightness(points)
                    tts_text = f"Brightness down {points}"
                except:
                    response = self.file_manager.decrease_brightness(1)
                    tts_text = "Brightness decreased"
            
            elif cmd.startswith('set brightness to'):
                try:
                    level = int(cmd.replace('set brightness to', '').strip())
                    response = self.file_manager.set_brightness(level)
                    tts_text = f"Brightness set to {level}"
                except:
                    response = "Please specify brightness level 0-100"
                    tts_text = "Please specify level 0-100"
            
            elif any(word in cmd for word in ['current brightness', 'brightness level']):
                response = self.file_manager.get_brightness()
                tts_text = "Current brightness"
            
            # Note Taking Commands
            elif cmd == 'write note':
                response = self.note_taker.start_note()
                tts_text = "Note recording started"
            
            elif cmd == 'save note':
                response = self.note_taker.prepare_to_save_note()
                tts_text = "Note name?"
            
            elif cmd == 'cancel note':
                response = self.note_taker.cancel_note()
                tts_text = "Note cancelled"
            
            elif cmd == 'note status':
                response = self.note_taker.get_note_status()
                tts_text = "Note status"
            
            elif cmd == 'list notes':
                response = self.note_taker.list_notes()
                tts_text = "Your notes"
            
            # If note recording is active, add all speech to note
            elif self.note_taker.is_recording and not any(word in cmd for word in ['save note', 'cancel note', 'note status']):
                note_response = self.note_taker.add_to_note(command)
                response = f"✓ Added to note\n{note_response}"
                tts_text = "Added to note"
            
            # Close application command
            elif cmd.startswith('close '):
                app_name = cmd.replace('close', '').strip()
                if app_name:
                    response = self.file_manager.close_application(app_name)
                    tts_text = f"Closing {app_name}"
                else:
                    response = "Please specify application"
                    tts_text = "Please specify application"
            
            # Create folder command
            elif cmd.startswith('create folder'):
                folder_name = cmd.replace('create folder', '').strip()
                if folder_name:
                    response = self.file_manager.create_folder(folder_name)
                    tts_text = f"Creating {folder_name}"
                else:
                    response = "Please specify folder name"
                    tts_text = "Please specify folder name"

            # Open application command
            elif cmd.startswith('open ') and not cmd.startswith('open folder'):
                app_name = cmd.replace('open', '').strip()
                if app_name:
                    response = self.file_manager.open_application(app_name)
                    tts_text = f"Opening {app_name}"
                else:
                    response = "Please specify what to open"
                    tts_text = "Please specify what to open"

            # Music Control Commands
            elif any(word in cmd for word in ['play music', 'start music']):
                response = self.music_player.play_music()
                tts_text = "Playing music"
            
            elif any(word in cmd for word in ['stop music', 'end music']):
                response = self.music_player.stop_music()
                tts_text = "Music stopped"
            
            elif any(word in cmd for word in ['pause music']):
                response = self.music_player.pause_music()
                tts_text = "Music paused"
            
            elif any(word in cmd for word in ['resume music', 'continue music']):
                response = self.music_player.unpause_music()
                tts_text = "Music resumed"
            
            elif any(word in cmd for word in ['volume up', 'increase volume']):
                response = self.music_player.volume_up()
                tts_text = "Volume increased"
            
            elif any(word in cmd for word in ['volume down', 'decrease volume']):
                response = self.music_player.volume_down()
                tts_text = "Volume decreased"
            
            elif any(word in cmd for word in ['next track', 'next song']):
                response = self.music_player.next_track()
                tts_text = "Next track"
            
            elif any(word in cmd for word in ['previous track', 'previous song']):
                response = self.music_player.previous_track()
                tts_text = "Previous track"
            
            elif any(word in cmd for word in ['playlist', 'playlist info']):
                response = self.music_player.get_playlist_info()
                tts_text = "Playlist info"

            # Greetings and basic responses
            elif any(word in cmd for word in ['good morning', 'morning']):
                response = "☀️ Good morning! How can I help?"
                tts_text = "Good morning!"
            
            elif any(word in cmd for word in ['good afternoon']):
                response = "🌞 Good afternoon!"
                tts_text = "Good afternoon!"
            
            elif any(word in cmd for word in ['good evening', 'evening']):
                response = "🌇 Good evening!"
                tts_text = "Good evening!"
            
            elif any(word in cmd for word in ['good night', 'night']):
                response = "🌙 Good night!"
                tts_text = "Good night!"
            
            elif 'how are you' in cmd:
                response = "🤖 I'm doing well, thank you!"
                tts_text = "I'm doing well"
            
            elif 'who are you' in cmd or 'your name' in cmd:
                response = "🤖 I'm Sara, your AI assistant"
                tts_text = "I'm Sara"
            
            elif 'thank' in cmd:
                response = "😊 You're welcome!"
                tts_text = "You're welcome"
            
            # System commands
            elif any(word in cmd for word in ['system info', 'system information', 'pc status']):
                response = self.system_monitor.get_system_info()
                tts_text = "System info"
            
            elif any(word in cmd for word in ['battery', 'battery status']):
                response = self.system_monitor.get_battery_status()
                tts_text = "Battery status"
            
            elif any(word in cmd for word in ['storage', 'disk', 'storage info']):
                response = self.system_monitor.get_storage_info()
                tts_text = "Storage info"
            
            elif any(word in cmd for word in ['process', 'running process']):
                response = self.system_monitor.get_running_processes()
                tts_text = "Running processes"
            
            # Time and date
            elif any(word in cmd for word in ['time', 'what time']):
                current_time = datetime.now().strftime("%I:%M %p")
                response = f"🕒 {current_time}"
                tts_text = f"The time is {current_time}"
            
            elif any(word in cmd for word in ['date', 'today date']):
                current_date = datetime.now().strftime("%B %d, %Y")
                response = f"📅 {current_date}"
                tts_text = f"Today is {current_date}"
            
            elif any(word in cmd for word in ['day', 'what day']):
                current_day = datetime.now().strftime("%A")
                response = f"📆 {current_day}"
                tts_text = f"Today is {current_day}"
            
            # Web Search commands
            elif 'wikipedia' in cmd:
                query = cmd.replace('wikipedia', '').replace('search', '').strip()
                if query:
                    response = self.web_search.search_wikipedia(query)
                    tts_text = f"Wikipedia: {query}"
                else:
                    response = "Please specify search query"
                    tts_text = "Please specify search"
            
            elif any(word in cmd for word in ['search web', 'web search']):
                query = cmd.replace('search web', '').replace('web search', '').strip()
                if query:
                    response = self.web_search.search_web(query)
                    tts_text = f"Searching: {query}"
                else:
                    response = "Please specify search query"
                    tts_text = "Please specify search"
            
            elif any(word in cmd for word in ['news', 'latest news']):
                response = self.web_search.get_news()
                tts_text = "Latest news"
            
            # File and System Control
            elif any(word in cmd for word in ['file info', 'list files']):
                response = self.file_manager.get_file_info()
                tts_text = "File info"
            
            elif any(word in cmd for word in ['screenshot', 'take screenshot']):
                response = self.file_manager.take_screenshot()
                tts_text = "Screenshot taken"
            
            elif any(word in cmd for word in ['shutdown computer', 'shutdown pc']):
                response = "🖥️ Shutting down in 1 minute"
                tts_text = "Shutting down"
            
            elif any(word in cmd for word in ['restart computer', 'restart pc']):
                response = "🖥️ Restarting in 1 minute"
                tts_text = "Restarting"
            
            # Reminder System
            elif 'set reminder' in cmd:
                try:
                    parts = cmd.replace('set reminder', '').split(' in ')
                    if len(parts) == 2:
                        message = parts[0].strip()
                        minutes = int(parts[1].split()[0])
                        response = self.reminder_system.add_reminder(message, minutes)
                        tts_text = f"Reminder set for {minutes} minutes"
                    else:
                        response = "Usage: Set reminder [message] in [X] minutes"
                        tts_text = "Please specify message and time"
                except:
                    response = "Usage: Set reminder [message] in [X] minutes"
                    tts_text = "Please specify message and time"
            
            elif any(word in cmd for word in ['show reminders', 'pending reminders']):
                response = self.reminder_system.get_pending_reminders()
                tts_text = "Your reminders"
            
            # Email System
            elif any(word in cmd for word in ['send email', 'email']):
                response = self.email_sender.get_email_template()
                tts_text = "Email instructions"
            
            # Help and information
            elif any(word in cmd for word in ['what can you do', 'help', 'commands']):
                response = self.commands_list
                tts_text = "Available commands"
            
            # Fun commands
            elif any(word in cmd for word in ['joke', 'tell joke']):
                response = "😄 Why do programmers prefer dark mode?\nBecause light attracts bugs!"
                tts_text = "Why do programmers prefer dark mode? Because light attracts bugs!"
            
            # Default response - SIMPLE
            else:
                response = "I didn't understand that. Please repeat."
                tts_text = "I didn't understand, please repeat"
        
        self._update_popup(response)
        self.voice_engine.speak(tts_text)
        print(f"✅ Command processed: {command}")
    
    def _handle_exit(self):
        """Handle exit command - completely shut down the program"""
        print("🛑 Exit command received - Shutting down...")
        self.reminder_system.stop()
        shutdown_msg = "🔴 Shutting down...\n\nThank you for using Sara!"
        self._update_popup(shutdown_msg)
        self.voice_engine.speak("Goodbye!")
        time.sleep(2)
        self.stop_completely()
    
    def _handle_sleep(self):
        """Handle sleep command - minimize popup but keep listening"""
        print("😴 Sleep command received - Minimizing popup...")
        self.voice_engine.speak("Minimizing. Say Hi Sara when you need me.")
        time.sleep(1)
        self.deactivate_assistant()
    
    def deactivate_assistant(self):
        """Deactivate assistant and minimize popup (but keep listening)"""
        print("😴 Deactivating Sara and minimizing popup...")
        self.assistant_active = False
        self.search_mode_active = False
        self.popup.minimize_popup()
        print("💤 Assistant sleeping - Popup minimized, listening for 'Hi Sara'...")
    
    def _update_popup(self, text):
        """Update popup with response"""
        if self.popup and self.popup.is_open:
            self.popup.update_response(text)
    
    def stop_completely(self):
        """Stop assistant completely and exit program"""
        print("\n👋 Shutting down Sara AI Assistant...")
        self.running = False
        self.assistant_active = False
        self.search_mode_active = False
        self.reminder_system.stop()
        self.popup.close_popup()
        print("✅ Sara AI Assistant stopped")
        sys.exit(0)

if __name__ == "__main__":
    assistant = SaraAssistant()
    assistant.run()