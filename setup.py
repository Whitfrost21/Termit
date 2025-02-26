from setuptools import setup

setup(
    name='termit',
    version='0.1',
    py_modules=['termit'],
    install_requires=[
        'click',
        'google-generativeai',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts':[
            'termit=termit:main',
        ],
    },
)
