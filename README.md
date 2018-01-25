
# env-tracker

## WORK IN PROGRESS

Track untracked files in your project
A meta git repo to track changes to untracked files in your projects

## Motivation

The `et` command stands for "Env Tracker". The name originally comes from a desire to 
track changes to .env files that aren't checked into source control.
I periodically found myself in situations where I made a change to
a .env file that only to find that I needed to revert that change.
At worst, I think I spent at least a few hours one time trying to
track down a password I had lost.

Env Tracker gives you a way to enjoy the benefits of source control
for your .env files and anything else you don't 
want committed to your project repository.

## Development

Run `python setup.py develop` to install the package locally
Run `python setup.py develop --uninstall` to uninstall the local installation
See https://stackoverflow.com/questions/3606457/removing-python-module-installed-in-develop-mode

## Caveats

- Only works on github repos
- Does not allow granular control over which env files to commit when running the `commit` command. You can manually manage the `~/.et`

## Goals
This project should be as minimal as possible. 
It should be as stateless as possible.
It should only require the filesystem and not require configuration files or database


## Process

### Installing Env Tracker

`et install`

```bash
mkdir -p ~/.et
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
mkdir ~/.et/$etdir
cd ~/.et/$etdir
git init
echo """
[{
  "project-dir": "~/src/mediasuite/sarr",
  "et-dir": "~/.et/mediasuite/sarr"
}]  # append to the config json or whatever
""" > ~/.et/.etconfig/projects
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

1. move the file
2. symlink the file back to the original location
3. if the tracked dir is clean - add and commit the file to the tracked repo
    - else if the tracked dir is dirty
        - if nothing is staged - add and commit the file to the tracked repo
        - else if stuff is staged - add the file to the tracked repo, but throw message saying we won't auto-commit
4. if the source file is not tracked by git yet
    - Add a pattern to .gitignore to make sure the file doesnt get tracked
    - else if the source file is tracked by the source repo
        - throw an error message



### Untracking a file

`et untrack server/.env`

```bash
# Validate that the file is tracked, that the project file is a symlink to the et-project mirror
rm $PROJ/server/.env
mv $ET_PROJ/server/.env


```

### Handling errors
What happens when we try to call a command within a project that hasnt been registered?
