import os.path

from BaseForPlugin import BaseForPlugin as parent
from BaseTools import BaseTools
from Config import Config
from SpecForOs import SpecForOs


class ForPlugin(parent):

    #Restoring original plugin files: 
    #copies the plugins specified in 'config.data["copy"][scriptDescriptor]' from the directory '{sourceDir}' to the target directory; 
    #the processing mode 'mode' is specified by argument 'arg0'; 
    #the path 'configFile' to the settings 'config' is specified by the argument 'arg1'; 
    #the directory 'sourceDir' is specified by argument 'arg2'; 
    #the script descriptor 'scriptDescriptor' is specified by argument 'arg3'; 
    #the target directory 'destDir' is specified by argument 'arg4'; 
    #the error file 'errorsFilePath' is either specified by argument 'arg5' or determined automatically; 
    #the array 'remove' of directories and files to be removed is specified by the argument 'arg6'
    @staticmethod
    def copy(arg0, arg1, arg2, arg3, arg4, arg5='', arg6=None):
        mode = arg0
        configFile = arg1
        config = Config(configFile)
        sourceDir = arg2
        scriptDescriptor = arg3
        destDir = arg4

        if arg5 == '':
            errorsFilePath = os.path.join(destDir, 'ERRORS.txt')
        else:
            errorsFilePath = arg5

        remove = arg6


        if 'copy' in config.data and scriptDescriptor in config.data['copy']:
            for line in config.data['copy'][scriptDescriptor]:
                if line != '':
                    index = line.find(' ', 0)
                    if index > 0:
                        line2 = line[:index]
                        line3 = line[index + 1:len(line)]
                    else:
                        line2 = line
                        line3 = ''
                    line = line3
                    index = line.find(' ', 0)
                    if index > 0:
                        line3 = line[:index]
                        line4 = line[index + 1:len(line)]
                    else:
                        line3 = line
                        line4 = ''
                    if line3 == './':
                        line3 = ''
                    sourcePath = os.path.join(sourceDir, line2.replace('/', os.sep))
                    destPath = os.path.join(destDir, line3.replace('/', os.sep))
                    if os.path.exists(sourcePath):
                        if line4 != '':
                            error = parent.copy(mode, sourcePath, destPath, scriptDescriptor, errorsFilePath, remove, line4)
                        else:
                            error = parent.copy(mode, sourcePath, destPath, scriptDescriptor, errorsFilePath, remove)
                        if error != 0:
                            return error


        return 0


    #Restoring modified plugin files: 
    #copies the plugins specified in 'config.data["copy"][scriptDescriptor]' from the directory '{sourceDir2}' to the target directory; 
    #the processing mode 'mode' is specified by argument 'arg0'; 
    #the path 'configFile2' to the settings 'config2' is specified by the argument 'arg1'; 
    #the path 'configFile' to the settings 'config' is specified by the parameter 'config2.data["change"]["configFile"]'; 
    #the directory 'sourceDir2' is specified by argument 'arg2'; 
    #the script descriptor 'scriptDescriptor' is specified by argument 'arg3'; 
    #the target directory 'destDir' is specified by argument 'arg4'; 
    #the error file 'errorsFilePath' is either specified by argument 'arg5' or determined automatically; 
    #the array 'remove' of directories and files to be removed is specified by the argument 'arg6'
    @staticmethod
    def change(arg0, arg1, arg2, arg3, arg4, arg5='', arg6=None):
        mode = arg0
        configFile2 = arg1
        config2 = Config(configFile2)
        sourceDir2 = arg2
        scriptDescriptor = arg3
        destDir = arg4

        if arg5 == '':
            errorsFilePath = os.path.join(destDir, 'ERRORS.txt')
        else:
            errorsFilePath = arg5

        remove = arg6

        scriptName0 = os.path.basename(__file__)
        position = scriptName0.rfind('.py')
        if position != -1:
            scriptName0 = scriptName0[:position]

        if not ('change' in config2.data and 'configFile' in config2.data['change']):
            SpecForOs.MessageBox1('The parameter config2.data[\'change\'][\'configFile\'] not set in a configuration file ' + configFile2, 'Script ' + scriptName0 + ', method \'change\'')
            return -1

        parentPath = os.path.dirname(configFile2)
        configFile = config2.data['change']['configFile']
        configFile = BaseTools.buildPath(parentPath, configFile)

        config = Config(configFile)


        if 'copy' in config.data and scriptDescriptor in config.data['copy']:
            for line in config.data['copy'][scriptDescriptor]:
                if line != '':
                    index = line.find(' ', 0)
                    if index > 0:
                        line2 = line[:index]
                        line3 = line[index + 1:len(line)]
                    else:
                        line2 = line
                        line3 = ''
                    line = line3
                    index = line.find(' ', 0)
                    if index > 0:
                        line3 = line[:index]
                        line4 = line[index + 1:len(line)]
                    else:
                        line3 = line
                        line4 = ''
                    if line3 == './':
                        line3 = ''
                    #sourcePath = os.path.join(sourceDir, line2.replace('/', os.sep))
                    sourcePath2 = os.path.join(sourceDir2, line2.replace('/', os.sep))
                    destPath = os.path.join(destDir, line3.replace('/', os.sep))
                    #if os.path.exists(sourcePath) and os.path.exists(sourcePath2):
                    if os.path.exists(sourcePath2):
                        if line4 != '':
                            error = parent.copy(mode, sourcePath2, destPath, scriptDescriptor, errorsFilePath, remove, line4)
                        else:
                            error = parent.copy(mode, sourcePath2, destPath, scriptDescriptor, errorsFilePath, remove)
                        if error != 0:
                            return error


        return 0
