import urllib.request
import shutil
import os 
import tarfile
import sys

import glob
import os

from tqdm.auto import tqdm
from latex_resolver import *

PATH = "./../data/papers/"

TEMP = "./../data/temp/"

papers = open("./../data/selected_papers.txt", "rt", encoding = "utf8")
lines = papers.read().split("\n")
papers.close()

EXCEPTIONS = ['begin', 'end'] # To not remove content inside tag
IGNORE = ['&', '$', '#', '_', '{', '}', '~', '^']# Ignore tag and consider it to be a part of the text

n = int(len(lines) / 2)
print("Number of papers:", n)

if not os.path.exists(PATH):
        os.mkdir(PATH)

if not os.path.exists(TEMP):
        os.mkdir(TEMP)

i1 = 0

if len(sys.argv) > 1:
    if not os.path.isfile("./../data/progress.txt"): 
        sys.exit("File doesn't exist: Try using arg 'restart'")
    progress = open("./../data/progress.txt", "rt", encoding = "utf8")
    i1 = int(progress.readlines()[-1])


progress = open("./../data/progress.txt", "wt", encoding = "utf8")


for i in range(i1, n, 1):
    print("="*100)
    paper_link = lines[2*i+1]
    paper_code = paper_link.split("/")[-1]
    paper_source_link = "https://export.arxiv.org/e-print/" + paper_code
    try:
            # Download the file from `paper_source_link` and save it locally under `str(i)+".tar.gz"`:
        compressed_file_path = TEMP + str(i)+".tar.gz"
        with urllib.request.urlopen(paper_source_link) as response, open(compressed_file_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

        # Extract from tar the tar file
        tar = tarfile.open(compressed_file_path)
        paper_folder = TEMP + str(i) + "/"
        tar.extractall(path=paper_folder)
        tar.close()

        extension = "*.tex"
        tex_files = glob.glob(paper_folder + extension, recursive=True)
        root_files = []

        for f_path in tex_files:
            with open(f_path, encoding = "utf8") as f:
                tex = f.readlines()
                root_files.append(tex)
       
        if len(root_files) < 1:
            print("No root file")
        elif len(root_files) > 1:
            print("Multiple root files %g" % (i))
            for j in range(len(root_files)):
                with open(PATH + str(i) + "-" + str(j) + ".tex", "wt", encoding = "utf8") as f:
                    tex = root_files[j]
                    tex = remove_comments(tex)
                    tex = ignore_tags(tex, IGNORE)
                    tex = remove_content(tex, EXCEPTIONS)
                    for line in tex:
                        f.writelines(line)
        else:
            print("Single root file %g" % (i))
            with open(PATH + str(i) + ".tex", "wt", encoding = "utf8") as f:
                tex = root_files[0]
                tex = remove_comments(tex)
                tex = ignore_tags(tex, IGNORE)
                tex = remove_content(tex, EXCEPTIONS)
                for line in tex:
                    f.writelines(line)
    except Exception as e:
        print("Error at paper %g" % (i))
        print(e)
    try:
        os.remove(TEMP + str(i) + ".tar.gz")
        shutil.rmtree(TEMP + str(i))
    except Exception:
        print("Cannot Delete")

    progress.writelines([str(i), '\n'])
    print("progress: %g / %g" % (i+1, n), end="\r")