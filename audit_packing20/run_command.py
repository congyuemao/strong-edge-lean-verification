"""Run a process with separate raw output, exit status and Sydney/UTC times."""
import datetime, json, os, pathlib, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')
ROOT = pathlib.Path(__file__).resolve().parent
PROJECT = ROOT / 'isolated' / 'strong_edge_lean_starter'
BIN = ROOT.parent / '.tools' / 'lean-4.35.0-rc4-windows' / 'bin'
label, *args = sys.argv[1:]
if args[0] in ('lean', 'lake'):
    args[0] = str(BIN / (args[0] + '.exe'))
env = os.environ.copy()
env['PATH'] = str(BIN) + os.pathsep + env['PATH']
env['MATHLIB_CACHE_DIR'] = str(ROOT / 'dependency-cache')
logs = ROOT / 'logs'
logs.mkdir(exist_ok=True)
start = datetime.datetime.now(datetime.timezone.utc)
with (logs / (label + '.stdout.log')).open('wb') as out, (logs / (label + '.stderr.log')).open('wb') as err:
    proc = subprocess.run(args, cwd=PROJECT, env=env, stdout=out, stderr=err)
end = datetime.datetime.now(datetime.timezone.utc)
record = dict(command=args, cwd=str(PROJECT), compiler_bin=str(BIN), start_utc=start.isoformat(), end_utc=end.isoformat(), start_sydney=start.astimezone(datetime.timezone(datetime.timedelta(hours=11))).isoformat(), seconds=(end-start).total_seconds(), exit_code=proc.returncode)
(logs / (label + '.json')).write_text(json.dumps(record, indent=2), encoding='utf-8')
print(json.dumps(record))
print((logs / (label + '.stdout.log')).read_text(encoding='utf-8', errors='replace')[-3000:])
print((logs / (label + '.stderr.log')).read_text(encoding='utf-8', errors='replace')[-3000:])
sys.exit(proc.returncode)
