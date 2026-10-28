import psutil
import platform
from datetime import datetime
import socket
import os

class SystemMonitor:
    @staticmethod
    def get_system_info():
        """Get comprehensive system information"""
        try:
            # CPU Information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            cpu_cores = psutil.cpu_count(logical=False)
            cpu_threads = psutil.cpu_count(logical=True)
            
            # Memory Information
            memory = psutil.virtual_memory()
            memory_total_gb = round(memory.total / (1024**3), 1)
            memory_used_gb = round(memory.used / (1024**3), 1)
            memory_percent = memory.percent
            
            # Disk Information
            disk = psutil.disk_usage('/')
            disk_total_gb = round(disk.total / (1024**3), 1)
            disk_used_gb = round(disk.used / (1024**3), 1)
            disk_percent = disk.percent
            
            # Battery Information
            try:
                battery = psutil.sensors_battery()
                if battery:
                    battery_percent = battery.percent
                    battery_plugged = "Plugged in" if battery.power_plugged else "On battery"
                else:
                    battery_percent = "N/A"
                    battery_plugged = "N/A"
            except:
                battery_percent = "N/A"
                battery_plugged = "N/A"
            
            # System Information
            system_info = f"""
🤖 SYSTEM INFORMATION:

💻 Computer: {platform.node()}
🖥️ OS: {platform.system()} {platform.release()}
⚙️ Architecture: {platform.architecture()[0]}

🚀 CPU: {cpu_cores} cores, {cpu_threads} threads
📊 CPU Usage: {cpu_percent}%
🎯 CPU Frequency: {cpu_freq.current if cpu_freq else 'N/A'} MHz

💾 Memory: {memory_used_gb}GB / {memory_total_gb}GB ({memory_percent}%)
💿 Storage: {disk_used_gb}GB / {disk_total_gb}GB ({disk_percent}%)

🔋 Battery: {battery_percent}% ({battery_plugged})

🌐 Boot Time: {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}
            """
            return system_info.strip()
            
        except Exception as e:
            return f"❌ Error getting system info: {e}"
    
    @staticmethod
    def get_battery_status():
        """Get detailed battery information"""
        try:
            battery = psutil.sensors_battery()
            if battery:
                status = "🔌 Plugged in" if battery.power_plugged else "🔋 On battery"
                time_left = f" ({battery.secsleft//3600}h {(battery.secsleft%3600)//60}m left)" if battery.secsleft > 0 else ""
                return f"🔋 Battery: {battery.percent}% {status}{time_left}"
            else:
                return "🔋 Battery information not available"
        except:
            return "🔋 Battery information not available"
    
    @staticmethod
    def get_storage_info():
        """Get detailed storage information"""
        try:
            partitions = psutil.disk_partitions()
            storage_info = "💾 STORAGE INFORMATION:\n\n"
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    total_gb = round(usage.total / (1024**3), 1)
                    used_gb = round(usage.used / (1024**3), 1)
                    free_gb = round(usage.free / (1024**3), 1)
                    percent = usage.percent
                    
                    storage_info += f"📁 {partition.device} ({partition.fstype})\n"
                    storage_info += f"   Used: {used_gb}GB / {total_gb}GB ({percent}%)\n"
                    storage_info += f"   Free: {free_gb}GB\n\n"
                    
                except Exception:
                    continue
            
            return storage_info.strip()
        except Exception as e:
            return f"❌ Error getting storage info: {e}"
    
    @staticmethod
    def get_running_processes():
        """Get top 5 processes by CPU usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage and get top 5
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            top_processes = processes[:5]
            
            process_info = "🔥 TOP PROCESSES (CPU):\n\n"
            for proc in top_processes:
                process_info += f"📊 {proc['name']}: {proc['cpu_percent']:.1f}% CPU, {proc['memory_percent']:.1f}% RAM\n"
            
            return process_info.strip()
        except Exception as e:
            return f"❌ Error getting process info: {e}"