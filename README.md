# QuickStart-Python-Extension

A quick-start repository for building and uploading a Python-focused BlueOS Extension.

## Intent

This is intended to showcase:
1. How to make a basic Extension with a simple web interface, using Python and some HTML
2. The difference between code running on the frontend vs the backend
    - Backend code has access to vehicle hardware and other service APIs, as well as the filesystem (for things like persistent logging)
    - Frontend code is in charge of the display, and runs in the browser interface (instead of on the vehicle's onboard computer)

## Usage

Forking the repository will try to automatically package and upload your Extension variant to a Docker registry (Docker Hub), using the built in GitHub Action.
This process makes use of some [GitHub Variables](https://github.com/BlueOS-community/Deploy-BlueOS-Extension#input-variables) that you can configure for your fork.

It is also possible to manually run the Action (via the Actions tab), or to build and deploy the extension manually on your local machine (although this requires installing the relevant build tools and cloning the repository onto your computer).

>💡**Note:** If you are forking this repository as a starting point for creating your own [BlueOS Extension](https://blueos.cloud/docs/blueos/latest/development/extensions), it is recommended to enable `Issues` in your fork (via the `Settings` tab at the top), so that users and co-developers of your Extension can raise problems and make suggestions.
