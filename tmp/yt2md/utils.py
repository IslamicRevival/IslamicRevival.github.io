def string_to_filename(filename, raw=False):
    """if raw, will delete all illegal characters. Else will replace '?' with '¿' and all others with '-'"""
    illegal_characters_in_file_names = r'"/\*?<>|:'

    if raw:
        return ''.join(c for c in filename if c not in illegal_characters_in_file_names)

    for x in [["?", "¿"]] + [[x, "-"] for x in illegal_characters_in_file_names.replace("?", "")]:
        filename = filename.replace(x[0], x[1])
    return filename
