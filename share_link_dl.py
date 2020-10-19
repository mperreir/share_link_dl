import urllib.request, urllib.parse
import sys, os, math, json
import os.path

# Formats a size in bytes into a human readable string
def format_size(num, suffix='B'):
    if num > 0:
        magnitude = int(math.floor(math.log(num, 1024)))
    else:
        magnitude = 0
    val = num / math.pow(1024, magnitude)
    if magnitude > 7:
        return '{:.1f}{}{}'.format(val, 'Y', suffix)
    return '{:3.1f}{}{}'.format(val, ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z'][magnitude], suffix)

# Simple utility function for displaying a text based progress bar
def report_progress( transfered, block_size, total_size, progress_size = 40):
    if block_size < total_size:
        current_size = transfered*block_size
    else:
        current_size = total_size
    progress = progress_size*current_size//total_size
    print('\r', end='')
    for i in range(progress):
        print("*", end='')
    for i in range(progress,progress_size):
        print(" ", end='')
    print("\t{}/{}   ".format(format_size(current_size), format_size(total_size)), end='')

# Queriies seafile API and recursively downloads all the files in the folder
# shared by a share link
def process_dir_url( base_url, path, destination_path ):
    opener = urllib.request.build_opener()
    url = base_url + '?path=' + urllib.parse.quote(path)
    try:
        with opener.open(url) as r:
            data = r.read().decode()
            json_data = json.loads(data)
            for entry in json_data['dirent_list']:
                if entry['is_dir'] == True:
                    process_dir_url( base_url, entry['folder_path'], destination_path)
                else:
                    file_url = "{}/files/?p={}&dl=1".format(original_url,urllib.parse.quote(entry['file_path']))
                    complete_dst_path = os.path.join(destination_path, os.path.split(entry['file_path'][1:])[0])
                    if not os.path.exists(complete_dst_path):
                        os.makedirs(complete_dst_path)
                    print("downloading:", entry['file_path'][1:])
                    file_path = os.path.join(destination_path, urllib.parse.quote(entry['file_path'][1:]))
                    urllib.request.urlretrieve(file_url, file_path, report_progress)
                    print()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        destination_path = '.'
        if len(sys.argv) == 1:
            print("Usage : share_link_dl.py share_link_url [destination_path]")
            sys.exit()
        elif len(sys.argv) == 3:
            destination_path = sys.argv[2]
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)

        original_url = sys.argv[1]
        base_url = original_url.replace('/d/', '/api/v2.1/share-links/') + '/dirents/'
        process_dir_url(base_url, '/', destination_path)
    except KeyboardInterrupt as e:
        print("\nDownload interrupted by user (Ctrl+C)")