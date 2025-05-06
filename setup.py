import os
from setuptools import setup, find_packages

setup(
    name='audio-downloader-cli',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A CLI tool to download audio from YouTube and other sites using yt-dlp.',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/audio-downloader-cli', # Optional: Replace with your project's URL
    py_modules=['audio_downloader'],
    install_requires=[
        'yt-dlp',
    ],
    entry_points={
        'console_scripts': [
            'audio-downloader-cli=audio_downloader:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', # Optional: Choose an appropriate license
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities',
        'Environment :: Console',
    ],
    python_requires='>=3.6',
)