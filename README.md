# env-tracker

Track untracked files in your project
A meta git repo to track changes to untracked files in your projects

## Possible names

- env-tracker aka "et" - available on npm

## Caveats

- Only works on github repos
- Does not allow granular control over which env files to commit when running the `commit` command. You can manually manage the `~/.envs`

## Spec

- Creates a git repo that lives in `~/.envs`
- Each project gets its own git repo...? Makes renaming and moving things around easier
- The `.etconfig/` directory is its own git repo as well - to follow the spirit of the whole thing
  - `.etconfig/project-mapping`
- Each project is registered in `~/.envs` as `github-user/project-name`
- The project directories in `~/.envs` mirrors the corresponding project structure. E.g. `~/src/my-project/client/app/env.json` maps to `~/.envs/my-github-username/my-project/client/app/env.json`
- It should project against pushing the directory to a remote
- Each project also has a special `.etconfig` file with important variables like
    - project home
    - any configuration options
- There exists a top-level `.etconfig/projects` file that maps project directories to their corresponding et directory.
  - This should allow the tool to determine the et directory based on your current working directory without
  - e.g. when registering a file, crawl up the directory tree until you hit a directory registered in `.etconfig/projects`, and then you have the working directory and the corresponding et subdir
  - This keeps the cli stateless - all state is stored in config files

- Optionally adds a postcommit hook to your git repo to remind you if you have unsaved changes to your env files

## Commands

- `install` Initialize the `~/.envs` repo
- `list` List all of the projects being tracked
- `init` Registers a new project. Inuits the name/namespace from the git configuration
  - optionally allow user to specify name...? that might complicate the
- `rmproject`
- `track` Registers an untracked file
- `commit` - accepts `-m`; git commits all of the env files in the current project. To
- `copy` - not sure how this would work - handles renaming a github project
- `restore` - Not sure how this will work - if I delete my project, and then re-clone it again, I should be able to restore my environment config from the `~/.envs` repo
  - This should be idempotent, so it can be used to validate that the
- `status` - Show if there are any changes that need to be committed


## Process

### Installing Env Tracker

`et install`

```bash
mkdir -p ~/.envs
mkdir -p ~/.envs .etconfig
cd ~/.envs .etconfig
git init
touch projects
git add -A
git commit -m "Scaffold"
```

### Adding a project

``

`et init --help`
```
NAME:
  et - Env Tracker

SYNOPSIS:
  et init etdir projectdir

OPTIONS:

EXAMPLE:
  et init mediasuite/sarr ~/src/mediasuite/sarr
```

```bash
DEFAULT_ETDIR = "git remote -v | head -n1 | awk '{print $2}' | sed -e 's,.*:\(.*/\)\?,,' -e 's/\.git$//' -e 's/https:\/\/github\.com\///'"  # use this if the user doesn't provide a name
mkdir ~/.envs/$etdir
cd ~/.envs/$etdir
git init
echo """
[{
  "project-dir": "~/src/mediasuite/sarr",
  "et-dir": "~/.envs/mediasuite/sarr"
}]  # append to the config json or whatever
""" > ~/.envs/.etconfig/projects
```

### Tracking a new file

`et track server/.env`


```bash
# Determine filepath relative to the project home: `$PROJ/server`
mkdir -p $ET_PROJ/server
mv $PROJ/server/.env $ET_PROJ/server/.env
ln -s $ET_PROJ/server/.env $PROJ/server/.env
cd $ET_PROJ
git add -A .
git commit -m "Track new file: server/.env"
```


### Untracking a file

`et untrack server/.env`

```bash
# Validate that the file is tracked, that the project file is a symlink to the et-project mirror
rm $PROJ/server/.env
mv $ET_PROJ/server/.env


```

### Handling errors
What happens when we try to call a command within a project that hasnt been registered?
