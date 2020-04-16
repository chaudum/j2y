import io
import os
from contextlib import contextmanager
from j2cli.cli import entrypoint


@contextmanager
def tmp_workdir(path):
    current = os.getcwd()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(current)


def test_write_template_in_different_location(tmpdir):
    template = tmpdir.mkdir("folder_a").join("template.j2")
    template.write('foo: "{{ value }}"')
    source = tmpdir.mkdir("folder_b").join("context.yaml")
    source.write('value: "bar"')
    output = io.StringIO()
    with tmp_workdir(tmpdir):
        entrypoint(str(template), output, contexts=[source])
    output.seek(0)
    assert output.read() == 'foo: "bar"\n'
