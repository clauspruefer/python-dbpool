from setuptools import setup

setup(

    name = 'pgdbpool',
    author = 'Claus Prüfer',
    author_email = 'pruefer@webcodex.de',
    description = 'A tiny database de-multiplexer primarily scoped for Web- / Application Server.',
    long_description = open('./README.md').read(),

    packages = [
        'pgdbpool'
    ],

    package_dir = {
        'pgdbpool': 'src/'
    },

    zip_safe = True

)
