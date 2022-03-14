# FRC Livescore

A package which can determine the score of a live FRC game from an image.

[![Build](https://github.com/TechplexEngineer/frc-livescore/actions/workflows/build.yml/badge.svg)](https://github.com/TechplexEngineer/frc-livescore/actions/workflows/build.yml)
[![GitHub license](https://img.shields.io/github/license/techplexengineer/frc-livescore)](https://github.com/TechplexEngineer/frc-livescore/blob/main/LICENSE)

## Features

- Access to common parts of the scoreboard (Time, Score, Match Number)
- Easy to use
- Super fast
- Template matching (it doesn't matter where the scoreboard is on the screen)

## Installation

```bash
$ pip install livescore
```

You will also need to have [Tesseract](https://github.com/tesseract-ocr/tesseract/wiki#installation)
and OpenCV 3 (instructions for
[macOS](http://www.pyimagesearch.com/2016/12/19/install-opencv-3-on-macos-with-homebrew-the-easy-way/),
[Windows](http://docs.opencv.org/3.2.0/d5/de5/tutorial_py_setup_in_windows.html) and
[Linux](http://docs.opencv.org/3.2.0/d7/d9f/tutorial_linux_install.html))
installed in order for `frc-livescore` to work.

Tested with python 3.10.

This fork of [andrewda/frc-livescore](https://github.com/andrewda/frc-livescore) updates dependencies, uses ORB algorithm for score board detection which is not restricted by licenses. Add support for 2020, 2021 and 2022 games.

## Usage

*Check out the `examples` or `tests` directory for full examples on the usage of
`frc-livescore`.*

A very simple example program would be to just get the score data from a single
image. To do this, we'll use OpenCV to read the image.

```python
from livescore import Livescore2022
import cv2

# Initialize a new Livescore instance
frc = Livescore2022()

# Read the image from disk
image = cv2.imread('./tests/images/2022/frame1991.png.png')

# Get score data
data = frc.read(image)

print(data)
```

## API

### Constructor

#### LivescoreYEAR(debug=False, save_training_data=False, training_data=None)

> Currently supported years: 2017, 2018, 2019, 2020, 2021, 2022
>
> e.g. Livescore2017(), Livescore2018() or Livescore2019() or Livescore2020() or Livescore2021() or Livescore2022()

- `debug` - Debug mode, where outputs are displayed.
- `save_training_data` - Whether the training should be saved to disk.
- `append_training_data` - Whether to start training from scratch

Creates and returns a new Livescore instance with specified options.

### Methods

#### .read(img, force_find_overlay=False)

- `img` - The image to read from.
- `force_find_overlay` - Whether we should forcefully find the overlay or only do
   so if the overlay cannot be found.

Reads an image and returns an [OngoingMatchDetails](#ongoingmatchdetails) class
containing the score data. Values that could not be determined from the input
image will be `False`.

### Classes

#### AllianceYEAR

> Currently supported years: 2017, 2018, 2019
>
> e.g. Alliance2017, Alliance2018 or Alliance2019

- `score` - The alliance's score.
- ... many more year-specific properties.

Stores year-specific properties for an alliance, such as whether the switch or
scale is owned for the 2018 game.

#### OngoingMatchDetails

- `match_key` - The match key, such as "qf1m2".
- `match_name` - The match name, such as "Qualifications 16 of 128".
- `mode` - The current game mode, one of `pre_match`, `auto`, `teleop`, or
  `post_match`.
- `time` - The time remaining in the match.
- `red` - An [Alliance](#alliance) class for the red alliance.
- `blue` - An [Alliance](#alliance) class for the blue alliance.


