#!/usr/bin/env python3


# Library Import
import asyncio
import websockets
import logging
from novaclient import client as nvc
from glanceclient import Client as gnc
from neutronclient.v2_0 import client as ntc
from keystoneauth1 import loading
from keystoneauth1 import session
from datetime import datetime


def importRequirements() -> bool:
    '''
    Checks whether the required libraries are installed or not.
    If not returns False else returns True.
    '''
    pass


# Start the loggers
logFile = "server.log"
logging.basicConfig( filename = logFile, level = logging.INFO, format = '%(asctime)s - %(message)s' )


# Define authentication parameters
auth_params = {
    "version" : 2,
    "auth_url" : "http://localhost/identity"
}


# Log the connection details
def logger( ip : str, port : str ) -> None:
    logging.info(f"CONNECTION FROM {ip}:{port}")


# Authenticate User
def authenticateClient(username: str, password: str, project_id: str, auth_url: str) -> bool:
    '''
    Authenticates user, returns True if authentication succeeds else returns False.
    '''
    try:
        loader = loading.get_plugin_loader('password')
        authentication = loader.load_from_options(
            auth_url=auth_url,
            username=username,
            password=password,
            project_id=project_id,
            user_domain_name='Default',
            project_domain_name='Default',
        )
        userSession = session.Session(auth=authentication)
        token = userSession.get_token()
        if not token:
            raise Exception("Invalid authentication token")
        nova = nvc.Client('2.0', session=userSession)
        glance = gnc('2', session=userSession)
        neutron = ntc.Client(session = userSession)
        return True, nova, glance, neutron
    except Exception as error:
        print(f"AUTH FAILED : {error}")
        return False, None, None, None


# Handle request for listing images
async def listImages(websocket : object, glance : object) -> list:
    '''
    Fetch images and send the list of images to the Client.
    '''
    images = glance.images.list()
    if images == []:
        await websocket.send("NO IMAGES AVAILABLE CURRENTLY. CONTACT  ADMIN")
    else:
        imageInfo = "\n".join([f"{img.id} : {img.name}" for img in images])
        await websocket.send(imageInfo)


# Handle the request for listing flavors
async def listFlavors(nova : object) -> list:
    '''
    Fetches flavors and sends the list of flavors to the Client.
    '''
    flavors = nova.flavors.list()
    return flavors


# Handle the request for listing networks
async def listNetworks(neutron : object) -> list:
    '''
    Fetches networks and sends the list of networks to the Client.
    '''
    networks = neutron.list_networks()['networks']
    return networks


# Handle request for creating instance
async def createInstance(websocket : object, nova : object, neutron : object):
    '''
    Handles the Instance creation request by the user."
    '''
    checkFlavors = await listFlavors(nova)
    checkNetwork = await listNetworks(neutron)
    if checkFlavors and checkNetwork:
        try:
            flavorsInfo = "\n".join([f"{flavor.id} : {flavor.name}" for flavor in checkFlavors])
            await websocket.send(flavorsInfo)
        except Exception as error:
            print(error)
        try:
            networksInfo = "\n".join([f"{network['id']} : {network['name']}" for network in checkNetwork])
            print(networksInfo)
            await websocket.send(networksInfo)
        except Exception as error:
            print(error)
        # await websocket.send("ENTER THE FLAVOR ID : ")
        # flavorID = await websocket.recv()
        #     flavorID = flavorID.strip()
        #     await websocket.send("ENTER INSTANCE NAME : ")
        #     instanceName = await websocket.recv()
        #     instance = nova.servers.create(name=instanceName, flavor=flavorID)
        #     await websocket.send(f"Instance Created Successfully : {instance.id} : {instance.name}")
        # except Exception as error:
        #     await websocket.send(f"Failed to create Instance : {error}")
    else:
        if not checkFlavors:
            await websocket.send("NO FLAVORS AVAILABLE CURRENTLY. CONTACT ADMIN.")
        if not checkNetwork:
            await websocket.send("NO NETWORKS AVAILABLE CURRENTLY. CONTACT ADMIN.")
        


# Handle client connection
async def handleClientRequest( websocket : object, path : str) -> None:
    '''
    Handles clients authentication and other requests for resource allocation, deletion and creation.
    '''
    clientIP, clientPort = websocket.remote_address
    logger( clientIP, clientPort )
    print( "CONNECTION INITIATED WITH CLIENT. LOG CREATED SUCCESS" )
    authenticated = False
    nova = None
    glance = None
    try:
        await websocket.send( "AUTH SEQUENCE INITIATED BY SERVER . . . " )
        authInfo = await websocket.recv()
        username, password, project_id = authInfo.split(",")
        isAuthenticated, nova, glance, neutron = authenticateClient( username, password, project_id, auth_params['auth_url'] ) 
        if isAuthenticated:
            authenticated = True
            await websocket.send( "success" )
            await websocket.send( "AUTH SEQUENCE COMPLETED BY CLIENT . . . " )
            logging.info( f"LOGIN SUCCESS FOR {clientIP}:{clientPort}" )
            while True:
                request = await websocket.recv()
                if request == 'lsimage':
                    await listImages(websocket, glance)
                elif request == 'createInstance':
                    await createInstance(websocket, nova, neutron)                    
        else:
            await websocket.send( "error" )
            await websocket.send( "AUTH SEQUENCE FAILED BY CLIENT . . . " )
            logging.warning( f"LOGIN FAILED FOR {clientIP}:{clientPort}" )
        
    except websockets.exceptions.ConnectionClosed:
        print( "CLIENT DISCONNECTED" )

serverListen = websockets.serve( handleClientRequest, "0.0.0.0", 8090 )
asyncio.get_event_loop().run_until_complete(serverListen)
print("SERVER RUNNING . . . . ")
asyncio.get_event_loop().run_forever()
