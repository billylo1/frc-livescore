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
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'livescore': ['templates/*.png', 'tessdata/*.traineddata', 'training_data/*.pkl']}
)
