import os

def cleanup_quotes_in_file(file_path: str):
    """
    Reads the file, strips away any leading/trailing quotes or triple quotes 
    if they wrap the entire file, and then rewrites the cleaned content.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Trim whitespace at start/end
    stripped_content = content.strip()

    # Potential quote fences to remove if they wrap the entire file
    fences = ['"""', "'''", "```", '"', "'"]

    # Try each fence in turn. If the file starts & ends with the same fence, remove them.
    for fence in fences:
        if stripped_content.startswith(fence) and stripped_content.endswith(fence):
            # Remove the leading/trailing fence
            stripped_content = stripped_content[len(fence):-len(fence)].strip()
            # After removing one matching fence pair, break or it might re-check 
            # with single quotes, etc.
            break
    
    if stripped_content.lower().startswith("python"):
        stripped_content = stripped_content[len("python"):].lstrip("\n").lstrip()
    
    # Write back the cleaned content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(stripped_content)

def read_file(path: str) -> str:
    """
    Liest die Datei unter `path` vollständig ein und gibt deren Inhalt
    als String zurück.

    :param path: Pfad zur Datei (absolut oder relativ)
    :return: Inhalt der Datei als String
    :raises FileNotFoundError: wenn die Datei nicht existiert
    :raises IOError / OSError: bei Lese‑/Zugriffsfehlern
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()