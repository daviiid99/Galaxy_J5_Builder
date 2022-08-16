import platform
import wget
from zipfile import ZipFile
from os.path import exists

class Adb :

	def __init__(self) :
		self.running = True


	def check_adb_tools(self) :

			# Check if platform tools dir exists

			if exists('platform-tools') :
				self.platform_tools_exists = True

			else :
				self.download_adb_tools()

	def download_adb_tools(self) :

		# Static urls for Platform tools from Google server
		adb_windows ="https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
		adb_linux ="https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
		url = adb_windows # Most common

		# Check current OS
		if platform.system() == "Linux" :
			url = adb_linux

		if platform.system() == "Windows" :
			# Download zip file
			os.system("cd binaries & wget.exe -O tools.zip %s" % url)
			os.system("cd binaries & move tools.zip ../tools.zip")

		else :
			wget.download(url)


		# Extract the file
		self.extract_zip("tools.zip")


	def extract_zip(self, zip_file) :

		# Method to extract the current zip file
		with ZipFile(zip_file) as obj :
			obj.extractall()

		self.set_path()


	def set_path(self) :
		os.system("""
		cat >> ~/.profile<< EOF if [ -d '\$HOME/platform-tools' ] ; then
 		PATH='\$HOME/platform-tools:\$PATH'
		fi
		EOF
		""")