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

### v0.5-alpha
```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2

    # Assuming you have an sbt scala project with scoverage plugin
    - name: Checkout code
      uses: actions/checkout@v2
      
    - name: Generate sbt-scoverage testing and coverage report
      run: |
        /usr/local/bin/platform-param-decrypt_linux > ~/.env
        sbt coverage test coverageReport coverageOff

    # Get changed files from PR
    - name: Get changed files
      if: ${{ github.event.pull_request }}
      uses: jitterbit/get-changed-files@v1
      id: changed-files
      with:
        format: 'json'

    # Get scala version from build (on PR event)
    - name: Get Scala Version
      if: ${{ github.event.pull_request }}
      id: get-version
      run: |
        version=$(echo target/scala* | cut -c14-)
      echo "scala version is ${version}"
      echo "::set-output name=version::$version"
                
    # Then call the report action to post comment to PR (on PR event)
    - name: Run report action
      if: ${{ github.event.pull_request }}
      uses: wishabi/scoverage-report-gha@v0.5-alpha
      id: scoverage
      with:
        repo: ${{ github.repository }}
        pr: ${{ github.event.pull_request.number }}
        token: ${{ secrets.GITHUB_TOKEN }}
        file: target/scala-${{ steps.get-version.outputs.version }}/scoverage-report/scoverage.xml
        minStatementCov: 0.95
        changedFiles: ${{ steps.changed-files.outputs.all }}
        includePackageCov: true
    
    # (Optional) Print test coverage output (on PR event)
    - name: Check outputs
        if: ${{ github.event.pull_request }}
        run: |
        echo "Statement Coverage - ${{ steps.scoverage.outputs.statementCoverage }}"
```

## Tests

```
cd scoverage-report-gha
python3 -m unittest -v
```