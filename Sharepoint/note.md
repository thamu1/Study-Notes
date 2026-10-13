To Get Main Page List ID from Sharepoint : 
 
Step 1: Find your base site URL and list name
  From that normal URL, look for two pieces of information:
  The Site URL: Everything up to the site name (Microsoft Office SharePoint Online, outils logiciels de collaboration d’équipe)
  The List Name: The exact name of your list (ProjectTracker)

Step 2: Combine them into a new link
  You are going to completely erase the (/Lists/ProjectTracker/AllItems.aspx) part and replace it with a special command (_api/web/lists/getByTitle('YourListName')/Id).
  Using our example, you would type this exact text directly into your browser's address bar:
  Microsoft Office SharePoint Online, outils logiciels de collaboration d’équipe
 
Step 3: Copy your ID
  Press Enter.
  The page will load a white screen with some code text.
  Look for a string of letters and numbers formatted like this: d3b07384-d113-4c3a-a2b1-5e2671561633. That is your List ID.
