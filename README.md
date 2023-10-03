# Marzban Expired Users Remover

 | Simply Show, Add, Modify and Delete User Templates With This Script.

## Table of Contents
- [About](#about)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Linux](#Linux)
- [Windows](#windows)

Make Sure To Change these variables before runing the script.
```python
DOMAIN = 'YOUR_DOMAIN'
PORT = 'YOUR_PORT'
USERNAME = 'YOUR_USERNAME'
PASSWORD = 'YOUR_PASSWORD'
HTTPS = True  # Set this to True for HTTPS, False for HTTP
```

## About

This script is designed to automate the management of users using marzban api. It securely logs in to an admin panel, retrieves a list of expired users, and removes them from the system, all while providing detailed logging for each operation. It is a valuable tool for efficiently managing user accounts in a web-based environment.

Feel free to modify and expand upon this description to better suit your project's specific goals and context.

## Getting Started

First of all you need to enable Marzban API which you can use this command below
```bash
echo 'DOCS=True' | sudo tee -a /opt/marzban/.env
```
or manually open the .env file with this command
```bash
nano /opt/marzban/.env
```
and then add this line to the file
```python
DOCS=True
```
Finally Restart The Marzban
```sh
marzban restart
```
### Prerequisites
Python 3.0+ with requests library required. you cant run the script on python 2.0
### Linux
```bash
# Clone the Repository
git clone https://github.com/ItsAML/MarzbanUserTemplateManagment.git

# Change Directory
cd MarzbanExpiredUserRemover

# Install pip (if not already installed)
wget -qO- https://bootstrap.pypa.io/get-pip.py | python3 -

# Install Dependencies
python3 -m pip install -r requirements.txt

# Run the Script
python3 main.py
```
### Windows
```bash
# Clone the Repository
git clone https://github.com/ItsAML/MarzbanUserTemplateManagment.git

# Navigate to the Repository Directory
cd MarzbanExpiredUserRemover

# Install Python (if not already installed)
# Download and install Python from https://www.python.org/downloads/
# Ensure you add Python to your system's PATH during installation

# Install Dependencies
pip install -r requirements.txt

# Run the Script
python main.py
```
