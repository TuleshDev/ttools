import os
import os.path

from BaseForAddIn import BaseForAddIn as parent
from BaseTools import BaseTools
from Config import Config


class ForAddIn(parent):

    #Restoring additional modules: 
    #copies the modules specified in 'config.data["copy"][scriptDescriptor1]' from the directory '{sourceDir}' to the target directory; 
    #the processing mode 'mode' is specified by argument 'arg0'; 
    #the path 'configFile' to the settings 'config' is specified by the argument 'arg1'; 
    #the directory 'sourceDir' is specified by argument 'arg2'; 
    #the script descriptor 'scriptDescriptor1' is specified by argument 'arg3'; 
    #the target directory 'destDir' is specified by argument 'arg4'; 
    #the error file 'errorsFilePath' is either specified by argument 'arg5' or determined automatically; 
    #the parameter 'isBuildIncluded', which determines whether to include build modules, is either specified by the argument 'arg6', or is determined automatically; 
    #the parameter 'buildPrefix', which specifies the prefix of the build modules, is either specified by the argument 'arg7', or is determined automatically; 
    #the array 'remove' of directories and files to be removed is specified by the argument 'arg8'
    @staticmethod
    def copy(arg0, arg1, arg2, arg3, arg4, arg5='', arg6='', arg7='', arg8=None):
        mode = arg0
        configFile = arg1
        config = Config(configFile)
        sourceDir = arg2
        scriptDescriptor1 = arg3
        destDir = arg4

        if arg5 == '' and arg6 == '' and arg7 == '':
            errorsFilePath = os.path.join(destDir, 'ERRORS.txt')
            isBuildIncluded = False
            buildPrefix = 'Build.'
        elif arg6 == '' and arg7 == '':
            errorsFilePath = arg5
            isBuildIncluded = False
            buildPrefix = 'Build.'
        elif arg7 == '':
            errorsFilePath = arg5
            isBuildIncluded = arg6
            buildPrefix = 'Build.'
        else:
            errorsFilePath = arg5
            isBuildIncluded = arg6
            buildPrefix = arg7

        remove = arg8


        if 'copy' in config.data and scriptDescriptor1 in config.data['copy']:
            for line in config.data['copy'][scriptDescriptor1]:
                if line != '':
                    index = line.find(' ', 0)
                    if index != -1:
                        line2 = line[:index]
                        line3 = line[index + 1:len(line)]
                    else:
                        line2 = line
                        line3 = ''
                    index = line.find(buildPrefix, 0)
                    if (index == 0 and isBuildIncluded) or index != 0:
                        sourcePath = os.path.join(sourceDir, line2)
                        if os.path.exists(sourcePath):
                            if line3 != '':
                                error = parent.copy(mode, sourcePath, destDir, errorsFilePath, remove, line3)
                            else:
                                error = parent.copy(mode, sourcePath, destDir, errorsFilePath, remove)
                            if error != 0:
                                return error


        return 0


    #Restoring additional modules: 
    #copies the modules specified in 'config.data["copy"][scriptDescriptor1]' from the directory '{sourceDir2}' to the target directory; 
    #the processing mode 'mode' is specified by argument 'arg0'; 
    #the path 'configFile2' to the settings 'config2' is specified by the argument 'arg1'; 
    #the path 'configFile' to the settings 'config' is specified by the parameter 'config2.data["variant"]["configFile"]'; 
    #the directory 'sourceDir2' is specified by argument 'arg2'; 
    #the directory 'sourceDir' is set to the directory of the file 'configFile'; 
    #the script descriptor 'scriptDescriptor1' is specified by argument 'arg3'; 
    #the target directory 'destDir' is specified by argument 'arg4'; 
    #the error file 'errorsFilePath' is either specified by argument 'arg5' or determined automatically; 
    #the parameter 'isBuildIncluded', which determines whether to include build modules, is either specified by the argument 'arg6', or is determined automatically; 
    #the parameter 'buildPrefix', which specifies the prefix of the build modules, is either specified by the argument 'arg7', or is determined automatically; 
    #the array 'remove' of directories and files to be removed is specified by the argument 'arg8'
    @staticmethod
    def variant(arg0, arg1, arg2, arg3, arg4, arg5='', arg6='', arg7='', arg8=None):
        mode = arg0
        configFile2 = arg1
        config2 = Config(configFile2)
        sourceDir2 = arg2
        scriptDescriptor1 = arg3
        destDir = arg4

        if arg5 == '' and arg6 == '' and arg7 == '':
            errorsFilePath = os.path.join(destDir, 'ERRORS.txt')
            isBuildIncluded = False
            buildPrefix = 'Build.'
        elif arg6 == '' and arg7 == '':
            errorsFilePath = arg5
            isBuildIncluded = False
            buildPrefix = 'Build.'
        elif arg7 == '':
            errorsFilePath = arg5
            isBuildIncluded = arg6
            buildPrefix = 'Build.'
        else:
            errorsFilePath = arg5
            isBuildIncluded = arg6
            buildPrefix = arg7

        remove = arg8

        scriptName0 = os.path.basename(__file__)
        position = scriptName0.rfind('.py')
        if position != -1:
            scriptName0 = scriptName0[:position]

        if not ('variant' in config2.data and 'configFile' in config2.data['variant']):
            SpecForOs.MessageBox1('The parameter config2.data[\'variant\'][\'configFile\'] not set in a configuration file ' + configFile2, 'Script ' + scriptName0 + ', method \'variant\'')
            return -1

        parentPath = os.path.dirname(configFile2)
        configFile = config2.data['variant']['configFile']
        configFile = BaseTools.buildPath(parentPath, configFile)

        config = Config(configFile)
        sourceDir = os.path.dirname(configFile)


        if 'copy' in config.data and scriptDescriptor1 in config.data['copy']:
            for line in config.data['copy'][scriptDescriptor1]:
                if line != '':
                    index = line.find(' ', 0)
                    if index != -1:
                        line2 = line[:index]
                        line3 = line[index + 1:len(line)]
                    else:
                        line2 = line
                        line3 = ''
                    index = line.find(buildPrefix, 0)
                    if (index == 0 and isBuildIncluded) or index != 0:
                        sourcePath = os.path.join(sourceDir, line2)
                        sourcePath2 = os.path.join(sourceDir2, line2)
                        if os.path.exists(sourcePath) and os.path.exists(sourcePath2):
                            if line3 != '':
                                error = parent.copy(mode, sourcePath2, destDir, errorsFilePath, remove, line3)
                            else:
                                error = parent.copy(mode, sourcePath2, destDir, errorsFilePath, remove)
                            if error != 0:
                                return error


        return 0
