# changegitremoteurl
# Description: 
This util helps you to change all the projects remote urls. When you changed your username on github, all of your repos links are changed as well, but not locally. So, this script solves this problem and changes the config file in your projects:
 `.git/config`:
 ```
[remote "origin"]
	url = https://github.com/<username>/<reponame>.git
```
# Installation:
  The only way to install this util is to clone the project          
# Usage:
in a directory where u cloned a project write in command-line:

    `Apple$ python3 chgitusname.py all`
    
or

    `Apple$ python3 chgitusname.py one`
    
    
  If you want to change all the config files in your project, you should use `all` arg. This only works if you have a directory where you store all the projects.
  
  In case if you want to change just one project's config file you should use `one` arg.
