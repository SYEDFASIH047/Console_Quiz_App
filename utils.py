import os
import sys
import time

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_valid_choice(prompt, valid_options):
    """
    Prompts the user for a choice and validates it.
    Input is normalized to uppercase and stripped of whitespace.
    """
    valid_options_upper = [str(opt).upper() for opt in valid_options]
    while True:
        try:
            choice = input(prompt).strip().upper()
            if choice in valid_options_upper:
                return choice
            print(f"Invalid input. Please choose from: {', '.join(valid_options)}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting program...")
            sys.exit(0)

def get_timed_input(prompt, timeout=30):
    """
    Prompts user for input with a countdown timer.
    On Windows, uses msvcrt for character-by-character non-blocking reading.
    On non-Windows (Unix), uses select.select.
    Returns the entered string, or an empty string if timeout is reached.
    """
    if os.name == 'nt':
        import msvcrt
        sys.stdout.write(prompt)
        sys.stdout.flush()
        start_time = time.time()
        input_chars = []
        last_title_update = -1
        
        try:
            while True:
                current_time = time.time()
                elapsed = current_time - start_time
                remaining = max(0.0, timeout - elapsed)
                
                if remaining <= 0:
                    print("\n[Timeout! Time's up for this question.]")
                    # Clear title bar
                    sys.stdout.write("\033]2;Quiz App\007")
                    sys.stdout.flush()
                    return ""
                
                # Update title bar with remaining time
                remaining_secs = int(remaining)
                if remaining_secs != last_title_update:
                    last_title_update = remaining_secs
                    sys.stdout.write(f"\033]2;Quiz App - Time Left: {remaining_secs}s\007")
                    sys.stdout.flush()
                
                if msvcrt.kbhit():
                    char_byte = msvcrt.getch()
                    # Handle special keys (e.g. arrow keys) which send a prefix byte
                    if char_byte in (b'\x00', b'\xe0'):
                        msvcrt.getch()  # consume the secondary byte
                        continue
                    
                    try:
                        char = char_byte.decode('utf-8', errors='ignore')
                    except Exception:
                        continue
                    
                    if char in ('\r', '\n'):
                        print()  # Move to next line
                        break
                    elif char == '\b':  # Backspace
                        if input_chars:
                            input_chars.pop()
                            sys.stdout.write('\b \b')
                            sys.stdout.flush()
                    elif char == '\x03':  # Ctrl+C
                        raise KeyboardInterrupt
                    elif char.isprintable():
                        input_chars.append(char)
                        sys.stdout.write(char)
                        sys.stdout.flush()
                
                time.sleep(0.02)
        except KeyboardInterrupt:
            sys.stdout.write("\033]2;Quiz App\007")
            sys.stdout.flush()
            raise KeyboardInterrupt
            
        # Reset title bar
        sys.stdout.write("\033]2;Quiz App\007")
        sys.stdout.flush()
        return "".join(input_chars).strip()
    else:
        import select
        sys.stdout.write(prompt)
        sys.stdout.flush()
        try:
            rlist, _, _ = select.select([sys.stdin], [], [], timeout)
            if rlist:
                return sys.stdin.readline().strip()
            else:
                print("\n[Timeout! Time's up for this question.]")
                return ""
        except KeyboardInterrupt:
            raise KeyboardInterrupt
