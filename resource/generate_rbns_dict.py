import re

def new_protein(line: str, data: dict, out_path: str) -> None:
	if line.strip():
		parts = line.split()
		protein = re.split("-|_", parts[0])[0]
		concentration = re.split("-|_", parts[0])[-1]
		url = parts[1]

		if protein not in data:
			print(f'\t"{protein}" : {{',sep="", end="", file=out_path)
			print(f'\n\t\t"{concentration}" : "{url}"', end="", sep="", file=out_path)
			data[protein] = []
		else:
			print(f',\n\t\t"{concentration}" : "{url}"', end="", sep="", file=out_path)
		data[protein].append(url)
	else:
		print(f" }},\n", sep="", end="", file=out_path)

def parse_file(file_path, output_file):
	data = {}
	print(f"rbns_data = {{\n",sep="",end="", file=output_file)
	with open(file_path, 'r') as f:
		for line in f:
			new_protein(line=line, data=data, out_path=output_file)
	print(f"}}\n",sep="",end="", file=output_file)
	return data

def save_data(data, output_file):
	with open(output_file, 'w') as f:
		f.write("protein_data = " + repr(data))

if __name__ == "__main__":
	file_path = "file.list"
	output_file_path = "rbns_downloader/data.py"
	output_file = open(output_file_path, "w")
	data = parse_file(file_path, output_file)
    # save_data(data, output_file)
