# LEARNING NOTES & DOCUMENTATION

> This markdown focuses on the key points, definitions of **OPEN STACK** and **REFERENCES.**

## TABLE OF CONTENT

1. **Introduction to OPEN STACK**
2. **Components of OPEN STACK**
3. **Features of OPEN STACK**
4. **REFERENCES & OFFICIAL DOCUMENTATION**

### Introduction to OPEN STACK

_Definition_ : Open Stack is an open source cloud computing platform which provides us with **IaaS (Infrastructure as a Service)** and allows the user or organization to build and manage both public and private clouds.

It combines various resources (stacking resources) to provide different cloud services such as compute, storage, and networking etc.

### Components of OPEN STACK

_Definition_ : Components in Open Stack refer to different resource that manage different functionalities such as compute, storage, authentication, UI dashboard etc.

> Some Featured Components Are :

1.  Horizon
2.  Nova
3.  Keystone
4.  Cinder
5.  Swift
6.  Neutron
7.  Glance
8.  Heat

#### Horizon

_Definition_ : The User Interface to manage resources (AWS Console).

#### Nova

_Definition_ : Handles the management of VMs & containers (AWS EC2).

#### Keystone

_Definition_ : Handles the identification i.e, authentication and authorization (AWS IAM).

#### Cinder

_Definition_ : Handles the persistent storages such as SSDs, Hard Drives (AWS EBS).

#### Swift

_Definition_ : Handles the object storage, or unstructured data like images, audio and video (AWS S3).

#### Neutron

_Definition_ : Handles the networking such as routers, load balancers (AWS VPC).

#### Glace

_Definition_ : Handles and manages the machine images (Amazon Machine Images).

#### Heat

_Definition_ : Manages the automation **Infrastructure as Code** (AWS Elastic BeanStalk).

### Features of OPEN STACK

1. **Modular Architecture** : Deploy only the component that you need.
2. **Multi-tenancy** : Multiple user can access the same infrastructure still maintaining security and isolation between them.
3. **Open-source** : Open Stack is open thus enabling users to customize as per needs without the need of license.
4. **Comprehensive Dashboard** : Open Stack provides nice UI interface to manage and monitor it's resources over web.

### REFERENCES & OFFICIAL DOCUMENTATION

- [OFFICIAL DOCUMENTATION](https://docs.openstack.org/devstack/latest/)
- [GFG](https://www.geeksforgeeks.org/introduction-to-openstack/)
- [OPENSTACK OFFICIAL WEBSITE](https://www.openstack.org/)
- [OPEN SOURCE](https://opensource.com/resources/what-is-openstack)
