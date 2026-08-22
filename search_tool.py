import os
import questionary

def search_files(term, start_path):
        """
        This function searches for files matching the term from a given path
        """

        print(f"\nSearching for '{term}' in '{start_path}'...")

        matches = []
        for root, _, files in os.walk(start_path):
            for file in files:
                if term.lower() in file.lower():
                    matches.append(os.path.join(root, file))

        return matches


def main():
        
        search_term = questionary.text("Enter the file name you want to search for:").ask()

        if not search_term:
            print("Search cannot be empty.")
            return

        home_dir = os.path.expanduser("~")
        search_path = questionary.text(
            "Enter the path where you want to search:",
            default=home_dir
        ).ask()

        found_files = search_files(search_term, search_path)

        if not found_files:
            print("No files found")
            return

        print(f"\nFound {len(found_files)} file(s):")
        for file_path in found_files:
            print(file_path)

        confirm = questionary.confirm(
            f"Are you SURE you want to delete {len(found_files)} file(s)"
        ).ask()

        if confirm:
            for file_path in found_files:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

            print("\nCleanup completed.")
        else:
            print("Deletion cancelled.")

if __name__ == "__main__":
    main()
