<h1 align="center">ttools/build</h1>

<div align="center">

  [![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/TuleshDev/ttools/blob/main/build/README.md)
  [![ru](https://img.shields.io/badge/lang-ru-red.svg)](https://github.com/TuleshDev/ttools/blob/main/build/README.ru.md)

</div>

## General information

This is a tool that allows you to build a project by copying files and folders from different sources and making changes. More precisely, this project provides a set of classes from which you can build a Python script that copies specific files and folders from various sources.

In fact, it all comes down to copying. First, copying is done from one folder, then from another, and so on, from several folders. Files from each next source-folder overwrite files from the previous source-folder if the files match. Since matching files are overwritten and the number of source-folders is unlimited, you can make changes where needed.

Sources are folders containing files and folders that should be copied. For example, source-folders can be copies of different projects.

In order to give this some structure, we need to agree on some assumptions that will be followed further on. Let's assume that all source-folders are collected in one place - an arbitrary folder on the disk. Let's call it the **source folder**. Copying is done to a specific folder - the **destination folder**. We will call the script itself a **build script**.

It is assumed that the *destination folder* is empty before running the *build script*. To clean it, you can write a script that will clean this folder. Naturally, after running the *build script*, the *destination folder* will contain the copied files and folders - this is the build result. The name, the **build result**, we will assign to this content of the *destination folder*. In general, I will try to highlight all the names I enter in **bold** when I first mention the name, and will highlight subsequent occurrences of the name in *italics* to distinguish it from the general text. And a certain number of names will have to be entered in order to have a set of terms that can be used in the process of presentation.

You can place copies of multiple projects in the *source folder*. These can be copies of your own projects or copies of projects from GitHub. Each of these projects must be placed in a separate folder and in it you must place a configuration file that specifies which files and folders should be copied during the process of obtaining the *build result*. More details about configuration files will be discussed later, but for now it can be mentioned that these are files in JSON format.

> **Note**: I am talking specifically about copies of projects because the *source folder* is purely for service purposes, it is only needed to obtain the *build result*, and it is better to place your own projects being developed in another place.

In general, this project can be used to copy arbitrary files and folders. But it is quite convenient to use it for copying program codes.

If we talk about program codes, then in addition to the mentioned projects, sources for copying, you can create an additional folder. It can contain codes that change and supplement the codes of the copied projects. In this folder you also need to place a configuration file that determines what and how to copy. Naturally, the codes from this folder should be copied last. More precisely, the use cases are described in the next section.

## Possible use cases

Here are some scenarios where this project might be useful:
- the *source folder* contains a copy of the project from GitHub, I would like to copy the project files to the *destination folder* and supplement the project with a number of new files (and folders) that modify the functionality of this project. These additional files (and folders) can be placed in a separate subfolder of the *source folder*, taking into account their placement in the project from GitHub, and then it turns out that we have two sources for copying - a folder with a copy of the main project from GitHub and a folder with additional files (and folders). The order of copying is important, so the contents of the first folder are copied first, then the second;
- there are copies of several projects from GitHub in the *source folder*, and in it there is a folder with additional files (and folders). I would like to copy the contents of all these projects from GitHub to the *destination folder* and add additional files (and folders) to it. Again, the order of copying is important. In this case, the folder with additional files (and folders) should be copied last, so that the files from it cover the files of the same name from GitHub and change their contents;
- there are codes of the own project under development, but it is divided into folders according to some principle convenient for the developer. For example, these could be folders like: a folder with main codes common to this and another project, a folder with codes specific to this project, a folder with additional modules or plugins that should appear in the *destination folder* or, on the contrary, should not be there, depending on the needs of the developer or user of the project, a folder with codes intended for the configuration of the project, a folder with documentation. If the developer frequently rebuilds and tests the project, and the plugins and documentation take up a lot of disk space or significantly increase the *build script's* runtime, then the developer may temporarily not include the already debugged plugins and ready documentation in the *build result* in the *destination folder*. At the same time, all plugins and documentation will be included in the final *build result* intended for production.

These are only some of the possible use cases of this project.

## Folder structure

The structure of folders and their names in the *source folder* can be arbitrary, for example:

```console
Origin/
Changes/
Plugins/
Docs/
```

In this case, the `Origin` folder may contain a copy of the project from GitHub, the `Changes` folder may contain files and folders with codes that modify the original project, the `Plugins` folder may contain codes that change the functionality of plugins from the `Origin` folder, or codes for new plugins, and the `Docs` folder may contain documentation.

## Building order

It matters in what order the files and folders from the project folders are copied, since different projects may have files with the same names and a copy of a file from one project will overlap a copy from another project. The copy order will be determined by the names of the project folders and the natural alphabetical ordering of these names.

The user is given the opportunity to name project folders as he wishes. But it is important to remember that before copying, folders are sorted in alphabetical order.

The folder names above can be changed as follows so that their contents are copied in the order they are listed above:

```console
1_Origin/
2_Changes/
3_Plugins/
4_Docs/
```

## How does this work?

As mentioned at the beginning, this project contains a set of Python classes that can be used to build a script that does the copying. In the future, we will call it a **build script**. The script can have any name, for the sake of clarity, let's call it `build.py`. An example of this script is contained in this folder (`build`) of the repository. It's called `"build (Example).py"`. Here are its contents:

> [From commit `1424691a`, file `build/build (Example).py`](https://github.com/TuleshDev/ttools/blob/1424691a/build/build (Example).py)

```python
1	import sys
2	sys.path.append('./0_Build/ttools/build')
3	sys.pycache_prefix='C:/__pycache__'
4	
5	from BuildHelper import BuildHelper
6	
7	
8	def main():
9	    isBuildIncluded = True
10	
11	    buildHelper = BuildHelper(__file__, isBuildIncluded)
12	    error = buildHelper.run()
13	    return error
14	
15	
16	if __name__ == '__main__':
17	    main()
```


We will call the folder where the `build.py` script is located the **build folder**. This folder can be any folder. The *build folder* can be the same as the *source folder* if the `build.py` script is located in the *source folder*.

In the `build.py` script, the `run()` method of the object of the `BuildHelper` class is called. This class, as well as its parent class `BasePaths`, are helper classes and are closely related to the *build result* and therefore should be written individually for the needs of the *build result* and located in the *build folder*. The `BuildHelper` class defines how the `ttools/build` tool classes will be used during the copy process, and the `BasePaths` class is for customizing the paths used. The `BasePaths` and `BuildHelper` classes rely on a set of classes defined in the `ttools/build` folder. This folder contains the files `"BasePaths (Example).py"` and `"BuildHelper (Example).py"`, which define examples of the `BasePaths` and `BuildHelper` classes, respectively.

This is what the `"BasePaths (Example).py"` file looks like:

> [From commit `1424691a`, file `build/BasePaths (Example).py`](https://github.com/TuleshDev/ttools/blob/1424691a/build/BasePaths (Example).py)

```python
1	import os.path
2	
3	from BaseTools import BaseTools
4	
5	
6	class BasePaths:
7	
8	    def __init__(self, file):
9	        self.rootDir = os.path.dirname(file)
10	        rootDirName = os.path.basename(self.rootDir)
11	
12	        sourceFragment = ''
13	        path = os.path.join(self.rootDir, 'source.txt')
14	        if os.path.exists(path):
15	            with open(path, 'r') as read_file:
16	                sourceFragment = read_file.readline().replace('\n', '')
17	
18	        if sourceFragment == '':
19	            self.sourceDir = os.path.join(self.rootDir, 'sourceDir')
20	        else:
21	            self.sourceDir = BaseTools.buildPath(self.rootDir, sourceFragment)
22	
23	        destFragment = ''
24	        path = os.path.join(self.rootDir, 'destination.txt')
25	        if os.path.exists(path):
26	            with open(path, 'r') as read_file:
27	                destFragment = read_file.readline().replace('\n', '')
28	
29	        if destFragment == '':
30	            self.destDir = os.path.join(self.rootDir, 'destDir')
31	        else:
32	            destFragment = BaseTools.buildPath(self.rootDir, destFragment)
33	            self.destDir = destFragment
34	
35	        self.version = ''
36	
37	        self.scriptName = os.path.basename(file)
38	        position = self.scriptName.rfind('.py')
39	        if position != -1:
40	            self.scriptName = self.scriptName[:position]
41	
42	        self.scriptDescriptor1 = rootDirName + '.' + self.scriptName
43	        self.scriptDescriptor2 = self.scriptDescriptor1
```


In the definition of the `BasePaths` class from this file, the values ​​written in the `source.txt`, `destination.txt`, `version.txt` files, which must be located in the root of the *build folder*, are read. These values ​​allow you to define class attributes for the *source folder*, *destination folder*, and version number of the *build result*. The class also defines several additional attributes, including `scriptName`, `scriptDescriptor1`, and `scriptDescriptor2`.

In some cases, the version of the *build result* is an important parameter, and in this case, it must be somehow used in forming the `self.destDir` attribute of the `BasePaths` class for the *destination folder*, in order to take into account where to copy depending on the version number. This can be done, for example, like this:

```python
1	class BasePaths:
2	
3	    def __init__(self, file):
4	        self.rootDir = os.path.dirname(file)
5	        rootDirName = os.path.basename(self.rootDir)
6	
7	        ...
8	
9	        destFragment = ''
10	        path = os.path.join(self.rootDir, 'destination.txt')
11	        if os.path.exists(path):
12	            with open(path, 'r') as read_file:
13	                destFragment = read_file.readline().replace('\n', '')
14	
15	        if destFragment == '':
16	            self.destDir = os.path.join(self.rootDir, 'destDir')
17	        else:
18	            destFragment = BaseTools.buildPath(self.rootDir, destFragment)
19	            self.destDir = os.path.join(destFragment, rootDirName)
20	
21	        path = os.path.join(self.rootDir, 'version.txt')
22	        if os.path.exists(path):
23	            with open(path, 'r') as read_file2:
24	                self.version = read_file2.readline().replace('\n', '')
25	                self.destDir = os.path.join(self.destDir, self.version)
26	        else:
27	            self.version = '1'
```


If the version number is not important for the *build result*, you can use the example from the file `"BasePaths (Example).py"` as a basis for the `BasePaths` class.
