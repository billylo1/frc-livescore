from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='frc-livescore-ng',
    version='%VERSION%',
    description='Get FRC scores from an image',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Blake Bourque',
    url='https://github.com/TechplexEngineer/frc-livescore',
    keywords=['frc', 'score', 'robotics'],
    license='MIT',
    # package_dir={"": "livescore"},
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'livescore': ['templates/*.png', 'tessdata/*.traineddata', 'training_data/*.pkl']},
    install_requires=[
        'pytesseract==0.3.9',
        'numpy>=1.14.0', #1.22.3
        'regex==2022.3.2',
        'pyyaml==6.0',
        'opencv-python==4.5.5.64',
        'opencv-contrib-python==4.5.5.64',
        'Pillow==9.0.1',
    ]
)
