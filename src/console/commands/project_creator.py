
from ast import Dict, Match, Tuple
from dataclasses import dataclass
import io
import json
import os
import contextlib
import re
import shutil
import subprocess
import tarfile
from typing import Any, Iterator, List, MutableMapping, Optional, Union
import zipfile

VAR_REF_REGEX = r'{{(.*?)}}'
TEMPLATES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'
)

OptInt = Optional[int]
OptBytes = Optional[bytes]
EnvVars = MutableMapping
StrPath = Union[str, 'os.PathLike[str]']

def create_new_project_skeleton(
    project_name: str, project_type: Optional[str] = 'legacy'
) -> None:
    osutils = OSUtils()
    all_projects = list_available_projects(TEMPLATES_DIR, osutils)
    project = [p for p in all_projects if p.key == project_type][0]
    template_kwargs = {
        'app_name': project_name,
    }
    project_creator = ProjectCreator(osutils)
    project_creator.create_new_project(
        os.path.join(TEMPLATES_DIR, project.dirname),
        project_name,
        template_kwargs=template_kwargs,
    )


class OSUtils(object):
    ZIP_DEFLATED = zipfile.ZIP_DEFLATED

    def environ(self) -> MutableMapping:
        return os.environ

    def open(self, filename: str, mode: str) -> IO:
        return open(filename, mode)

    def remove_file(self, filename: str) -> None:
        """Remove a file, noop if file does not exist."""
        # Unlike os.remove, if the file does not exist,
        # then this method does nothing.
        try:
            os.remove(filename)
        except OSError:
            pass

    def file_exists(self, filename: str) -> bool:
        return os.path.isfile(filename)

    def get_file_contents(
        self, filename: str, binary: bool = True, encoding: Any = 'utf-8'
    ) -> str:
        # It looks like the type definition for io.open is wrong.
        # the encoding arg is unicode, but the actual type is
        # Optional[Text].  For now we have to use Any to keep mypy happy.
        if binary:
            mode = 'rb'
            # In binary mode the encoding is not used and most be None.
            encoding = None
        else:
            mode = 'r'
        with io.open(filename, mode, encoding=encoding) as f:
            return f.read()

    def set_file_contents(
        self, filename: str, contents: str, binary: bool = True
    ) -> None:
        if binary:
            mode = 'wb'
        else:
            mode = 'w'
        with open(filename, mode) as f:
            f.write(contents)

    def extract_zipfile(self, zipfile_path: str, unpack_dir: str) -> None:
        with zipfile.ZipFile(zipfile_path, 'r') as z:
            z.extractall(unpack_dir)

    def extract_tarfile(self, tarfile_path: str, unpack_dir: str) -> None:
        with tarfile.open(tarfile_path, 'r:*') as tar:
            tar.extractall(unpack_dir)

    def directory_exists(self, path: str) -> bool:
        return os.path.isdir(path)

    def get_directory_contents(self, path: str) -> List[str]:
        return os.listdir(path)

    def makedirs(self, path: str) -> None:
        os.makedirs(path)

    def dirname(self, path: str) -> str:
        return os.path.dirname(path)

    def abspath(self, path: str) -> str:
        return os.path.abspath(path)

    def joinpath(self, *args: str) -> str:
        return os.path.join(*args)

    def walk(
        self, path: str, followlinks: bool = False
    ) -> Iterator[Tuple[str, List[str], List[str]]]:
        return os.walk(path, followlinks=followlinks)

    def copytree(self, source: str, destination: str) -> None:
        if not os.path.exists(destination):
            self.makedirs(destination)
        names = self.get_directory_contents(source)
        for name in names:
            new_source = os.path.join(source, name)
            new_destination = os.path.join(destination, name)
            if os.path.isdir(new_source):
                self.copytree(new_source, new_destination)
            else:
                shutil.copy2(new_source, new_destination)

    def rmtree(self, directory: str) -> None:
        shutil.rmtree(directory)

    def copy(self, source: str, destination: str) -> None:
        shutil.copy(source, destination)

    def move(self, source: str, destination: str) -> None:
        shutil.move(source, destination)

    @contextlib.contextmanager
    def tempdir(self) -> Any:
        tempdir = tempfile.mkdtemp()
        try:
            yield tempdir
        finally:
            shutil.rmtree(tempdir)

    def popen(
        self,
        command: List[str],
        stdout: OptInt = None,
        stderr: OptInt = None,
        env: Optional[EnvVars] = None,
    ) -> subprocess.Popen:
        p = subprocess.Popen(command, stdout=stdout, stderr=stderr, env=env)
        return p

    def mtime(self, path: str) -> float:
        return os.stat(path).st_mtime

    def stat(self, path: str) -> os.stat_result:
        return os.stat(path)

    def normalized_filename(self, path: str) -> str:
        """Normalize a path into a filename.

        This will normalize a file and remove any 'drive' component
        from the path on OSes that support drive specifications.

        """
        return os.path.normpath(os.path.splitdrive(path)[1])

    @property
    def pipe(self) -> int:
        return subprocess.PIPE

    def basename(self, path: str) -> str:
        return os.path.basename(path)
    

