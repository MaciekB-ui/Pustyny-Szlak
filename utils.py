def get_not_empty_input(label: str) -> str:
    while True:
        if name := input(label).strip():
            return name
        print("Nazwa nie może być pusta.")
