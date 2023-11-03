import os
import os.path
import shutil
from pathlib import Path
from stat import S_IREAD, S_IWUSR


class BaseTools:

    @staticmethod
    def createFolder(dir):
        i = 0
        p = -1
        while i == 0 or p != -1:
            p = dir.find('\\', p + 1)
            if p != -1:
                dir2 = dir[:p + 1]
            else:
                dir2 = dir
            if not os.path.exists(dir2):
                os.mkdir(dir2)
            i = i + 1

    @staticmethod
    def copy2(src, dst):
        if os.path.isfile(src):
            shutil.copy2(src, dst)
        if os.path.isdir(src):
            with os.scandir(src) as it:
                for entry in it:
                    relpath = os.path.relpath(entry.path, src)
                    dst2 = os.path.join(dst, relpath)
                    if entry.is_dir():
                        if not os.path.exists(dst2):
                            BaseTools.createFolder(dst2)
                        BaseTools.copy2(entry.path, dst2)
                    elif entry.is_file():
                        dst3 = os.path.dirname(dst2)
                        if not os.path.exists(dst3):
                            BaseTools.createFolder(dst3)
                        shutil.copy2(entry.path, dst2)


    @staticmethod
    def buildPath(firstPath, secondPath):
        p = secondPath.find(':', 0)
        if p == -1:
            p = secondPath.find('./', 0)
            if p == 0:
                secondPath = secondPath[2:]
            else:
                p = 0
                while p == 0:
                    p = secondPath.find('../')
                    if p == 0:
                        firstPath = Path(firstPath).parent.absolute()
                        secondPath = secondPath[p + 3:]
            secondPath = os.path.join(firstPath, secondPath)
        return secondPath.replace('/', os.sep)


    @staticmethod
    def clearReadOnlyFileAttribute(file3):
        os.chmod(file3, S_IWUSR|S_IREAD)


    @staticmethod
    def clearReadOnlyFolderAttribute(dir3):
        os.chmod(dir3, S_IWUSR|S_IREAD)

        with os.scandir(dir3) as it:
            for entry in it:
                if entry.is_dir():
                    BaseTools.clearReadOnlyFolderAttribute(entry.path)
                elif entry.is_file():
                    BaseTools.clearReadOnlyFileAttribute(entry.path)


    @staticmethod
    def shouldItemBeRemoved(item, remove):
        if remove == None:
            return False

        for line in remove:
            index = line.find('./', 0)
            if index == 0:
                line2 = line[2:]
            else:
                line2 = './' + line
            if item == line or item == line2:
                return True

        return False


    @staticmethod
    def jsonForCompare_copy(line, isFile, source, json):
        if isFile:
            line2 = line.replace(os.sep, '/')
            if not (line2 in json.data['copy']):
                json.data['copy'].append(line2)
        else:
            with os.scandir(source) as it:
                for entry in it:
                    if entry.is_file():
                        name = os.path.basename(entry.path)
                        line2 = os.path.join(line, name).replace(os.sep, '/')
                        if not (line2 in json.data['copy']):
                            json.data['copy'].append(line2)

            with os.scandir(source) as it:
                for entry in it:
                    if entry.is_dir():
                        name = os.path.basename(entry.path)
                        line2 = os.path.join(line, name)
                        BaseTools.jsonForCompare_copy(line2, os.path.isfile(entry.path), entry.path, json)


    @staticmethod
    def jsonForCompare_remove(line, isFile, source, json):
        if isFile:
            line2 = line.replace(os.sep, '/')
            if line2 in json.data['copy']:
                json.data['copy'].remove(line2)
        else:
            with os.scandir(source) as it:
                for entry in it:
                    if entry.is_file():
                        name = os.path.basename(entry.path)
                        line2 = os.path.join(line, name).replace(os.sep, '/')
                        if line2 in json.data['copy']:
                            json.data['copy'].remove(line2)

            with os.scandir(source) as it:
                for entry in it:
                    if entry.is_dir():
                        name = os.path.basename(entry.path)
                        line2 = os.path.join(line, name)
                        BaseTools.jsonForCompare_remove(line2, os.path.isfile(entry.path), entry.path, json)
