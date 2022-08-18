# ========= Dependencies =============

import os

os.system("pip install pyfiglet")
os.system("pip3 install pyfiglet")
os.system("pip install wget")
os.system("pip3 install wget")

import wget
import pyfiglet
import threading
from adb import *


# ========= Main Class ==============

class Main :
	def __init__(self) :

		self.banner = pyfiglet.figlet_format("J5 Builder")
		self.user = 'welcome'
		self.adb = Adb()
		self.los_version = 'los'

		# Build variables
		self.building = False
		self.initialized_repo = False
		self.downloaded_manifest = False
		self.synced_repo = False
		self.opengapps_config = False
		self.start = False
		self.target = ""
		self.target_building = False


	def install_linux_dependencies(self) :

		# This function will download and install the required AOSP dependencies for building
		# User will be prompted to enter the sudo user password 
		os.system("sudo apt update&&sudo apt install bc bison build-essential ccache curl flex g++-multilib gcc-multilib git gnupg gperf imagemagick lib32ncurses5-dev lib32readline-dev lib32z1-dev liblz4-tool libncurses5 libncurses5-dev libsdl1.2-dev libssl-dev libxml2 libxml2-utils lzop pngcrush rsync schedtool squashfs-tools xsltproc zip zlib1g-dev python2 python3 zip unzip wget")


	def install_repo(self) :

		# Create dir for repo
		os.system("mkdir ~/bin")

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
		os.system("git config --global user.name '%s'" % name)

	def remove_aosp_dir(self) :
		# Clean existing 'android' directory
		os.system("rm -rf android")

	def system_alerts(self) :
		# This notifies the user of completed events while building

		while self.building :

			# Notify of initialized repo
			if self.initialized_repo :
				print("\n---------------------------\n Your repo have been initialized :) \n---------------------------\n")
				self.initialized_repo = False

			if self.downloaded_manifest :
				print("\n---------------------------\n Your manifest have been initialized :) \n---------------------------\n")
				self.downloaded_manifest = False

			if self.synced_repo :
				print("\n---------------------------\n Your repo have been synced :)\n---------------------------\n")
				self.synced_repo = False

			if self.opengapps_config :
				print("\n---------------------------\n Your opengapps source have been synced :)\n---------------------------\n")
				self.opengapps_config = False

			if self.target_building :
				print("\n---------------------------\nBuilding for %s :D\n---------------------------\n" % self.target)
				self.target_building = False



	# ============= Methods for building aosp =============
	# This functions are bigger so it's better to make a commentary here

	def build_target(self) :
		# This functions is common for all aosp version
		# Choose your desired build target device

		while self.building :
			if self.start :

				print("\n---------------------------\nChoose your build target\n---------------------------\n ")
				self.target = input("%s\n---------------------------------------------\n[1] : SM-J500FN (j5nlte)\n---------------------------------------------\n[2] : SM-J500F/G/M/NO/Y (j5lte)\n---------------------------------------------\n[3] : SM-J5008 (j5ltechn)\n---------------------------------------------\n[4] : SM-J500H (j53gxx)\n---------------------------------------------\n[5] : SM-J510F (j5xnlte)\n---------------------------------------------\n" % self.banner)

				match target :

					case "1" :
						self.target = "j5nlte"
						self.target_building = True
						os.system("lunch lineage_%s-userdebug" % self.target)
						os.system("make -j4")
						self.building = False

					case "2" :
						self.target = "j5lte"
						self.target_building = True
						os.system("lunch lineage_%s-userdebug" % self.target)
						os.system("make -j4")
						self.building = False

					case "3" :
						self.target = "j5ltechn"
						self.target_building = True
						os.system("lunch lineage_%s-userdebug" % self.target)
						os.system("make -j4")
						self.building = False

					case "4" :
						self.target = "j53gxx"
						self.target_building = True
						os.system("lunch lineage_%s-userdebug" % self.target)
						os.system("make -j4")
						self.building = False

					case "5" :
						self.target = "j5xnlte"
						self.target_building = True
						os.system("lunch lineage_%s-userdebug" % self.target)
						os.system("make -j4")
						self.building = False

	# Android 11 building

	def build_sdk30_permissive(self) :

		while self.building :

			# Initialize lineageos repo
			os.system("rm -rf .repo")
			os.system("mkdir -p android/lineage")
			os.system("cd android/lineage")
			os.system("repo init -u https://github.com/Galaxy-J5-Unofficial-LineageOS-Sources/Manifest.git -b lineage-18.1-permissive")
			self.initialized_repo = True

			# Download latest manifest
			os.system("mkdir -p .repo/local_manifests")
			os.system("curl https://raw.githubusercontent.com/Galaxy-J5-Unofficial-LineageOS/Manifest/lineage-18.1-permissive/Manifests/manifest.xml > .repo/local_manifests/manifest.xml")
			os.system("curl https://raw.githubusercontent.com/Galaxy-J5-Unofficial-LineageOS/Manifest/lineage-18.1-permissive/Manifests/LOS-GApps.xml > .repo/local_manifests/gapps.xml")
			self.downloaded_manifest = True

			# Sync repo
			os.system("repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags")
			os.system("source build/envsetup.sh")
			self.synced_repo = True

			# OpenGApps configure
			os.system("sudo apt install git-lfs")
			os.system("git lfs install")
			os.system("repo forall -c git lfs pull")
			os.system("rm android/lineage/vendor/opengapps/build/modules/TrichromeLibrary/Android.mk")
			self.opengapps_config = True

			# Everything is ready!
			# Time to start building
			self.start = True

	def build_sdk30_enforcing(self) :
		while self.building :

			# Initialize lineageos repo
			os.system("rm -rf .repo")
			os.system("mkdir -p android/lineage")
			os.system("cd android/lineage")
			os.system("repo init -u git://github.com/Galaxy-J5-Unofficial-LineageOS-Sources/Manifest.git -b lineage-18.1-enforcing")
			self.initialized_repo = True

			# Download latest manifest
			os.system("mkdir -p .repo/local_manifests")
			os.system("curl https://raw.githubusercontent.com/Galaxy-J5-Unofficial-LineageOS/Manifest/lineage-18.1-enforcing/Manifests/manifest.xml > .repo/local_manifests/manifest.xml")
			os.system("curl https://raw.githubusercontent.com/Galaxy-J5-Unofficial-LineageOS/Manifest/lineage-18.1-enforcing/Manifests/LOS-GApps.xml > .repo/local_manifests/gapps.xml")
			self.downloaded_manifest = True

			# Sync repo
			os.system("repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags")
			os.system("source build/envsetup.sh")
			self.synced_repo = True

			# OpenGApps configure
			os.system("sudo apt install git-lfs")
			os.system("git lfs install")
			os.system("repo forall -c git lfs pull")
			os.system("rm android/lineage/vendor/opengapps/build/modules/TrichromeLibrary/Android.mk")
			self.opengapps_config = True

			# Everything is ready!
			# Time to start building
			self.start = True


	# Android 12 building

	def build_sdk31_permissive(self) :
		while self.building :

			# Initialize lineageos repo
			os.system("rm -rf .repo")
			os.system("mkdir -p android/lineage")
			os.system("cd android/lineage")
			os.system("repo init -u https://github.com/Galaxy-J5-Unofficial-LineageOS-Sources/Manifest.git -b lineage-19.0-permissive")
			self.initialized_repo = True

			# Download latest manifest
			os.system("mkdir -p .repo/local_manifests")
			os.system("curl https://raw.githubusercontent.com/Galaxy-J5-Unofficial-LineageOS/Manifest/lineage-19.0-permissive/Manifests/manifest.xml > .repo/local_manifests/manifest.xml")
			self.downloaded_manifest = True

			# Sync repo
			os.system("repo sync -c -j$(nproc --all) --force-sync --no-clone-bundle --no-tags")
			os.system("source build/envsetup.sh")
			self.synced_repo = True

			# Platform patches and hacks
			# Add support for App Signature Spoofing (This is actually needed by MicroG)
			os.system("patch -d frameworks/base/ -p1 < .repo/manifests/patches/0023-Add-support-for-app-signature-spoofing.patch")

			# ADB Patch
			os.system("patch -d  vendor/lineage/ -p1 < .repo/manifests/patches/0001-TEMP-Disable-ADB-authentication.patch")

			# Monet
			os.system("patch -d vendor/lineage -p1 < .repo/manifests/patches/monet_colors.patch")
			os.system("patch -d vendor/lineage -p1 < .repo/manifests/patches/monet_enable.patch")
			os.system("patch -d frameworks/base -p1 < .repo/manifests/patches/monet_frameworks.patch")

			# BPF patches
			os.system("patch -d art -p1 < .repo/manifests/patches/art.patch")
			os.system("patch -d external/perfetto -p1 < .repo/manifests/patches/perfetto.patch")
			os.system("patch -d system/bpf -p1 < .repo/manifests/patches/bpf.patch")
			os.system("patch -d system/netd -p1 < .repo/manifests/patches/netd.patch")
			os.system("repopick -P frameworks/native 321934")

			# Hacks
			os.system("patch -d frameworks/base -p1 < .repo/manifests/patches/0001-Hack-Ignore-SensorPrivacyService-Security-Exception.patch")
			os.system("patch -d frameworks/base -p1 < .repo/manifests/patches/0002-Bring-Back-XML-Format-UTF-8-TWRP.patch")
			os.system("patch -d frameworks/base -p1 < .repo/manifests/patches/0001-Fix-Brightness-Slider-12.patch")
			os.system("patch -d frameworks/base -p1 < .repo/manifests/patches/0001-FIX-CRASH-ON-FIRST-J5-BOOT.patch")
			os.system("patch -d frameworks/native -p1 < .repo/manifests/patches/0001-keystore2-fallback-mCallingSid-to-getpidcon.patch")
			os.system("patch -d frameworks/base -p1 < .repo/manifests/patches/0002-Disable-vendor-mismatch-warning.patch")

			# Everything is ready!
			# Time to start building
			self.start = True


	# Android 12L building

	def build_sdk32_permissive_vanilla(self) :
		print("Not avalaible yet ;)")

	def build_sdk32_permissive_gapps(self) :
		print("Not avalaible yet ;)")


	# Android 13 building

	def build_sdk33_permissive_vanilla(self) :
		print("Not avalaible yet ;)")




	# ======================================================


		
	def menu(self) :

		while self.user != "" :

			self.user = input("%s\n---------------------------------------------\n[1] : Install AOSP dependencies\n---------------------------------------------\n[2] : Clean AOSP dir\n---------------------------------------------\n[3] : Build LineageOS\n---------------------------------------------\n" % self.banner)
			match self.user :

				case "1" :
					# Dependencies
					print("\n-------------------------------\nDownloading Linux dependencies..\nYou'll be prompted to enter your sudo password\n-------------------------------\n")
					self.install_linux_dependencies()
					print("\n-------------------------------\nAOSP Dependencies installed succesfully! [1/5]\n-------------------------------\n")

					# repo
					print("\n-------------------------------\nDownloading repo from Google server..\n-------------------------------\n")
					self.install_repo()
					print("\n-------------------------------\nGoogle repo installed succesfully! [2/5]\n-------------------------------\n")

					# platform-tools
					print("\n-------------------------------\nDownloading latest platform-tools from Google server..\n-------------------------------\n")
					self.adb.check_adb_tools()
					print("\n-------------------------------\nplatform-tools installed succesfully! [3/5]\n-------------------------------\n")

					# ccache
					cache = int(input("\nSetting ccache\nThis will have an impact on build speed\nEnter a value between 25GB and 100GB (more is better) : "))
					self.set_ccache(cache)
					print("\n-------------------------------\nccache size set succesfully! [4/5]\n-------------------------------\n")

					# git config
					print("\n-------------------------------\nYou have to complete a git config for start building..\nEnter the following required fields\n-------------------------------\n")
					email = input("\nEnter your email : ")
					name = input("\nEnter your name : ")
					self.git_config(email, name)
					print("\n-------------------------------\ngit config set succesfully! [5/5]\n-------------------------------\n")

				case "2" :
					print("\n-------------------------------\nRemoving /android dir\nPlease wait...\n-------------------------------\n")
					self.remove_aosp_dir()

				case "3" :
					self.los_version = input("%s\n---------------------------------------------\n[1] : LineageOS 18.1 (Permissive)\n---------------------------------------------\n[2] : LineageOS 18.1 (Enforcing)\n---------------------------------------------\n[3] : LineageOS 19.0 (Permissive)\n---------------------------------------------\n[4] : LineageOS 19.1 (Permissive)(Vanilla)\n---------------------------------------------\n[5] : LineageOS 19.1 (Permissive)(GApps)\n---------------------------------------------\n[6] : LineageOS 20.0 (Permissive)(Vanilla)\n---------------------------------------------\n" % self.banner)

					match self.los_version :

						case "1" :

							self.building = True

							# Create new threads
							thread_1 = threading.Thread(target = self.build_sdk30_permissive, name="building")
							thread_2 = threading.Thread(target = self.system_alerts, name="alerts")
							thread_3 = threading.Thread(target = self.build_target, name="target")

							# Start threads
							thread_1.start()
							thread_2.start()
							thread_3.start()

							# Wait for all threads to end
							while self.building :
								thread_1.join()
								thread_2.join()
								thread_3.join()

						case "2" :
							self.building = True

							# Create new threads
							thread_1 = threading.Thread(target = self.build_sdk30_enforcing, name="building")
							thread_2 = threading.Thread(target = self.system_alerts, name="alerts")
							thread_3 = threading.Thread(target = self.build_target, name="target")

							# Start threads
							thread_1.start()
							thread_2.start()
							thread_3.start()

							# Wait for all threads to end
							while self.building :
								thread_1.join()
								thread_2.join()
								thread_3.join()

						case "3" :
							self.building = True

							# Create new threads
							thread_1 = threading.Thread(target = self.build_sdk31_permissive, name="building")
							thread_2 = threading.Thread(target = self.system_alerts, name="alerts")
							thread_3 = threading.Thread(target = self.build_target, name="target")

							# Start threads
							thread_1.start()
							thread_2.start()
							thread_3.start()

							# Wait for all threads to end
							while self.building :
								thread_1.join()
								thread_2.join()
								thread_3.join()

						case "4" :
							self.build_sdk32_permissive_vanilla()

						case "5" :
							self.build_sdk32_permissive_gapps()

						case "6" :
							self.build_sdk33_permissive_vanilla()


main = Main()
main.menu()