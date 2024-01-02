from distutils.core import setup

setup(
    name='fast',
    version='0.2.1',
    description='辅助测试的工具包',
    author='sfwwslm',
    author_email='sfwwslm@gmail.com',
    url='https://github.com/sfwwslm/tools.git',
    packages=['fast'],
    package_dir={"": "src"},
    install_requires=[],
    keywords='test faker',
    long_description="....",
    python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*"
)
