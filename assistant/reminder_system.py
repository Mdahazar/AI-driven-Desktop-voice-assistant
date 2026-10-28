import threading
import time
from datetime import datetime, timedelta

class ReminderSystem:
    def __init__(self):
        self.reminders = []
        self.reminder_thread = None
        self.running = True
        self.start_reminder_checker()
    
    def start_reminder_checker(self):
        """Start background thread to check reminders"""
        self.reminder_thread = threading.Thread(target=self._check_reminders)
        self.reminder_thread.daemon = True
        self.reminder_thread.start()
        print("⏰ Reminder system started")
    
    def add_reminder(self, message, minutes_from_now):
        """Add a new reminder"""
        try:
            reminder_time = datetime.now() + timedelta(minutes=minutes_from_now)
            reminder_id = len(self.reminders) + 1
            
            self.reminders.append({
                'id': reminder_id,
                'message': message,
                'time': reminder_time,
                'triggered': False,
                'created': datetime.now()
            })
            
            time_str = reminder_time.strftime("%I:%M %p")
            return f"⏰ Reminder #{reminder_id} set for {time_str} ({minutes_from_now} minutes from now): '{message}'"
        except Exception as e:
            return f"❌ Error setting reminder: {e}"
    
    def add_reminder_with_time(self, message, hour, minute, am_pm="AM"):
        """Add a reminder for specific time"""
        try:
            # Parse the time
            if am_pm.upper() == "PM" and hour != 12:
                hour += 12
            elif am_pm.upper() == "AM" and hour == 12:
                hour = 0
            
            now = datetime.now()
            reminder_time = datetime(now.year, now.month, now.day, hour, minute)
            
            # If the time has already passed today, set for tomorrow
            if reminder_time < now:
                reminder_time += timedelta(days=1)
            
            minutes_from_now = (reminder_time - now).total_seconds() / 60
            return self.add_reminder(message, int(minutes_from_now))
            
        except Exception as e:
            return f"❌ Error setting time-based reminder: {e}"
    
    def _check_reminders(self):
        """Check and trigger reminders in background"""
        while self.running:
            now = datetime.now()
            for reminder in self.reminders:
                if not reminder['triggered'] and now >= reminder['time']:
                    print(f"\n" + "🔔" * 50)
                    print(f"🔔 REMINDER: {reminder['message']}")
                    print("🔔" * 50)
                    reminder['triggered'] = True
            
            time.sleep(30)  # Check every 30 seconds
    
    def get_pending_reminders(self):
        """Get list of pending reminders"""
        pending = [r for r in self.reminders if not r['triggered']]
        if not pending:
            return "📋 No pending reminders"
        
        reminder_list = "📋 PENDING REMINDERS:\n\n"
        for reminder in pending:
            time_left = reminder['time'] - datetime.now()
            minutes_left = max(0, int(time_left.total_seconds() / 60))
            hours_left = minutes_left // 60
            remaining_minutes = minutes_left % 60
            
            time_str = reminder['time'].strftime("%I:%M %p")
            
            if hours_left > 0:
                time_display = f"{hours_left}h {remaining_minutes}m"
            else:
                time_display = f"{remaining_minutes}m"
            
            reminder_list += f"#{reminder['id']}. ⏰ {time_str} (in {time_display})\n   📝 {reminder['message']}\n\n"
        
        return reminder_list.strip()
    
    def get_completed_reminders(self):
        """Get list of completed reminders"""
        completed = [r for r in self.reminders if r['triggered']]
        if not completed:
            return "✅ No completed reminders"
        
        completed_list = "✅ COMPLETED REMINDERS:\n\n"
        for reminder in completed[-5:]:  # Show last 5 completed
            time_str = reminder['time'].strftime("%I:%M %p")
            completed_list += f"#{reminder['id']}. ⏰ {time_str}\n   📝 {reminder['message']}\n\n"
        
        return completed_list.strip()
    
    def delete_reminder(self, reminder_id):
        """Delete a specific reminder"""
        try:
            for i, reminder in enumerate(self.reminders):
                if reminder['id'] == reminder_id:
                    del self.reminders[i]
                    return f"🗑️ Reminder #{reminder_id} deleted"
            return f"❌ Reminder #{reminder_id} not found"
        except Exception as e:
            return f"❌ Error deleting reminder: {e}"
    
    def clear_completed_reminders(self):
        """Clear all completed reminders"""
        try:
            initial_count = len(self.reminders)
            self.reminders = [r for r in self.reminders if not r['triggered']]
            cleared_count = initial_count - len(self.reminders)
            return f"🧹 Cleared {cleared_count} completed reminders"
        except Exception as e:
            return f"❌ Error clearing reminders: {e}"
    
    def clear_all_reminders(self):
        """Clear all reminders"""
        try:
            count = len(self.reminders)
            self.reminders = []
            return f"🗑️ Cleared all {count} reminders"
        except Exception as e:
            return f"❌ Error clearing all reminders: {e}"
    
    def get_reminder_stats(self):
        """Get reminder statistics"""
        total = len(self.reminders)
        pending = len([r for r in self.reminders if not r['triggered']])
        completed = total - pending
        
        stats = f"📊 REMINDER STATISTICS:\n\n"
        stats += f"📥 Total: {total}\n"
        stats += f"⏳ Pending: {pending}\n"
        stats += f"✅ Completed: {completed}\n"
        
        if pending > 0:
            next_reminder = min([r for r in self.reminders if not r['triggered']], 
                              key=lambda x: x['time'])
            time_left = next_reminder['time'] - datetime.now()
            minutes_left = int(time_left.total_seconds() / 60)
            stats += f"\n⏰ Next reminder in {minutes_left} minutes"
        
        return stats
    
    def stop(self):
        """Stop the reminder system"""
        self.running = False
        print("⏰ Reminder system stopped")