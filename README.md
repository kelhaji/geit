
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)


<p align="center">
  <p align="center">
     <img src="https://github.com/kelhaji/geit/blob/master/logos/logo-white.png?raw=true" alt="Geit" width="400">
  </p>
  <p align="center">
    <b>G</b>it <b>e</b>ducational <b>i</b>nsights <b>t</b>ool. Because f*#k slackers.
  </p>
</p>


## About Geit

Geit is a tool developed to aggregate contribution data of developers in a software development group project that uses Git. It is designed for teachers and teaching assistants to asses an entire group project and its individual members in terms of their code contributions behavior. 

## Demo
Here is one example output created by Geit
<!-- Click <a href="http://geitsoftware.com/demos.html" target="_blank">here</a> to find two demos generated by Geit. -->
<p align="center">
  <p align="center">
    <img src="https://github.com/kelhaji/geit/blob/master/output_examples/example-fake-project.png?raw=true" alt="Geit" width="400">
  </p>
</p>

## Features

- Shows contributions by contribution types for each developer. Contribution types are:
    - Code contributions
    - Test contributions
    - Comment contributions
    - Configuration contributions
    - User interface contributions
    - Documentation contributions
- Heuristically points out developers who are performing below average, above average, or need attention
- Shows project files and folders with percentage of contribution for each developer
- Displays overall commit distribution since inception of project
- Shows issues and merge requests contribution activity (if available)
- GitLab integration

## Requirements

- [Python 3.6](https://www.python.org/downloads/) or greater
- [PIP](https://pypi.org/project/pip/)
- [Git](https://git-scm.com/)

## Installation
Install the latest version using the following instructions:

```
git clone https://github.com/kelhaji/geit
cd geit
pip3 install -r requirements.txt
```

**A note for Windows users:** Currently, the only way to run Geit on Windows is via the Windows Subsystem for Linux (WSL). Click [here](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to see how to install WSL. After installing WSL 2, you can follow the installation instructions here to set up Geit on the Linux subsystem.

## How to Use

You can generate a report by running the following command:
```
python3 geit.py --target-repo /path/to/repo
```

You can also specify the output type:
```
python3 geit.py --target-repo /path/to/repo --output json
```
The default output type is HTML.

**Note for WSL users:** when running the above commands ensure that the target repo was cloned within WSL.  

### Usage with GitLab

You can generate a report by running the following command:
```
python3 geit.py --gitlab-url <YOUR_GITLAB_URL> --gitlab-api-key <YOUR_API_KEY> --gitlab-project-id <YOUR_PROJECT_ID>
```