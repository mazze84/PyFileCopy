# This is a sample Python script.
import hashlib
import pathlib
import shutil
import os
import argparse
import logging

from typing import List

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

BLOCKSIZE = 65536


def hash_file(path):
    if os.path.isdir(path):
        return False

    hasher = hashlib.md5()
    with open(path, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()


def copy_file(source_file, destination_file):
    if not os.path.exists(os.path.dirname(destination_file)):
        os.makedirs(os.path.dirname(destination_file))
    # TODO try catch block for reading or writing errors
    try:
        shutil.copyfile(source_file, destination_file)
    except PermissionError:
        logger.error("No permissions to copy file " + source_file + " to " + destination_file)
        return False
    else:
        logger.info("File " + source_file + " copied to " + destination_file)
        return True


def get_files_in_subfolders(path_dir, extension_filter=""):
    content_dir: List[str] = os.listdir(path_dir)
    files_dir: List[str] = []
    for filename in content_dir:
        path_file = os.sep.join([path_dir, filename])
        if os.path.isdir(path_file):
            # TODO add switch not to search recursive for subfolders
            files_dir.extend(get_files_in_subfolders(path_file, extension_filter))
        else:
            if extension_filter.strip():
                file_extension = pathlib.Path(filename).suffix
                if file_extension.lower() != extension_filter.lower():
                    continue
            files_dir.append(path_file)
    return files_dir


def get_relpath(file_path, source_dir):
    logger.debug(os.path.relpath(file_path, source_dir))
    return os.path.relpath(file_path, source_dir)


def check_files(source_file, destination_file):
    if not os.path.isfile(source_file):
        logger.error(source_file + " is not a file")
        return False
    if not os.path.isfile(destination_file):
        logger.error(destination_file + " is not a file")
        return False

    hash_source = hash_file(source_file)

    hash_dest = hash_file(destination_file)
    logger.debug("Hashes source:" + hash_source + " destination:" + hash_dest)
    return hash_source == hash_dest


def check_source_destination(source, destination):
    if os.path.isfile(source) and os.path.isdir(destination):
        if os.path.realpath(source) != destination:
            return True
    return False


def get_destination(file_name, destination_dir):
    return os.sep.join([destination_dir, file_name])


# check if move is true then delete
def check_delete_file(file_dir, destination_file):
    if args['Move'] is not None and check_files(file_dir, destination_file):
        logger.info("removing file " + file_dir)
        os.remove(file_dir)


def copy_files(source_dir, destination_dir, filter, move):
    if filter != None:
        files_dir: List[str] = get_files_in_subfolders(source_dir, filter)
    else:
        files_dir: List[str] = get_files_in_subfolders(source_dir)

    for file in files_dir:
        if not check_source_destination(file, destination_dir):
            logger.error("Not a valid path")
            continue
        logger.debug(file)
        destination_file = get_destination(get_relpath(file, source_dir), destination_dir)

        if os.path.isfile(destination_file):
            # TODO ask if file should be overridden
            # file is not the same delete the destination file
            if not check_files(file, destination_file):
                logger.debug("deleting destination file " + destination_file)
                os.remove(destination_file)
            else:

                check_delete_file(file, destination_file)
                continue


        copy_file(file, destination_file)

        if move is not None and check_files(file, destination_file):
            check_delete_file(file, destination_file)


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

    copy_files(args['Source'], args['Destination'], args['Filter'], args['Move'])

