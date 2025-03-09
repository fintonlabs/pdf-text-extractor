from setuptools import setup, find_packages

setup(
    name='pdf_processor',
    version='0.1.0',
    description='A Python utility for processing PDF files',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'pandas==1.3.3',
        'PyPDF2==1.26.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)