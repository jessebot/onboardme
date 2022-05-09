#!/usr/bin/env python3
"""
Python program to build the boilerplate infrastructure needed to
properly take over an environment and provide a homogenous base
from which to run/deploy IaC.
"""

import json, yaml, shutil, os, requests, sys, time, io, math, pathlib
import logging as log
from logging import debug
from queue import Queue
from threading import Thread
from yaml.loader import SafeLoader


vm_config_path = "/Users/max/Desktop/Repos/Onboardme/notes/vm.yaml"

log_level = log.INFO
program_log = log.getLogger(f"qemu-py")
log.basicConfig(level=log_level)
program_log.info("logging config loaded")

def read_yaml_file(yaml_file_path):
    """
    Reads a .yaml file as raw, converts to json, formats it, then reloads 
    it as a dict for uniformity of transformation later
    """

    with open(yaml_file_path, 'r') as f:

        # reads the files as raw - unusable until loaded
        raw = f.read()
        #print(raw)

        # converts the raw data into a json string
        yaml_object = yaml.safe_load(raw)
        #print(yaml_object)

        # pretty format the json to make it uniform
        json_data = json.dumps(yaml_object, separators=(',', ":"))
        #print(json_data)

        # Load the clean json into a python dict
        json_object = json.loads(f"{json_data}")
        #print(json_object)

    return json_object

def make_dir(path: str, clear: bool = False, debug: bool = False,
             format="json"):
    """
    makes/deletes directory
    """
    # if the directory does not exist, try to create it
    if not os.path.isdir(path):
        program_log.info(f'Directory is not present. Creating {path}')
        try:
            os.makedirs(path)
        except Exception as e:
            program_log.error(f"Oof", print(e.__class__), "occurred")
            program_log.error(f"Unable to create dir at {path}")
            if debug:
                name = input("Any key to continue")

    # if the directory DOES exist, and clear=True, notify that we
    # will be removing and overwriting it
    if os.path.isdir(path):
        if clear == True:
            program_log.info(f'Deleting directory: {path}')
            program_log.info('clearing...')
            
            try:
                shutil.rmtree(path)
                os.makedirs(path)
            except Exception as e:
                program_log.error(f"Oof", print(e.__class__), "occurred")
                program_log.error(f"failed to clear directory: {path}")
                if debug:
                    name = input("Any key to continue")
    # otherwise skip
    if not clear:
        program_log.info(f'Directory {path} already exists.')

