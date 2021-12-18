import glob
import gzip
import os
import time
DIR_NAME = "/Users/mrnk/Documents/Workspace/platform/logs/one_api/"
DEFAULT_LIMIT = 30
TAR_FILE_EXT = ".gz"
LOG_FILE_EXT = ".log"


def get_files_from_directory(dir_name):
    # Get list of all files only in the given directory
    list_of_files = filter(os.path.isfile, glob.glob(dir_name + '*'))
    # Sort list of files based on last modification time in ascending order
    list_of_files = sorted(list_of_files, key=os.path.getmtime)
    # Iterate over sorted list of files and print file path
    # along with last modification time of file
    return list_of_files


def get_required__file_list(files_list, limit=DEFAULT_LIMIT):
    return files_list[:limit]


def print_list(printable_list):
    for index, file_path in enumerate(printable_list):
        timestamp_str = time.strftime('%d/%m/%Y :: %H:%M:%S', time.gmtime(os.path.getmtime(file_path)))
        print(f"{timestamp_str}: {index}: {file_path}")


def get_filtered_list_by_file_ext(files):
    tar_files_list = []
    non_tar_files_list = []
    for file in files:
        ext = file.split("/")[-1].split(".")
        print(f"ext: {ext}")
        if ext == TAR_FILE_EXT:
            tar_files_list.append(file)
        else:
            non_tar_files_list.append(file)
    return tar_files_list, non_tar_files_list


def upload_to_s3(files):
    """ Upload .tar files to s3 """
    uploaded_files_list = []
    return uploaded_files_list


def delete_uploaded_files(files):
    """ delete files which got uploaded to s3 successfully """
    pass


def compress_file(file_name):
    """This is an temp function and we have to improve it with better compression algorithm"""
    compressed_file = file_name + TAR_FILE_EXT

    f_in = open(file_name, 'rb')
    f_out = gzip.open(compressed_file, 'wb')
    f_out.writelines(f_in)
    f_out.close()
    f_in.close()
    return compressed_file


def compress_files(files):
    compressed_files = []
    for file_name in files:
        compressed_files.append(compress_file(file_name))
    return compressed_files


def archive_logs(files):
    """ archive last N days logs """
    tar_files, non_tar_files = get_filtered_list_by_file_ext(files)
    uploaded_file_list1 = upload_to_s3(tar_files)
    # TODO: make this upload python async and proceed for compressing non-tar files
    compressed_files = compress_files(non_tar_files)
    print(f"compressed_files: {compressed_files}")
    uploaded_file_list2 = upload_to_s3(compressed_files)
    uploaded_file_list = uploaded_file_list1 + uploaded_file_list2
    delete_uploaded_files(uploaded_file_list)


# TODO: make this file object oriented
file_list = get_files_from_directory(DIR_NAME)
required_list = get_required__file_list(file_list, 30)
print_list(required_list)
archive_logs(required_list)





