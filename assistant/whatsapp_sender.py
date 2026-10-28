import webbrowser
import pyautogui
import time
import re
from urllib.parse import quote

class WhatsAppSender:
    def __init__(self):
        self.contact = None
        self.message = None
        self.waiting_for_contact = False
        self.waiting_for_message = False
        self.ready_to_send = False
        self.contact_type = None
        
        # Common contacts mapping (you can extend this)
        self.contacts = {
            'mom': '+911234567890',  # Replace with actual numbers
            'dad': '+911234567891',
            'brother': '+911234567892',
            'sister': '+911234567893',
            'friend': '7411126826',
            'wife': '+911234567895',
            'husband': '+911234567896',
        }
    
    def start_message(self):
        """Start the WhatsApp message flow"""
        self.waiting_for_contact = True
        self.contact = None
        self.message = None
        self.ready_to_send = False
        self.contact_type = None
        return "📱 WhatsApp Message\n\nWho do you want to send message to? (Say name or phone number with country code)"
    
    def set_contact(self, contact_input):
        """Set the contact for the message"""
        contact_input = contact_input.strip()
        
        # Check if it's a phone number
        if self._is_phone_number(contact_input):
            self.contact = self._clean_phone_number(contact_input)
            self.contact_type = 'number'
        else:
            # Check if it's in contacts list
            contact_lower = contact_input.lower()
            if contact_lower in self.contacts:
                self.contact = self.contacts[contact_lower]
                self.contact_type = 'name'
            else:
                # Ask for phone number since name not found
                self.waiting_for_contact = True
                return f"❌ '{contact_input}' not in contacts.\n\nPlease provide phone number with country code (e.g., +911234567890):"
        
        self.waiting_for_contact = False
        self.waiting_for_message = True
        
        if self.contact_type == 'name':
            return f"📱 Message to: {contact_input.title()}\n\nWhat message do you want to send?"
        else:
            return f"📱 Message to: {self.contact}\n\nWhat message do you want to send?"
    
    def set_message(self, message_text):
        """Set the message content"""
        self.message = message_text.strip()
        self.waiting_for_message = False
        self.ready_to_send = True
        
        contact_display = self._get_contact_display()
        return f"📱 Ready to Send\n\nTo: {contact_display}\nMessage: {self.message}\n\nSay 'send' to send or 'cancel' to cancel."
    
    def send_message(self):
        """Send WhatsApp message INSTANTLY using direct URL"""
        try:
            if not self.contact or not self.message:
                return "❌ No message to send. Please start again."
            
            # Validate phone number format
            if not self._is_valid_phone_number(self.contact):
                return "❌ Invalid phone number format. Please use country code (e.g., +911234567890)"
            
            print(f"📱 Sending message to: {self.contact}")
            print(f"💬 Message: {self.message}")
            
            # Method: Direct WhatsApp URL (INSTANT)
            result = self._send_via_direct_url()
            
        except Exception as e:
            error_msg = str(e)
            if "country code" in error_msg.lower():
                result = "❌ Country code missing. Please use format: +911234567890"
            elif "internet" in error_msg.lower():
                result = "❌ No internet connection. Please check your connection."
            else:
                result = f"❌ Error sending message: {error_msg}"
            
            print(f"⚠️ WhatsApp error: {error_msg}")
        
        # Reset state
        self._reset()
        return result
    
    def _send_via_direct_url(self):
        """Send message instantly using WhatsApp direct URL"""
        try:
            # Remove '+' from phone number for URL
            phone_number = self.contact.replace('+', '')
            
            # URL encode the message
            encoded_message = quote(self.message)
            
            # Create WhatsApp direct URL
            whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
            
            print(f"🔗 Opening WhatsApp URL...")
            
            # Open WhatsApp in default browser
            webbrowser.open(whatsapp_url)
            
            # Wait for page to load
            print("⏳ Waiting for WhatsApp to load...")
            time.sleep(10)  # Wait for WhatsApp Web to load
            
            # Press Enter to send the message
            print("🚀 Sending message...")
            pyautogui.press('enter')
            time.sleep(2)
            
            contact_display = self._get_contact_display()
            return f"✅ Message sent to {contact_display}"
            
        except Exception as e:
            return f"❌ Failed to send message: {str(e)}"
    
    def cancel_message(self):
        """Cancel the current message"""
        result = "❌ Message cancelled"
        self._reset()
        return result
    
    def _is_phone_number(self, text):
        """Check if text looks like a phone number"""
        # Remove spaces and common separators
        clean_text = re.sub(r'[\s\-\(\)\.]', '', text)
        
        # Check if it starts with + and has digits, or just has 10+ digits
        if clean_text.startswith('+') and clean_text[1:].isdigit():
            return True
        elif clean_text.isdigit() and len(clean_text) >= 10:
            return True
        return False
    
    def _clean_phone_number(self, phone_number):
        """Clean and format phone number"""
        # Remove spaces and common separators
        clean_number = re.sub(r'[\s\-\(\)\.]', '', phone_number)
        
        # Add + if missing but number is long enough
        if not clean_number.startswith('+') and clean_number.isdigit() and len(clean_number) >= 10:
            # Assume Indian number if no country code
            if len(clean_number) == 10:
                clean_number = '+91' + clean_number
            else:
                clean_number = '+' + clean_number
        
        return clean_number
    
    def _is_valid_phone_number(self, phone_number):
        """Validate phone number format"""
        if not phone_number.startswith('+'):
            return False
        
        # Remove + and check if rest are digits
        digits = phone_number[1:]
        if not digits.isdigit():
            return False
        
        # Check minimum length (country code + number)
        if len(digits) < 10:
            return False
        
        return True
    
    def _get_contact_display(self):
        """Get display name for contact"""
        if self.contact_type == 'name':
            # Find the name from contacts
            for name, number in self.contacts.items():
                if number == self.contact:
                    return name.title()
        return self.contact
    
    def _reset(self):
        """Reset all states"""
        self.contact = None
        self.message = None
        self.waiting_for_contact = False
        self.waiting_for_message = False
        self.ready_to_send = False
        self.contact_type = None
    
    def add_contact(self, name, phone_number):
        """Add a contact to the contacts list"""
        clean_number = self._clean_phone_number(phone_number)
        if self._is_valid_phone_number(clean_number):
            self.contacts[name.lower()] = clean_number
            return f"✅ Contact '{name}' added: {clean_number}"
        else:
            return "❌ Invalid phone number format"
    
    def list_contacts(self):
        """List all saved contacts"""
        if not self.contacts:
            return "📱 No contacts saved"
        
        contacts_list = "📱 Saved Contacts:\n\n"
        for name, number in self.contacts.items():
            contacts_list += f"• {name.title()}: {number}\n"
        
        return contacts_list