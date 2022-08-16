# ========= Dependencies =============

import os

os.system("pip install pyfiglet")
os.system("pip3 install pyfiglet")
os.system("pip install wget")
os.system("pip3 install wget")

import wget
import pyfiglet
from adb import *


# ========= Main Class ==============

class Main :
	def __init__(self) :

		self.banner = pyfiglet.figlet_format("J5 Builder")
		self.user = 'welcome'
		self.adb = Adb()


	def install_linux_dependencies(self) :

		# This function will download and install the required AOSP dependencies for building
		# User will be prompted to enter the sudo user password 
		os.system("sudo apt update&&sudo apt install bc bison build-essential ccache curl flex g++-multilib gcc-multilib git gnupg gperf imagemagick lib32ncurses5-dev lib32readline-dev lib32z1-dev liblz4-tool libncurses5 libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync schedtool squashfs-tools xsltproc zip zlib1g-dev python2 python3 zip unzip wget")


	def install_repo(self) :

		# Create dir for repo
		os.sytem("mkdir ~/bin")

		# Set the new dir into the PATH environment variable
		os.system("PATH=~/bin:$PATH")

		# Download latest repo
		os.system("curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo")

		# Give repo proper permissions as executable
		os.system("chmod a+x ~/bin/repo")

	def set_ccache(self, size) :
		# Anything between 25GB and 100GB will speed up the building

		# Export ccache environment variables
		os.system("export USE_CCACHE=1")
		os.system("export CCACHE_EXEC=/usr/bin/ccache")
		os.system("ccache -M %dG" % size)

	def git_config(self, email, name) :
		# User needs to identify on git

		# Git config
		os.system("git config --global user.email '%s'" % email)
		os,system("git config --global user.name '%s'" % name)
		
	def menu(self) :

		while self.user != "" :

			self.user = input("%s\n---------------------------------------------\n[1] : Install AOSP dependencies\n---------------------------------------------\n[2] : Clean AOSP dir\n---------------------------------------------\n[3] : Build LineageOS\n---------------------------------------------\n" % self.banner)
			match self.user :

				case "1" :
					# Dependencies
					print("\nDownloading Linux dependencies..\nYou'll be prompted to enter your sudo password\n")
					self.install_linux_dependencies()
					print("\nAOSP Dependencies installed succesfully! [1/5]")

					# repo
					print("\nDownloading repo from Google server..\n")
					self.install_repo()
					print("\nGoogle repo installed succesfully! [2/5]")

					# platform-tools
					print("\nDownloading latest platform-tools from Google server..\n")
					self.adb.check_adb_tools()
					print("\nplatform-tools installed succesfully! [3/5]")

					# ccache
					cache = int(input("\nEnter a value between 25GB and 100GB : "))
					self.set_ccache(cache)
					print("\nccache size set succesfully! [4/5]")

					# git config
					print("You have to complete a git config for start building..\nEnter the following required fields\n")
					email = input("\nEnter your email : ")
					name = input("\nEnter your name : ")
					self.git_config(email, name)
					print("\ngit config set succesfully! [5/5]")


main = Main()
main.menu()