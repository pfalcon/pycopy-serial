from setuptools import setup


setup(name='pycopy-serial',
      version='0.4.2',
      description="pySerial-like module for Pycopy unix port (https://github.com/pfalcon/pycopy).",
      url='https://github.com/pfalcon/pycopy-serial',
      author='Paul Sokolovsky',
      author_email='pfalcon@users.sourceforge.net',
      license='MIT',
      py_modules=['serial'],
      install_requires=['pycopy-os', 'pycopy-fcntl'])
