
# env-tracker

## **\*\*WORK IN PROGRESS\*\***

Adds source-control features to important .gitignore'd files in your project.


## Motivation

Source control is awesome. If you don't think so, maybe this isn't the project for you.

Unfortunately, a whole heckin' lot of projects require top secret files that shouldn't be checked into source control.
Those files often have names like `.env` (and looks a whole lot like `.env-example`, but with real data!) 
and they contain all of your secrets: passwords, database connection details, api keys, and that 
embarrassing thing you said like five years ago and oh god I hope no one remembers that... etcetera etcetera.

Or, maybe you have some configuration files or scripts or macros for your project that you wrote for your own 
local dev environment to make your life easier.
You can't very well check those into your project either, because that would just be rude.

So what do you do? 

You add your private files to `.gitignore` and hope you don't accidentally delete them 
and always remember to keep a copy/pasted copy of any values that you change in the line below 
or manually keep backups
so that you don't "oh crap I closed that window after changing that config value yesterday on my feature branch
and now my undo buffer's cleared 
and now my config is broken after checking out the develop branch
and what was that dev api key again for that service that we had and then removed and just re-added?"

**Source control is awesome, but best practices dictate that some of your most important files 
are second class citizens that aren't allowed to benefit from source control**. 

Env Tracker aims to change that by being a simple tool that lets you use source control on your important .gitignore'd files. 

## How does it work?

Env Tracker works by 

- Create a git repository outside of your project repository
- Any .gitignore'd files you wish you could keep source-controlled are moved to the second repository where they can reap the benefits of source control.
- Those files are then symlinked back to their original location.
- As far as your project is concerned, nothing has changed.

If you're more of a code reading person, you could manually replicate the main 
features of Env Tracker by performing the following steps manually in your shell:

```bash
# Create a second repository for your project to house all of your ignored files
mkdir -p ~/.et/my-project
cd ~/.et/my-project
git init

cd path/to/my-project

# Create a secret file that you don't want to include in 
touch secret-file.txt
echo "secret password" > secret-file.txt
echo "secret-file.txt" >> .gitignore

# move your secret file to the second repository
mv secret-file.txt ~/.et/my-project/

# create a symlink in the files original location which points to the file
ln -s ~/.et/my-project/secret-file.txt secret-file.txt
```  

## Installation

Coming soon

## Configuration

Coming soon

## Caveats

- Only works on git repos

???

## CLI Methods

Coming soon

## Development

Run `python setup.py develop` to install the package locally
Run `python setup.py develop --uninstall` to uninstall the local installation
See https://stackoverflow.com/questions/3606457/removing-python-module-installed-in-develop-mode

## Development Goals
This project should be as minimal as possible (Maybe. Not sure what the qualifications for that are). 
It should be as stateless as possible.
It should only require the filesystem and not require configuration files or database

## Roadmap

Coming soon.

## Contributing

Coming soon

