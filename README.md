# rnmd - markdown execution runtime

Why? Execute code contained in markdown documentation.

## Running code contained in a markdown file

Execute a markdown document using the rnmd markdown execution runtime.
The document location passed to rnmd can currently be:

1. A file path
2. An url containing a document

```bash
rnmd notebook/test.md
```

## Passing arguments to the runtime

```bash
rnmd notebook/test.md --args arg1 arg2 arg3
```

Note: If passing arguments to an installed proxy then the **--args** flag is not required.

## Using rnmd to make a proxy linking to the specified document

Proxies are itermediate bash scripts that link to the document to be run.
(They also contain a shebang so you do not need to specify "bash" to run the script)
By executing a proxy we are using rnmd to execute our linked document without having to write the command ourselves.

```bash
#Make Proxy
rnmd notebook/test.md --proxy proxy/test
#Run Proxy
proxy/test
```

## Setting up rnmd for installation of proxies

You can also use rnmd to install proxies to your system.
To use the install feature of rnmd you need to run the setup process once before.
During this process have to specify a location (your **notebook**) where the proxies and document backups are installed to.
After this you are asked if you want to add this location to your path (using your shell configuration) making your installed proxies
executable from anywhere on your system by its name.

```bash
rnmd --setup
```

## Installing proxies

Install a proxy to your document on your system and make the command available from you path.
(Requires **rnmd --setup** to have been run)
Also moves a backup copy of your document into your notbook, which can be executed if the main linked document was not found.

```bash
#Make and install Proxy
rnmd notebook/test.md --install test-proxy-install
#Execute (if in path)
test-proxy-install
```

Note: Installing works for .sh scripts as well, so you can easily install them to your system.

## Making portable installs

If you want to transport your notebook to another machine you might want to perform a portable install of your documents instead.
By doing this the document you are installing is moved to your notebook and the location inside of your notebook is linked by the proxy instead.
The advantage of this is that you for instance can move you notebook around and to a different machine and the commands will all still work,
as the documents stay inside of the notebook. (for example if you make your notebook a git repo)

```bash
#Make and install Proxy
rnmd notebook/test.md --portableinstall test-portable-proxy-install
#Execute (if in path)
test-portable-proxy-install
```

## List installed commands of your notebook

```bash
rnmd --list
rnmd -l
```

## Remove/uninstall a command of your notebook

```bash
rnmd --remove test-portable-proxy-install
```

## Print the code contained inside of a document

```bash
rnmd --extract notebook/test.md
```

## Compile markdown to target location

```bash
rnmd notebook/test.md --compile compiled/test
```

## Create backups

Create a backup of the specified document in the backup dir of your notebook directory.

```bash
rnmd --backup notebook/test.md
```

## Create backups at location

Create a backup of the specified document in the backup dir of your notebook directory.
"backupto" path can either be a file path or a directory into which to move the source document.
Also useful for downloading documents to the local machine.

```bash
rnmd notebook/test.md --backupto target/test.md
```

## Check if the specified document exists

```bash
rnmd --check notebook/test.md
```

## Licence notes

The choice for using LGPL 2.1 is strategic so if i may stop developing the runtime
it will still receive  bugfixes/improvements from entities using this software in their programs.

As you could build whole programs based on the rn_md runtime (markdown -> script) interpreter
the GPL licence is not the way to go as it probably would make those programs GPL as well,
which in turn hurts adoption of this project as it would pretty much restrict its
usage to GPL programs only.

Because of these reasons the LGPL2.1 Licence was chosen.
