# GUT-PY

Gut-py is a wrapper around git to make it a lot simpler to use. It is based on [John Saints'post on making git more usable](http://www.saintsjd.com/2012/01/a-better-ui-for-git/).

## Install
Copy `gut.py` into your path, and possibly rename it to simply `gut` and make it executable; something like so:

```
sudo mv gut.py /usr/local/bin/gut
sudo chmod +x /usr/local/bin/gut
```

## Usage
Gut-py currently provides the following additions to git. Any command that isn't supported will trickle down to git.

### Retreat
Undoes changes, either local-repo wide or on a single file. Use like so:

```
# Undo all the changes I made to working directory.
# Automatically save the user's work in a stash, then
# Instead of git stash; git reset --hard HEAD, just type:
> gut retreat

# Just undo the changes I made to one file.
# Automatically save a stash of the user's work first
# Rather than git checkout FILE (side note: why is it not git reset FILE? or is it?)
# Instead, just type:
> gut retreat FILE
```

### Switch
Change your local copy to another branch. Will detect if it needs to create a new branch or not.

```
> gut switch BRANCH
```

### Sync
Pushes your commited changes upstream. If the remote branch doesn't exist, will ask you before proceeding.

```
# If remote branch exists
> gut sync
Done

# If remote branch doesn't exists
> gut sync
The branch foobar doesn't exist on the remote. Create it? [Y/n] y
Done
```

