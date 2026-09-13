LANGUAGES = {
    "en": {
        "prompt_search": "Enter the file name you want to search for:",
        "prompt_path": "Enter the path where you want to search:",
        "empty_search": "[!] Search cannot be empty.",
        "searching": "Searching for '{term}' in '{path}'...",
        "no_files": "[-] No files found.",
        "retry": "Do you want to search again?",
        "exiting": "[x] Exiting.",
        "select_delete": "[*] Select the files you want to delete (Space to select, 'a' to select all, Enter to confirm):",
        "no_selected": "[x] No files selected. Exiting.",
        "select_mode": "[*] Choose deletion mode:",
        "trash_mode": "Move to Trash (Recommended)",
        "permanent_mode": "Permanently Delete (Not Recommended)",
        "confirm_trash": "[*] Are you sure you want to move the selected files to trash?",
        "confirm_permanent": "[!] Are you sure you want to permanently delete the selected files? This action cannot be undone.",
        "success_trash": "[+] Moved to trash:",
        "success_permanent": "[+] Permanently deleted:",
        "cleanup_trash": "\n[*] Cleanup completed. {success}/{total} files moved to trash.",
        "cleanup_permanent": "\n[*] Cleanup completed. {success}/{total} files permanently deleted.",
        "cancelled": "[x] Operation cancelled. No files were modified.",
        "keyboard_interrupt": "\n\n[x] The operation has been cancelled by user. Exiting cleanly.",
        "failed_to_move_to_trash": "[!] Failed to move to trash: {file}. Error: {error}",
        "failed_to_delete": "[!] Failed to delete: {file}. Error: {error}",
        "dry_run": "[DRY RUN] Would move to trash: {file}.",
    },
    "es": {
        "prompt_search": "Introduce el nombre del archivo que quieres buscar:",
        "prompt_path": "Introduce la ruta donde quieres buscar:",
        "empty_search": "[!] La búsqueda no puede estar vacía.",
        "searching": "Buscando '{term}' en '{path}'...",
        "no_files": "[-] No se encontraron archivos.",
        "retry": "¿Quieres buscar de nuevo?",
        "exiting": "[x] Saliendo.",
        "select_delete": "[*] Selecciona los archivos que quieres eliminar (Espacio para seleccionar, 'a' para todos, Enter para confirmar):",
        "no_selected": "[x] No se seleccionaron archivos. Saliendo.",
        "select_mode": "[*] Elige el modo de eliminación:",
        "trash_mode": "Mover a la papelera (Recomendado)",
        "permanent_mode": "Eliminar permanentemente (No recomendado)",
        "confirm_trash": "[*] ¿Estás seguro de que quieres mover los archivos seleccionados a la papelera?",
        "confirm_permanent": "[!] ¿Estás seguro de que quieres eliminar permanentemente los archivos seleccionados? Esta acción no se puede deshacer.",
        "success_trash": "[+] Movido a la papelera: {file}",
        "success_permanent": "[+] Eliminado permanentemente: {file}",
        "cleanup_trash": "\n[*] Limpieza completada. {success}/{total} archivos movidos a la papelera.",
        "cleanup_permanent": "\n[*] Limpieza completada. {success}/{total} archivos eliminados permanentemente.",
        "cancelled": "[x] Operación cancelada. No se modificaron archivos.",
        "keyboard_interrupt": "\n\n[x] Operación cancelada por el usuario. Saliendo de la herramienta.",
        "failed_to_move_to_trash": "[!] No se pudo mover a la papelera: {file}. Error: {error}",
    },
    # Future languages can be added here -> "fr": { ... }, "de": { ... }, etc.
}

# Set the active language here (or load it from an environment variable/config file)
CURRENT_LANG = "es"

def t(key, **kwargs):
    """Translate string and format variables if needed."""
    text = LANGUAGES.get(CURRENT_LANG, LANGUAGES["en"]).get(key, key)
    return text.format(**kwargs)