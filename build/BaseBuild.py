import os
import os.path

from ForProject import ForProject
from ForPlugin import ForPlugin
from ForAddIn import ForAddIn


class BaseBuild:

    def __init__(self, sourceDir, destDir, version, scriptName, scriptDescriptor1, scriptDescriptor2, isBuildIncluded, buildPrefix):
        self.sourceDir = sourceDir
        self.destDir = destDir
        self.version = version

        self.scriptName = scriptName
        self.scriptDescriptor1 = scriptDescriptor1
        self.scriptDescriptor2 = scriptDescriptor2

        self.errorsFilePath = os.path.join(self.destDir, 'ERRORS.txt')
        self.isBuildIncluded = isBuildIncluded
        self.buildPrefix = buildPrefix

        self.forProject_copy = 'forProject.copy.json'
        self.forProject_change = 'forProject.change.json'
        self.forPlugin_copy = 'forPlugin.copy.json'
        self.forPlugin_change = 'forPlugin.change.json'
        self.forAddIn_copy = 'forAddIn.copy.json'
        self.forProject_variant = 'forProject.variant.json'
        self.forAddIn_variant = 'forAddIn.variant.json'


    def checkFile(self, mode, file, destDir, remove):
        fileName = os.path.basename(file)
        sourcePath = os.path.dirname(file)

        if self.forProject_copy != '' and fileName == self.forProject_copy:
            self.isConfigFound = True
            error = ForProject.copy(file, sourcePath, destDir, self.scriptName, remove)
            return error
        if self.forProject_change != '' and fileName == self.forProject_change:
            self.isConfigFound = True
            error = ForProject.change(mode, file, sourcePath, destDir, self.errorsFilePath, remove)
            return error
        if self.forPlugin_copy != '' and fileName == self.forPlugin_copy:
            self.isConfigFound = True
            error = ForPlugin.copy(mode, file, sourcePath, self.scriptDescriptor1, destDir, self.errorsFilePath, remove)
            return error
        if self.forPlugin_change != '' and fileName == self.forPlugin_change:
            self.isConfigFound = True
            error = ForPlugin.change(mode, file, sourcePath, self.scriptDescriptor1, destDir, self.errorsFilePath, remove)
            return error
        if self.forAddIn_copy != '' and fileName == self.forAddIn_copy:
            self.isConfigFound = True
            error = ForAddIn.copy(mode, file, sourcePath, self.scriptDescriptor1, destDir, self.errorsFilePath, self.isBuildIncluded, self.buildPrefix, remove)
            return error
        if self.forProject_variant != '' and fileName == self.forProject_variant:
            self.isConfigFound = True
            error = ForProject.variant(mode, file, sourcePath, self.scriptDescriptor2, destDir, self.errorsFilePath, remove)
            return error
        if self.forAddIn_variant != '' and fileName == self.forAddIn_variant:
            self.isConfigFound = True
            error = ForAddIn.variant(mode, file, sourcePath, self.scriptDescriptor1, destDir, self.errorsFilePath, self.isBuildIncluded, self.buildPrefix, remove)
            return error

        return 0
