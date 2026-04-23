"""
Sound effects for Bubble Flow Web Builder
Uses system beep for cross-platform compatibility
"""

import sys
import winsound
import threading

class SoundEffects:
    """Simple sound effects using system beeps"""
    
    @staticmethod
    def play_async(frequency, duration):
        """Play sound in background thread to not block UI"""
        def play():
            try:
                if sys.platform == 'win32':
                    winsound.Beep(frequency, duration)
            except:
                pass  # Silently fail if sound not available
        
        thread = threading.Thread(target=play, daemon=True)
        thread.start()
    
    @staticmethod
    def node_pickup():
        """Sound when picking up a node"""
        SoundEffects.play_async(800, 50)  # High pitch, short
    
    @staticmethod
    def node_drop():
        """Sound when dropping a node"""
        SoundEffects.play_async(600, 80)  # Medium pitch, slightly longer
    
    @staticmethod
    def node_added():
        """Sound when adding a new node"""
        SoundEffects.play_async(1000, 100)  # Higher pitch, success sound
    
    @staticmethod
    def connection_start():
        """Sound when starting a connection"""
        SoundEffects.play_async(700, 60)  # Medium-high pitch
    
    @staticmethod
    def connection_complete():
        """Sound when completing a connection"""
        # Two-tone success sound
        SoundEffects.play_async(800, 80)
        threading.Timer(0.1, lambda: SoundEffects.play_async(1000, 80)).start()
    
    @staticmethod
    def wiggle_activate():
        """Sound when wiggle mode activates"""
        # Rising tone
        SoundEffects.play_async(600, 60)
        threading.Timer(0.08, lambda: SoundEffects.play_async(800, 60)).start()
        threading.Timer(0.16, lambda: SoundEffects.play_async(1000, 80)).start()
    
    @staticmethod
    def cancel():
        """Sound when cancelling an action"""
        SoundEffects.play_async(400, 100)  # Low pitch, cancel sound
    
    @staticmethod
    def hover():
        """Subtle sound when hovering over a node"""
        SoundEffects.play_async(900, 30)  # Very short, high pitch