@dataclass
class ProjectTemplate:
    dirname: str
    metadata: Dict[str, Any]
    key: str

    @property
    def description(self) -> str:
        # Pylint doesn't understand the attrs types.
        # pylint: disable=no-member
        return self.metadata.get('description', self.key)


def list_available_projects(
    templates_dir: str, osutils: OSUtils
) -> List[ProjectTemplate]:
    projects = []
    for dirname in sorted(osutils.get_directory_contents(templates_dir)):
        filename = osutils.joinpath(templates_dir, dirname, 'metadata.json')
        metadata = json.loads(osutils.get_file_contents(filename, False))
        key = dirname.split('-', 1)[1]
        projects.append(ProjectTemplate(dirname, metadata, key=key))
    return projects


class ProjectCreator(object):
    def __init__(self, osutils: Optional[OSUtils] = None) -> None:
        if osutils is None:
            osutils = OSUtils()
        self._osutils = osutils

    def create_new_project(
        self,
        source_dir: str,
        destination_dir: str,
        template_kwargs: Dict[str, Any],
    ) -> None:
        for full_src_path, full_dst_path in self._iter_files(
            source_dir, destination_dir
        ):
            dest_dir = self._osutils.dirname(full_dst_path)
            if not self._osutils.directory_exists(dest_dir):
                self._osutils.makedirs(dest_dir)
            contents = self._osutils.get_file_contents(
                full_src_path, binary=False
            )
            templated_contents = get_templated_content(
                contents, template_kwargs
            )
            self._osutils.set_file_contents(
                full_dst_path, templated_contents, binary=False
            )

    def _iter_files(
        self, source_dir: str, destination_dir: str
    ) -> Iterator[Tuple[str, str]]:
        for rootdir, _, filenames in self._osutils.walk(source_dir):
            for filename in filenames:
                if self._should_ignore(filename):
                    continue
                full_src_path = os.path.join(rootdir, filename)
                # The starting index needs `+ 1` to account for the
                # trailing `/` char (e.g. foo/bar -> foo/bar/).
                full_dst_path = os.path.join(
                    destination_dir, full_src_path[len(source_dir) + 1:]
                )
                yield full_src_path, full_dst_path

    
def get_templated_content(
    contents: str, template_kwargs: Dict[str, Any]
) -> str:
    def lookup_var(match: Match) -> str:
        var_name = match.group(1)
        try:
            return template_kwargs[var_name]
        except KeyError:
            raise Exception(
                f"Template variable '{var_name}' not found in "
                f"template kwargs: {template_kwargs}"
            )

    new_contents = re.sub(VAR_REF_REGEX, lookup_var, contents)
    return new_contents

