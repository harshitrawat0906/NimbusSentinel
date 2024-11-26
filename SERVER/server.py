#!/usr/bin/env python3

# Required libraries to run the server cli.
import importlib.metadata
from art import text2art
import os
import asyncio
import websockets
import json
import time
from openstack import connection 
import logging
from aiolimiter import AsyncLimiter
from dotenv import load_dotenv
import ssl
from collections import defaultdict


# Load the environments variables.
load_dotenv()


# Configure logging for creating logs at the server.
logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')


# Rate Limiter for controlling brute force (MAX 5 Request Per Minute)
rateLimiter = AsyncLimiter(5, 60)
attempts = defaultdict(int)
timestamps = defaultdict(float)


# SSL Configurations
SSL_CERTIFICATE_PATH = os.getenv("SSL_CERT_PATH")
SSL_KEY_PATH = os.getenv("SSL_KEY_PATH")


# Check for required libraries before starting the server.
def checkRequiredLibraries(libraries : list) -> tuple[bool, list]:
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
    
    if missing:
        return False, missing
    else:
        return True, missing


# Clear the terminal before starting the server.
def clearTerminal() -> None:
    '''
    Clears the terminal.
    '''
    os.system('cls' if os.name == 'nt' else 'clear')


# Print the banner for the server cli.
def printBanner() -> None:
    '''
    Prints the banner for the server on the cli. Uses ascii art library for printing the banner.
    '''
    banner = text2art("OPENSTACK SERVER", font = "usa_flag")
    print(banner)


# Authenticate the client with the openstack server.
async def authenticateClient(credentials : object) -> str:
    '''
    Authenticates the client with the openstack server.
    Returns session token if auth credentials are valid else Authentication failed is returned.
    '''
    authParameters = {
        "auth_url" : "http://localhost/identity",
        "project_name" : credentials["project_name"],
        "username" : credentials["username"],
        "password" : credentials["password"],
        "user_domain_name" : "default",
        "project_domain_name" : "default"
    }

    try:
        connect = connection.Connection(**authParameters)
        token = connect.authorize()
        logging.info("Authentication successful for user: %s", credentials["username"])
        return f"Authentication Sucessful.\nSession Token : {token}"
    except Exception as error:
        logging.warning("Authentication failed: %s", str(error))
        return f"Authentication Failed. Check Your Crendentials."


# Handle the incoming request of clients.
async def handleRequest(websocket: object) -> None:
    clientIP = websocket.remote_address[0]
    async for auth in websocket:
        try:
            credentials = json.loads(auth)
            currentTime = asyncio.get_event_loop().time()
            if currentTime - timestamps[clientIP] >= 900:
                attempts[clientIP] = 0
                logging.info("Attempts reset for %s", clientIP)
            timestamps[clientIP] = currentTime
            if attempts[clientIP] >= 5:
                response = "Too many attempts. Please wait before trying again."
                await websocket.send(response)
                logging.warning("Rate limit exceeded for %s", clientIP)
                continue
            async with rateLimiter:
                response = await authenticateClient(credentials)
                attempts[clientIP] += 1
        except json.JSONDecodeError:
            response = "Error! Invalid Request Format."
            logging.warning("MALFORMED REQUEST FROM %s", clientIP)
        await websocket.send(response)


# Main driver function
async def main() -> None:
    '''
    The main execution point.
    '''
    required = ["art", "websockets", "openstacksdk"]
    isInstalled, missing = checkRequiredLibraries(required)
    if not isInstalled:
        print("The following libraries are missing:", ", ".join(missing))
        return
    clearTerminal()
    time.sleep(1)
    printBanner()
    bindIP = "0.0.0.0"
    bindPort = int(os.getenv("PORT", 8090))
    sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslContext.load_cert_chain(SSL_CERTIFICATE_PATH, SSL_KEY_PATH)
    async with websockets.serve(handleRequest, bindIP, bindPort, ssl = sslContext):
        print(f"SERVER STARTED LISTENING ON wss://{bindIP}:{bindPort}/")
        await asyncio.Future()


# Execute the main entry point
asyncio.run(main())
