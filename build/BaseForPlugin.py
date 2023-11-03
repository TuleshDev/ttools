import os
import os.path
import shutil

from AdditionalAction import AdditionalAction
from BaseForCommands import BaseForCommands as parent
from BaseTools import BaseTools
from Config import Config
from BuildMode import BuildMode
from JsonFile import JsonFile


class BaseForPlugin(parent):

    #A helper method for a specific plugin, intended for copying and deleting: 
    #copies and deletes directories and files specified in 'config.data' to the target directory; 
    #the processing mode 'mode' is specified by argument 'arg0'; 
    #the path 'configFile' to the settings 'config' is specified by the argument 'arg1'; 
    #the target directory 'destDir' is specified by argument 'arg2'; 
    #the plugin name 'pluginName' is specified by the argument 'arg3'; 
    #the error file 'errorsFilePath' is specified by argument 'arg4'; 
    #the array 'remove' of directories and files to be removed is specified by the argument 'arg5'
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
            elif i == 5:
                arg5 = param
                break
            i = i + 1


        commands = list()
        commandsArgument1 = list()
        commandsArgument2 = list()

        i = 0
        for param in params:
            if i >= 6:
                line = param
                commands[i - 6] = line[:line.find(',', 0)]
                line = line[line.find(',', 0) + 1:len(line)]
                commandsArgument1[i - 6] = line[:line.find(',', 0)]
                commandsArgument2[i - 6] = line[line.find(',', 0) + 1:len(line)]
            i = i + 1


        mode = arg0
        configFile = arg1
        config = Config(configFile)
        sourceDir = os.path.dirname(configFile)
        destDir = arg2
        pluginName = arg3
        errorsFilePath = arg4
        remove = arg5

        jsonForCompare = None
        if mode == BuildMode.jsonForCompare:
            if not os.path.exists(destDir):
                BaseTools.createFolder(destDir)

            jsonForCompareFile = os.path.join(destDir, 'jsonForCompare.json')
            jsonForCompare = JsonFile(jsonForCompareFile)

            if not ('copy' in jsonForCompare.data):
                jsonForCompare.data['copy'] = []

        for key in config.data:
            for line in config.data[key]:
                if not BaseTools.shouldItemBeRemoved(line, remove):
                    index = line.find(' ', 0)
                    if index > 0 and key == 'copy':
                        line2 = line[:index]
                        line5 = line[index + 1:len(line)]
                    else:
                        line2 = line
                        line5 = line

                    index = line2.rfind('/')
                    line3 = line2[:index]
                    line4 = line2[index + 1:len(line2)]

                    index = line5.find('{pluginName}', 0)
                    if index != -1:
                        line5 = line5.replace('{pluginName}', pluginName, 1)

                    index = line5.rfind('/')
                    line6 = line5[:index]
                    line7 = line5[index + 1:len(line5)]

                    if line3 != '.':
                        sourceDir2 = os.path.join(sourceDir, line3)
                    else:
                        sourceDir2 = sourceDir

                    if line6 != '.':
                        destDir2 = os.path.join(destDir, line6)
                        destDir3 = line6
                    else:
                        destDir2 = destDir
                        destDir3 = ''

                    if mode == BuildMode.jsonForCompare:
                        if key == 'copy':
                            sourceDir3 = os.path.join(sourceDir, line)
                            BaseTools.jsonForCompare_copy(line5, line4 != '' and line7 != '', sourceDir3, jsonForCompare)

                        if key == 'delete':
                            destDir4 = os.path.join(destDir, line)
                            BaseTools.jsonForCompare_remove(line5, line4 != '' and line7 != '', destDir4, jsonForCompare)

                    if key == 'copy':
                        if not os.path.exists(destDir2):
                            BaseTools.createFolder(destDir2)

                    if line4 != '' and line7 != '':
                        sourcePath2 = os.path.join(sourceDir2, line4)
                        destPath2 = os.path.join(destDir2, line7)

                        if key == 'copy':
                            if os.path.exists(destPath2):
                                os.remove(destPath2)
                            BaseTools.copy2(sourcePath2, destPath2)

                            parent.performCommands(mode, destPath2, line, commands, commandsArgument1, commandsArgument2, jsonForCompare)

                        if key == 'delete':
                            if os.path.exists(destPath2):
                                os.remove(destPath2)
                    else:
                        if key == 'copy':
                            BaseTools.clearReadOnlyFolderAttribute(destDir2)

                            ##-->
                            ##if line6 != '.':
                            ##    destDir2_ = os.path.join(destDir, line6)
                            ##else:
                            ##    destDir2_ = destDir
                            ##
                            ##BaseTools.copy2(sourceDir2, destDir2_)
                            BaseTools.copy2(sourceDir2, destDir2)
                            ##<--

                            parent.performCommandsHelperForFolder(mode, destDir2, destDir3 + '/', commands, commandsArgument1, commandsArgument2, jsonForCompare)

                        if key == 'delete':
                            if os.path.exists(destDir2):
                                BaseTools.clearReadOnlyFolderAttribute(destDir2)
                                shutil.rmtree(destDir2)


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
            if i >= 6:
                params2.append(param)
            i = i + 1
        error = AdditionalAction.run(*params2)

        return error
