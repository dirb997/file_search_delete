import os
from turtle import mode
import questionary
from send2trash import send2trash
from halo import Halo
from constants import _FILE_SIZES, _DELETE_MODES, EXClUDE_DIRS
from locales import t

def process_file(file_path, mode="trash", dry_run=False):
    """This helper function processes a file based on the selected deletion mode."""
    if dry_run:
        print(t("dry_run", file=file_path))
        return

    try:
        if mode == "trash":
            send2trash(file_path)
            print(t("success_trash", file=file_path))
        elif mode == "permanent":
            os.remove(file_path)
            print(t("success_permanent", file=file_path))
        return True
    except Exception as e:
        key = "failed_to_move_to_trash" if mode == "trash" else "failed_to_delete"
        print(t(key, file=file_path, error=e))
        return False


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
    term_lower = term.lower()
    
    for root, dirs, files in os.walk(start_path, topdown=True):
        dirs[:] = [d for d in dirs if d not in EXClUDE_DIRS]

        for file in files:
            if term_lower in file.lower():
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

            deletion_mode_keys = _DELETE_MODES.keys() if isinstance(_DELETE_MODES, dict) else _DELETE_MODES
            choose_deteletion_mode = questionary.select(
                t("select_mode"),
                choices=[questionary.Choice(title=t(f"{mode}_mode"), value=mode) for mode in deletion_mode_keys]
            ).unsafe_ask()

            if choose_deteletion_mode is None:
                print(t("cancelled"))
                return

            confirm_deletion = t("confirm_trash") if choose_deteletion_mode == "trash" else t("confirm_permanent")
            confirm = questionary.confirm(confirm_deletion).unsafe_ask()

            if confirm:
                success_count = 0
                for file_path in selected_files:
                    if process_file(file_path, mode=choose_deteletion_mode, dry_run=False):
                        success_count += 1
                print(t("cleanup_trash", success=success_count, total=len(selected_files)))
            else:
                print(t("cancelled"))

        except KeyboardInterrupt:
            print(t("keyboard_interrupt"))
            break

if __name__ == "__main__":
    main()