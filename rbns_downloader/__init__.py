import argparse
from argparse import Namespace
from .downloader import *

def download(args: Namespace, rbns_downloader: RBNSDownloader) -> None:
	if args.target == 'all':
		rbns_downloader.download_all()
	else:
		rbns_downloader.download_experiment(target=args.target)

def list_target(args: Namespace, rbns_downloader: RBNSDownloader) -> None:
	if args.target == 'all':
		rbns_downloader.list_all()
	else:
		rbns_downloader.list_experiment(target=args.target)

def main():
	parser = argparse.ArgumentParser(
		prog='rbns',
		description='A package to download RNA Bind-n-Seq experimental data')
	parser.add_argument('-o', '--output', type=str, required=False, default='',
	                    help='Output directory to save RBNS data to.')
	parser.add_argument('-v', '--verbose', action='store_true',
	                    help='Show download progress of targets')
	parser.add_argument('action', type=str, choices=['download', 'list'],
	                    help='Specify what action to take. `download\' to download an experiment, `list\' to list files from experiment.')
	parser.add_argument('target', type=str,
	                    help='Specify which target to download, or `all\' to download all experiments.')
	
	args = parser.parse_args()

	rbns_downloader = RBNSDownloader(output_dir=args.output, verbose=args.verbose)
	if args.action == 'download':
		download(args=args, rbns_downloader=rbns_downloader)
	elif args.action == 'list':
		list_target(args=args, rbns_downloader=rbns_downloader)

if __name__ == "__main__":
	main()
