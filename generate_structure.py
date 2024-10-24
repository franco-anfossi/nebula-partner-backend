import os


def generate_structure(root_dir, output_file, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = []

    def print_tree(dir_path, prefix="", file=None):
        # Filtra las carpetas que deben ser excluidas
        contents = [d for d in os.listdir(dir_path) if d not in exclude_dirs]
        # Ordena el contenido para mantener carpetas y archivos organizados
        contents.sort()
        # Define los punteros para las ramas del árbol
        pointers = ["├── "] * (len(contents) - 1) + ["└── "]

        for pointer, name in zip(pointers, contents):
            path = os.path.join(dir_path, name)
            file.write(f"{prefix}{pointer}{name}\n")
            # Si es un directorio, llama recursivamente para imprimir su contenido
            if os.path.isdir(path):
                extension = "│   " if pointer == "├── " else "    "
                print_tree(path, prefix + extension, file)

    with open(output_file, "w") as f:
        f.write(f"{os.path.basename(root_dir)}/\n")
        print_tree(root_dir, "", f)


if __name__ == "__main__":
    generate_structure(
        ".",
        "estructura.md",
        exclude_dirs=[".git", "__pycache__", "venv", ".ruff_cache"],
    )
