#!/usr/bin/env python3

# Required libraries to run the client cli.
import importlib.metadata
from art import text2art
import os
import asyncio
import websockets
import json
import pwinput
import ssl
import websockets.exceptions


# Clear the terminal before starting the client.
def clearTerminal() -> None:
    '''
    Clears the terminal.
    '''
    osName = os.name
    if osName == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# Check for required libraries before starting the client.
def checkRequiredLibraries(libraries: list) -> tuple[bool, list]:
    '''
    Checks whether all the required libraries are installed or not.
    Returns True and an empty list if all required libraries are installed.
    Returns False and a list of missing libraries to be installed.
    '''
    missing = []
    for library in libraries:
        try:
            importlib.metadata.version(library)
        except importlib.metadata.PackageNotFoundError:
            missing.append(library)

    return (not missing), missing


# Print the banner for the server cli.
def printBanner() -> None:
    '''
    Prints the banner for the server on the cli. Uses ascii art library for printing the banner.
    '''
    banner = text2art("OPENSTACK CLIENT", font="usa_flag")
    print(banner)


# Send the credentials to the server for authentication.
async def authenticateWithServer() -> str:
    '''
    Authenticate the client with the server.
    Returns the Session token if the authentication sequence is completed.
    '''
    serverURI = "wss://<YOUR_SERVER_IP>:<YOUR_SERVER_PORT>"
    username = input("Enter Your Username : ")
    password = pwinput.pwinput("Enter Your Password : ")
    project_name = input("Enter Your Project Name : ")
    credentials = {
        "username": username,
        "password": password,
        "project_name": project_name
    }
    sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    sslContext.check_hostname = False
    sslContext.verify_mode = ssl.CERT_NONE
    try:
        async with websockets.connect(serverURI, ssl = sslContext) as connection:
            await connection.send(json.dumps(credentials))
            return await connection.recv()
    except websockets.exceptions.InvalidStatusCode as error:
        return f"Connection error: {error.status_code} - Ensure server URI is correct."
    except Exception as error:
        return f"An error occurred: {str(error)}"
        


# Main driver function
def main():
    clearTerminal()
    required = ["art", "asyncio", "websockets", "pwinput"]
    isInstalled, missing = checkRequiredLibraries(required) 
    if not isInstalled:
        print("The following libraries are missing:", ", ".join(missing))
        return 

    printBanner()
    response = asyncio.run(authenticateWithServer())
    print(response)

# Execute the main entry point
if __name__ == "__main__":
    main()
