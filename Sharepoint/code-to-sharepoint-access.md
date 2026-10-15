Office 365 - SharePoint - Azure App Graph API Permission to access a SharePoint site

To access a SharePoint site using the Azure App Graph API, you need to set up the appropriate permissions for your Azure App.

Note: Only App owners will be able to add API permissions in their respective Apps.

Please follow below detailed steps:

1. Verify whether your application is registered in Microsoft Entra Id under App registrations.
2. 
<img width="896" height="408" alt="image" src="https://github.com/user-attachments/assets/c163a36d-e249-4988-abda-c4b3030009a5" />

For registered application, please follow next steps.

2. To use Graph API to access SharePoint, assign the Graph API permissions

Navigate to 'App registrations' in the Entra Id -> App registrations and search for your registered application.
On the application page, under 'Manage', select 'API permissions'.
Click '+ Add a permission' to include a new permission. (Refer below screenshot)

<img width="950" height="337" alt="image" src="https://github.com/user-attachments/assets/927dad76-28cf-47f2-8b8e-b16915696ce1" />

<img width="1713" height="844" alt="image" src="https://github.com/user-attachments/assets/a5f97eec-a910-4241-ab9d-72bfd57a0723" />

Select the type of permission for your application - Delegated or Application Permissions

<img width="988" height="325" alt="image" src="https://github.com/user-attachments/assets/9e9ca580-b827-48af-97cc-aa75fa47b0fa" />

Delegated Permissions: These are used when an app is acting on behalf of a user. The permissions are granted to the app by the user, and the app can only do what the user is allowed to do.

Application Permissions: These are used when an app needs to act as itself without a user context. The app is granted permissions directly by an admin, and it can perform actions across all users and data that it has been granted access to. 

 

Request Delegated Permissions

To request for Delegated permissions, click on Delegated permissions, search for the permission level (refer list in below screenshot) you are looking for your App to access SharePoint site, select the permission and click on Add Permission.

<img width="1005" height="834" alt="image" src="https://github.com/user-attachments/assets/e3fe777b-42ae-4f46-80b8-a7af464063fe" />

<img width="1005" height="834" alt="image" src="https://github.com/user-attachments/assets/e61c1c66-f095-4969-ab99-6a9d7d29fc2f" />

<img width="1005" height="834" alt="image" src="https://github.com/user-attachments/assets/fb480f7a-6344-4bbc-baa2-113ff231ee5f" />

After adding the permission to your registered Azure App, please create a SNOW case here: Service Catalog - Employee Self-Service Portal (service-now.com) 

Provide the following details in the SNOW case 

1. Name of the application registered in Azure AD:
2. App ID: 

(If you are requesting for Delegated Permissions for "Sites.Selected", please provide below information as well in the support case)

3. SharePoint Site URL (Specify the SharePoint Site URL for which your app requires read/write permissions): 
4. Specify the role – Read or Write (Write provides both read as well as write access):

Note: Do not add any other permission to your registered Azure App other than the one you are requesting in the support case.

 

Request Application Permissions

To request for Application permissions, click on Application permissions, search for the permission level "Sites.Selected", select the permission and click on Add Permission.

Note: Application Permission can only be granted for "Sites.Selected" Graph Api Permission.

<img width="862" height="616" alt="image" src="https://github.com/user-attachments/assets/e183a18d-1027-4107-aebc-5b9c1f9fae9a" />

Important: Do not add any other permission to your registered Azure Apps other than Sites.Selected. Admin consent cannot be granted if any other permission is added to the API permission list.

<img width="1663" height="310" alt="image" src="https://github.com/user-attachments/assets/9a65d68c-3218-4082-a576-4fc72be499c9" />

After adding Sites.Selected Application permission to your registered Azure App, please create a SNOW case here: Service Catalog - Employee Self-Service Portal (service-now.com) 

Provide the following details in the SNOW case

1. Name of the application registered in Azure AD:
2. App ID: 
3. SharePoint Site URL (Specify the SharePoint Site URL for which your app requires read/write permissions): 
4. Specify the role – Read or Write (Write provides both read as well as write access):








