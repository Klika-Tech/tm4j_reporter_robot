import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tm4j-reporter-robot",
    description="python package providing Robot Framework integration with Jira Test Management (tm4j) Cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="v0.1.0",
    url="https://github.com/Klika-Tech/tm4j_reporter_robot",
    author="Yury Kuptsou",
    author_email="ykuptsou@klika-tech.com",
    license="MIT",
    packages=["tm4j_reporter_robot.tm4j_robot_helpers", "tm4j_reporter_robot"],
    platforms="any",
    python_requires=">=3.6",
    install_requires=["tm4j-reporter-api"],
    keywords="python tm4j jira test testmanagement report robotframework",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
