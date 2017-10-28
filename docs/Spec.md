# Env Tracker Spec

## Overview

- Creates a git repo that lives in `~/.et`
- Each project gets its own git repo, similar to how prm works.
- The `.etconfig/` directory is its own git repo as well - to follow the spirit of the whole thing
  - `.etconfig/project-mapping`
  
- Each project is registered in `~/.et/$current_directory` by default
    - If there is a conflict, then fail hard and ask for a specific name
    - `~/.et` must be a flat directory. No subdirectories allowed. This allows us to read all of the project infos without a mast config file or something
- The project directories in `~/.et` mirrors the corresponding project structure. E.g. `~/src/my-project/client/app/env.json` maps to `~/.et/my-github-username/my-project/client/app/env.json`


- ET does not provide support for pushing the tracking repos to remotes.
    - These are meant to be private files, so push to remote at your own risk

- ~~Optionally adds a postcommit hook to your git repo to remind you if you have unsaved changes to your env files~~
- Add commit hook to automatically commit changes in a post-commit hook


# Commands defined by the et application

# Version 1 - Basics, tracking and untracking
- `init [project_name='parent_directory_name'] [parent_directory='.']` Registers a new project. Inuits the name/namespace from the git configuration
  - if `$ET_HOME` doesn't exist, creates it
  - optionally allow user to specify a parent directory. 
  - optionally allow user to specify name.
  - force the user to specify a name if the current dirname is already taken
  - allow user to set `auto-commit=false` to omit registering the post-commit hook
- `track filename` Registers an untracked file - rename to add
- `untrack filename` Unregisters a tracked file and moved it back - rename to rm
- Git commit hook that looks for changes in the follower dir and automatically commits changes
    - commit message contains the branch you were on when you committed and the actual commit message.
    - follower directory should mirror upstream branches, because it would be prohibitively complicated to try to keep track of everything, like a merge happening on a remote and deleting the branch.

# Version 2 - Env Tracker meta commands
- Convert commands to use a proper python command line tool
- `current` Display information about the current project
- `list` List all of the projects being tracked
    - Or should it list all of the tracked files???
- `rmproject` untracks all tracked files and removes the tracked directory
- `mvproject` rename a project
- `auto-commit=false` option for tracking a file which means the file is not automatically commited on commit hook

# Version 3 - Git
- `commit` - accepts `-m`; git commits all of the env files in the current project. To
- `status` - Show if there are any changes that need to be committed
- `copy` - not sure how this would work - handles renaming a github project



Follower directory structure


Hmm... You don't even need the parent directory to be under parent control technically
If you're not under parent control, it's essentially a symlinking tool
