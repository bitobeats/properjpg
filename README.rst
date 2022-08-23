.. |pypi| image:: https://img.shields.io/pypi/v/properjpg
.. |pythonver| image:: https://img.shields.io/pypi/pyversions/properjpg
.. |downloads| image:: https://img.shields.io/pypi/dm/properjpg
.. |build| image:: https://img.shields.io/github/workflow/status/vitorrloureiro/properjpg/Tests
.. |cov| image:: https://img.shields.io/codecov/c/github/vitorrloureiro/properjpg
.. |wheel| image:: https://img.shields.io/pypi/wheel/properjpg
.. |license| image:: https://img.shields.io/pypi/l/properjpg


ProperJPG
=========

*Convert images to optimized JPEGs. Fast.*

|

|pypi| |pythonver| |build| |cov| |wheel| |downloads| |license|

ProperJPG is a super fast, lightweight CLI app that converts and compress images to optimized jpg.If you like, it can also resize them!

If you need a tool to batch convert and optimize images
making them "ready for the web", this may be the tool for you.

It works by accepting almost all image formats and converting them to JPEG, while compressing and stripping metadata in the process.

ProperJPG allows you to set a max width/height so any images that crosses the threshold is atuomatically resized while keeping the correct aspect ratio.

It also allows you to input a folder with multiple images. In this case, ProperJPG clones the original folder structure in the output path.



**Actively soliciting contributors!**

Feel free to open a pull request in case you find an issue or a way to improve the 
app. New features are also welcome, considering they don't add unecessary complexity to the
user experience.

Installation
------------

- `Regular`_
- `Developer`_

Regular
~~~~~~~
**Pipx (recommended)**
   
::

   pipx install properjpg

**Pip**

::

   pip install properjpg

Developer
~~~~~~~~~
**Poetry**

::

   poetry add properjpg

**Git**

::

   git clone https://github.com/vitorrloureiro/properjpg

Features
--------

- `Smart resize`_
- `Multiprocessing`_
- `Progressive JPG`_

Smart resize
~~~~~~~~~~~~

It has a super cool 'smart resize' functionality.
It allows you to set a max width and height, and you can be sure that
every image compressed by it will be no larger or taller than what you
specify. This 'smart resize' mode makes sure to don't resize images
that doesn't need to, and also takes in account if it's best for an
image to be resized based on it's width or height.

Progressive JPG
~~~~~~~~~~~~~~~

Images are saved as progressive JPEG as default. You can disable this behaviour
with `-np` flag. Learn more `here <https://www.thewebmaster.com/develop/articles/how-progressive-jpegs-can-speed-up-your-website/>`_

Multiprocessing
~~~~~~~~~~~~~~~

This app uses the multiprocessing module to leverage all the power on your computer.
It'll work faster if you have multiple cores.

How does it work?
-----------------
**This app works in two modes:**

- `"Single file" mode`_
- `"Directory" mode`_

"Single file" mode
~~~~~~~~~~~~~~~~~~
Input an image path and the desired output path.

Basic usage:
   
::

   properjpg [input_path] [output_path] -wi=[max_width] -he=[max_height]


"Directory" mode
~~~~~~~~~~~~~~~~
This is where this app really shines. Input a directory path and a desired destination
path and the app will clone the folder struct of the original directory on the output path.
Then it will look for all images in the input folder and will try to convert (and
resize, if you setted it to) them.

ProperJPG uses multiprocessing to speed up the process.

Basic usage:

::

   properjpg [input_path] [output_path] -d -wi=[max_width] -he=[max_height]


Commands
--------

-h    Shows the help screen.
-d    Turns on directory mode.
-o    If set, the encoder will make an extra pass in order to select optimal encoder settings.
-q    If set, the input will be compressed to the set value (using Pillow library). Choose a value from 1 to 95.
-np   If set, disables progressive jpeg and saves as baseline instead.
-wi   Sets the max width.
-he   Sets the max height.
-re   Turns on "reduce" mode and set the factore to which the images are to be resized.
-v    Shows ProperJPG's version.





Notes
-----
This software is in Alpha stage. A lot of things may change, including syntax and dependencies. I'm looking for help
to improve this tool in terms of speed, features and code readability. Feel free to make suggestions and improvements!.
Also feel free to help me improve the tests 😅

The goal is to always keep the code with 100% test coverage.

Contributing
------------

Requirements
~~~~~~~~~~~~

This repository automatically lints code with flake8 and black, and also runs mypy
and pytest. Pull requests must pass in all those tests.

- `black <https://github.com/psf/black>`_
- `flake8 <https://github.com/PyCQA/flake8>`_
- `mypy <https://github.com/python/mypy>`_
- `pytest <https://github.com/pytest-dev/pytest>`_

Roadmap
~~~~~~~

- Improve UI (maybe switch to Click? Add Colorama?).
   - Add a better progress view when using `"Directory" Mode`_
- Improve testing.
- Improve Docs.
- Improve Performance.

Known Issues
~~~~~~~~~~~~

Client
......
- None

Dev
...
- 100% coverage, but tests are a mess.
- Improve GitHub Action.
- Create a workflow for :code:`poetry publish --build`

License
-------
**MIT**
