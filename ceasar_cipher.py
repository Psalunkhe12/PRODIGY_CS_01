import sys
import subprocess
import shutil

# Color and style class using ANSI escape sequences
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'      # Reset
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def encrypt(message, shift):
    encrypted_message = ""
    for char in message:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            encrypted_message += encrypted_char
        else:
            encrypted_message += char
    return encrypted_message

def decrypt(encrypted_message, shift):
    decrypted_message = ""
    for char in encrypted_message:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - shift_base - shift) % 26 + shift_base)
            decrypted_message += decrypted_char
        else:
            decrypted_message += char
    return decrypted_message

def get_shift():
    while True:
        shift_input = input(f"{Colors.WARNING}Enter the shift value (1-25): {Colors.ENDC}").strip()
        if not shift_input.isdigit():
            print(f"{Colors.FAIL}Invalid input. Please enter a number between 1 and 25.{Colors.ENDC}")
            continue
        shift = int(shift_input)
        if 1 <= shift <= 25:
            return shift
        else:
            print(f"{Colors.FAIL}Shift value must be between 1 and 25.{Colors.ENDC}")

def show_output_in_new_terminal(output_text):
    terminals = [
        ("gnome-terminal", ["gnome-terminal", "--"]),
        ("konsole", ["konsole", "-e"]),
        ("xterm", ["xterm", "-hold", "-e"]),
        ("xfce4-terminal", ["xfce4-terminal", "-H", "-e"]),
        ("lxterminal", ["lxterminal", "-e"]),
        ("mate-terminal", ["mate-terminal", "-e"]),
        ("terminator", ["terminator", "-x"])
    ]

    # Escape characters for safe terminal use
    safe_text = output_text.replace('\\', '\\\\').replace('"', '\\"')

    for term_name, base_cmd in terminals:
        if shutil.which(term_name):
            bash_command = f'echo -e "{safe_text}"; echo; echo "Press ENTER to close..."; read -r'
            full_cmd = base_cmd + ["bash", "-c", bash_command]
            try:
                subprocess.Popen(full_cmd)
                return True
            except Exception:
                continue

    print(f"\n{Colors.FAIL}No supported terminal emulator found to display output in a new window.{Colors.ENDC}")
    print("Output:\n" + output_text)
    return False

def main():
    # Clear the terminal first
    subprocess.call('clear' if shutil.which('clear') else 'cls', shell=True)

    print(f"{Colors.HEADER}{'='*55}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.OKCYAN}🔐 Welcome to the Advanced Caesar Cipher Program 🔐{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*55}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}Features:{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}- Encrypt and decrypt messages{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}- 🎯 Supports uppercase and lowercase letters{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}- 🛡️  Preserves spaces, punctuation, and numbers{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}- 🪟 Output shown in a separate terminal window{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}- 💾 Option to save output to a file{Colors.ENDC}")
    print(f"  {Colors.OKGREEN}- 👌 Clear and user-friendly prompts{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*55}{Colors.ENDC}")

    while True:
        choice = input(f"\n{Colors.BOLD}Choose an option:{Colors.ENDC}\n[E] Encrypt\n[D] Decrypt\n[Q] Quit\nEnter choice: ").strip().upper()
        if choice == 'Q':
            print(f"\n{Colors.OKCYAN}Thank you for using the Caesar Cipher Program. Goodbye! 💖{Colors.ENDC}")
            sys.exit(0)
        elif choice in ['E', 'D']:
            message = input(f"{Colors.OKBLUE}Enter your message: {Colors.ENDC}")
            if not message.strip():
                print(f"{Colors.FAIL}Message cannot be empty. Please try again.{Colors.ENDC}")
                continue
            shift = get_shift()
            if choice == 'E':
                result = f"{Colors.BOLD}{Colors.OKGREEN}🔐 Encrypted Message:\n{encrypt(message, shift)}{Colors.ENDC}"
            else:
                result = f"{Colors.BOLD}{Colors.OKCYAN}🔓 Decrypted Message:\n{decrypt(message, shift)}{Colors.ENDC}"

            # Show output in a new terminal window
            if not show_output_in_new_terminal(result):
                print("\n" + result)

            save_choice = input(f"\n{Colors.WARNING}Would you like to save the output to a file? (y/n): {Colors.ENDC}").strip().lower()
            if save_choice == 'y':
                filename = input(f"{Colors.OKBLUE}Enter the filename (e.g., output.txt): {Colors.ENDC}").strip()
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        # Remove color codes when saving
                        from re import sub
                        plain_result = sub(r'\033\[[0-9;]*m', '', result)
                        f.write(plain_result)
                    print(f"{Colors.OKGREEN}Output saved successfully to {filename}{Colors.ENDC}")
                except Exception as e:
                    print(f"{Colors.FAIL}Failed to save output: {e}{Colors.ENDC}")
        else:
            print(f"{Colors.FAIL}Invalid choice. Please enter E, D, or Q.{Colors.ENDC}")

if __name__ == "__main__":
    main()

