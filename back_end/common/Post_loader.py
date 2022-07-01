import os
from os import listdir
import csv
from os.path import isfile, join
import zipfile
import json
import pickle
import xml.etree.ElementTree as ET
import sys
maxInt = sys.maxsize
import time
import functools, inspect
import numpy as np
from xml.dom import minidom

root = os.path.dirname(__file__)
inputFiles = []
outputFiles = []
caller = ''

while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        global inputFiles, outputFiles, caller
        inputFiles = []
        outputFiles = []
        caller = ''
        func(*args, **kw)
        with open(root + '/log/runLog.txt', 'a', encoding='utf-8') as file_w:
            file_w.write('=' * 20 + '\n')
            file_w.write("Time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n')
            file_w.write("Call Func: " + caller + ': ' + func.__name__ + '\n')
            file_w.write("Input files: " + ', '.join(set(inputFiles)) + '\n')
            file_w.write("Output file: " + ', '.join(set(outputFiles)) + '\n')
    return wrapper


def before_and_after(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kw):
        if hasattr(self, 'before') and inspect.ismethod(self.before):
            self.before(*args, **kw)
        result = f(self, *args, **kw)
        if hasattr(self, 'after') and inspect.ismethod(self.after):
            self.after(*args, **kw)
        return result
    return wrapper


class BeforeAfterMeta(type):
    def __new__(mcs, classname, bases, body):
        for name, value in body.items():
            if not inspect.isfunction(value):
                continue
            if name in ('before', 'after') or name[:2] + name[-2:] == '_' * 4:
                # before or after hook, or a special method name like __init__.
                continue
            body[name] = before_and_after(value)
        return super(BeforeAfterMeta, mcs).__new__(mcs, classname, bases, body)


class PostLoader(metaclass=BeforeAfterMeta):
    def __init__(self):
        self.root = os.path.dirname(__file__)
        pass

    def before(self, *args, **kw):
        pass

    def after(self, *args, **kw):
        global inputFiles, caller
        inputFiles.append(args[0])
        frame = inspect.stack()
        caller = frame[2].filename

    def load_csv(self, file_path,  delimiter=',', ignore_header=False, encoding='utf-8'):
        with open(self.root + file_path, encoding=encoding, errors='ignore') as file_r:
            file_r = csv.reader(file_r, delimiter=delimiter)
            if ignore_header:
                next(file_r, None)
            csv_file = []
            for one_line in file_r:
                csv_file.append(one_line)
            return csv_file

    def load_cve(self, file_path='/output/nvd'):
        files = [f for f in listdir(self.root + file_path) if isfile(join(self.root + file_path, f))]
        files = [name for name in files if name.startswith('nvdcve-1.0-') and name.endswith('.zip')]
        files.sort()

        cve_list = []
        for file in files:
            archive = zipfile.ZipFile(join(self.root + file_path, file), 'r')
            jsonfile = archive.open(archive.namelist()[0])
            cve_dict = json.loads(jsonfile.read())
            jsonfile.close()
            for cve_entity in cve_dict['CVE_Items']:
                cve_list.append(cve_entity)
        return cve_list

    def load_files(self, file_path):
        with open(self.root +file_path, encoding='utf-8') as file_r:
            return [one_line.strip('\r\n') for one_line in file_r]

    def load_pickle(self, file_path):
        with open(self.root + file_path, 'rb') as file_r:
            file_r = pickle.load(file_r)
            return file_r

    def load_txt(self, file_path):
        with open(self.root + file_path, 'r', encoding='utf-8') as file_r:
            return [[one_line.strip('\r\n')] for one_line in file_r]

    def load_xml(self, file_path):
        tree = ET.parse(self.root + file_path)
        root = tree.getroot()
        return root

    def load_json(self, file_path):
        with open(self.root + file_path, 'r', encoding='utf-8') as file_r:
            return json.load(file_r)

    def load_npy(self, file_path):
        return np.load(self.root + file_path, allow_pickle=True)

    def load_xml_dom(self, file_path):
        doc = minidom.parse(self.root + file_path)
        root = doc.documentElement
        return root

    def load_jsonl(self, file_path):
        return_file = []
        with open(self.root + file_path, 'r', encoding='utf-8') as file_r:
            for one_line in file_r:
                return_file.append(json.loads(one_line))
        return return_file


class PostWriter(metaclass=BeforeAfterMeta):
    def __init__(self,input_path):
        self.file_path = os.path.dirname(__file__) + input_path

    def before(self, *args, **kw):
        pass

    # log the func call
    def after(self, *args, **kw):
        global outputFiles, caller
        outputFiles.append(self.file_path)
        frame = inspect.stack()
        caller = frame[2].filename

    def write_summary(self, write_dict):
        for (key, value) in write_dict.items():
            if len(value) > 0:
                with open(os.path.dirname(__file__) + '/raw_stories2/' + key + '.story', 'w', encoding='utf-8') as file_w:
                    write_sent = []
                    for one_value in value:
                        for one_sent in one_value[0]:
                            if not one_sent in write_sent:
                                write_sent.append(one_sent)
                    for one_ele in write_sent:
                        file_w.write(one_ele + '\n\n')
                    for one_value in value:
                        if len(one_value[1]) > 0:
                            file_w.write('@highlight' + '\n\n')
                            file_w.write(one_value[1] + '\n\n')
                            break

    def write_summary_exploit(self, write_dict):
        for (key, value) in write_dict.items():
            if len(value[1]) > 0:
                with open(os.path.dirname(__file__) + '/raw_stories4/' + key + '.story', 'w', encoding='utf-8') as file_w:
                    for one_ele in value[0]:
                        file_w.write(one_ele + '\n\n')
                    for one_value in value[1]:
                        if len(one_value) > 0:
                            file_w.write('@highlight' + '\n\n')
                            file_w.write(one_value + '\n\n')

    def write_csv(self, file_write, delimiter=','):
        with open(self.file_path, 'w', encoding='utf-8', newline='') as file_w:
            file_w = csv.writer(file_w, delimiter=delimiter)
            for one_line in file_write:
                file_w.writerow(one_line)

    def write_tsv(self, file_write, delimiter='\t'):
        with open(self.file_path, 'w', encoding='utf-8', newline='') as file_w:
            file_w = csv.writer(file_w, delimiter=delimiter, quotechar='\"')
            for one_line in file_write:
                file_w.writerow(one_line)

    def write_pickle(self, write_pkl):
        with open(self.file_path, 'wb') as file_w:
            pickle.dump(write_pkl, file_w)
            file_w.flush()

    def write_edgelist(self, write_edge):
        with open(self.file_path, 'w') as file_w:
            for one_line in write_edge:
                file_w.write(str(one_line[0]) + ' ' + str(one_line[1]) + '\n')

    def write_stopwords(self, write_file):
        with open(self.file_path, 'w') as file_w:
            for one_word in write_file:
                os.path.dirname(__file__)

    def write_txt(self, write_file):
        with open(self.file_path, 'w', encoding='utf-8') as file_w:
            for one_line in write_file:
                if len(one_line) == 1:
                    file_w.write(one_line[0] + '\n')
                else:
                    file_w.write(' '.join(one_line) + '\n')

    def write_json(self, write_file):
        with open(self.file_path, 'w', encoding='utf-8') as file_w:
            json.dump(write_file, file_w)

    def write_npy(self, write_file):
        np.save(self.file_path, write_file, allow_pickle=True)

    def write_jsonl(self, write_file):
        with open(self.file_path, 'w', encoding='utf-8') as file_w:
            for one_line in write_file:
                file_w.write(json.dumps(one_line) + '\n')