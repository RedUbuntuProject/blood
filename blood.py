import os
import json
import tarfile
import shutil
import sys
import argparse
import subprocess
import urllib.request

class BloodPM:
    def __init__(self):
        self.lib_dir = "/usr/lib/blood/"
        self.bin_dir = "/usr/local/bin/"
        self.db_dir = "/var/lib/blood/db/"
        self.temp_surgery = "/tmp/blood-surgery/"
        self.repo_url = "https://raw.githubusercontent.com/RedShelfProject/hypernova-tools/main/packages/"
        self._initialize_system()

    def _initialize_system(self):
        paths = [self.lib_dir, self.db_dir, self.temp_surgery]
        for path in paths:
            if not os.path.exists(path):
                try:
                    os.makedirs(path, exist_ok=True)
                except: pass

    def scout(self, package_path):
        if not os.path.exists(package_path): return None
        try:
            with tarfile.open(package_path, "r:gz") as tar:
                dna_file = tar.extractfile("dna.json")
                if dna_file:
                    return json.loads(dna_file.read().decode('ascii'))
        except: return None

    def fetch_hypernova(self, name):
        print(f"[*] SCANNING HYPERNOVA: Searching for {name} in RedShelf...")
        target_url = f"{self.repo_url}{name}.bld"
        local_path = f"/tmp/{name}.bld"
        try:
            urllib.request.urlretrieve(target_url, local_path)
            return local_path
        except:
            return None

    def hunt_apt(self, name):
        print(f"[*] SCOUTING OS REPOS: Seeking {name}...")
        try:
            process = subprocess.Popen(
                ['apt-get', 'install', '-y', name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={'DEBIAN_FRONTEND': 'noninteractive'}
            )
            process.wait()
            return process.returncode == 0
        except: return False

    def hunt(self, target):
        pkg_path = target
        if not os.path.exists(target) and not target.endswith(".bld"):
            remote_pkg = self.fetch_hypernova(target)
            if remote_pkg:
                pkg_path = remote_pkg
            else:
                if self.hunt_apt(target):
                    print(f"[+] CAPTURED: {target} extracted from OS.")
                    return
                else:
                    print(f"[-] ERROR: Target '{target}' not found in any vein.")
                    return

        dna = self.scout(pkg_path)
        if not dna: return
        name = dna.get('name')
        print(f"[+] HUNTING: Injecting {name} v{dna.get('version')}...")
        
        for dep in dna.get('dependencies', []):
            if not os.path.exists(os.path.join(self.lib_dir, dep)):
                print(f"[!] MISSING: Dependency '{dep}' not in {self.lib_dir}")
                return

        try:
            with tarfile.open(pkg_path, "r:gz") as tar:
                tar.extractall(self.temp_surgery)
                src_bin = os.path.join(self.temp_surgery, dna['binary_path'])
                dest_bin = os.path.join(self.bin_dir, name)
                shutil.copy(src_bin, dest_bin)
                os.chmod(dest_bin, 0o755)
            with open(os.path.join(self.db_dir, f"{name}.json"), "w") as db:
                json.dump(dna, db, indent=4)
            print(f"[*] CAPTURED: {name} is now locked in system veins.")
        except Exception as e:
            print(f"[-] SURGERY FAILED: {e}")
        finally:
            if os.path.exists(self.temp_surgery): shutil.rmtree(self.temp_surgery)
            if pkg_path.startswith("/tmp/") and os.path.exists(pkg_path): os.remove(pkg_path)

    def eliminate(self, name):
        db_path = os.path.join(self.db_dir, f"{name}.json")
        if os.path.exists(db_path):
            os.remove(os.path.join(self.bin_dir, name))
            os.remove(db_path)
            print(f"[+] ELIMINATED: {name} purged from system.")
        else:
            print(f"[*] SEEKING OS: Eliminating {name} via secondary layer...")
            subprocess.run(['apt-get', 'remove', '-y', name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[+] DONE: {name} neutralized.")

def main():
    if os.geteuid() != 0:
        print("[-] ACCESS DENIED: Root privileges required.")
        sys.exit(1)
    parser = argparse.ArgumentParser(prog='blood')
    parser.add_argument('action', choices=['hunt', 'eliminate', 'scout', 'bleed'])
    parser.add_argument('target', nargs='?', help='Target package or name')
    args = parser.parse_args()
    pm = BloodPM()
    if args.action == 'hunt' and args.target: pm.hunt(args.target)
    elif args.action == 'eliminate' and args.target: pm.eliminate(args.target)
    elif args.action == 'bleed':
        print("[*] BLEEDING: Purifying system veins...")
        subprocess.run(['apt-get', 'autoremove', '-y'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[*] DONE: System is clear.")
    else: parser.print_help()

if __name__ == "__main__":
    main()
