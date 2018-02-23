import sys
import math
import random
import warnings
import numpy as np
from collections import namedtuple

class RamanSample(object):
    def __init__(self, names, rruffid, spectrum, ideal_chemistry=None, 
            locality=None, owner=None, source=None,
            description=None, status=None, url=None, measured_chemistry=None):
        self.names = names
        self.rruffid = rruffid
        self.ideal_chemistry = ideal_chemistry
        self.locality = locality
        self.owner = owner
        self.source = source
        self.description = description
        self.status = status
        self.url = url
        self.measured_chemistry = measured_chemistry
        self.spectrum = spectrum
        self.spectrum_matrix = np.array(spectrum)

    @classmethod
    def create_from_file(cls, file_path):
        attrs = cls.parse_raw_file(file_path)
        return cls(**attrs)


    @staticmethod
    def get_spectrum_and_label_from_file(file_path):
        attrs = RamanSample.parse_raw_file(file_path)
        spectrum = np.array(attrs.get("spectrum"))
        label = attrs.get("names")
        return (spectrum, label)

    @staticmethod
    def parse_line(l):
        if l.strip() == "":
            return None, None
        elif l.startswith("##"):
            k_raw, v = l.split("=")[:2]
            k = k_raw[2:].lower().replace(" ", "_")
            if k == "end":
                return None, None
        else:
            k = "spectrum"
            try:
                x_val, y_val = [float(x.strip()) for x in l.split(", ")]
            except ValueError:
                warnings.warn("Could not convert to string: {}".format(l))
                x_val, y_val = (float(l.split(", ")[0]), 0)
            v = np.array([x_val, y_val])

        return k, v

    @staticmethod
    def parse_raw_file(file_path):
        attrs = {"spectrum" : []}
        with open(file_path) as f:
            c = 0
            for line in f:
                c +=1
                k, v = RamanSample.parse_line(line.strip())
                if k:
                    if k == "spectrum":
                        attrs[k].append(v)
                    else:
                        attrs[k] = v
        return attrs


    @staticmethod
    def find_nearest(array,value):
        idx = np.searchsorted(array, value, side="left")
        if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
            return idx-1
        else:
            return idx

    def conform_to_range(self, start=500, end=1500, by=0.1):
        return RamanSample.conform_to_range(self.spectrum_matrix, start, end, by)

    @staticmethod
    def conform_to_range(spectrum_matrix, start=500, end=1500, by=0.1):
        ran = np.arange(start, end, by)
        b = [RamanSample.find_nearest(spectrum_matrix[:,0], x) for x in ran]
        return np.array(spectrum_matrix[b, 1])


if __name__ == "__main__":
    path = sys.argv[1]
    r = RamanSample.create_from_file(path)
    d = r.conform_to_range()
    print(d.shape)


