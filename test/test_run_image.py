import os.path, docker
import nose.tools         as nose
import helper.application as app_helper
import helper.file        as file_helper

import nucleotides.util              as util
import nucleotides.command.run_image as image

from nose.plugins.attrib import attr

def test_docstring_parse():
    nose.assert_equal(util.parse(image.__doc__, ["run-image", "1"]),
            {'<task>': '1', 'run-image': True})

@attr('slow')
def test_execute_assembler_image():
    import json, shutil
    app = app_helper.mock_short_read_assembler_state(reads = True)
    os.environ['TMPDIR'] = file_helper.test_dir()
    image.execute_image(app)
    file_helper.assert_is_file(app["path"] + "/tmp/contig_fasta")
    file_helper.assert_is_file(app["path"] + "/outputs/container_runtime_metrics/metrics.json")
