

<img width="1080" alt="image" src="https://github.com/user-attachments/assets/1bebb186-4d78-41a3-b3f0-6db02ff772a8" />


git set folder:
git config --global --add safe.directory 'D:/thamu/study Album/Study-Note'

git init

git clone <repository_url>

git checkout -b <branch_name>

git status

git add <file(s)>

git config --global --add safe.directory 'D:/thamu/study Album/git'

git commit -m "Your commit message"

git push <remote> <branch>
=> git push origin "" 

git merge <branch_name>

-----------------------------------------------

Git:
	- git is a version control system.
	- open source, free tool.
	- allow all community to use.


Settings:
	- Name
	- Email
	- Default Editor.
	- Line ending.

Levels:
	- System (all users )
	- Global (All repositories of the current user)
	- Local (The current repository)
	
cmd:
	git config:
		- git config --help
		- git config --global user.name "<name>" 
		- git config --global user.email <gmail_id>	
		- git config --global core.editor "code --wait"
		- git config --global -e
		
			=> config file
		
		End of line:
			-	core.cutocrlf
			- windows end line:
				- \r (carriage return)
				- \n (Line Feed)
				- git config --global core.autocrlf true
			- MacOS/ linux:
				- \n (Line Feed)
				- git 
				- git config --global core.autocrlf input
	
	Snapshot:
		- mkdir moon
		- cd moon
		- git init [initialize initial git repository]
		- ls -a
		
	Workflow:
		- Our Project dir -> staging area -> git repo.
		- git add . -> staging area -> review (git commit -m "") -> release ().
		
		- Each commit :
			- ID
			- Message
			- Date/time
			- Author
			- Complete snapshot
			
		- Git compress the content and doesn't store the duplicate content.
		- Each git commit command store the snapshot of the folder in staging area.
		- add file:
			- echo "hi" > file.txt [> - overwrite, >> - append]
			- git status
			- git add .
		
		- commit changes:
			- git commit -m "msg"
			- git commit -> open commit_editmsg :
				- A short description
				- Long description
			
			best practice:
				- commit often. [as you reach a state you want to record then make a commit]
				- seperate the commit dev, bug fix etc.
				- make msg meaning full.
				- use past tense : fixed the bug.
				
		- skip staging area:
			- git commit -a -m "" (-am "")
				
		- remove file:
			- git ls-files
			- rm file2.txt
			- git status
			- git rm file2.txt 
			
		- rename and move file:
			- mv file.txt main.js
			- git add file.txt
			- git add main.js
			- git mv main.js file1.js
			- git status
			- git commit -m ""

		- git ignore [it skip the folder to add to staging area]
			- gitingnore
			- git add .ignore
			- git commit -m ""
			- git rm --chched <file>
			- git ls-files
			
		- short status:
			- git status -s 
		
	View staged and unstaged status:
		
		Staged:
			- git diff --staged 
			- git diff
			
			visual diff tools:
			
				- kdiff3
				- p4merge
				- vscode
			
			congig setting:
			
				- git config --global diff.tool vscode
				- git config --global difftool.vscode.cmd "code --wait --diff $LOCAL $REMOTE"
			
				- git config --global -e [edit in file]
				
				test:
					- git difftool
					- git difftool --staged
					
			Log file:
				- git log
				- git log ---oneline
				
			viewing commit:
				
				- git log --oneline
				- git show <id>
				- git show HEAD~<n>
				- git show HEAD~<n>:.gitignore
				
				- git ls-tree HEAD~1
				
			Git objects:
			
				- Commits 
				- Blobs (Files)
				- trees (Directories)
				- Tags
			
		Unstaging:
			
			- git restore --staged <files>
		
	Discarding Local changes:
		
		git doesn't know about unknown added files. so it still show up.
		
		- git restore .
		- git clean
		- git clean --help (-h)
		
	Restore a file to an earlier version:
		
		Restore the deleted file
		
		- git rm file.json [if use git rm both working dir and git repo]
		- git log --oneline
		- git restore -h or --help
		- git restore --source=HEAD~1 fil.json
		
