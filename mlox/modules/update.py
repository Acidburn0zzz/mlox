# Update a file from the internet
# with the option of auto extracting it

import os
import urllib
import subprocess
import logging

update_logger = logging.getLogger('mlox.update')

#Check if a file has changed (size) compared to local version
def isNewer(local_file,url):
    if not os.path.isfile(local_file):
        return True
    try:
        connection = urllib.urlopen(url)
    except:
        update_logger.warning('Unable to connect to {0}, skipping update.'.format(url))
        return False

    local_size = os.stat(local_file).st_size
    update_logger.debug('Current size: {0}'.format(local_size))
    url_size = connection.info()['Content-Length']
    update_logger.debug('Downloadable size: {0}'.format(url_size))

    return int(url_size) != int(local_size)

#Extract the contents of a file to a directory (using 7za)
def extract(file_path,directory):
    cmd = ['7za', 'e', '-aoa', '-o{0}'.format(directory), file_path]
    update_logger.debug("Extracting via command %s",cmd)
    try:
        devnull = open(os.devnull, 'w')
        subprocess.check_call(cmd, stdout=devnull)
    except Exception as e:
        update_logger.error('Error while extracting from {0}'.format(file_path))
        #update_logger.error('Exception {0} while trying to execute command:  {0}'.format(str(e),cmd))
        return False
    return True

#Check if a compressed file needs updating.
#If it does, download it, and extract it to a directory
def update_compressed_file(file_path,url,directory):
    update_needed = isNewer(file_path,url)
    if update_needed:
        update_logger.info('Updating {0}'.format(file_path))
        try:
            urllib.urlretrieve(url,file_path)
        except Exception as e:
            update_logger.error('Unable to download {0}, skipping update.'.format(url))
            update_logger.debug('Error: {0}'.format(e))
            return False

        update_logger.info('Downloaded {0}'.format(file_path))
        if not extract(file_path,directory):
            return False
        return True
    else:
        update_logger.info('No update necessary for file {0}'.format(file_path))
        return False
