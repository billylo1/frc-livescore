from setuptools import setup, find_packages

setup(
    name='frc-livescore-ng',
    version='%VERSION%',
    description='Get FRC scores from an image',
    author='Blake Bourque',
    url='https://github.com/TechplexEngineer/frc-livescore',
    keywords=['frc', 'score', 'robotics'],
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'livescore': ['templates/*.png', 'tessdata/*.traineddata', 'training_data/*.pkl']}
)
