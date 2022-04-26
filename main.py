# This is a sample Python script.
import hashlib
import pathlib
import shutil
import os
import argparse
import logging

from typing import List, Tuple
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

BLOCKSIZE = 65536
def hashFile(path):
    if os.path.isdir(path):
        return False

    hasher = hashlib.md5()
    with open(path, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()


def copyFile(source_file, destination_file):
    shutil.copyfile(source_file, destination_file)

def getFilesForPath(path_dir, extension_filter=""):
    content_dir: List[str] = os.listdir(path_dir)
    files_dir: List[Tuple] = []
    for filename in content_dir:
        path_file = os.sep.join([path_dir, filename])
        if os.path.isdir(path_file):
            files_dir.extend(getFilesForPath(path_file, extension_filter))
        else:
            if extension_filter.strip():
                file_extension = pathlib.Path(filename).suffix
                if file_extension != extension_filter:
                    continue
            files_dir.append((createRelPath(path_dir, path_file), path_file))
    return files_dir

def createRelPath(source_dir, file_path):
    print(os.path.relpath(file_path, source_dir))
    return os.path.relpath(file_path, args['Source'])


def checkCopyFile(source_file, destination_file):
    if not os.path.isfile(source_file):
        logger.error(source_file + " is not a file")
        return False
    if not os.path.isfile(destination_file):
        logger.error(destination_file + " is not a file")
        return False

    hash_source = hashFile(source_file)

    hash_dest = hashFile(destination_file)
    logger.debug(hash_source + " " + hash_dest)
    return hash_source == hash_dest

def checkFiles(source, destination):
    if os.path.isfile(source) and os.path.isdir(destination):
        if os.pathdir(source) != destination:
            return True
    return False

def getDestinationFilePath(file_name, destination_dir):
    return os.sep.join([destination_dir, file_name])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # create logger
    logger = logging.getLogger('copy_file')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    # Construct an argument parser
    all_args = argparse.ArgumentParser()

    # Add arguments to the parser
    all_args.add_argument("-s", "--Source", required=True, help="source directory")
    all_args.add_argument("-d", "--Destination", required=True, help="second Value")
    all_args.add_argument("-f", "--Filter", required=False, help="extension filter")
    all_args.add_argument("-m", "--Move", required=False, help="delete files after copy")

    args = vars(all_args.parse_args())

    if checkFiles(args['Source'], args['Destination']):
        logger.error("Not a path")
        exit(0)

    if args['Filter'] != None:
        files_dir: List[Tuple] = getFilesForPath(args['Source'], args['Filter'])
    else:
        files_dir: List[Tuple] = getFilesForPath(args['Source'])

    destination = args['Destination']

    for file in files_dir:
        logger.debug(file[1])
        destination_file = getDestinationFilePath(file[0], destination)
        logger.debug(destination_file)
        logger.info(checkCopyFile(file[1], destination_file))
        pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

