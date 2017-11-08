from setuptools import setup, find_packages

setup(name='hikyaku',
      version='0.1',
      description='A messaging library that wraps multiple messaging protocols into one easy to use package.',
      url='',
      author='Karim Shehadeh',
      author_email='kshehadeh@underarmour.com',
      license='MIT',
      packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
      zip_safe=False,
      classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
      ],
      keywords="messaging email slack notificiation communication",
      install_requires=[
            'emails',
            'slackclient',
            'boto3'
      ],
      python_requires='>=2.7, <3',
)