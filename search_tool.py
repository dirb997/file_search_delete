import os
import questionary
from send2trash import send2trash
from halo import Halo
from constants import _FILE_SIZES, _DELETE_MODES

# Constants for file size units

def get_file_size(path):
    """This function calculates the file size and returns a string."""
    try:
        size_bytes = os.path.getsize(path)
        for unit in _FILE_SIZES.keys():
            if size_bytes < _FILE_SIZES[unit] * 1024:
                return f"{size_bytes / _FILE_SIZES[unit]:.1f} {unit}"

    except OSError:
        return "Unknown size"

def search_files(term, start_path):
    matches = []
    
    for root, _, files in os.walk(start_path):
        for file in files:
            if term.lower() in file.lower():
                matches.append(os.path.join(root, file))
                
    return matches

def main():
    while True:
        try:
            search_term = questionary.text(">>> Enter the file name you want to search for:").ask()

            # Handles Ctrl+C or cancellation by the user
            if search_term is None:
                return

            # Handles when user presses Enter on an empty input
            if not search_term.strip():
                print("[!] Search cannot be empty.")
                return

            home_dir = os.path.expanduser("~")
            
            search_path = questionary.path(
                ">>> Enter the path where you want to search:",
                default=home_dir
            ).ask()
            
            if search_path is None:
                return

            spinner = Halo(text=f"[*] Searching for '{search_term}' in '{search_path}'...", spinner='line')
            spinner.start()

            try:
                found_files = search_files(search_term, search_path)
            finally:
                spinner.stop()

            if not found_files:
                print("[-] No files found.")

                retry = questionary.confirm("Do you want to search again?").ask()
                if retry:
                    continue  # Restart the loop cleanly
                else:
                    print("[x] Exiting.")
                    return

            choices = []
            for file_path in found_files:
                size_str = get_file_size(file_path)
                choices.append(questionary.Choice(title=f"{file_path} ({size_str})", value=file_path))

            selected_files = questionary.checkbox(
                "[*] Select the files you want to delete (Space to select, 'a' to select all, Enter to confirm):",
                choices=choices
            ).ask()

            if selected_files is None:
                print("[x] Operation cancelled by the user. Exiting cleanly.")
                return

            if not selected_files:
                print("[x] No files selected. Exiting.")
                return

            choose_deteletion_mode = questionary.select(
                "[*] Choose deletion mode:",
                choices=[questionary.Choice(title=title, value=value) for title, value in _DELETE_MODES.items()]
            ).ask()

            if choose_deteletion_mode == "trash":
                confirm = questionary.confirm(
                    "[*] Are you sure you want to move the selected files to trash?"
                ).ask()

                if confirm:
                    success_count = 0
                    for file_path in selected_files:
                        try:
                            send2trash(file_path)
                            print(f"[+] Moved to trash: {file_path}")
                            success_count += 1
                        except Exception as e:
                            print(f"[-] Failed to move to trash {file_path}: {e}")

                    print(f"\n[*] Cleanup completed. {success_count}/{len(selected_files)} files moved to trash.")
                else:
                    print("[x] Operation cancelled. No files were moved to trash.")

            elif choose_deteletion_mode == "permanent":
                confirm_full_delete = questionary.confirm(
                    "[!] Are you sure you want to permanently delete the selected files? This action cannot be undone."
                ).ask()

                if confirm_full_delete:
                    success_count = 0
                    for file_path in selected_files:
                        try:
                            os.remove(file_path)
                            print(f"[+] Permanently deleted: {file_path}")
                            success_count += 1
                        except Exception as e:
                            print(f"[-] Failed to delete {file_path}: {e}")

                    print(f"\n[*] Cleanup completed. {success_count}/{len(selected_files)} files permanently deleted.")
                else:
                    print("[x] Operation cancelled. No files were permanently deleted.")
            
            # Exit loop after successful execution
            break

        except KeyboardInterrupt:
            print("\n\n[x] The operation has been cancelled by user. Exiting cleanly.")
            break

if __name__ == "__main__":
    main()