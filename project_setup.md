# Project Setup

Here we provide some details about the project setup. Most of the choices are explained in the
[guide](https://guide.esciencecenter.nl). Links to the relevant sections are included below. Feel free to remove this
text when the development of the software package takes off.

For a quick reference on software development, we refer to [the software guide
checklist](https://guide.esciencecenter.nl/#/best_practices/checklist).

## Python versions

This repository is set up with Python versions:

- 3.9
- 3.10
- 3.11
- 3.12

Add or remove Python versions based on project requirements. See [the
guide](https://guide.esciencecenter.nl/#/best_practices/language_guides/python) for more information about Python
versions.

## Package management and dependencies

You can use either pip or conda for installing dependencies and package management. This repository does not force you
to use one or the other, as project requirements differ. For advice on what to use, please check [the relevant section
of the
guide](https://guide.esciencecenter.nl/#/best_practices/language_guides/python?id=dependencies-and-package-management).

- Runtime dependencies should be added to `pyproject.toml` in the `dependencies` list under `[project]`.
- Development dependencies should be added to `pyproject.toml` in one of the lists under `[project.optional-dependencies]`.

## Packaging/One command install

You can distribute your code using PyPI.
[The guide](https://guide.esciencecenter.nl/#/best_practices/language_guides/python?id=building-and-packaging-code) can
help you decide which tool to use for packaging.

## Documentation

The documentation is contained in the [README.md](README.md) file

## Coding style conventions and code quality

- [Relevant section in the NLeSC guide](https://guide.esciencecenter.nl/#/best_practices/language_guides/python?id=coding-style-conventions) and [README.dev.md](README.dev.md).

## Continuous code quality

[Sonarcloud](https://sonarcloud.io/) is used to perform quality analysis and code coverage report

- `sonar-project.properties` is the SonarCloud [configuration](https://docs.sonarqube.org/latest/analysis/analysis-parameters/) file
- `.github/workflows/sonarcloud.yml` is the GitHub action workflow which performs the SonarCloud analysis

## Package version number

- We recommend using [semantic versioning](https://guide.esciencecenter.nl/#/best_practices/releases?id=semantic-versioning).
- For convenience, the package version is stored in a single place: `mixed_meal_model_sbml/pyproject.toml` under the `tool.bumpversion` header.
- Don't forget to update the version number before [making a release](https://guide.esciencecenter.nl/#/best_practices/releases)!

## Logging

- We recommend using the logging module for getting useful information from your module (instead of using print).
- The project is set up with a logging example.
- [Relevant section in the guide](https://guide.esciencecenter.nl/#/best_practices/language_guides/python?id=logging)

## CHANGELOG.md

- Document changes to your software package
- [Relevant section in the guide](https://guide.esciencecenter.nl/#/best_practices/releases?id=changelogmd)

## CITATION.cff

- To allow others to cite your software, add a `CITATION.cff` file
- It only makes sense to do this once there is something to cite (e.g., a software release with a DOI).
- Follow the [making software citable](https://guide.esciencecenter.nl/#/citable_software/making_software_citable) section in the guide.

## CODE_OF_CONDUCT.md

- Information about how to behave professionally
- [Relevant section in the guide](https://guide.esciencecenter.nl/#/best_practices/documentation?id=code-of-conduct)

## CONTRIBUTING.md

- Information about how to contribute to this software package
- [Relevant section in the guide](https://guide.esciencecenter.nl/#/best_practices/documentation?id=contribution-guidelines)

## MANIFEST.in

- List non-Python files that should be included in a source distribution
- [Relevant section in the guide](https://guide.esciencecenter.nl/#/best_practices/language_guides/python?id=building-and-packaging-code)

## NOTICE

- List of attributions of this project and Apache-license dependencies
- [Relevant section in the guide](https://guide.esciencecenter.nl/#/best_practices/licensing?id=notice)
