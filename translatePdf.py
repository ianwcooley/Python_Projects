#! python3

# translatePdf.py: Takes a given pdf file and translates it from
# one language to another, creating a translated pdf in the cwd.
# Usage: ./translatePdf.py <source pdf> <source language> <destination language>

import PyPDF2, os, sys, re, googletrans, docx, pypandoc

translator = googletrans.Translator()

sourcePdf = sys.argv[1]
sourceLang = sys.argv[2].lower()
destLang = sys.argv[3].lower()

# Check if languages are supported.
def is_lang_unsupported(lang):
    return (lang not in googletrans.LANGUAGES.keys() 
        and lang not in googletrans.LANGUAGES.values())
# If one of the languages is not supported, exit the program
for lang in (sourceLang, destLang):
    if is_lang_unsupported(lang):
        print('Language "' + lang + '" is not supported.')
        sys.exit()

# Function to remove newlines from source pdf, as these are often peppered
# throughout the source pdf in random places.
# TODO: Improve this function so that the paragraph and chapter breaks
# in the dest pdf match their appearance in the source pdf.
def condense_paragraphs(input_string):
    condensed_string = re.sub(r'\n', ' ', input_string)
    return condensed_string

# Make reader for source pdf and writer for dest docx
sourcePdfFileObj = open(sourcePdf, 'rb')
reader = PyPDF2.PdfReader(sourcePdfFileObj)
destDoc = docx.Document()
paraObj = destDoc.add_paragraph('')

# Read each page from source pdf and write it to dest docx
for page in reader.pages:
    sourceText = page.extract_text()
    destText = translator.translate(sourceText, src=sourceLang, dest=destLang).text
    paraObj.add_run(destText)

# save dest docx
destDocName = os.path.splitext(sourcePdf)[0] + '(' + sourceLang +'_to_' + destLang +')' + '.docx'
destDoc.save(destDocName)

# Convert dest docx to pdf
pypandoc.convert_file(destDocName, 'pdf', outputfile=os.path.splitext(destDocName)[0] + '.pdf')
