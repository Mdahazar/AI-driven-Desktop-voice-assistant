import os
from datetime import datetime

class NoteTaker:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.notes_dir = os.path.join(base_dir, "notes")
        self.current_note = None
        self.is_recording = False
        self.waiting_for_filename = False
        
        # Create notes directory if it doesn't exist
        os.makedirs(self.notes_dir, exist_ok=True)
    
    def start_note(self):
        """Start a new note"""
        try:
            self.is_recording = True
            self.current_note = {
                'content': '',
                'start_time': datetime.now(),
                'filename': None  # Will be set when saving
            }
            return "📝 Note recording started! Speak your notes. Say 'save note' when done to name your note."
        except Exception as e:
            return f"❌ Error starting note: {e}"
    
    def add_to_note(self, text):
        """Add text to current note"""
        if not self.is_recording or not self.current_note:
            return "❌ No active note recording. Say 'write note' to start."
        
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.current_note['content'] += f"[{timestamp}] {text}\n"
            return f"✅ Added to note: {text}"
        except Exception as e:
            return f"❌ Error adding to note: {e}"
    
    def save_note_with_name(self, filename):
        """Save the current note with specified filename"""
        if not self.is_recording or not self.current_note:
            return "❌ No active note to save."
        
        try:
            # Clean filename and ensure .txt extension
            filename = "".join(c for c in filename if c not in '<>:"/\\|?*')
            if not filename.lower().endswith('.txt'):
                filename += '.txt'
            
            filepath = os.path.join(self.notes_dir, filename)
            
            # Check if file already exists
            counter = 1
            original_filepath = filepath
            while os.path.exists(filepath):
                name, ext = os.path.splitext(original_filepath)
                filepath = f"{name}_{counter}{ext}"
                counter += 1
            
            # Add header with creation time
            header = f"Note: {filename}\n"
            header += f"Created: {self.current_note['start_time'].strftime('%Y-%m-%d %H:%M:%S')}\n"
            header += f"Saved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            header += "=" * 50 + "\n\n"
            
            full_content = header + self.current_note['content']
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            # Reset note
            self.current_note = None
            self.is_recording = False
            self.waiting_for_filename = False
            
            return f"💾 Note saved as: {os.path.basename(filepath)}"
        except Exception as e:
            return f"❌ Error saving note: {e}"
    
    def prepare_to_save_note(self):
        """Prepare to save note and ask for filename"""
        if not self.is_recording or not self.current_note:
            return "❌ No active note to save."
        
        self.waiting_for_filename = True
        return "📝 Please tell me the name for your note:"
    
    def cancel_note(self):
        """Cancel current note without saving"""
        if not self.is_recording:
            return "❌ No active note recording."
        
        self.current_note = None
        self.is_recording = False
        self.waiting_for_filename = False
        return "❌ Note recording cancelled."
    
    def get_note_status(self):
        """Get current note status"""
        if self.is_recording and self.current_note:
            lines = len(self.current_note['content'].split('\n'))
            duration = datetime.now() - self.current_note['start_time']
            minutes = int(duration.total_seconds() / 60)
            return f"📝 Active Note: {lines} lines, recording for {minutes} minutes\n💡 Say 'save note' to save and name your note."
        else:
            return "📝 No active note recording. Say 'write note' to start."
    
    def list_notes(self):
        """List all saved notes"""
        try:
            notes = []
            for file in os.listdir(self.notes_dir):
                if file.endswith('.txt'):
                    notes.append(file)
            
            if not notes:
                return "📝 No notes found in notes folder."
            
            notes.sort(reverse=True)  # Show newest first
            result = "📝 SAVED NOTES:\n\n"
            for note in notes[:10]:  # Show last 10 notes
                note_path = os.path.join(self.notes_dir, note)
                created_time = datetime.fromtimestamp(os.path.getctime(note_path))
                result += f"• {note} (Created: {created_time.strftime('%Y-%m-%d %H:%M')})\n"
            
            if len(notes) > 10:
                result += f"\n... and {len(notes) - 10} more notes"
            
            return result
        except Exception as e:
            return f"❌ Error listing notes: {e}"