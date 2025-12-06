from setuptools import setup, find_packages

setup(
    name='md2pdf',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'markdown',
        'weasyprint',
        'click',
        'jinja2',
        'pygments',
        'PyYAML',
        'pymdown-extensions',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'md2pdf=cli:cli',
        ],
    },
)
