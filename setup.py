from setuptools import setup, find_packages

setup(
    name='py-tor-ver',
    version='1.0',  # Change this to your version number
    description='A script to verify torrent files',  # Brief description of your package
    author='Clem Morton',  # Your name
    author_email='clem16@gmail.com',  # Your email
    url='https://github.com/cjemorton/py-tor-ver',  # URL to your GitHub repo
    packages=find_packages(),
    scripts=['ptver.py'],  # This will install ptver.py as an executable script
    install_requires=[  # List dependencies here if any
        'libtorrent',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # Or your license
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
