from setuptools import setup

setup(
    name='opgg-helper',
    description='CLI tool for increase accessibility to OP.GG stats',
    version='0.0.1',
    url='https://github.com/JoMingyu/opgg-helper',
    license='MIT License',
    author='PlanB',
    author_email='mingyu.planb@gmail.com',
    maintainer='PlanB',
    maintainer_email='mingyu.planb@gmail.com',
    install_requires=[
        'click',
        'bs4',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=['helper'],
    entry_points={
        'console_scripts': [
            'opgg = helper.cli:handler',
        ],
    },
)
