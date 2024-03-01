import setuptools
import sys

if sys.version_info < (3, 6):
    raise RuntimeError("hms-python requires Python 3.6+")


setuptools.setup(
    name='hms-python',
    version="1.0.0",
    author="Adrián Carrera (EMMA MOBILE SOLUTIONS)",
    author_email="tech@emma.io",
    description="Simple hms client to send push notification to Huawei devices.",
    url="https://github.com/EMMADevelopment/hms-python",
    license='Apache 2',
    packages=setuptools.find_packages(),
    classifiers=[
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: AsyncIO',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Apache Software License 2.0',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'aiohttp>=3.6.2',
        'cchardet>=2.1.6',
        'aiodns>=2.0.0',
        'brotlipy>=0.7',
        'urllib3>=1.0.0',
    ]
)