def convert_size(size_bytes):
    """
    Convert bytes to readable formats
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def download_file_worker():
    """
    Downloads a file and shows a simple progress bar. 
    Sets a frame_length to throttle resource consumption.
    Allows changing the bar length and fill chatacter

    furmulas are:
        Filled bar percentage: bar_length * downloaded_bytes / total_bytes
        Download progress: (downloaded_bytes/total_bytes) * 100
        Download speed: (downloaded_bytes // time_elapsed) / 100000
        Character to fill the bar: 
            left: '*' * bar_fill
            right: ' ' * (bar_length - bar_fill)
        
        Frame Length: Seconds between frame renders
        Time: Elapsed: current_time  - start_time
        Current Frame: time_elapsed / frame_length

    Optimization Notes:
        1. Smaller chunk sizes trigger more IO operations on
           faster connections and thus increase CPU consumption
        2. Smaller frame times (under .3) have a non-negligible 
           impact on performance
    """
    # bytes to download before serializing
    chunk_size = 16384

    # Time between frames in seconds
    frame_length = .5
    
    # Total horizontal length of the progress bar
    bar_length = 25

    # Character that fills the progress bar
    fill_character = "="
    empty_character = " "

    while True:
        # Get a job object from the queue and assign the name and url
        job = q.get()
        url = job[0]
        name = job[1]
        path = job[2]
        working_dir = pathlib.Path().resolve()
        download_file_path = pathlib.Path(f"{working_dir}/{path}/{name}")
        skippable = True

        # get the size of the file from the header and compare it
        # to the file size on disk (if it exists)
        remote_file_info = requests.head(url)
        total_bytes = 0
        
        try:
            total_bytes = int(remote_file_info.headers['Content-Length'])
            convered_Size = convert_size(int(total_bytes))
        except Exception as e:
            program_log.error(f"Oof, looks like a {e.__class__}.")
            program_log.error(f"Status Code: {remote_file_info.status_code}")
            program_log.error(f"Headers: {remote_file_info.headers}")
            q.task_done()
            sys.exit()


        downloaded_bytes = 0

        # Check if file exists
        if os.path.exists(f"{download_file_path}"):
            program_log.info(f"file: {download_file_path} already exists on disk...")
            downloaded_bytes = int(os.path.getsize(download_file_path))

            # Check if existing file needs to be updated
            if downloaded_bytes == total_bytes:
                program_log.info(f"file is the same bytesize as {url}, skipping downloading")
                q.task_done()
                sys.exit()
            else:
                program_log.info(f"file is not the same bytesize as {url}, not skippable")
                skippable = False
        else:
            program_log.info(f"{download_file_path} not present.")
            skippable = False


        # finally start the download
        if skippable == False:
            program_log.info(f"Downloading {name}")
            response = requests.get(f"{url}", stream=True)

            # download file
            with open(download_file_path, 'wb') as file:
                frames_rendered = 0

                # cache the start time of the job
                start = time.time()

                # Begin the download
                if total_bytes is None: 
                    program_log.error("{response.content}")
                else:
                    for chunk in response.iter_content(chunk_size):
                        # Save each chunk as it comes in
                        file.write(chunk)
                        file.flush()
                        os.fsync(file.fileno())

                        # track our frame times
                        time_elapsed = time.time()  - start
                        this_frame = math.trunc(time_elapsed/frame_length)
                        
                        # Update our values to display a new frame
                        if this_frame > frames_rendered:

                            # metrics
                            downloaded_bytes = int(os.path.getsize(download_file_path))
                            progress = math.ceil((downloaded_bytes / total_bytes) * 100)
                            speed = math.trunc((downloaded_bytes // time_elapsed) / 100000)

                            # progress bar pieces
                            bar_fill = int(bar_length * downloaded_bytes / int(total_bytes))
                            bar_left = fill_character * bar_fill
                            bar_right = empty_character * (bar_length - bar_fill)

                            # assemble the frame and flush the buffer
                            sys.stdout.write(f"\r[{bar_left}{bar_right}] {progress}% of {convered_Size} @ {speed}Mbps")
                            sys.stdout.flush()

                            # record that we finished the frame
                            frames_rendered = this_frame
            q.task_done()
        else:
            q.task_done()
            sys.exit()

def download_file(url, name, path):
    """
    Downloads a file in a new thread
    based on https://towardsdatascience.com/multithreading-multiprocessing-python-180d0975ab29
    """
    global q
    q = Queue()
    q.put([url, name, path])
    worker = Thread(target=download_file_worker)
    worker.daemon = True
    worker.start()
    q.join()

def create_ssh_keys():
    from cryptography.hazmat.primitives import serialization as crypto_serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.backends import default_backend as crypto_default_backend

    program_log.info(f"Generating key files...")
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )

def main():
    """
    main logic looop 
    """
    # load the yaml config file
    vm_config = read_yaml_file(vm_config_path)
    program_log.debug(f"loaded vm_config: {vm_config}")

    # create a directory to hold the VM assets
    make_dir(vm_config['VM']['vm_name'], clear=False)

    # download a cloud image
    name = f"{vm_config['VM']['cloud_image_name']}"
    path = f"{vm_config['VM']['vm_name']}"
    url = f"{vm_config['VM']['cloud_image_url']}/{name}"
    download_file(url, name, path)

main()
create_ssh_keys()