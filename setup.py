import os
from setuptools import setup, find_packages

def recursive_include(relative_dir):
    all_paths = []
    root_prefix = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'src', 'console')
    full_path = os.path.join(root_prefix, relative_dir)
    for rootdir, _, filenames in os.walk(full_path):
        for filename in filenames:
            abs_filename = os.path.join(rootdir, filename)
            all_paths.append(abs_filename[len(root_prefix) + 1:])
    return all_paths


setup(
    name='console',
    version='0.1.0',
    description='A console app',
    author='Author',
     packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={
        'console': ['py.typed', 'templates/*/*']
    },
    entry_points={
        'console_scripts': [
            'console = console.cli:main',
        ]
    },
    zip_safe=False,
    keywords='console',
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        "typer",
        "typer-cli",
        "pydantic-settings",
        "pydantic",
        "rich",
        "colorama",
        "pandas",
        "elasticsearch",
        "opensearch-dsl",
        "emoji",
        "python-dotenv",
    ],
)