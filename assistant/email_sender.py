import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_email(self, recipient, subject, message, sender_email, sender_password):
        """Send email using SMTP"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Add message body
            msg.attach(MIMEText(message, 'plain'))
            
            # Create server connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(sender_email, recipient, text)
            server.quit()
            
            return f"📧 Email sent successfully to {recipient}"
            
        except Exception as e:
            return f"❌ Error sending email: {e}"
    
    def get_email_template(self):
        """Return email sending instructions"""
        return """
📧 EMAIL SENDING INSTRUCTIONS:

To send emails through Sara, you need to:

1. Enable 2-factor authentication on your Gmail
2. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   
3. Command format:
   "Send email to [recipient] subject [subject] message [message]"

Example:
"Send email to friend@gmail.com subject Hello message How are you doing?"

🔐 Your email and password are handled securely and not stored.
"""