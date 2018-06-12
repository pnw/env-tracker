
# $ et_

## What is Env Tracker (et)?

If you're a web developer, you probably have some files in your project with names like ".env", 
which store private data like passwords and api keys. 
Unfortunately, sane practices dictate that you hide these important files from source control (for good reason!)
by adding their names to .gitignore.

Not having source control on those files kind of sucks, because source control preserves file histories and allows
you to easily revert changes when you rollback commits or change branches.

Env Tracker is a CLI tool that adds private, local source control to your private files so you don't lose them.

**\*\*WORK IN PROGRESS\*\***

## How does it work?

Env Tracker creates a git repository parallel to your project repository.
When you tell Env Tracker to monitor a file, it moves that file into the parallel repository and symlinks
the file back to its original location.

As far as your project is concerned, nothing has changed, but now you have source control on your private files.

Before Env Tracker

```
some-project/
    .gitignore
    .env
    some-files.txt
    src/
```

After Env Tracker

```
~/.et/some-project/
    .git/
    .env

some-project/
    .git/
    .gitignore
    .env@ -> ~/.et/my-project/.env
    some-files.txt
    src/
```


## Goals

- It should be able to be used without requiring buy-in from other project collaborators.
Your colleagues shouldn't know that you're using Env Tracker unless you tell them.
That means not touching any of the tracked repository files, including .gitignore.
- It should require as few commands as possible.
- It should rely only on the filesystem for state, instead of a database or configuration files.


## Installation

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/).

```
pip install env-tracker
```

Env Tracker currently supports only python 3.6+, but plans to support 2.7 and 3.4+

## Configuration

Coming soon


## Documentation

Coming soon

## Development

Run `python setup.py develop` to install the package locally
Run `python setup.py develop --uninstall` to uninstall the local installation
See https://stackoverflow.com/questions/3606457/removing-python-module-installed-in-develop-mode

## Roadmap

Coming soon.

## Contributing

Coming soon

## Links

- Website:
- Documentation:
- License:
- Releases:
- Code:
- Issue tracker:
- Test status:
- Linux, Mac:
- Windows:
- Test coverage:

