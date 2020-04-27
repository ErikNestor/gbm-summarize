from setuptools import setup

setup(
    name = 'gbm_summarize',
    version = '0.1.0',
    packages = ['gbm_summarize'],
    entry_points = {
        'console_scripts': [
            'gbm_summarize = gbm_summarize.__main__:main'
        ]
    }
)