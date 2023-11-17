import os
import os.path
import shutil

from AdditionalAction import AdditionalAction
from BaseTools import BaseTools as parent
from Config import Config
from BuildMode import BuildMode
from JsonFile import JsonFile


class ForProject(parent):

    #Restoring original files: 
    #copies the directories and files specified in 'config.data["copy"]' from the directory '{sourceDir}' to the target directory, whereinto, 
    #files specified by 'config.data["move"]' are moved to other directories, 
    #files specified by 'config.data["delete"]' are deleted; 
    #the path 'configFile' to the settings 'config' is specified by the argument 'arg0'; 
    #the directory 'sourceDir' is specified by argument 'arg1'; 
    #the target directory 'destDir' is specified by argument 'arg2'; 
    #the script name 'scriptName' is specified by the argument 'arg3'; 
    #the array 'remove' of directories and files to be removed is specified by the argument 'arg4'
    @staticmethod
    def copy(arg0, arg1, arg2, arg3='', arg4=None):
        configFile = arg0
        config = Config(configFile)
        sourceDir = arg1
        destDir = arg2

        if arg3 == '':
            scriptName = ''
        else:
            scriptName = arg3

        remove = arg4

        if not os.path.exists(destDir):
            parent.createFolder(destDir)


        #Copying the directories and files specified in 'config.data["copy"]' from the directory '{sourceDir}' to the target directory
        if 'copy' in config.data:
            for line in config.data['copy']:
                if not parent.shouldItemBeRemoved(line, remove):
                    index = line.rfind('/')
                    line2 = line[:index]
                    line3 = line[index + 1:len(line)]

                    if line2 != '.':
                        sourceDir2 = os.path.join(sourceDir, line2)
                        destDir2 = os.path.join(destDir, line2)
                    else:
                        sourceDir2 = sourceDir
                        destDir2 = destDir

                    if not os.path.exists(destDir2):
                        parent.createFolder(destDir2)

                    if line3 != '':
                        sourcePath2 = os.path.join(sourceDir2, line3)
                        destPath2 = os.path.join(destDir2, line3)
                        if os.path.exists(destPath2):
                            os.remove(destPath2)
                        parent.copy2(sourcePath2, destPath2)
                    else:
                        if line2 != '.':
                            destDir2 = os.path.join(destDir, line2)
                        else:
                            destDir2 = destDir

                        parent.copy2(sourceDir2, destDir2)


        #Moving files specified by 'config.data["move"]' to other directories
        if 'move' in config.data:
            for line in config.data['move']:
                if not parent.shouldItemBeRemoved(line, remove):
                    line2 = line[:line.find(' ', 0)]
                    line3 = line[line.find(' ', 0) + 1:len(line)]

                    index = line2.rfind('/')
                    line4 = line2[:index]
                    line5 = line2[index + 1:len(line2)]

                    index = line3.rfind('/')
                    line6 = line3[:index]
                    line7 = line3[index + 1:len(line3)]

                    index2 = line.find('{scriptName}', 0)
                    if index2 != -1:
                        line7 = line7.replace('{scriptName}', scriptName, 1)

                    if index == -1 or (index != -1 and line5 != line7):
                        if line4 != '.':
                            sourceDir2 = os.path.join(destDir, line4)
                        else:
                            sourceDir2 = destDir

                        if line6 != '.':
                            destDir2 = os.path.join(destDir, line6)
                        else:
                            destDir2 = destDir

                        if line5 != '' and line7 != '':
                            sourcePath2 = os.path.join(sourceDir2, line5)
                            destPath2 = os.path.join(destDir2, line7)

                            if os.path.exists(sourcePath2):
                                if not os.path.exists(destDir2):
                                    parent.createFolder(destDir2)

                                if os.path.exists(destPath2):
                                    os.remove(destPath2)
                                shutil.move(sourcePath2, destPath2)


        #Deleting files specified by 'config.data["delete"]'
        if 'delete' in config.data:
            for line in config.data['delete']:
                if not parent.shouldItemBeRemoved(line, remove):
                    index = line.rfind('/')
                    line2 = line[:index]
                    line3 = line[index + 1:len(line)]

                    if line2 != '.':
                        destDir2 = os.path.join(destDir, line2)
                    else:
                        destDir2 = destDir

                    if line3 != '':
                        destPath2 = os.path.join(destDir2, line3)
                        if os.path.exists(destPath2):
                            os.remove(destPath2)
                    else:
                        if os.path.exists(destDir2):
                            parent.clearReadOnlyFolderAttribute(destDir2)
                            shutil.rmtree(destDir2)


        return 0


    #Restoring modified files of general plan: 
    #copies the directories and files specified in 'config.data["change"]' from the directory '{sourceDir}' to the target directory; 
    #the processing mode 'mode' is specified by argument 'arg0'; 
    #the path 'configFile' to the settings 'config' is specified by the argument 'arg1'; 
    #the directory 'sourceDir' is specified by argument 'arg2'; 
    #the target directory 'destDir' is specified by argument 'arg3'; 
    #the error file 'errorsFilePath' is either specified by argument 'arg4' or determined automatically; 
    #the array 'remove' of directories and files to be removed is specified by the argument 'arg5'
    @staticmethod
    def change(arg0, arg1, arg2, arg3, arg4='', arg5=None):
        mode = arg0
        configFile = arg1
        config = Config(configFile)
        sourceDir = arg2
        destDir = arg3

        if arg4 == '':
            errorsFilePath = os.path.join(destDir, 'ERRORS.txt')
        else:
            errorsFilePath = arg4

        remove = arg5

        jsonForCompare = None
        if mode == BuildMode.jsonForCompare:
            if not os.path.exists(destDir):
                parent.createFolder(destDir)

            jsonForCompareFile = os.path.join(destDir, 'jsonForCompare.json')
            jsonForCompare = JsonFile(jsonForCompareFile)

            if not ('copy' in jsonForCompare.data):
                jsonForCompare.data['copy'] = []

        if 'change' in config.data:
            for line in config.data['change']:
                if not parent.shouldItemBeRemoved(line, remove):
                    index = line.rfind('/')
                    line2 = line[:index]
                    line3 = line[index + 1:len(line)]

                    if line2 != '.':
                        sourceDir2 = os.path.join(sourceDir, line2)
                        destDir2 = os.path.join(destDir, line2)
                    else:
                        sourceDir2 = sourceDir
                        destDir2 = destDir

                    if mode == BuildMode.jsonForCompare:
                        sourceDir3 = os.path.join(sourceDir, line)
                        parent.jsonForCompare_copy(line, line3 != '', sourceDir3, jsonForCompare)

                    if not os.path.exists(destDir2):
                        parent.createFolder(destDir2)

                    if line3 != '':
                        sourcePath2 = os.path.join(sourceDir2, line3)
                        destPath2 = os.path.join(destDir2, line3)
                        if os.path.exists(destPath2):
                            os.remove(destPath2)
                        parent.copy2(sourcePath2, destPath2)
                    else:
                        parent.clearReadOnlyFolderAttribute(destDir2)

                        if line2 != '.':
                            destDir2 = os.path.join(destDir, line2)
                        else:
                            destDir2 = destDir

                        parent.copy2(sourceDir2, destDir2)


        if mode == BuildMode.jsonForCompare:
            jsonForCompare.save()

        #Performing an additional action
        error = AdditionalAction.run(configFile, sourceDir, destDir, errorsFilePath)

        return error


    #Deletes directories and files specified in 'config2.data["delete"]' and 'config.data[scriptDescriptor2]["delete"]' from the target directory + 
    #copies the directories and files specified in 'config.data[scriptDescriptor2]["copy"]' from the directory '{sourceDir}' to the target directory; 
    #the processing mode 'mode' is specified by argument 'arg0'; 
    #the path 'configFile' to the settings 'config' is specified by the argument 'arg1'; 
    #the path 'configFile2' to the settings 'config2' is specified by the parameter 'config.data["deleteConfigFile"]'; 
    #the directory 'sourceDir' is specified by argument 'arg2'; 
    #the script descriptor 'scriptDescriptor2' is specified by argument 'arg3'; 
    #the target directory 'destDir' is specified by argument 'arg4'; 
    #the error file 'errorsFilePath' is either specified by argument 'arg5' or determined automatically; 
    #the array 'remove' of directories and files to be removed is specified by the argument 'arg6'
    @staticmethod
    def variant(arg0, arg1, arg2, arg3, arg4, arg5='', arg6=None):
        mode = arg0
        configFile = arg1
        config = Config(configFile)
        sourceDir = arg2
        scriptDescriptor2 = arg3
        destDir = arg4

        if arg5 == '':
            errorsFilePath = os.path.join(destDir, 'ERRORS.txt')
        else:
            errorsFilePath = arg5

        remove = arg6

        jsonForCompare = None
        if mode == BuildMode.jsonForCompare:
            if not os.path.exists(destDir):
                parent.createFolder(destDir)

            jsonForCompareFile = os.path.join(destDir, 'jsonForCompare.json')
            jsonForCompare = JsonFile(jsonForCompareFile)

            if not ('copy' in jsonForCompare.data):
                jsonForCompare.data['copy'] = []


        #Deleting directories and files specified in 'config2.data["delete"]' and 'config.data[scriptDescriptor2]["delete"]' in the target directory
        if 'deleteConfigFile' in config.data:
            parentPath = os.path.dirname(configFile)
            configFile2 = config.data['deleteConfigFile']
            configFile2 = parent.buildPath(parentPath, configFile2)
            config2 = Config(configFile2)
            if 'delete' in config2.data:
                ForProject.__deleteFilesFromFolder(mode, destDir, config2.data['delete'], jsonForCompare)
        if scriptDescriptor2 in config.data and 'delete' in config.data[scriptDescriptor2]:
            ForProject.__deleteFilesFromFolder(mode, destDir, config.data[scriptDescriptor2]['delete'], jsonForCompare)


        #Copying the directories and files specified in 'config.data[scriptDescriptor2]["copy"]' from the directory '{sourceDir}' to the target directory
        if scriptDescriptor2 in config.data and 'copy' in config.data[scriptDescriptor2]:
            for line in config.data[scriptDescriptor2]['copy']:
                if line != '' and not parent.shouldItemBeRemoved(line, remove):
                    index = line.rfind('/')
                    line2 = line[:index]
                    line3 = line[index + 1:len(line)]

                    if line2 != '.':
                        sourceDir2 = os.path.join(sourceDir, line2)
                        destDir2 = os.path.join(destDir, line2)
                    else:
                        sourceDir2 = sourceDir
                        destDir2 = destDir

                    if mode == BuildMode.jsonForCompare:
                        sourceDir3 = os.path.join(sourceDir, line)
                        parent.jsonForCompare_copy(line, line3 != '', sourceDir3, jsonForCompare)

                    if not os.path.exists(destDir2):
                        parent.createFolder(destDir2)

                    if line3 != '':
                        sourcePath2 = os.path.join(sourceDir2, line3)
                        destPath2 = os.path.join(destDir2, line3)
                        if os.path.exists(destPath2):
                            os.remove(destPath2)
                        parent.copy2(sourcePath2, destPath2)
                    else:
                        parent.clearReadOnlyFolderAttribute(destDir2)

                        ##-->
                        ##if line2 != '.':
                        ##    destDir2 = os.path.join(destDir, line2)
                        ##else:
                        ##    destDir2 = destDir
                        ##<--

                        parent.copy2(sourceDir2, destDir2)


        if mode == BuildMode.jsonForCompare:
            jsonForCompare.save()

        #Performing an additional action
        error = AdditionalAction.run(configFile, sourceDir, destDir, errorsFilePath)

        return error


    @staticmethod
    def __deleteFilesFromFolder(mode, dir1, data, json):
        if os.path.exists(dir1):
            for line in data:
                if line != '':
                    index = line.rfind('/')
                    line2 = line[:index]
                    line3 = line[index + 1:len(line)]

                    if line2 != '.':
                        dir2 = os.path.join(dir1, line2)
                    else:
                        dir2 = dir1

                    if mode == BuildMode.jsonForCompare:
                        dir3 = os.path.join(dir1, line)
                        parent.jsonForCompare_remove(line, line3 != '', dir3, json)

                    if line3 != '':
                        path2 = os.path.join(dir2, line3)
                        if os.path.exists(path2):
                            os.remove(path2)
                    else:
                        if os.path.exists(dir2):
                            shutil.rmtree(dir2)
