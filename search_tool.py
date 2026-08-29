import os
import questionary

def get_file_size(path):
    """This function calculates the file size and returns a string."""
    try:
        size_bytes = os.path.getsize(path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    except OSError:
        return "Unknown size"

def search_files(term, start_path):
    print(f"\n[*] Searching for '{term}' in '{start_path}'...\n")
    matches = []
    
    for root, _, files in os.walk(start_path):
        for file in files:
            if term.lower() in file.lower():
                matches.append(os.path.join(root, file))
                
    return matches

def main():
    try:
        search_term = questionary.text(">>> Enter the file name you want to search for:").ask()

        if not search_term:
            print("[!] Search cannot be empty.")
            return

        home_dir = os.path.expanduser("~")
        
        # Use questionary.path for auto-complete support when typing directories
        search_path = questionary.path(
            ">>> Enter the path where you want to search:",
            default=home_dir
        ).ask()
        
        if not search_path:
            return

        found_files = search_files(search_term, search_path)

        if not found_files:
            print("[-] No files found.")
            return

        # Format the choices to show the file path AND the file size
        choices = []
        for file_path in found_files:
            size_str = get_file_size(file_path)
            choices.append(questionary.Choice(title=f"{file_path} ({size_str})", value=file_path))

        # Checkbox menu for selecting files to delete
        selected_files = questionary.checkbox(
            "[*] Select the files you want to delete (Space to select, 'a' to select all, Enter to confirm):",
            choices=choices
        ).ask()

        if not selected_files:
            print("[x] No files selected. Exiting.")
            return

        confirm = questionary.confirm(
            f"[WARNING] Are you SURE you want to permanently delete {len(selected_files)} file(s)?"
        ).ask()

        if confirm:
            success_count = 0
            for file_path in selected_files:
                try:
                    os.remove(file_path)
                    print(f"[+] Deleted: {file_path}")
                    success_count += 1
                except Exception as e:
                    print(f"[-] Failed to delete {file_path}: {e}")

            print(f"\n[*] Cleanup completed. {success_count}/{len(selected_files)} files deleted.")
        else:
            print("[x] Deletion cancelled.")

    except KeyboardInterrupt:
        # This will handle the error if the user presses Ctrl+C to quit
        print("\n\n[x] The operation has been cancelled by user. Exiting cleanly.")

if __name__ == "__main__":
    main()