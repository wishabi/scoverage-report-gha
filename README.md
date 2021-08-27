# scoverage-report-gha

[![Action Template](https://img.shields.io/badge/Action%20Template-scoverage%20report%20action-blue.svg?colorA=24292e&colorB=0366d6&style=flat&longCache=true&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAM6wAADOsB5dZE0gAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAERSURBVCiRhZG/SsMxFEZPfsVJ61jbxaF0cRQRcRJ9hlYn30IHN/+9iquDCOIsblIrOjqKgy5aKoJQj4O3EEtbPwhJbr6Te28CmdSKeqzeqr0YbfVIrTBKakvtOl5dtTkK+v4HfA9PEyBFCY9AGVgCBLaBp1jPAyfAJ/AAdIEG0dNAiyP7+K1qIfMdonZic6+WJoBJvQlvuwDqcXadUuqPA1NKAlexbRTAIMvMOCjTbMwl1LtI/6KWJ5Q6rT6Ht1MA58AX8Apcqqt5r2qhrgAXQC3CZ6i1+KMd9TRu3MvA3aH/fFPnBodb6oe6HM8+lYHrGdRXW8M9bMZtPXUji69lmf5Cmamq7quNLFZXD9Rq7v0Bpc1o/tp0fisAAAAASUVORK5CYII=)](https://github.com/wishabi/scoverage-report-gha)
[![Actions Status](https://github.com/wishabi/scoverage-report-gha/workflows/Lint/badge.svg)](https://github.com/wishabi/scoverage-report-gha/actions)

This action publishes `sbt-scoverage` test coverage report results as comments in Github PRs.

- Meant to be used in `scala` projects that have Github actions for CI.
- Parses `xml` contents from `sbt-scoverage` reports and extracts useful metrics.
- Creates a markdown formatted comment and posts to Github PR.
- This action was built using templates from [python-container-action](https://github.com/jacobtomlinson/python-container-action)
- The overall execution is inspired by the work done in [jacoco-report](https://github.com/Madrapps/jacoco-report)

Sample output

![img.png](figures/sample-output-1.png)

## Example usage

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master

    # Assuming you have an sbt scala project with scoverage plugin
    # ...
    - name: Generate sbt-scoverage testing and coverage report
      run: |
        /usr/local/bin/platform-param-decrypt_linux > ~/.env
        sbt coverage test coverageReport

    # Get scala version from build
    - name: Get Scala Version
      id: get-version
      run: |
        version=$(echo target/scala* | cut -c14-)
      echo "scala version is ${version}"
      echo "::set-output name=version::$version"
        
    # Get PR number
    - name: Get current PR number
      uses: jwalton/gh-find-current-pr@v1
      id: findPr
      with:
        state: open
        
    # Then call the report action to post comment to PR   
    - name: Run report action
      uses: wishabi/scoverage-report-gha@v0.1
      id: scoverage
      with:
        repo: ${{ github.repository }}
        pr: ${{ steps.findPr.outputs.number }}
        token: ${{ secrets.GITHUB_TOKEN }}
        file: target/scala-${{ steps.get-version.outputs.version }}/scoverage-report/scoverage.xml
        minStatementCov: 0.95
    
    - name: Check outputs
        run: |
        echo "Statement Coverage - ${{ steps.scoverage.outputs.statementCoverage }}"
```
