import os
import os.path

from BaseBuild import BaseBuild
from BuildMode import BuildMode


class Build(BaseBuild):

    def __init__(self, sourceDir, destDir, version, scriptName, scriptDescriptor1, scriptDescriptor2, isBuildIncluded, buildPrefix):
        super().__init__(sourceDir, destDir, version, scriptName, scriptDescriptor1, scriptDescriptor2, isBuildIncluded, buildPrefix)


    def run(self, mode=BuildMode.build, remove=None):
        self.isConfigFound = False
        self.checkVersion = False
        if self.version != '' and self.version is not None:
            self.checkVersion = True
        error = self.__checkFolder(mode, self.sourceDir, remove)
        return error


    def __checkFile(self, mode, file, remove):
        error = super().checkFile(mode, file, self.destDir, remove)
        return error


    def __checkFolder(self, mode, dir, remove):
        if mode == BuildMode.build or mode == BuildMode.jsonForCompare:
            error = self.__folder_build(mode, dir, True, remove)
            return error

        if mode == BuildMode.forProject_copy:
            error = self.__folder_forProject_copy(mode, dir, True, remove)
            return error

        return 0


    def __folder_build(self, mode, dir, topDir, remove):
        error = 0

        if not self.checkVersion or not topDir:
            items = sorted(filter(lambda x: os.path.isfile(os.path.join(dir, x)), os.listdir(dir)), key=lambda x: x.lower())
            for item in items:
                file = os.path.join(dir, item)
                error = self.__checkFile(mode, file, remove)
                if error != 0:
                    break

        if not self.isConfigFound:
            items = sorted(filter(lambda x: os.path.isdir(os.path.join(dir, x)), os.listdir(dir)), key=lambda x: x.lower())
            for item in items:
                folder = os.path.join(dir, item)
                if topDir and self.checkVersion:
                    folderName = os.path.basename(folder)
                    if folderName != self.version:
                        continue
                error = self.__folder_build(mode, folder, False, remove)
                if error != 0:
                    break

        self.isConfigFound = False

        return error


    def __folder_forProject_copy(self, mode, dir, topDir, remove):
        error = 0

        if topDir:
            dirName = os.path.basename(dir)
            if self.checkVersion:
                if dirName != self.version:
                    return error

        if not self.checkVersion or not topDir:
            items = sorted(filter(lambda x: os.path.isfile(os.path.join(dir, x)), os.listdir(dir)), key=lambda x: x.lower())
            for item in items:
                file = os.path.join(dir, item)
                if self.forProject_copy != '' and item == self.forProject_copy:
                    error = self.__checkFile(mode, file, remove)
                    if error != 0:
                        break
                if ((self.forProject_change != '' and item == self.forProject_change) or
                    (self.forPlugin_copy != '' and item == self.forPlugin_copy) or
                    (self.forPlugin_change != '' and item == self.forPlugin_change) or
                    (self.forAddIn_copy != '' and item == self.forAddIn_copy) or
                    (self.forProject_variant != '' and item == self.forProject_variant) or
                    (self.forAddIn_variant != '' and item == self.forAddIn_variant)):
                    self.isConfigFound = True
                    error = 0

        if not self.isConfigFound:
            items = sorted(filter(lambda x: os.path.isdir(os.path.join(dir, x)), os.listdir(dir)), key=lambda x: x.lower())
            for item in items:
                folder = os.path.join(dir, item)
                if topDir and self.checkVersion:
                    folderName = os.path.basename(folder)
                    if folderName != self.version:
                        continue
                error = self.__folder_forProject_copy(mode, folder, False, remove)
                if error != 0:
                    break

        self.isConfigFound = False

        return error
