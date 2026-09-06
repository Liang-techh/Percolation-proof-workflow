"""Content-addressed, per-lemma verification bundles for the trusted coordinator.

The dependency checkout/cache is environment-owned and must already be pinned and
trusted. This does not turn arbitrary shared caches into authenticated artifacts.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re


def stage_bundle(source_project, destination_root, *, node_name, challenge_module,
                 solution_module, source_files, dependency_project, dependency_name,
                 link_cache=True, manifest_identity=None):
    source_project = Path(source_project).resolve()
    dependency_project = Path(dependency_project).resolve()
    destination_root = Path(destination_root).resolve()
    for module in (challenge_module, solution_module, dependency_name):
        if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*(\.[A-Za-z_][A-Za-z_0-9]*)*', module):
            raise ValueError('unsupported module or dependency name')
    files = {}
    for name in source_files:
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name or relative.suffix != '.lean':
            raise ValueError('bundle requires explicit safe relative Lean source paths')
        path = source_project.joinpath(*relative.parts).resolve()
        if not path.is_relative_to(source_project):
            raise ValueError('source symlink escapes project')
        files[relative.as_posix()] = path.read_bytes()
    for module in (challenge_module, solution_module):
        if module.replace('.', '/') + '.lean' not in files:
            raise ValueError('both comparator modules must be frozen in the bundle')
    files['lean-toolchain'] = (source_project / 'lean-toolchain').read_bytes()
    if files['lean-toolchain'].strip() != (dependency_project / 'lean-toolchain').read_bytes().strip():
        raise ValueError('dependency toolchain mismatch')
    manifest = json.loads((source_project / 'lake-manifest.json').read_text(encoding='utf-8'))
    dependency_manifest = json.loads((dependency_project / 'lake-manifest.json').read_text(encoding='utf-8'))
    # The source manifest records the trusted dependency as a path package,
    # while the dependency checkout records that same package as a git pin.
    # Compare all other git pins; the path package is checked below by name and
    # by the supplied dependency checkout itself.
    pins = lambda data: {
        p['name']: (p.get('url'), p.get('rev'))
        for p in data['packages']
        if p['type'] == 'git' and p['name'] != dependency_name
    }
    if pins(manifest) != pins(dependency_manifest):
        raise ValueError('dependency revisions differ from the source project')
    found = False
    logical_dependency = '.lake/pinned-dependency'
    for package in manifest['packages']:
        if package['type'] == 'path':
            if package['name'] != dependency_name:
                raise ValueError('unmapped path dependency')
            # Keep the bundle content-addressed across hosts. The coordinator
            # materializes this logical path as a symlink below the bundle.
            package['dir'] = logical_dependency
            found = True
    if not found:
        raise ValueError('expected pinned path dependency missing')
    files['lake-manifest.json'] = json.dumps(manifest, sort_keys=True, indent=2).encode()
    if manifest_identity is not None:
        if (not isinstance(manifest_identity, dict)
                or not isinstance(manifest_identity.get('sha256'), str)):
            raise ValueError('bundle manifest identity is malformed')
        files['manifest.identity.json'] = json.dumps(manifest_identity, sort_keys=True,
                                                      indent=2).encode()
    modules = sorted(name[:-5].replace('/', '.') for name in files if name.endswith('.lean'))
    config = ('name = "verifiedLemmaBundle"\n' +
              'defaultTargets = [' + ', '.join(json.dumps(module) for module in modules) + ']\n' +
              '[[require]]\nname = ' + json.dumps(dependency_name)
              + '\npath = ' + json.dumps(logical_dependency) + '\n')
    config += ''.join('[[lean_lib]]\nname = ' + json.dumps(module) + '\n' for module in modules)
    files['lakefile.toml'] = config.encode()
    files['comparator.json'] = json.dumps({
        'challenge_module': challenge_module, 'solution_module': solution_module,
        'theorem_names': [node_name], 'definition_names': [],
        'permitted_axioms': ['propext', 'Quot.sound', 'Classical.choice'],
        'enable_nanoda': True}, indent=2).encode()
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files.items())}
    digest = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    destination = destination_root / digest
    marker = destination / 'bundle.json'
    if destination.exists():
        if not marker.is_file() or json.loads(marker.read_text()) != {'digest': digest, 'files': hashes}:
            raise ValueError('incomplete or mismatched existing bundle; inspect instead of overwriting')
        for name, data in files.items():
            if (destination / name).read_bytes() != data:
                raise ValueError('frozen verification bundle was modified')
    else:
        destination.mkdir(parents=True)
        for name, data in files.items():
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        marker.write_text(json.dumps({'digest': digest, 'files': hashes}, indent=2), encoding='utf-8')
    if link_cache:
        cache = dependency_project / '.lake/packages'
        if not cache.is_dir():
            # A path dependency may itself be a package checkout (for example
            # mathlib under a parent project's `.lake/packages`). In that
            # layout the package's sibling directory is the shared cache.
            package_cache = dependency_project.parent
            if dependency_project.parent.name == 'packages' and package_cache.is_dir():
                cache = package_cache
            else:
                raise ValueError('pinned dependency cache unavailable')
        local = destination / '.lake/packages'
        local.parent.mkdir(exist_ok=True)
        if local.exists() or local.is_symlink():
            if not local.is_symlink() or local.resolve() != cache.resolve():
                raise ValueError('bundle cache does not match pinned environment')
        else:
            local.symlink_to(cache, target_is_directory=True)
        pinned = destination / logical_dependency
        pinned.parent.mkdir(parents=True, exist_ok=True)
        if pinned.exists() or pinned.is_symlink():
            if not pinned.is_symlink() or pinned.resolve() != dependency_project:
                raise ValueError('bundle pinned dependency does not match environment')
        else:
            pinned.symlink_to(dependency_project, target_is_directory=True)
    return destination
