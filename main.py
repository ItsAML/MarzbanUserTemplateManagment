import json
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Constants
DOMAIN = 'YOUR_DOMAIN'
PORT = "YOUR_PORT"
USERNAME = 'YOUR_USERNAME'
PASSWORD = 'YOUR_PASSWORD'
HTTPS = True  # Set this to True for HTTPS, False for HTTP

# Create a reusable session
session = requests.Session()

# Force User To Insert Digits only
def get_integer_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            return int(user_input)
        else:
            print("Please enter a valid integer.")

# Function to convert bytes to gigabytes
def bytes_to_gigabytes(bytes):
    return bytes / (1024 ** 3)  # 1 GB = 1024^3 bytes

# Function to convert gigabytes to bytes
def gigabytes_to_bytes(gigabytes):
    bytes_in_a_gigabyte = 1073741824  # 1024 bytes * 1024 kilobytes * 1024 megabytes
    return gigabytes * bytes_in_a_gigabyte

# Function to convert days to seconds
def days_to_seconds(days):
    seconds_in_a_day = 86400  # 60 seconds * 60 minutes * 24 hours
    return days * seconds_in_a_day

# Function to convert seconds to days
def seconds_to_days(seconds):
    return seconds / (24 * 60 * 60)  # 1 day = 24 hours * 60 minutes * 60 seconds

def get_access_token(username, password):
    use_protocol = 'https' if HTTPS else 'http'
    url = f'{use_protocol}://{DOMAIN}:{PORT}/api/admin/token'
    data = {
        'username': username,
        'password': password
    }

    try:
        response = session.post(url, data=data)
        response.raise_for_status()
        access_token = response.json()['access_token']
        logging.info(".:Logged in Successfully:.")
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while obtaining access token: {e}')
        return None

def get_all_inbounds(access_token):
    use_protocol = 'https' if HTTPS else 'http'
    url = f'{use_protocol}://{DOMAIN}:{PORT}/api/inbounds'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        inboundsList = response.json()
        return inboundsList
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while retrieving inbounds: {e}')
        return None

def print_inbounds(inbounds, indent=0):
    for protocol, subprotocols in inbounds.items():
        if subprotocols:
            print("│   " * indent + "├─🌐 " + protocol.upper())
            for subprotocol in subprotocols:
                print("│   " * (indent + 1) + f"└─{subprotocol}")
        else:
            print("│   " * indent + "├─🌐 " + protocol.upper())

def get_users_templates(access_token):
    use_protocol = 'https' if HTTPS else 'http'
    url = f'{use_protocol}://{DOMAIN}:{PORT}/api/user_template'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()
        user_templates_list = response.json()
        for entry in user_templates_list:
            print(f"ID: {entry['id']}")
            print(f"Name: {entry['name']}")
            
            inbounds = entry['inbounds']
            print("Inbounds:")
            print_inbounds(inbounds)

            # Handle the "data_limit" field
            if entry['data_limit'] == 0:
                print("Data Limit: Unlimited")
            else:
                data_limit_gb = bytes_to_gigabytes(entry['data_limit'])
                print(f"Data Limit: {data_limit_gb:.2f} GB")

            # Handle the "expire_duration" field
            if entry['expire_duration'] == 0:
                print("Expire Duration: Never expire")
            else:
                expire_duration_days = seconds_to_days(entry['expire_duration'])
                print(f"Expire Duration: {expire_duration_days:.2f} days")

            print(f"UserName Prefix: {entry['username_prefix']}")
            print(f"UserName Suffix: {entry['username_suffix']}")
            print("---------------------------------------------")
        return user_templates_list
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while retrieving users templates: {e}')
        return None

def add_user_template(access_token, json):
    use_protocol = 'https' if HTTPS else 'http'
    url = f'{use_protocol}://{DOMAIN}:{PORT}/api/user_template'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = session.post(url, data=json, headers=headers)
        response.raise_for_status()
        print("User Template Has Been Created Succesfuly.")
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while creating user template: {e}')

def modify_user_template(access_token, json, template_id):
    use_protocol = 'https' if HTTPS else 'http'
    url = f'{use_protocol}://{DOMAIN}:{PORT}/api/user_template/{template_id}'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    try:
        response = session.put(url, data=json, headers=headers)
        response.raise_for_status()
        print("User Template Has Been Modified Succesfuly.")
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while Modifing user template: {e}')


