from setuptools import setup

setup(name='onboardme',
      version='0.1',
      description='An onboarding tool to install dot files and packages',
      url='http://github.com/jessebot/onboardme',
      author='Jesse Hitch',
      author_email='jessebot@linux.com',
      license='GPL version 3 or later',
      packages=['onboardme'],
      install_requires=[
          'wget',
          'PyYAML',
          'rich',
          'click'
      ],
      include_package_data=True,
      zip_safe=False)
