"""Install comparator prerequisites in a task-local directory, without sudo/profile edits.

Run in WSL with Python 3. Downloads are checked against publisher SHA256 manifests.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import urllib.request

BASE = Path('/home/z5242/.local/share/percolation-workflow/tools')


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'percolation-workflow'})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def download(url, destination, expected):
    if destination.exists() and hashlib.sha256(destination.read_bytes()).hexdigest() == expected:
        return
    data = fetch(url)
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError(f'SHA256 mismatch: {url}')
    destination.write_bytes(data)


def main():
    BASE.mkdir(parents=True, exist_ok=True)
    (BASE / 'bin').mkdir(exist_ok=True)
    releases = json.loads(fetch('https://go.dev/dl/?mode=json'))
    release = next(r for r in releases if r['stable'])
    archive = next(f for f in release['files'] if f['os'] == 'linux' and f['arch'] == 'amd64'
                   and f['kind'] == 'archive')
    go_dir = BASE / release['version']
    if not (go_dir / 'go/bin/go').exists():
        package = BASE / archive['filename']
        print(f'Downloading {archive["filename"]}', flush=True)
        download('https://go.dev/dl/' + archive['filename'], package, archive['sha256'])
        go_dir.mkdir(exist_ok=True)
        with tarfile.open(package) as tar:
            tar.extractall(go_dir, filter='data')
    print(subprocess.check_output([str(go_dir / 'go/bin/go'), 'version'], text=True), flush=True)
    jq_base = 'https://github.com/jqlang/jq/releases/download/jq-1.8.1/'
    checksums = fetch(jq_base + 'sha256sum.txt').decode()
    jq_sha = next(line.split()[0] for line in checksums.splitlines()
                  if line.split()[-1].lstrip('*') == 'jq-linux-amd64')
    jq = BASE / 'bin/jq'
    download(jq_base + 'jq-linux-amd64', jq, jq_sha)
    jq.chmod(0o755)
    print(subprocess.check_output([str(jq), '--version'], text=True), flush=True)
    rust_base = 'https://static.rust-lang.org/rustup/dist/x86_64-unknown-linux-gnu/'
    rust_sha = fetch(rust_base + 'rustup-init.sha256').decode().split()[0]
    installer = BASE / 'rustup-init'
    download(rust_base + 'rustup-init', installer, rust_sha)
    installer.chmod(0o755)
    import os
    env = dict(os.environ, CARGO_HOME=str(BASE / 'cargo'), RUSTUP_HOME=str(BASE / 'rustup'))
    subprocess.run([str(installer), '-y', '--no-modify-path', '--profile', 'minimal',
                    '--default-toolchain', 'stable'], env=env, check=True)
    manifest = {'go_bin': str(go_dir / 'go/bin'), 'bin': str(BASE / 'bin'),
                'cargo_home': env['CARGO_HOME'], 'rustup_home': env['RUSTUP_HOME'],
                'go_archive_sha256': archive['sha256'], 'jq_sha256': jq_sha,
                'rustup_init_sha256': rust_sha}
    (BASE / 'installation.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest), flush=True)


if __name__ == '__main__':
    main()
