import os
import os.path

from AdditionalAction import AdditionalAction
from BaseForCommands import BaseForCommands as parent
from BaseTools import BaseTools
from Config import Config
from BuildMode import BuildMode
from JsonFile import JsonFile


class BaseForAddIn(parent):

    #A helper method designed to copy a specific module: 
    #copies the directories and files specified in 'config.data' to the target directory; 
    #the processing mode 'mode' is specified by argument 'arg0'; 
    #the path 'configFile' to the settings 'config' is specified by the argument 'arg1'; 
    #the target directory 'destDir' is specified by argument 'arg2'; 
    #the error file 'errorsFilePath' is specified by argument 'arg3'; 
    #the array 'remove' of directories and files to be removed is specified by the argument 'arg4'
    @staticmethod
    def copy(*params):
        i = 0
        for param in params:
            if i == 0:
                arg0 = param
            if i == 1:
                arg1 = param
            elif i == 2:
                arg2 = param
            elif i == 3:
                arg3 = param
            elif i == 4:
                arg4 = param
                break
            i = i + 1


        commands = list()
        commandsArgument1 = list()
        commandsArgument2 = list()

        i = 0
        for param in params:
            if i >= 5:
                line = param
                commands.append(line[:line.find(',', 0)])
                line = line[line.find(',', 0) + 1:len(line)]
                commandsArgument1.append(line[:line.find(',', 0)])
                commandsArgument2.append(line[line.find(',', 0) + 1:len(line)])
            i = i + 1


        mode = arg0
        configFile = arg1
        config = Config(configFile)
        sourceDir = os.path.dirname(configFile)
        destDir = arg2
        errorsFilePath = arg3
        remove = arg4

        jsonForCompare = None
        if mode == BuildMode.jsonForCompare:
            if not os.path.exists(destDir):
                BaseTools.createFolder(destDir)

            jsonForCompareFile = os.path.join(destDir, 'jsonForCompare.json')
            jsonForCompare = JsonFile(jsonForCompareFile)

            if not ('copy' in jsonForCompare.data):
                jsonForCompare.data['copy'] = []

        for key in config.data:
            if key == 'copy':
                for line in config.data[key]:
                    if not BaseTools.shouldItemBeRemoved(line, remove):
                        index = line.rfind('/')
                        line2 = line[:index]
                        line3 = line[index + 1:len(line)]

                        if line2 != '.':
                            sourceDir2 = os.path.join(sourceDir, line2)
                            destDir2 = os.path.join(destDir, line2)
                            destDir3 = line2
                        else:
                            sourceDir2 = sourceDir
                            destDir2 = destDir
                            destDir3 = ''

                        if mode == BuildMode.jsonForCompare:
                            sourceDir3 = os.path.join(sourceDir, line)
                            BaseTools.jsonForCompare_copy(line, line3 != '', sourceDir3, jsonForCompare)

                        if not os.path.exists(destDir2):
                            BaseTools.createFolder(destDir2)

                        if line3 != '':
                            sourcePath2 = os.path.join(sourceDir2, line3)
                            destPath2 = os.path.join(destDir2, line3)
                            if os.path.exists(destPath2):
                                os.remove(destPath2)
                            BaseTools.copy2(sourcePath2, destPath2)

                            parent.performCommands(mode, destPath2, line, commands, commandsArgument1, commandsArgument2, jsonForCompare)
                        else:
                            BaseTools.clearReadOnlyFolderAttribute(destDir2)

                            ##-->
                            ##if line2 != '.':
                            ##    destDir2_ = os.path.join(destDir, line2)
                            ##else:
                            ##    destDir2_ = destDir
                            ##
                            ##BaseTools.copy2(sourceDir2, destDir2_)
                            BaseTools.copy2(sourceDir2, destDir2)
                            ##<--

                            parent.performCommandsHelperForFolder(mode, destDir2, destDir3 + '/', commands, commandsArgument1, commandsArgument2, jsonForCompare)


        if mode == BuildMode.jsonForCompare:
            jsonForCompare.save()

        #Performing an additional action
        params2 = list()
        params2.append(configFile)
        params2.append(sourceDir)
        params2.append(destDir)
        params2.append(errorsFilePath)
        i = 0
        for param in params:
            if i >= 5:
                params2.append(param)
            i = i + 1
        error = AdditionalAction.run(*params2)

        return error
