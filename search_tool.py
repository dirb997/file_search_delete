import os
import questionary
from send2trash import send2trash
from halo import Halo
from constants import _FILE_SIZES, _DELETE_MODES
from locales import t

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
            search_term = questionary.text(t("prompt_search"), qmark=">>>").unsafe_ask()

            # Handles Ctrl+C or cancellation by the user
            if search_term is None:
                print(t("cancelled"))
                return

            # Handles when user presses Enter on an empty input
            if not search_term.strip():
                print(t("empty_search"))
                return

            home_dir = os.path.expanduser("~")
            
            search_path = questionary.path(
                t("prompt_path"),
                default=home_dir,
                qmark=">>>"
            ).unsafe_ask()
            
            if search_path is None:
                return

            spinner = Halo(text=f"[*] {t('searching', term=search_term, path=search_path)}", spinner='bouncingBar', placement='right')
            spinner.start()

            try:
                found_files = search_files(search_term, search_path)
            finally:
                spinner.stop()

            if not found_files:
                print(t("no_files"))

                retry = questionary.confirm(t("retry"), qmark=">>>").unsafe_ask()
                if retry:
                    continue  # Restart the loop cleanly
                else:
                    print(t("exiting"))
                    return

            choices = []
            for file_path in found_files:
                size_str = get_file_size(file_path)
                choices.append(questionary.Choice(title=f"{file_path} ({size_str})", value=file_path))

            selected_files = questionary.checkbox(
                t("select_delete"),
                choices=choices
            ).unsafe_ask()

            if selected_files is None:
                print(t("cancelled"))
                return

            if not selected_files:
                print(t("no_selected"))
                return

            choose_deteletion_mode = questionary.select(
                t("select_mode"),
                choices=[questionary.Choice(title=t(f"{value}_mode"), value=value) for value in _DELETE_MODES.items()]
            ).unsafe_ask()

            if choose_deteletion_mode is None:
                print(t("cancelled"))
                return

            if choose_deteletion_mode == "trash":
                confirm = questionary.confirm(
                    t("confirm_trash")
                ).unsafe_ask()

                if confirm:
                    success_count = 0
                    for file_path in selected_files:
                        try:
                            send2trash(file_path)
                            print(t("success_trash", file=file_path))
                            success_count += 1
                        except Exception as e:
                            print(t("failed_to_move_to_trash", file=file_path, error=e))

                    print(t("cleanup_trash", success=success_count, total=len(selected_files)))
                else:
                    print(t("cancelled"))

            elif choose_deteletion_mode == "permanent":
                confirm_full_delete = questionary.confirm(
                    t("confirm_permanent")
                ).unsafe_ask()

                if confirm_full_delete:
                    success_count = 0
                    for file_path in selected_files:
                        try:
                            os.remove(file_path)
                            print(t("success_permanent", file=file_path))
                            success_count += 1
                        except Exception as e:
                            print(t("failed_to_delete", file=file_path, error=e))

                    print(t("cleanup_permanent", success=success_count, total=len(selected_files)))
                else:
                    print(t("cancelled"))
            
            # Exit loop after successful execution
            break

        except KeyboardInterrupt:
            print(t("keyboard_interrupt"))
            break

if __name__ == "__main__":
    main()