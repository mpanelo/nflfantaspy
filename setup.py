from setuptools import setup

setup(
    name="nflfantaspy",
    version="0.1.0",
    description="Scrape public NFL fantasy league data and save it as JSON or on Airtable.",
    url="https://github.com/mpanelo/nflfantaspy",
    author="Mauricio Panelo",
    author_email="17281354+mpanelo@users.noreply.github.com",
    license="MIT",
    packages=["nflfantaspy"],
    install_requires=[
        "beautifulsoup4==4.10.0",
        "certifi==2021.10.8",
        "charset-normalizer==2.0.11",
        "idna==3.3",
        "pyairtable==1.0.0.post1",
        "requests==2.27.1",
        "soupsieve==2.3.1",
        "urllib3==1.26.8",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
    ],
)
