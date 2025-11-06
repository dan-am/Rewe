from setuptools import find_packages, setup

setup(
    name='rewe',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    version='0.1.0',
    description='Analytical Python project for Rewe',
    author='Your Name',
    license='MIT',
    install_requires=[
        'numpy>=1.24.0',
        'pandas>=2.0.0',
        'matplotlib>=3.7.0',
        'seaborn>=0.12.0',
        'scipy>=1.10.0',
        'python-dotenv>=1.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.3.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'isort>=5.12.0',
            'mypy>=1.0.0',
        ],
        'notebooks': [
            'jupyter>=1.0.0',
            'ipykernel>=6.0.0',
        ],
    },
    python_requires='>=3.8',
)
