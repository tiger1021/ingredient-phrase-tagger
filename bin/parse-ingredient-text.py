#!/usr/bin/env python
from __future__ import print_function

import sys
import os
import tempfile
import StringIO
import json
import subprocess
from ingredient_phrase_tagger.training import utils


if len(sys.argv) < 2:
    sys.stderr.write('Usage: parse-ingredients.py TEXT')
    sys.exit(1)

text = sys.argv[1]


_, tmpFile = tempfile.mkstemp()

string_file = StringIO.StringIO(text)
text_file = open(tmpFile, "wt")
text_file.write(utils.export_data(string_file.readlines()))
text_file.close()

tmpFilePath = "../tmp/model_file"
modelFilename = os.path.join(os.path.dirname(__file__), tmpFilePath)
results = StringIO.StringIO(subprocess.check_output(["crf_test", "-v", "1", "-m", modelFilename, tmpFile]))
os.system("rm %s" % tmpFile)
results_json = (json.dumps(utils.import_data(results), indent=4))
print(results_json)


