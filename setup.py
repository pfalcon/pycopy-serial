from setuptools import setup


setup(name='micropython-serial',
      version='0.1',
      description="pySerial-like module for MicroPython (unix port).",
      url='https://github.com/pfalcon/micropython-serial',
      author='Paul Sokolovsky',
      author_email='pfalcon@users.sourceforge.net',
      license='MIT',
      py_modules=['serial'],
      install_requires=['micropython-os'])
