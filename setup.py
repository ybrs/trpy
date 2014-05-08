from setuptools import setup

setup(
    name='trpy',
    version='0.1',
    long_description=__doc__,
    packages=['trpy'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points = {
        'console_scripts': [
            'trpy = trpy.translate:run_file',
        ],
    }
)
