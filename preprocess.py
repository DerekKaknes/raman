from lib.utils import RamanSample
import glob
import sys
import csv
import numpy as np
import warnings


def run(outfile):
    raw_files = glob.glob("data/*/*RAW*")
    samples = map(RamanSample.get_spectrum_and_label_from_file, raw_files)

    with open(outfile, "w") as f:
        writer = csv.writer(f)
        for s in samples:
            spectrum_matrix = s[0]
            label = s[1]
            try:
                new_spec = RamanSample.conform_to_range(
                        spectrum_matrix, 400, 1800, 2.0
                        )
                writer.writerow([label] + list(new_spec))
            except IndexError:
                warnings.warn("IndexError")
                pass

if __name__ == "__main__":
    outfile = sys.argv[1]
    run(outfile)

