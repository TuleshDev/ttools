import os
import os.path
import shutil

from BaseTools import BaseTools as parent


class BaseForCommands(parent):

    @staticmethod
    def performCommands(mode, path, relPath, commands, commandsArgument1, commandsArgument2, json):
        index = 0
        for argument1 in commandsArgument1:
            if relPath == argument1:
                if commands(index).lower() == 'rename':
                    if relPath[len(relPath) - 1:len(relPath)] == '/':
                        if os.path.exists(path):
                            ##line4 = path[:len(path)]
                            ##index2 = line4.rfind('/') + 1
                            ##dir2_ = line4[:index2] + commandsArgument2(index)
                            ##dir2 = dir2_ + '/'
                            parentPath = os.path.dirname(path)
                            dir2 = os.path.join(parentPath, commandsArgument2(index))
                            parentRelPath = os.path.dirname(relPath)
                            line = os.path.join(parentRelPath, commandsArgument2(index))

                            if not os.path.exists(dir2):
                                parent.createFolder(dir2)
                            parent.clearReadOnlyFolderAttribute(dir2)
                            ##parent.copy2(path, dir2_)
                            parent.copy2(path, dir2)

                            parent.jsonForCompare_copy(line, False, dir2, json)
                            parent.jsonForCompare_remove(relPath, False, path, json)

                            shutil.rmtree(path)
                    else:
                        if os.path.exists(path):
                            ##line4 = path
                            ##index2 = line4.rfind('/') + 1
                            ##path2 = line4[:index2] + commandsArgument2(index)
                            parentPath = os.path.dirname(path)
                            path2 = os.path.join(parentPath, commandsArgument2(index))
                            parentRelPath = os.path.dirname(relPath)
                            line = os.path.join(parentRelPath, commandsArgument2(index))

                            if os.path.exists(path2):
                                os.remove(path2)
                            parent.copy2(path, path2)

                            parent.jsonForCompare_copy(line, True, path2, json)
                            parent.jsonForCompare_remove(relPath, True, path, json)

                            os.remove(path)
            index = index + 1


    @staticmethod
    def performCommandsHelperForFolder(mode, path, relPath, commands, commandsArgument1, commandsArgument2, json):
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_dir():
                    BaseForCommands.performCommandsHelperForFolder(mode, path + os.sep + entry.name, relPath + entry.name + '/', commands, commandsArgument1, commandsArgument2, json)
                elif entry.is_file():
                    BaseForCommands.performCommands(mode, path + os.sep + entry.name, relPath + entry.name, commands, commandsArgument1, commandsArgument2, json)

        BaseForCommands.performCommands(mode, path, relPath, commands, commandsArgument1, commandsArgument2, json)
