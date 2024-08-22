import setuptools

setuptools.setup(
    name="LevelZero Contract Mapper",
    version="0.0.1",
    author="archi.ac",
    author_email="dont@message.me",
    url="https://github.com/Toast-arch/LZE-contract-mapper",
    packages=['lzcm'],
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.9",
    install_requires=[
        "pyqt5",
        "pillow"
    ]
)