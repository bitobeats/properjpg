ProperJPG
=========

*Make any image ready for the web. Fast.*

ProperJPG is a super fast, lightweight CLI app that converts images to jpg. It also resizes them!

|

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

Smart resize
~~~~~~~~~~~~

It has a super cool 'smart resize' functionality.
It allows you to set a max width and height, and you can be sure that
every image compressed by it will be no larger or taller than what you
specify. This 'smart resize' mode makes sure to don't resize images
that doesn't need to, and also takes in account if it's best for an
image to be resized based on it's width or height.

Multiprocessing
~~~~~~~~~~~~~~~

This app uses the multiprocessing module to leverage all the power on your computer.
It'll work faster if you have multiple cores.

How it works?
-------------
**This app works in two modes:**

- `"Single file" mode`_
- `"Directory" mode`_





"Single file" mode
~~~~~~~~~~~~~~~~~~
Input an image path and the desired output path.

Usage:
   
::

   properjpg [input_path] [output_path] -wi=[max_width] -he=[max_height]


"Directory" mode
~~~~~~~~~~~~~~~~
This is where this app really shines. Input a directory path and a desired destination
path and the app will clone the folder struct of the original directory on the output path.
Then it will look for all images in the input folder and will try to convert (and
resize, if you setted it to) them.

ProperJPG uses multiprocessing to speed up the process.

Usage:

::

   properjpg [input_path] [output_path] -d -wi=[max_width] -he=[max_height]


Notes
-----
This software is in Alpha stage. A lot of things may change, including syntax and dependencies. I'm looking for help
to improve this tool in terms of speed, features and code readability. Feel free to make suggestions and appoint improvements!.
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

- Improve testing.
- Improve Docs.
- Improve UI (maybe switch to Click?).
- Improve Performance.

Known Issues
~~~~~~~~~~~~

Client
......
- None

Dev
...
- Tests are incomplete.

License
-------
**MIT**
