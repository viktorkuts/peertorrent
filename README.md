# peertorrent
A bad (no really, it's like a torrent client but really bad) torrent client for a school project of mine

# windows users
you will not be able to run this unfortunatly, libtorrent installs perfectly on linux, but not on windows.  
you will have to use a virtual machine, preferably ubuntu or debian based, to install python3-libtorrent and libtorrent-rasterbar

# how to use on linux
This example is for distros that use the aptitude package manager

Step 1, get packages: ``sudo apt update && sudo apt install git python3 pip libtorrent21``
Step 2, clone repo and enter directory ``git clone https://github.com/volkingqc/peertorrent.git && cd peertorrent``
Step 4, install required python modules ``pip install -r requirements``
Step 5, run the program ``python3 main.py``
Step 6, enjoy

# Dependencies used in the software:
Qt5 (for python) - Licensed under  LGPLv3  
libtorrent (Rasterbar) - Licensed under BSD-2 Clause  

**I was kind of in a rush and have not really read all about licensing if using libraries, thus I included them in this list. This software is licensed using GPLv3 and if you spot that I need to include the license for another program because I am using such license, please open an issue and I will try to resolve it ASAP. Thank you.*
