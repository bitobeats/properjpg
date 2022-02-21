from pathlib import Path

import pytest
from PIL import Image

from properjpg import __version__
from properjpg.cli import run


def test_version():
    assert __version__ == "0.3.0"


@pytest.mark.parametrize("output_path", [None, "custom_output.jpg"])
@pytest.mark.parametrize("max_width", [None, 100, 20])
@pytest.mark.parametrize("max_height", [None, 100, 20])
@pytest.mark.parametrize("quality", [None, 80])
@pytest.mark.parametrize(
    ("original_width", "original_height"), [(50, 200), (200, 50), (200, 200)]
)
@pytest.mark.parametrize("img_exist", [False, True])
def test_single_file(
    tmp_path: Path,
    output_path: str,
    max_width: int,
    max_height: int,
    quality: int,
    original_width: int,
    original_height: int,
    img_exist: bool,
) -> None:
    """Tests the main `properjpg [input]` function."""
    # tmp_path.mkdir()
    img_path = Path(tmp_path, "test_image.jpg")

    if not output_path:
        processed_img_path = Path(tmp_path, "test_image-1.jpg")
    else:
        processed_img_path = Path(tmp_path, output_path)

    tmp_img = Image.new("RGB", (original_width, original_height))
    tmp_img.save(img_path)

    if img_exist:
        tmp_img.save(img_path.with_name(f"{img_path.stem}-1.jpg"))
        processed_img_path = img_path.with_name(f"{img_path.stem}-2.jpg")

    args = [str(img_path.resolve())]

    if output_path:
        args.append(str(processed_img_path.resolve()))

    if max_width:
        args.append(f"-wi={max_width}")
    if max_height:
        args.append(f"-he={max_height}")
    if quality:
        args.append(f"-q={quality}")

    run(args)

    assert processed_img_path.is_file()
    with Image.open(processed_img_path) as img:
        if max_width or max_height:
            assert img.size[0] == max_width or img.size[1] == max_height
        else:
            assert img.size == (original_width, original_height)


@pytest.mark.parametrize("output_path", [None, "custom_output", "parent/image-0.jpg"])
@pytest.mark.parametrize("max_width", [None, 100, 20])
@pytest.mark.parametrize("max_height", [None, 100, 20])
@pytest.mark.parametrize(
    ("original_width", "original_height"), [(50, 200), (200, 50), (200, 200)]
)
def test_directory(
    tmp_path: Path,
    output_path: str,
    max_width: int,
    max_height: int,
    original_width: int,
    original_height: int,
) -> None:
    """Tests the `properjpg -d` function."""

    def dir_generator() -> tuple[Path, Path, Path]:
        """Generates files and folders for the test."""
        parent_dir = Path(tmp_path, "parent")
        first_child = Path(parent_dir, "first_child")
        second_child = Path(first_child, "second_child")

        parent_dir.mkdir()
        first_child.mkdir()
        second_child.mkdir()

        tmp_img = Image.new("RGB", (original_width, original_height))

        for index, dir in enumerate((parent_dir, first_child, second_child)):
            for i in range(index + 1):
                img_path = Path(dir, f"image-{i}.jpg")
                tmp_img.save(img_path)

        return parent_dir, first_child, second_child

    parent_dir, first_child, second_child = dir_generator()

    args = [str(parent_dir.resolve())]
    if output_path:
        args.append(str(Path(tmp_path, output_path).resolve()))
        processed_folder_path = Path(tmp_path, output_path)
    else:
        processed_folder_path = Path(tmp_path, "PROPER JPG")

    if max_width:
        args.append(f"-wi={max_width}")
    if max_height:
        args.append(f"-he={max_height}")

    args.append("-d")

    if output_path == "parent/image-0.jpg":
        with pytest.raises(ValueError):
            run(args)
        return
    else:
        run(args)

    # Test folders
    assert processed_folder_path.is_dir()
    assert Path(processed_folder_path, first_child.name).is_dir()
    assert Path(processed_folder_path, first_child.name, second_child.name).is_dir()
    # Test files
    for index, dir in enumerate((parent_dir, first_child, second_child)):
        for i in range(index + 1):
            img_path = Path(dir, f"image-{i}.jpg")
            assert img_path.is_file()


def test_reduce(tmp_path: Path):
    """Tests for "reduce" function."""
    img_path = tmp_path.joinpath("test_image.jpg")
    tmp_img = Image.new("RGB", (100, 100))
    tmp_img.save(img_path)

    args = [
        f"{img_path.resolve()}",
        f"{img_path.with_stem('processed_img').resolve()}",
        "-re=2",
    ]
    run(args)
    with Image.open(img_path.with_stem("processed_img").resolve()) as image:
        assert image.size == (50, 50)


def test_optimize(tmp_path: Path):
    """Tests for "optimize" function."""
    img_path = tmp_path.joinpath("test_image.jpg")
    tmp_img = Image.new("RGB", (100, 100))
    tmp_img.save(img_path)

    args = [
        f"{img_path.resolve()}",
        f"{img_path.with_stem('processed_img').resolve()}",
        "-o",
    ]
    run(args)
    assert img_path.with_stem("processed_img").is_file()


def test_progressive(tmp_path: Path):
    """Tests for "progressive" function."""
    img_path = tmp_path.joinpath("test_image.jpg")
    tmp_img = Image.new("RGB", (100, 100))
    tmp_img.save(img_path)

    args = [
        f"{img_path.resolve()}",
        f"{img_path.with_stem('processed_img').resolve()}",
        "-p",
    ]
    run(args)
    with Image.open(img_path.with_stem("processed_img").resolve()) as image:
        assert image.info["progression"] == True


## Test Exceptions
@pytest.mark.parametrize("input_path", ("invalid_filename.jpg", "invalid_folder"))
@pytest.mark.parametrize("directory", (True, False))
def test_incorrect_input(tmp_path: Path, input_path: str, directory: bool) -> None:
    """Tests for wrong input in `properjpg [input]`."""
    img_path = Path(tmp_path, input_path)
    args = [f"{img_path.resolve()}"]

    if directory:
        args.append(f"-d")

    with pytest.raises((ValueError, FileNotFoundError)):
        run(args)


def test_incorrect_reduce(tmp_path: Path):
    """Tests for "reduce" function."""
    args = ["whatever", "whatever", "-he=100", "-re=2"]
    with pytest.raises((ValueError)):
        run(args)
