import pygame
import os
import threading
import time

class MusicPlayer:
    def __init__(self, music_dir):
        pygame.mixer.init()
        self.music_dir = music_dir
        self.current_track = None
        self.is_playing = False
        self.volume = 0.5
        self.playlist = []
        self.current_index = 0
        pygame.mixer.music.set_volume(self.volume)
        self.load_playlist_from_directory()
    
    def load_playlist_from_directory(self):
        """Load music files from sara-data/music directory"""
        try:
            if not os.path.exists(self.music_dir):
                print(f"❌ Music directory not found: {self.music_dir}")
                return
            
            music_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac']
            self.playlist = []
            
            for file in os.listdir(self.music_dir):
                if any(file.lower().endswith(ext) for ext in music_extensions):
                    self.playlist.append(os.path.join(self.music_dir, file))
            
            if self.playlist:
                self.current_index = 0
                self.current_track = self.playlist[0]
                print(f"📀 Playlist loaded: {len(self.playlist)} tracks found")
            else:
                print("❌ No music files found in the music directory")
        except Exception as e:
            print(f"❌ Error loading playlist: {e}")
    
    def play_music(self, file_path=None):
        """Play music file from playlist or specific file"""
        try:
            if not self.playlist:
                return "❌ No music files found in E:\\sara-data\\music folder. Please add some music files."
            
            if file_path and os.path.exists(file_path):
                pygame.mixer.music.load(file_path)
                self.current_track = file_path
                track_name = os.path.basename(file_path)
            elif self.current_track:
                pygame.mixer.music.load(self.current_track)
                track_name = os.path.basename(self.current_track)
            else:
                # Play first track from playlist
                self.current_index = 0
                self.current_track = self.playlist[0]
                pygame.mixer.music.load(self.current_track)
                track_name = os.path.basename(self.current_track)
            
            pygame.mixer.music.play()
            self.is_playing = True
            return f"🎵 Now playing: {track_name}\n📀 Playlist: {len(self.playlist)} tracks available"
        except Exception as e:
            return f"❌ Error playing music: {e}"
    
    def stop_music(self):
        """Stop music"""
        try:
            pygame.mixer.music.stop()
            self.is_playing = False
            return "⏹️ Music stopped"
        except Exception as e:
            return f"❌ Error stopping music: {e}"
    
    def pause_music(self):
        """Pause music"""
        try:
            pygame.mixer.music.pause()
            self.is_playing = False
            return "⏸️ Music paused"
        except Exception as e:
            return f"❌ Error pausing music: {e}"
    
    def unpause_music(self):
        """Unpause music"""
        try:
            pygame.mixer.music.unpause()
            self.is_playing = True
            return "▶️ Music resumed"
        except Exception as e:
            return f"❌ Error resuming music: {e}"
    
    def set_volume(self, volume_level):
        """Set volume level (0.0 to 1.0)"""
        try:
            self.volume = max(0.0, min(1.0, volume_level))
            pygame.mixer.music.set_volume(self.volume)
            return f"🔊 Volume set to {int(self.volume * 100)}%"
        except Exception as e:
            return f"❌ Error setting volume: {e}"
    
    def volume_up(self):
        """Increase volume"""
        return self.set_volume(self.volume + 0.1)
    
    def volume_down(self):
        """Decrease volume"""
        return self.set_volume(self.volume - 0.1)
    
    def next_track(self):
        """Play next track in playlist"""
        if not self.playlist:
            return "❌ No playlist loaded"
        
        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.current_track = self.playlist[self.current_index]
        return self.play_music()
    
    def previous_track(self):
        """Play previous track in playlist"""
        if not self.playlist:
            return "❌ No playlist loaded"
        
        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.current_track = self.playlist[self.current_index]
        return self.play_music()
    
    def get_current_track(self):
        """Get currently playing track info"""
        if self.current_track and self.is_playing:
            track_name = os.path.basename(self.current_track)
            return f"🎵 Now playing: {track_name} (Volume: {int(self.volume * 100)}%)"
        elif self.current_track:
            track_name = os.path.basename(self.current_track)
            return f"⏸️ Loaded: {track_name} (Paused)"
        else:
            return "❌ No track loaded"
    
    def get_playlist_info(self):
        """Get playlist information"""
        if not self.playlist:
            return "📀 No music files found in E:\\sara-data\\music"
        
        info = f"📀 Playlist: {len(self.playlist)} tracks from E:\\sara-data\\music\n\n"
        for i, track in enumerate(self.playlist[:5]):  # Show first 5 tracks
            track_name = os.path.basename(track)
            if i == self.current_index:
                info += f"▶️ {i+1}. {track_name}\n"
            else:
                info += f"  {i+1}. {track_name}\n"
        
        if len(self.playlist) > 5:
            info += f"\n... and {len(self.playlist) - 5} more tracks"
        
        return info