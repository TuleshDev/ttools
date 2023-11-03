import sys
sys.path.append('../../_Bat_Files_')
sys.path.append('sourceDir')
sys.pycache_prefix='C:/Projects/My/__pycache__'
import os.path

from BuildHelper import BuildHelper


def main():
    isBuildIncluded = True

    buildHelper = BuildHelper(__file__, isBuildIncluded)
    error = buildHelper.run()
    return error


if __name__ == '__main__':
    main()
