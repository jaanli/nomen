from setuptools import setup

setup(name='nomen',
      version='0.1',
      description='Light configuration and command line flags',
      url='https://github.com/altosaar/nomen',
      author='Jaan Altosaar',
      author_email='j@jaan.io',
      license='MIT',
      packages=['nomen'],
      install_requires=[
          'markdown',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
