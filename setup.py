import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Based off https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56
setuptools.setup(
    name='Geit',
    packages=setuptools.find_packages(),
    version='0.0.1',
    license='MIT',
    description='Geit provides contribution insights on software group projects that use Git',
    author='Khalid El Haji',
    author_email='khalid.el.haji@gmail.com',
    url='https://github.com/kelhaji/geit',
    keywords=['GIT', 'INSIGHTS', 'STATISTICS', 'EDUCATIONAL', 'CONTRIBUTIONS', 'DATA'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'GitPython',
        'binaryornot',
        'Click',
        'python'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Topic :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Natural Language :: English'
    ],
    python_requires='>=3.6',
)