import os, sys
from setuptools import setup, find_packages

version = '0.1.0'

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

setup(
    name='django-yamaps',
    version=version,
    author='herald-it',
    author_email='wessmoke@gmail.com',
    maintainer='Dmitry Shlagov',
    maintainer_email='wessmoke@gmail.com',

    url='https://github.com/herald-it/django-yamaps',
    download_url='https://github.com/herald-it/django-yamaps/archive/%s.tar.gz' % (version),

    description='A django widget which allows you to select the address using the yandex map.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    license='MIT',

    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.js', '*.html', '*.*']},
    install_requires=['setuptools'],
    zip_safe=False,
    keywords = ['django', 'address', 'yandex', 'maps', 'admin']
)