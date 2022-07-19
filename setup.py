from setuptools import setup

setup(name='pytest-repeat',
      use_scm_version=True,
      description='pytest plugin for repeating tests',
      long_description=open('README.rst').read(),
      author='Bob Silverberg',
      author_email='bsilverberg@mozilla.com',
      url='https://github.com/pytest-dev/pytest-repeat',
      py_modules=['pytest_repeat'],
      entry_points={'pytest11': ['repeat = pytest_repeat']},
      setup_requires=['setuptools_scm'],
      install_requires=['pytest>=3.6'],
      license='Mozilla Public License 2.0 (MPL 2.0)',
      keywords='pytest pytest repeat',
      python_requires='>=3.7',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Framework :: Pytest',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
          'Topic :: Utilities',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
      ])
