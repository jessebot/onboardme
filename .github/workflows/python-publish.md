---
name: Python package
on:
  push:
    tags:
      - "v*.*.*"
jobs:
  build_and_publish_to_pypi:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build and publish to pypi
        uses: JRubics/poetry-publish@v1.16
        with:
          python_version: "3.11.2"
          pypi_token: ${{ secrets.DEPLOY_FROM_GITHUB_TO_PYPI_ONBOARDME }}

      - name: Release
        uses: softprops/action-gh-release@v1
        if: startsWith(github.ref, 'refs/tags/')
