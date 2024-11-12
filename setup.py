from setuptools import setup

setup(
    name = 'python-dbpool',
    version = '0.1.0a0',
    author = 'Claus Prüfer',
    author_email = 'pruefer@webcodex.de',
    maintainer = 'Claus Prüfer',
    description = 'A tiny static postgresql database pool for threaded wsgi webserver (apache2).',
    license = 'GPLv3',
    url = 'http://dbpool.python.webcodex.de',
    long_description = open('./README.md').read(),

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Database Tools',
        'License :: OSI Approved :: GPLv3 License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    packages = [
        'pgdbpool'
    ],
    package_dir = {
        'pgdbpool': 'src/'
    },
    install_requires = [
        'psycopg2'
    ],

    python_requires = '>=3',
    zip_safe = True
)
