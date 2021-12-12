import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='jellex',
    version='0.5.0',
    author='Kelly Brazil',
    author_email='kellyjonbrazil@gmail.com',
    description='TUI Jello Explorer - filter JSON and JSON Lines data with Python syntax.',
    install_requires=[
        'jello>=1.4.4',
        'prompt-toolkit>=3.0.19',
        'Pygments>=2.4.2'
    ],
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    url='https://github.com/kellyjonbrazil/jellex',
    packages=setuptools.find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'jellex=jellex.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ]
)
