from setuptools import setup

setup(name='pybot',
      version='0.1',
      description='Telegram bot with allow dynamic plugin arquitecture.',
      url='http://github.com/raelga/pybot',
      author='Rael Garcia',
      author_email='self@rael.io',
      license='MIT',
      install_requires=[
          'future',
          'requests',
          'python-telegram-bot'
      ],
      zip_safe=False)
