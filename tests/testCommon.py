import difflib
import yaml
import cv2.cv2 as cv2

import livescore as ls


def processYear(gameYear, **kwargs):
    error = False

    # Initialize new Livescore instance
    className = "Livescore{}".format(gameYear)
    constructor = getattr(ls, className)
    frc = constructor(**kwargs)

    yamlFile = 'data/{}.yml'.format(gameYear)
    with open(yamlFile) as data:
        values = yaml.load(data)

    if values is None:
        error = True
        print("No images listed in", yamlFile, "\n")
        return

    for fileName in values:
        expected_value = values[fileName]

        # Read the image with OpenCV
        filePath = 'images/{}/{}'.format(gameYear, fileName)
        image = cv2.imread(filePath)
        # image = cv2.resize(image, (720, 720))
        if image is None:
            error = True
            print("ERROR! Unable to open", filePath, "\n")
            continue

        # Get score data
        try:
            data = frc.read(image, force_find_overlay=True)
            # print(data)
        except ls.NoOverlayFoundException as err:
            error = True
            print("ERROR! Unable to find Overlay", fileName, err, "\n")
            continue
        except ls.InvalidScaleException as err:
            error = True
            print("ERROR! Unable to find Overlay", fileName, err, "\n")
            continue

        if str(data) != expected_value:
            error = True

            d = difflib.Differ()
            diff = '\n'.join(d.compare(expected_value.splitlines(), str(data).splitlines()))
            print('[{}] Error Processing: {}\nDiff:\n{}'.format(gameYear, fileName, diff))
        else:
            print('[{}] {}\t Passed'.format(gameYear, fileName))

    return error
