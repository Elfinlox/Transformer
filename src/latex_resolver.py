import glob
import os
import re

exceptions = ['begin', 'end'] # To not remove content inside tag
ignorelist = ['&', '$', '#', '_', '{', '}', '~', '^']# Ignore tag and consider it to be a part of the text

def remove_comments(text):
    text = [(lambda x: re.sub(re.compile("\\\\%"), "\n", x))(line) for line in text]
    text = [(lambda x: re.sub(re.compile("\s*%.*?\n"), "\n", x))(line) for line in text] # remove all occurance singleline comments (% COMMENT) from string
    return text

def ignore_tags(text, ignorelist):
    bracket = ['\\\\'+tag+"{[^{}]*}" for tag in ignorelist]
    nobracket = ['\\\\'+tag for tag in ignorelist]
    pattern = '|'.join(bracket + nobracket)
    pattern = r"(%s)" % pattern
    text = [(lambda x: re.sub(pattern, "", x))(line) for line in text]
    return text

def remove_content(text, exceptions):
    exceptions = ['\s*\\\\'+tag+"{[^{}]*}" for tag in exceptions]
    pattern = exceptions + ["\s*\\\\\w*|{|}|\$|\[|\]"]
    pattern = '|'.join(pattern)
    pattern = r"(%s)" % pattern
    tokenized = [(lambda x: re.split(pattern, x))(line) for line in text] # re.sub(re.compile(r"\\.*{.*}"), " ", text)
    final = []
    for line in tokenized:
        line = list(filter(None, line))
        line = ''.join([token if (re.match(pattern, token) or token == '\n') else "<text>" for token in line]) 
        if not re.match(r"\s*\n\s*", line):
            final.append(line)
    return final
