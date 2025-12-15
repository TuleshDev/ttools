import sys
sys.path.append('./0_Build/ttools/build')
sys.pycache_prefix='C:/__pycache__'

from BuildHelper import BuildHelper


def main():
    isBuildIncluded = True

    buildHelper = BuildHelper(__file__, isBuildIncluded)
    error = buildHelper.run()
    return error


if __name__ == '__main__':
    main()
