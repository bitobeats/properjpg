import mimetypes
import os
from pathlib import Path


def ignore_files(dir: str, files: list[str]):
    """
    Returns a list of files to ignore.

    To be used by shutil.copytree()
    """
    return [f for f in files if Path(dir, f).is_file()]


def get_input_images(input_folder: Path, output_path: Path):
    """
    Get all images from a folder and it's subfolders.

    Also outputs a save path to be used by the image.

    :param input_folder: The folder to be scanned.
    :param output_path: The root folder of the destination path.
    """
    for root, _, files in os.walk(input_folder):
        for file in files:
            mime_type = mimetypes.guess_type(file)[0]

            if isinstance(mime_type, str):
                if "image" in mime_type:
                    image = Path(root, file)
                    relative_path = image.relative_to(input_folder)
                    save_path = Path(output_path, relative_path)
                    yield image, save_path


def generate_filename(input_path: Path) -> Path:
    gen_counter = 1
    gen_output = input_path.with_name(f"{input_path.stem}-{gen_counter}").with_suffix(
        ".jpg"
    )

    while gen_output.is_file():
        gen_counter += 1
        gen_output = input_path.with_name(
            f"{input_path.stem}-{gen_counter}"
        ).with_suffix(".jpg")

    output_path = gen_output
    return output_path
