# share_link_dl
Python 3 script for downloading the content of a Seafile folder using a (public) share link

## Why should I use this script ?

Seafile share links are great, but if you want to download a folder Seafile will have to generate a zip file. This is not a limitation of Seafile, all other cloud storage web client do the same as it is not possible for a web browser to create folders. If the shared folder is big, Seafile might take a very long time generating the zip archive of will simply refuse to create it. In that case the only thing you can do is downloading each file manually :-(.

This script helps solving this problem by automating the download of a shared folder without any zip file creation :-).

## Requirements

This script uses only standard python 3 modules, so you only need python 3 on your system.

## Usage

 `share_link_dl.py share_link_url [destination_path]`

where:

- share_link_url : url created using the "create share link" feature of Seafile. It usually look like http://url_of_seafile_server/d/long_random_string
- destination_path : is the path where you want to store the content of the shared folder on you local filesystem. If this parameter is omitted the default location is the current folder `.`  (no enclosing folder is created by default so be careful when downloading a folder containing lots of files at its root)