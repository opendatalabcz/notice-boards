import shutil
import os
import traceback
import pdf2image
import PIL
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def clear_dir(dir):
    for f in [f for f in os.listdir(dir)]:
        os.remove(os.path.join(dir, f))


def rename_files(dir, temp_dir):
    for filename in os.listdir(dir):
        if not filename.endswith('.pdf'):
            continue

        clear_dir(temp_dir)
        full_filename = '{}/{}'.format(dir, filename)
        print('renaming {}'.format(full_filename))
        if os.path.getsize(full_filename) > 8000000:
            print('File is too big and will not be renamed')
            continue

        try:
            pages = pdf2image.convert_from_path(
                full_filename, 500, first_page=1, last_page=1, output_folder=temp_dir)
        except pdf2image.exceptions.PDFPageCountError:
            print('PDF page count error occured. File will not be renamed')
            continue
        except PIL.Image.DecompressionBombError:
            print('Decompression bomb error occured. File will not be renamed')
            continue
        imagename = "{}.jpg".format(filename[:-4])
        full_imagename = '{}/{}'.format(dir, imagename)
        try:
            pages[0].save(full_imagename, 'JPEG')
        except IndexError:
            print('Error occured. File will not be renamed')
            continue
        text = str(
            ((pytesseract.image_to_string(PIL.Image.open(full_imagename)))))
        os.remove(full_imagename)
        # The recognized text is stored in variable text
        # Any string processing may be applied on text
        # Here, basic formatting has been done:
        # In many PDFs, at line ending, if a word can't
        # be written fully, a 'hyphen' is added.
        # The rest of the word is written in the next line
        # Eg: This is a sample text this word here GeeksF-
        # orGeeks is half on first line, remaining on next.
        # To remove this, we replace every '-\n' to ''.
        text = text.replace('-\n', '')
        new_name = text.split('\n')[0]+'.pdf'
        for forbiden_char in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
            new_name = new_name.replace(forbiden_char, '')
        if os.path.isfile('{}/{}'.format(dir, new_name)):
            count = 2
            while os.path.isfile('{}/{}({}).pdf'.format(dir, new_name[:-4], count)):
                count = count+1
            new_name = '{}({}).pdf'.format(new_name[:-4], count)
        print('new name is {}/{}'.format(dir, new_name))
        os.rename(full_filename, '{}/{}'.format(dir, new_name))


# directory to save a temporary file for pdf to image conversion
directories = [d.name for d in os.scandir('.') if d.is_dir()]
temp_dir = 'temp'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
for dir in range(len(directories)):
    print('current dir is {}'.format(directories[dir]))
    print('{} directories left'.format(len(directories)-dir-1))
    rename_files(directories[dir], temp_dir)
print('finished')
shutil.rmtree('temp')
