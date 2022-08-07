import mimetypes
from functools import cache
from pathlib import Path

from PIL import Image


def process_image(
    image_path: Path,
    output_path: Path,
    max_width: int = 0,
    max_height: int = 0,
    quality: int = 0,
    reduce: int = 0,
    optimize: bool = False,
    no_progressive: bool = False,
) -> None:
    """
    Process the image.

    :param image_path: The original image path.
    :param output_path: The path where the processed image should be saved.
    :param max_width: The max width the processed image can have.
    :param max_height: The max height the processed image can have.
    :param quality: The quality when optimizing an image.
    :param reduce: The factor by which the image will be resized.
    """
    print("Processing image: ", image_path)
    kwargs: dict[str, int | bool] = dict()
    with Image.open(image_path) as image:
        if reduce != 0:
            image = reduce_image(image, reduce)

        if max_width != 0 or max_height != 0:
            ## If width or height is set.
            image = resize_image(image, max_width, max_height)

        if not "jpg" in mimetypes.guess_type(image_path):
            image = image.convert("RGB")

        if quality != 0:
            kwargs["quality"] = quality
        else:
            kwargs["quality"] = 85
        if optimize:
            kwargs["optimize"] = True
        if no_progressive:
            kwargs["progressive"] = False
        else:
            kwargs["progressive"] = True

        image.save(output_path.with_suffix(".jpg"), **kwargs)  # type: ignore


def resize_image(
    image: Image.Image, max_width: int = 0, max_height: int = 0
) -> Image.Image:
    """
    Resize an image and return it.

    :param image: A Pill.Image object.
    :param max_width: The max width the processed image can have.
    :param max_height: The max height the processed image can have.
    """
    old_width, old_height = image.size[0], image.size[1]

    @cache
    def get_proper_sizes(
        max_width: int, max_height: int, old_width: int, old_height: int
    ) -> tuple[int, int]:

        new_width, new_height = max_width, max_height

        if max_width == 0:
            """If width is not set."""
            new_width = round(old_width * (max_height / old_height))
        elif max_height == 0:
            """If height is not set."""
            new_height = round(old_height * (max_width / old_width))
        else:
            if old_width > old_height:
                """If image's original width is bigger than original height."""
                new_height = round(old_height * (new_width / old_width))
            elif old_height > old_width:
                """If image's original height is bigger than original width."""
                new_width = round(old_width * (new_height / old_height))
            elif old_width == old_height:
                """If image's original width and height are the same."""
                if max_width > max_height:
                    """If new width is bigger than new height."""
                    new_width = max_height
                elif max_height > max_width:
                    """If new height is bigger than new width."""
                    new_height = max_height

        if new_width > max_width and max_width != 0:
            new_width = max_width
            new_height = round(old_height * (new_width / old_width))
        if new_height > max_height and max_height != 0:
            new_height = max_height
            new_width = round(old_width * (new_height / old_height))

        new_width = new_width
        new_height = new_height

        return new_width, new_height

    new_width, new_height = get_proper_sizes(
        max_width, max_height, old_width, old_height
    )

    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return image


def reduce_image(image: Image.Image, factor: int) -> Image.Image:
    """Reduce images by percentage.

    :param image: The image to be reduced
    :param factor: The "x" times the image will be resized to."""
    result = image.reduce(factor)
    return result