def delete_user_template(access_token, template_id):
    use_protocol = 'https' if HTTPS else 'http'
    url = f'{use_protocol}://{DOMAIN}:{PORT}/api/user_template/{template_id}'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    templateid = {
        id : template_id
    }
    try:
        response = session.delete(url, data=templateid, headers=headers)
        response.raise_for_status()
        print("User Template Has Been Deleted Succesfuly.")
    except requests.exceptions.RequestException as e:
        logging.error(f'Error occurred while deleting user template: {e}')


token = get_access_token(USERNAME, PASSWORD)

if token:
    print("Welcome To The Script (Developed By AML)")
    while True:
        menu = input("""
1 | Get All User Templates
2 | Add New User Template
3 | Modify User Template
4 | Delete User Template
5 | Exit The Script

Enter a Number to continue : """)
        if menu == "1":
            get_users_templates(token)
        elif menu == "2":
            template_name = input("Please Enter a Name for your template: ")
            all_inbounds = get_all_inbounds(token)
            protocols = {
                        "vmess": [],
                        "vless": [],
                        "trojan": [],
                        "shadowsocks": []
                        }
            # Loop through the keys in the JSON data
            for key, value in all_inbounds.items():
                # Check if the key is one of the supported protocols
                if key in protocols:
                    protocols[key].extend([subprotocol["tag"] for subprotocol in value])

            # Handle the possibility of missing protocols (trojan and shadowsocks)
            for protocol in ["trojan", "shadowsocks"]:
                try:
                    protocols[protocol].extend([subprotocol["tag"] for subprotocol in all_inbounds[protocol]])
                except KeyError:
                    pass
            vmess_inbounds = []
            while True:
                print("Enter your VMESS inbound names. (You Can Type '/' To Select All)")
                available_inbounds = ", ".join(protocols.get("vmess", []))
                print("Available Inbounds:", available_inbounds or "No Inbounds Found")
                vmess_input = input("Enter Inbound Name: ")
                if vmess_input:
                    if vmess_input == "/":
                        vmess_inbounds.extend(protocols.get("vmess", []))
                        break
                    else:
                        vmess_inbounds.append(vmess_input)
                else:
                    break

            vless_inbounds = []
            while True:
                print("Enter your VLESS inbound names. (You Can Type '/' To Select All)")
                available_inbounds = ", ".join(protocols.get("vless", []))
                print("Available Inbounds:", available_inbounds or "No Inbounds Found")
                vless_input = input("Enter Inbound Name: ")
                if vless_input:
                    if vless_input == "/":
                        vless_inbounds.extend(protocols.get("vless", []))
                        break
                    else:
                        vless_inbounds.append(vless_input)
                else:
                    break

            trojan_inbounds = []
            while True:
                print("Enter your TROJAN inbound names. (You Can Type '/' To Select All)")
                available_inbounds = ", ".join(protocols.get("trojan", []))
                print("Available Inbounds:", available_inbounds or "No Inbounds Found")
                trojan_input = input("Enter Inbound Name: ")
                if trojan_input:
                    if trojan_input == "/":
                        trojan_inbounds.extend(protocols.get("trojan", []))
                        break
                    else:
                        trojan_inbounds.append(trojan_input)
                else:
                    break

            shadowsocks_inbounds = []
            while True:
                print("Enter your SHADOWSOCKS inbound names. (You Can Type '/' To Select All)")
                available_inbounds = ", ".join(protocols.get("shadowsocks", []))
                print("Available Inbounds:", available_inbounds or "No Inbounds Found")
                shadowsocks_input = input("Enter Inbound Name: ")
                if shadowsocks_input:
                    if shadowsocks_input == "/":
                        shadowsocks_inbounds.extend(protocols.get("shadowsocks", []))
                        break
                    else:
                        shadowsocks_inbounds.append(shadowsocks_input)
                else:
                    break

            data_limit = get_integer_input("Enter The Data Limit Per (GB): ")
            expire_duration = get_integer_input("Enter Expire Duration Per Days: ")

            # Build the 'inbounds' dictionary
            inbounds = {
                "vmess": vmess_inbounds,
                "vless": vless_inbounds,
                "trojan": trojan_inbounds,
                "shadowsocks": shadowsocks_inbounds
            }

            # Create the 'data' dictionary
            data = {
                "name": template_name,
                "inbounds": inbounds,
                "data_limit": gigabytes_to_bytes(data_limit),
                "expire_duration": days_to_seconds(expire_duration)
            }

            # Convert the 'data' dictionary to JSON format
            json_data = json.dumps(data, indent=4)

            # Sending To The API
            add_user_template(token, json_data)
            print("----------------------------------------------------------------")

        elif menu == "3":
            template_id = input("Please Enter Your Template ID : ")
            template_name = input("Please Enter a Name for your template: ")
            all_inbounds = get_all_inbounds(token)
            protocols = {
                        "vmess": [],
                        "vless": [],
                        "trojan": [],
                        "shadowsocks": []
                        }
            # Loop through the keys in the JSON data
            for key, value in all_inbounds.items():
                # Check if the key is one of the supported protocols
                if key in protocols:
                    protocols[key].extend([subprotocol["tag"] for subprotocol in value])

            # Handle the possibility of missing protocols (trojan and shadowsocks)
            for protocol in ["trojan", "shadowsocks"]:
                try:
                    protocols[protocol].extend([subprotocol["tag"] for subprotocol in all_inbounds[protocol]])
                except KeyError:
                    pass
            vmess_inbounds = []
            while True:
                print("Enter your VMESS inbound names. (You Can Type '/' To Select All)")
                available_inbounds = ", ".join(protocols.get("vmess", []))
                print("Available Inbounds:", available_inbounds or "No Inbounds Found")
                vmess_input = input("Enter Inbound Name: ")
                if vmess_input:
                    if vmess_input == "/":
                        vmess_inbounds.extend(protocols.get("vmess", []))
                        break
                    else:
                        vmess_inbounds.append(vmess_input)
                else:
                    break

            vless_inbounds = []
            while True:
                print("Enter your VLESS inbound names. (You Can Type '/' To Select All)")
                available_inbounds = ", ".join(protocols.get("vless", []))
                print("Available Inbounds:", available_inbounds or "No Inbounds Found")
                vless_input = input("Enter Inbound Name: ")
                if vless_input:
                    if vless_input == "/":
                        vless_inbounds.extend(protocols.get("vless", []))
                        break
                    else:
                        vless_inbounds.append(vless_input)
                else:
                    break

            trojan_inbounds = []
            while True:
                print("Enter your TROJAN inbound names. (You Can Type '/' To Select All)")
                available_inbounds = ", ".join(protocols.get("trojan", []))
                print("Available Inbounds:", available_inbounds or "No Inbounds Found")
                trojan_input = input("Enter Inbound Name: ")
                if trojan_input:
                    if trojan_input == "/":
                        trojan_inbounds.extend(protocols.get("trojan", []))
                        break
                    else:
                        trojan_inbounds.append(trojan_input)
                else:
                    break

            shadowsocks_inbounds = []
            while True:
                print("Enter your SHADOWSOCKS inbound names. (You Can Type '/' To Select All)")
                available_inbounds = ", ".join(protocols.get("shadowsocks", []))
                print("Available Inbounds:", available_inbounds or "No Inbounds Found")
                shadowsocks_input = input("Enter Inbound Name: ")
                if shadowsocks_input:
                    if shadowsocks_input == "/":
                        shadowsocks_inbounds.extend(protocols.get("shadowsocks", []))
                        break
                    else:
                        shadowsocks_inbounds.append(shadowsocks_input)
                else:
                    break

            data_limit = get_integer_input("Enter The Data Limit Per (GB): ")
            expire_duration = get_integer_input("Enter Expire Duration Per Days: ")

            # Build the 'inbounds' dictionary
            inbounds = {
                "vmess": vmess_inbounds,
                "vless": vless_inbounds,
                "trojan": trojan_inbounds,
                "shadowsocks": shadowsocks_inbounds
            }

            # Create the 'data' dictionary
            data = {
                "name": template_name,
                "inbounds": inbounds,
                "data_limit": gigabytes_to_bytes(data_limit),
                "expire_duration": days_to_seconds(expire_duration)
            }

            # Convert the 'data' dictionary to JSON format
            json_data = json.dumps(data, indent=4)

            # Sending To The API
            modify_user_template(token, json_data, template_id)
            print("----------------------------------------------------------------")

        elif menu == "4":
            user_id = int(input("Please Enter Your Template ID: "))
            delete_user_template(token, user_id)
            print("----------------------------------------------------------------")
        elif menu == "5":
            print("Make Sure To Check Other Scripts At https://github.com/itsAML :)")
            print("----------------------------------------------------------------")
            exit()
        
