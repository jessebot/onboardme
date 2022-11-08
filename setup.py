from setuptools import setup


def readme():
    """
    grab and return contents of README.md for use in long description
    """
    with open('README.md') as f:
        return f.read()


lic_class = ('License :: OSI Approved :: GNU Affero General Public License v3'
             ' or later (AGPLv3+)')

setup(name='onboardme',
      description='An onboarding tool to install dot files and packages',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=['Development Status :: 3 - Alpha',
                   'Programming Language :: Python :: 3.10',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: POSIX :: Linux',
                   'Intended Audience :: End Users/Desktop',
                   'Topic :: System :: Installation/Setup',
                   lic_class],
      python_requires='>3.10',
      keywords='onboardme, onboarding, desktop-setup, setuptools, development',
      version='0.14.15',
      project_urls={
          'Documentation': 'https://jessebot.github.io/onboardme/onboardme',
          'Source': 'http://github.com/jessebot/onboardme',
          'Tracker': 'http://github.com/jessebot/onboardme/issues'},
      author='jessebot',
      author_email='jessebot@linux.com',
      license='GPL version 3 or later',
      packages=['onboardme'],
      install_requires=['wget', 'GitPython', 'PyYAML', 'rich', 'click'],
      data_files=[('onboardme/config',
                   ['onboardme/config/onboardme_config.yml',
                    'onboardme/config/packages.yml',
                    'onboardme/config/brew/Brewfile_Darwin',
                    'onboardme/config/brew/Brewfile_devops'])],
      entry_points={'console_scripts': ['onboardme = onboardme:main']},
      include_package_data=True,
      zip_safe=False)
