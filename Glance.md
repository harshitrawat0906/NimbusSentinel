![GLANCE LOGO](https://gitlab.in2p3.fr/uploads/-/system/project/avatar/6720/OpenStack_Project_Glance_mascot.png)

# GLANCE OPENSTACK (IMAGE MANAGER)

> This markdown fouces on definitions, configurations and use cases of **GLACNCE RESOURCE** the image manager of OPEN STACK similar to AWS Amazon Machine Image.

## TABLE OF CONTENT

1. **Introduction to GLANCE**
2. **Uploading Images via Web Interface (HORIZON)**
3. **Uploading Images via OPENSTACK Command Line Utility**
4. **Common Issues & Resolves**
5. **OFFICIAL DOCUMENTATION & REFERENCES**

### Introduction to GLANCE

_Definition_ : **GLANCE** is the image service component that manages the Virtual Machine Images for the user allowing them to manage and register the images.

#### Key Features of GLANCE

- **IMAGE REPOSITORY** : Stores VM images which can be used as templates to create new instances.
- **FORMATS SUPPORT** : Supports multiple image formats. Example ova, iso, qcow2, raw etc.
- **Integration with Other Services** : Integrates with other OpenStack services like Nova, Cinder, Swift enabling seamless deployment.

### Uploading Images via Web Interface (HORIZON)

> This section focuses on uploading images using the **HORIZON SERVICE** web interface of OPEN STACK for managing and monitoring the resources.

##### STEPS

1. Login to the **Horizon Interface** with `admin : admin` as `username : password`

![Horizon Login Panel](/images/general/login.png)

2. Navigate to the Images section under the Compute Services.

![Glance Image Manager](/images/glance-gui/glance.png)

3. Now click on the Create image to to upload your image.

![Glance Image Manager](/images/glance-gui/image-upload.png)

4. Fill out the necessary details about your image

![Configuring Your Image](/images/glance-gui/configurations.png)

5. Click on next and click on create image, that should start uploading you image.

![Uploading Image](/images/glance-gui/create-image.png)

6. Once the image is created it will be visible in the web console.

![Image Uploaded](/images/glance-gui/created-image.png)

> **IMPORTANT : To download and convert your image file into supported format of GLANCE GUI in this case .iso use the commands below.**

`wget https://cloud-images.ubuntu.com/jammy/20241002/jammy-server-cloudimg-s390x.img`

> To download the .img file from ubuntu cloud web service

`dd if=jammy-server-cloudimg-s390x.img of=ubuntu.iso`

`dd if=<your-image-file.img of=<your-output-file.iso>`

> To convert your .img into .iso

### Uploading Images via OPENSTACK Command Line Utility

> Open Stack offers it's command line utility to manage images, VMs and other service using the command line. In this section we will use the command line utility to upload and list the images.

##### STEPS

1. Export the auth configurations.

```
export OS_IDENTITY_API_VERSION=3
export OS_AUTH_URL=http://localhost/identity
export OS_DEFAULT_DOMAIN=default
export OS_USERNAME=admin
export OS_PASSWORD=admin
export OS_PROJECT_NAME=demo
```

![Export Authentication Configurations](/images/glance-cli/export.png)

2. Follow the below command to upload your image via Command Line Utility.

`openstack image create "SERVER" --file jammy-server-cloudimg-s390x.img --disk-format iso --container-format bare --public --unprotected`

![Image Upload via CLI](/images/glance-cli/cli-upload.png)

3. If the image is successfully updated your terminal will recieve the information about the image (Refer the image below).

![Image Uploaded Success](/images/glance-cli/upload-success.png)

4. Check whether the image is uploaded via Command Line Utility

`openstack image list`

![Image Listing via CLI](/images/glance-cli/cli-images.png)

5. The same is updated on the Web Console.

![Web Console](/images/glance-cli/ui-images.png)

### Common Issues & Resolves

> This section deals with some of the most common issues that one can encounter while uploading images via Web or CLI are listed here with the resolves.

1. Missing value auth-url required for auth plugin password.

> _Resolve_ : Export the auth configurations given above.

2. Error while uploading via Web Interface.

> _Resolve_ : Make sure your service are running and the image format is one from the available ones. If everything is well try running `./stack.sh` once more.

3. Permission denied to the folder /opt/stack/devstack

> _Resolve_ : Give required permissions to the folder and sub-folders

**INFO : If you encountered some other errors while installing raise a issue in the [Issues Section](https://github.com/syncattacker/OpenStack-Documentation/issues). I will be happy to resolve and provide support.**

### REFERENCES & OFFICIAL DOCUMENTATION

- [OFFICIAL GLANCE DOCUMENTATION](https://docs.openstack.org/glance/latest/)
- [OPENSTACK OFFICIAL WEBSITE](https://www.openstack.org/)
- [OPENSTACK AUTHENTICATION](https://docs.openstack.org/python-openstackclient/pike/cli/authentication.html)
- [JAMMY IMG FILE](https://cloud-images.ubuntu.com/jammy/20241002/jammy-server-cloudimg-s390x.img)
- [MORE UBUNTU CLOUD IMAGES](https://cloud-images.ubuntu.com/)
