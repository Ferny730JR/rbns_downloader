from rbns_downloader.data import rbns_data
from rbns_downloader.error_logger import *

from jellyfish import damerau_levenshtein_distance
from clint.textui.progress import Bar
from io import BufferedWriter
from requests import Response
import requests
import logging
import os

class RBNSDownloader:
	def __init__(self, output_dir: str="", chunk_size: int=1024*1024, verbose: bool=True) -> None:
		self.__rbns_data = rbns_data
		self.output_dir = output_dir
		self.chunk_size = chunk_size
		self.verbose = verbose
		logging.getLogger("requests").setLevel(logging.WARNING)
		logging.getLogger("urllib3").setLevel(logging.WARNING)

	def download_all(self) -> None:
		for target in self.__rbns_data.keys():
			self.download_experiment(target=target)
	
	def download_experiment(self, target: str) -> None:
		if target.upper() in self.__rbns_data:
			target = target.upper()
			num_files = len(self.__rbns_data[target])
			for i,files in enumerate(self.__rbns_data[target].keys()):
				# Extract the download information
				url = self.__rbns_data[target][files]
				out = os.path.join(self.output_dir, target)
				filename=f'{target}_{files}.fasta.gz'

				# Print update to console
				if self.verbose:
					print(f"Downloading {ANSI_COLOR_CYAN}{filename}{ANSI_COLOR_RESET} [{i+1}/{num_files}]...")

				# Download the file
				self.download_file(url=url, save_dir=out, filename=filename)
				remove_lines(1)
			if self.verbose:
				print(f"Downloaded {ANSI_COLOR_CYAN}{target}{ANSI_COLOR_RESET} [{num_files}/{num_files}]")
		else:
			self._check_typo_(target=target)
	
	def download_file(self, url: str, save_dir: str, filename: str=None) -> None:
		"""Download the specified file.

		Args:
			url (str): URL link that contains file to download
			save_dir (str): Directory to save the file to
			filename (str): Name to safe file to. Defaults to download filename if none provided.

		Returns:
			None: Does not return. Raises if encountered error downloading file.
		"""

		# Create output directory
		if not os.path.exists(save_dir):
			# warning_message("Directory `%s' does not exist. Creating directory...", save_dir)
			os.makedirs(save_dir)

		# Create local save file
		if filename == None:
			local_filename = os.path.join(save_dir, url.split('/')[-1])
		else:
			local_filename = os.path.join(save_dir, filename)

		# Begin download
		with requests.get(url, stream=True) as r:
			r.raise_for_status()
			with open(local_filename, 'wb') as f:
				if(self.verbose):
					self._download_progress_(response=r, out_file=f)
				else:
					self._download_(response=r, out_file=f)
	
	def list_all(self) -> None:
		print(f'{ANSI_COLOR_BRIGHT}Available RBNS experiments:{ANSI_COLOR_RESET}')
		for target in self.__rbns_data.keys():
			print(f'  - {ANSI_COLOR_CYAN}{target}{ANSI_COLOR_RESET}')
	
	def list_experiment(self, target: str) -> None:
		if target.upper() in self.__rbns_data:
			target = target.upper()
			controls = [concentration for concentration in self.__rbns_data[target].keys() if concentration == '0nM' or concentration == 'input']
			concentrations = [concentration for concentration in self.__rbns_data[target].keys() if concentration != '0nM' and concentration != 'input']

			print(f"Available files for {ANSI_COLOR_CYAN}{target}{ANSI_COLOR_RESET}")

			print(f"{ANSI_COLOR_BRIGHT}Concentration:{ANSI_COLOR_RESET}")
			if len(concentrations) > 0:
				for concentration in concentrations:
					print(f"  - {concentration}")
			else:
				print(f"  - None")
			
			print(f"{ANSI_COLOR_BRIGHT}Controls:{ANSI_COLOR_RESET}")
			if len(controls) > 0:
				for control in controls:
					print(f"  - {control}")
			else:
				print(f"  - None")
		else:
			self._check_typo_(target=target)
	
	def _download_progress_(self, response: Response, out_file: BufferedWriter) -> None:
		expected_size = int(response.headers.get('content-length'))/(self.chunk_size)
		bar = Bar(expected_size=expected_size)

		# Download file and show download progress
		for i,chunk in enumerate(response.iter_content(chunk_size=self.chunk_size)):
			out_file.write(chunk)
			bar.show(i+1)

		# Remove download bar
		remove_line()
	
	def _download_(self, response: Response, out_file: BufferedWriter) -> None:
		for chunk in response.iter_content(chunk_size=self.chunk_size):
			out_file.write(chunk)

	def _check_typo_(self, target: str) -> None:
		min_dist= float('inf')
		experiment_match = "None"

		for experiment in self.__rbns_data.keys():
			dist = damerau_levenshtein_distance(target.upper(), experiment.upper())
			if(dist < min_dist):
				min_dist = dist
				experiment_match = experiment

		error_message("Experiment for '%s%s%s'%s not found!", ANSI_COLOR_MAGENTA, target, ANSI_COLOR_RESET, ANSI_COLOR_BRIGHT)
		if(0 < min_dist and min_dist < 4):
			error_message("Did you mean '%s%s%s'%s?", ANSI_COLOR_CYAN, experiment_match, ANSI_COLOR_RESET, ANSI_COLOR_BRIGHT)
