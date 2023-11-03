import os
import os.path

from BaseTools import BaseTools
from Build import Build


class BuildHelper:

    def __init__(self, file, isBuildIncluded):
        rootDir = os.path.dirname(file)
        rootDirName = os.path.basename(rootDir)

        sourceFragment = ''
        path = os.path.join(rootDir, 'source.txt')
        if os.path.exists(path):
            with open(path, 'r') as read_file:
                sourceFragment = read_file.readline().replace('\n', '')

        if sourceFragment == '':
            sourceDir = os.path.join(rootDir, 'sourceDir')
        else:
            #sourceFragment = BaseTools.buildPath(rootDir, sourceFragment)
            #sourceDir = os.path.join(sourceFragment, rootDirName)
            sourceDir = BaseTools.buildPath(rootDir, sourceFragment)

        destFragment = ''
        path = os.path.join(rootDir, 'destination.txt')
        if os.path.exists(path):
            with open(path, 'r') as read_file:
                destFragment = read_file.readline().replace('\n', '')

        if destFragment == '':
            destDir = os.path.join(rootDir, 'destDir')
        else:
            destFragment = BaseTools.buildPath(rootDir, destFragment)
            destDir = os.path.join(destFragment, rootDirName)

        path = os.path.join(rootDir, 'version.txt')
        if os.path.exists(path):
            with open(path, 'r') as read_file2:
                version = read_file2.readline().replace('\n', '')
                destDir = os.path.join(destDir, version)
        else:
            version = '1'

        scriptName = os.path.basename(file)
        position = scriptName.rfind('.py')
        if position != -1:
            scriptName = scriptName[:position]

        scriptDescriptor1 = rootDirName + '.' + scriptName
        scriptDescriptor2 = scriptDescriptor1

        buildPrefix = 'Build.'

        self.build = Build(sourceDir, destDir, version, scriptName, scriptDescriptor1, scriptDescriptor2, isBuildIncluded, buildPrefix)


    def run(self):
        error = self.build.run()
        return error
