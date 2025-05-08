# AppServiceQuickRepo

## Project Goal
### The goal of the project is to provide a __**quick**__ method for engineers to get started on setting up Azure Environments.

The resources you deploy will not match prefectly what you are trying to create, but they can be used as a **starting point**. 


## Open your [Azure Cloud Shell](https://learn.microsoft.com/en-us/azure/cloud-shell/overview), copy / paste the following code block in your shell to run. 
```
git clone https://github.com/kedsouza/AppServiceLinuxQuickRepo.git && cd AppServiceLinuxQuickRepo && python app.py
```
![Video Project 2 (1)](https://github.com/user-attachments/assets/a46b623a-b8c2-4313-8e32-fd4273c4693f)

Running tool this in your Azure Cloud Shell is the quickest way as you should be signed in by default and the shell has python installed by default.

## Optional Parameters
`location=<azure-region> ` default is northcentralus
example usage: `python app.py location=eastus`

## Project Reasonin / Sample Use Cases.

Creating interconnected Azure resources can be time consuming:
- Creation from the Azure Portal can involve a lot of clicks.
- Using the Azure CLI can involve a lot of workload in terms of making sure you are typing the correct parameters.

##  Run on your local machine. 
Prerequistes:
- Install the latest version of the Azure CLI and login to your Azure account.
- Have Python3 installed on your machine.

Run the following command from the command line:
`git clone https://github.com/kedsouza/AppServiceLinuxQuickRepo.git && cd AppServiceLinuxQuickRepo && python DEBUG app.py`
