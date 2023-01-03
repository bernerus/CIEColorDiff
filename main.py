# Extract colorimetric data from Alex' PDF library and compute CIE E00 differences.
# Source data is in PDF format. This code extracts the interesting data from the
# PDF documents, computes differences and produces an Excel worksheet.

import PyPDF2 # To read PDFs
from ciecolor import * # The colorimetry computation


import xlsxwriter # To prodyce Excel

workbook = xlsxwriter.Workbook('colorimetric_results.xlsx')
worksheet = workbook.add_worksheet()
merge_format = workbook.add_format({'align':'center',
                                    'bold': True})
worksheet.merge_range('A1:R1', 'Colorimetric results', merge_format)

def get_color_coords(pdf_file_object) -> Ciecolor:
	""" Extract color coordinaes in the PDF document"""
	pdfreader = PyPDF2.PdfFileReader(pdf_file_object)
	# This will store the number of pages of this pdf file
	x = pdfreader.numPages
	# create a variable that will select the selected number of pages
	page_object = pdfreader.getPage(x - 1)
	# create text variable which will store all text data from the pdf file
	text = page_object.extractText()
	lines = text.split('\n')

	# There are two types of documents
	if "Color Coordinates" in lines:
		line = lines.pop(0)
		while "Coordinates" not in line:
			line = lines.pop(0)
		lines.pop(0)
		lines.pop(0)
		lines.pop(0)
		lines.pop(0)
		line = lines.pop(0)
		hdeg = float(line.replace(',', '.'))
		lines.pop(0)
		lines.pop(0)
		line = lines.pop(0)
		cstar = float(line.replace(',', '.'))
		lines.pop(0)
		lines.pop(0)
		line = lines.pop(0)
		bstar = float(line.replace(',', '.'))
		lines.pop(0)
		lines.pop(0)
		line = lines.pop(0)
		astar = float(line.replace(',', '.'))
		lines.pop(0)
		lines.pop(0)
		line = lines.pop(0)
		lstar = float(line.replace(',', '.'))
		lines.pop(0)
		lines.pop(0)
		line = lines.pop(0)
		name = line.replace(',', '.')
		return Ciecolor(name, hdeg, cstar, bstar, astar, lstar)
	elif "Job Results" in lines:
		line = lines.pop()  # Looking backwards here, hence not pop(0)
		while "Std" not in line:
			line = lines.pop()
		lines.pop()
		lines.pop()
		name = lines.pop()
		lines.pop()
		lines.pop()
		lines.pop()
		lines.pop()
		lines.pop()
		line = lines.pop()
		astar = float(line.replace(',', '.'))
		lines.pop()
		lines.pop()
		line = lines.pop()
		lstar = float(line.replace(',', '.'))
		lines.pop()
		lines.pop()
		line = lines.pop()
		bstar = float(line.replace(',', '.'))
		lines.pop()
		lines.pop()
		line = lines.pop()
		cstar = float(line.replace(',', '.'))
		lines.pop()
		lines.pop()
		line = lines.pop()
		hdeg = float(line.replace(',', '.'))
		return Ciecolor(name, hdeg, cstar, bstar, astar, lstar)
	else:
		return None


# Path where the calorimeter PDF's are stored
dirname = "~/colorimetry/standards pdf/sample bed 2"


from pathlib import Path

# Get a list of all the "before" PDFs
pathlist = Path(dirname).glob('**/*before.pdf')

worksheet.set_column('A:A', 15)
worksheet.write('A3','Color name', merge_format)
worksheet.merge_range('B2:F2', 'Before ageing', merge_format)
worksheet.merge_range('G2:L2', 'After 308 hours', merge_format)
worksheet.merge_range('M2:R2', 'After 786 hours', merge_format)
worksheet.write('B3','h°')
worksheet.write('C3','a*')
worksheet.write('D3','b*')
worksheet.write('E3','C*')
worksheet.write('F3','L*')
worksheet.write('G3','h°')
worksheet.write('H3','a*')
worksheet.write('I3','b*')
worksheet.write('J3','C*')
worksheet.write('K3','L*')
worksheet.write('L3','∆E00')
worksheet.write('M3','h°')
worksheet.write('N3','a*')
worksheet.write('O3','b*')
worksheet.write('P3','C*')
worksheet.write('Q3','L*')
worksheet.write('R3','∆E00')

row=4

for b4 in sorted(pathlist):  # Gio through them sorted

	before = open(b4, "rb")
	# print(b4)
	before_color = get_color_coords(open(b4, "rb"))
	color_name = b4.stem.replace('bed 2_','').replace('_before','')
	worksheet.write('A'+str(row), color_name)
	worksheet.write('B' + str(row), before_color.hdeg)
	worksheet.write('C' + str(row), before_color.astar)
	worksheet.write('D' + str(row), before_color.bstar)
	worksheet.write('E' + str(row), before_color.cstar)
	worksheet.write('F' + str(row), before_color.lstar)
	try:
		mid_color = get_color_coords(open(b4.as_posix().replace("before", "308"), "rb"))
		worksheet.write('G' + str(row), mid_color.hdeg)
		worksheet.write('H' + str(row), mid_color.astar)
		worksheet.write('I' + str(row), mid_color.bstar)
		worksheet.write('J' + str(row), mid_color.cstar)
		worksheet.write('K' + str(row), mid_color.lstar)
	except FileNotFoundError:
		mid_color = None

	try:
		after_color_filename = b4.as_posix().replace("before", "after")
		after_color = get_color_coords(open(after_color_filename, "rb"))
		worksheet.write('M' + str(row), after_color.hdeg)
		worksheet.write('N' + str(row), after_color.astar)
		worksheet.write('O' + str(row), after_color.bstar)
		worksheet.write('P' + str(row), after_color.cstar)
		worksheet.write('Q' + str(row), after_color.lstar)
	except FileNotFoundError:
		after_color = None


	print(str(before_color), "\n",
	      str(mid_color), "\n",
	      str(after_color))

	if mid_color:
		mdiff = before_color.diff(mid_color)  # Compute diff
		worksheet.write('L' + str(row), mdiff)
		print("Diff before to 308: %f" % mdiff)
	else:
		print("No 308 color")
	if after_color:
		adiff = before_color.diff(after_color) # Compute diff
		worksheet.write('R' + str(row), adiff)
		print("Diff before to after: %f" % adiff)
	else:
		print("No after color")

	print()
	row += 1


workbook.close()