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
