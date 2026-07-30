Creating Slack APP for Pipeline Notification.. 
-------------------------------------------------

1. https://api.slack.com/apps/
2. Create New App
3. From Scratch
4. Give App Name + Choose "<name> Development"
5. Go to Features/Org Level Apps
  > Enable it
6. Go to > Features/Incoming Webhook
  > Enable it
7. Go to > Features/Oauth & Permissions
  > Add Oauth Scope  > Scopes > Bot Token Scopes
    * chat write + read
    * im-write + read
    * channel write + read
  > Click "<name>-Development"
8. Go to > Features/Incoming Webhook
  > You can see the webhook URL now.... Use the "Webhook URL" for Notification...
