import argparse
import multiprocessing as mp
import sys
import time
from functools import partial
from pathlib import Path
from shutil import copytree

from . import __version__
from .filesmanager import generate_filename, get_input_images, ignore_files
from .processing import process_image


def run(args=None):
    """
    Main CLI function.

    :param list[str] args: A list of arguments to be passed to the CLI.
    """
    if not args:
        args = sys.argv[1:]  # pragma: no cover

    parser = argparse.ArgumentParser(
        description="""ProperJPG aims to be a fast tool to convert and optimize any image before using it
        on the web. It does so by automatically stripping some meta data and also allowing easy resizing
        of a single or multiple images at once.
        
        Type 'properjpg -h' for help."""
    )
    parser.add_argument(
        "input", type=Path, help="The path to the file or folder to be used as input."
    )
    parser.add_argument(
        "output",
        type=Path,
        nargs="?",
        default=None,
        help="The path to the file or folder to save the output file(s).",
    )
    parser.add_argument(
        "-d",
        "--directory",
        action="store_true",
        help="""Acceps directories. Copy the original directory tree,
        search for all image files and tries to convert and save them to the selected output folder.
        In case no output folder is provided, "PROPER JPG" is created in the parent of the input folder.""",
    )
    parser.add_argument(
        "-wi",
        "--max-width",
        type=int,
        default=0,
        help="Sets the max width. Output images will be resized to this value or less.",
    )
    parser.add_argument(
        "-he",
        "--max-height",
        type=int,
        default=0,
        help="Sets the max height. Output images will be resized to this value or less.",
    )
    parser.add_argument(
        "-re",
        "--reduce",
        type=int,
        default=0,
        help='Set a value to turn "reduce" mode on. In this mode, the image will be resized by the x fator introduced in this flag.',
    )
    parser.add_argument(
        "-o",
        "--optimize",
        action="store_true",
        help="If set, the encoder will make an extra pass over the image in order to select optimal encoder settings.",
    )
    parser.add_argument(
        "-np",
        "--no-progressive",
        action="store_true",
        help="If set, disables progressive jpeg and saves as baseline instead.",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=0,
        help="""If set, the input will be compressed to the set value (using Pillow library). Choose a value from 1 to 95.
    
    ATTENTION: This is being tested. It may behave unpredictably.""",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"ProperJPG {__version__}"
    )

    args = parser.parse_args(args)
    input_path: Path = args.input

    max_width: int = args.max_width
    max_height: int = args.max_height
    reduce: int = args.reduce
    optimize: bool = args.optimize
    no_progressive: bool = args.no_progressive
    quality: int = args.quality

    if reduce != 0:
        if max_width != 0 or max_height != 0:
            raise ValueError("You can't use --re with --wi or --he.")

    if args.output is None:
        if args.directory:
            output_path = input_path.parent.joinpath("PROPER JPG")
        else:
            output_path = generate_filename(input_path)
    else:
        output_path: Path = args.output

    print("Output path: ", output_path.resolve())

    if args.directory:
        print("STARTING PROCESS")
        start_time = time.perf_counter()

        try:
            assert input_path.is_dir()
        except:
            raise ValueError(
                f"The input path '{input_path.resolve()}' is not a directory."
            )

        try:
            assert not output_path.is_file()
        except:
            raise ValueError(
                f"The output path '{output_path.resolve()}' is not a directory."
            )

        copytree(input_path, output_path, ignore=ignore_files)

        image_list = [
            (image, save_path)
            for image, save_path in get_input_images(input_path, output_path)
        ]

        with mp.Pool() as pool:
            pool.starmap(
                partial(
                    process_image,
                    max_width=max_width,
                    max_height=max_height,
                    reduce=reduce,
                    optimize=optimize,
                    quality=quality,
                    no_progressive=no_progressive,
                ),
                image_list,
            )

        end_time = time.perf_counter()
        print("")
        print("DONE")
        print(f"Elapsed time: {end_time - start_time}")
        print(f"Images processed: {len(image_list)}")

    else:
        print("STARTING PROCESS")
        start_time = time.perf_counter()

        try:
            assert input_path.is_file()
        except:
            raise ValueError(f"The input path '{input_path.resolve()}' is not a file.")

        process_image(
            input_path,
            output_path,
            max_width,
            max_height,
            quality,
            reduce,
            optimize,
            no_progressive,
        )

        end_time = time.perf_counter()
        print("")
        print("DONE")
        print(f"Elapsed time: {end_time - start_time}")

    print("Output path: ", output_path.resolve())
