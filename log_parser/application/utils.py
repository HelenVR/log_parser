def get_re_model(file_path: str):
    with open(file_path, "r") as file:
        line = file.read().strip()
        return line
