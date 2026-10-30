"""Resume local episode production on Windows using the existing cached voices.

Usage: .venv/Scripts/python -B tools/production_resume.py voice ep05 ep06
       ... schedule|stills|picture|package ep05 ep06
Voice and picture jobs are sequential to respect the machine's memory limit.
No uploads, publishing, or removal of the YAYIN directory are performed.
"""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
PY = str(ROOT / '.venv/Scripts/python.exe')
os.chdir(ROOT)
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'
ffmpeg = shutil.which('ffmpeg')
if not ffmpeg:
    candidates = sorted((Path(os.environ['LOCALAPPDATA']) / 'Microsoft/WinGet/Packages').glob('Gyan.FFmpeg_*/ffmpeg-*/bin/ffmpeg.exe'))
    if not candidates:
        raise SystemExit('FFmpeg is not installed')
    os.environ['PATH'] = str(candidates[-1].parent) + os.pathsep + os.environ['PATH']
LANGS = ('tr', 'hi', 'pt', 'es')

def run(ep, label, args, cwd=ROOT):
    folder = ROOT / 'video' / ep / 'build' / 'production'
    folder.mkdir(parents=True, exist_ok=True)
    log = folder / (label + '.log')
    print(f'[{ep}] {label} START {time.strftime("%H:%M:%S")} -> {log.relative_to(ROOT)}', flush=True)
    with log.open('w', encoding='utf-8') as out:
        result = subprocess.run(args, cwd=cwd, stdout=out, stderr=subprocess.STDOUT)
    if result.returncode:
        print(log.read_text(encoding='utf-8', errors='replace')[-6000:], flush=True)
        raise SystemExit(f'{ep} {label} failed: {result.returncode}')
    print(f'[{ep}] {label} DONE {time.strftime("%H:%M:%S")}', flush=True)

def py(ep, label, script, *args):
    run(ep, label, [PY, '-B', script, *args])

def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hash(ep, render_only=False):
    folder = ROOT / 'video' / ep
    files = [folder / n for n in ('index.html', ep + '.js', 'sketches.js', 'script.json', 'build/schedule.json')]
    files += [f for f in (ROOT / 'video/engine').iterdir() if f.suffix in ('.js', '.css', '.mjs')]
    if (folder / 'assets').exists():
        files += [f for f in (folder / 'assets').rglob('*') if f.is_file()]
    if not render_only:
        files += [ROOT / 'tools' / n for n in ('build.py', 'dub.py', 'bumpers.py', 'music.py', 'cbx.py')]
        files += [ROOT / 'video/bumper' / n for n in ('bumper.js', 'index.html')]
        files += [f for d in ('dub', 'subs') for f in (folder / d).glob('*.json')]
        files += [f for f in (ROOT / 'footage' / ep).glob('*') if f.is_file()]
        files += [f for f in (ROOT / 'video/assets/music').glob('*') if f.is_file()]
        for lang in ('en', *LANGS):
            audio = folder / 'build' / ('audio' if lang == 'en' else 'dub_' + lang)
            files += list(audio.glob('s*.mp3'))
            files += [audio / ('timings.json' if lang == 'en' else 'cache.json')]
    digest = hashlib.sha256()
    for f in sorted(set(files)):
        digest.update(f.relative_to(ROOT).as_posix().encode())
        digest.update(bytes.fromhex(hash_file(f)))
    return digest.hexdigest()


def write_proof(path, signature, outputs):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'source': signature, 'outputs': {
        f.relative_to(ROOT).as_posix(): hash_file(f) for f in outputs}}, indent=2), encoding='utf-8')


def proof_current(path, signature):
    try:
        proof = json.loads(path.read_text(encoding='utf-8'))
        return proof['source'] == signature and bool(proof['outputs']) and all(
            (ROOT / name).exists() and hash_file(ROOT / name) == digest
            for name, digest in proof['outputs'].items())
    except (OSError, ValueError, KeyError):
        return False


@contextmanager
def gpu_lock():
    import msvcrt
    path = ROOT / 'build/production-gpu.lock'
    path.parent.mkdir(exist_ok=True)
    with path.open('a+b') as lock:
        lock.seek(0, 2)
        if lock.tell() == 0:
            lock.write(b'0')
            lock.flush()
        lock.seek(0)
        try:
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            raise SystemExit('A voice/shorts production job already holds the GPU lock.')
        try:
            yield
        finally:
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)


def short_signature(ep):
    folder = ROOT / 'video/shorts' / ep
    spec = json.loads((folder / 'short.json').read_text(encoding='utf-8'))
    files = [folder / 'short.json', ROOT / spec['source'], ROOT / 'tools/short.py',
             ROOT / 'tools/cbx.py', ROOT / 'video/shorts/short.js', ROOT / 'video/shorts/short.html']
    files += [f for f in (ROOT / 'video/engine').iterdir() if f.suffix in ('.js', '.css', '.mjs')]
    if 'schedule' in spec:
        files.append(ROOT / spec['schedule'])
    for segment in spec['segments']:
        for shot in segment['shots']:
            if 'file' in shot:
                files.append(ROOT / shot['file'])
            if 'footage' in shot and (ROOT / shot['footage']['file']).exists():
                files.append(ROOT / shot['footage']['file'])
    for lang in ('en', 'tr'):
        out = folder / 'build' / lang
        files += [out / 'cbx_cache.json'] + [out / (seg['id'] + '.mp3') for seg in spec['segments']]
    return hashlib.sha256(''.join(hash_file(f) for f in files).encode()).hexdigest()


def short_status(ep):
    folder = ROOT / 'video/shorts' / ep
    try:
        current = proof_current(folder / 'build/production-proof.json', short_signature(ep))
    except (OSError, ValueError, KeyError):
        current = False
    return 'ready for review' if current else 'pending: run the separate shorts step'


def fingerprint(ep, lang):
    folder = ROOT / 'video' / ep
    spec = folder / ('script.json' if lang == 'en' else f'dub/{lang}.json')
    audio = folder / 'build' / ('audio' if lang == 'en' else f'dub_{lang}')
    digest = hashlib.sha256(spec.read_bytes())
    for p in sorted(audio.glob('s*.mp3')):
        digest.update(p.name.encode())
        digest.update(p.read_bytes())
    for name in ('tools/cbx.py', 'tools/cbx_retake.py', 'tools/chatterbox_say.py', 'tools/align.py', 'tools/dub_check.py'):
        digest.update((ROOT / name).read_bytes())
    return digest.hexdigest()

def retake(ep, lang):
    marker = ROOT / 'video' / ep / 'build' / 'production' / f'retake_{lang}.sha256'
    before = fingerprint(ep, lang)
    if marker.exists() and marker.read_text() == before:
        print(f'[{ep}] retake_{lang} reused unchanged retake inputs', flush=True)
        return
    py(ep, f'retake_{lang}', 'tools/cbx_retake.py', f'video/{ep}', lang)
    marker.write_text(fingerprint(ep, lang))

def voice(ep):
    py(ep, 'tts', 'tools/tts.py', f'video/{ep}')
    retake(ep, 'en')
    py(ep, 'schedule0', 'tools/build.py', f'video/{ep}', 'schedule')
    for lang in LANGS:
        py(ep, f'narrate_{lang}', 'tools/dub.py', f'video/{ep}', lang, '--report')
        retake(ep, lang)
    schedule(ep)

def schedule(ep):
    py(ep, 'schedule', 'tools/build.py', f'video/{ep}', 'schedule')
    py(ep, 'lesson_lint', 'tools/lesson_lint.py', ep)
    py(ep, 'anchor_check', 'tools/anchor_check.py', ep)
    py(ep, 'pace_check', 'tools/pace_check.py', f'video/{ep}')
    loc = ROOT / 'video' / ep / 'make_localize.py'
    if loc.exists():
        py(ep, 'localize', str(loc))
    sched = json.loads((ROOT / 'video' / ep / 'build/schedule.json').read_text())
    print(f'[{ep}] timeline {sched["duration"]:.2f} seconds', flush=True)

def stills(ep):
    schedule_data = json.loads((ROOT / 'video' / ep / 'build/schedule.json').read_text())
    scenes = {}
    for sid, seg in schedule_data['segments'].items():
        scenes.setdefault(seg['scene'], []).append(seg)
    times = [str(round((v[0]['start'] + v[-1]['end']) / 2, 2)) for v in scenes.values()]
    run(ep, 'stills', ['node', 'engine/render.mjs', ep, '--stills', ','.join(times)], ROOT / 'video')

def picture(ep):
    p = ROOT / 'video' / ep
    duration = json.loads((p / 'build/schedule.json').read_text())['duration']
    py(ep, 'anchor_check', 'tools/anchor_check.py', ep)
    baseline = source_hash(ep)
    render_source = source_hash(ep, render_only=True)
    render_proof = p / 'build/production/render-proof.json'
    if proof_current(render_proof, render_source):
        print(f'[{ep}] current render reused', flush=True)
    else:
        run(ep, 'render', ['node', 'engine/render.mjs', ep], ROOT / 'video')
        assert render_source == source_hash(ep, render_only=True), 'Inputs changed during render'
        write_proof(render_proof, render_source, [p / 'build/video.mp4', p / 'build/clips.json'])
    py(ep, 'audio', 'tools/build.py', f'video/{ep}', 'audio')
    py(ep, 'compose', 'tools/build.py', f'video/{ep}', 'compose')
    for lang in LANGS:
        py(ep, f'dub_{lang}', 'tools/dub.py', f'video/{ep}', lang)
    py(ep, 'subs', 'tools/build.py', f'video/{ep}', 'subs')
    py(ep, 'localize', f'video/{ep}/make_localize.py')
    assert baseline == source_hash(ep), 'Production inputs changed during picture job'
    outputs = [p / 'build/video.mp4', p / 'build/clips.json', p / 'build' / f'{ep}_final.mp4']
    outputs += [p / 'build' / f'dub_{lang}.m4a' for lang in LANGS]
    outputs += [p / 'build' / f'{ep}_{lang}_dub.mp4' for lang in LANGS]
    outputs += list((p / 'build').glob(f'{ep}_*.srt'))
    write_proof(p / 'build/production/picture-proof.json', baseline, outputs)
    print(f'[{ep}] long video ready for review; Shorts: {short_status(ep)}', flush=True)

def package(ep):
    p = ROOT / 'video' / ep
    b = p / 'build'
    target = ROOT / 'YAYIN' / ep
    target.mkdir(parents=True, exist_ok=True)
    needed = [b / f'{ep}_final.mp4', p / 'localize.json', p / 'youtube.md']
    needed += [b / f'dub_{l}.m4a' for l in LANGS]
    needed += [b / f'{ep}_{l}.srt' for l in ('en', 'tr', 'hi', 'pt', 'es', 'ar', 'de', 'fr', 'id', 'ja', 'ru', 'vi')]
    missing = [str(f.relative_to(ROOT)) for f in needed if not f.exists()]
    if missing:
        raise SystemExit('Cannot package incomplete media: ' + ', '.join(missing))
    for f in needed:
        destination = target
        if f.suffix == '.m4a':
            destination = target / 'dublaj_sesleri'
        elif f.suffix == '.srt':
            destination = target / 'altyazilar'
        destination.mkdir(parents=True, exist_ok=True)
        name = f.name.replace('dub_', '') if f.suffix == '.m4a' else f.name
        shutil.copy2(f, destination / name)
    loc = json.loads((p / 'localize.json').read_text(encoding='utf-8'))
    for lang, entry in loc.items():
        (target / f'aciklama_{lang}.txt').write_text(entry['title'] + chr(10)*2 + entry['description'] + chr(10), encoding='utf-8')
    print(f'[{ep}] package {target}', flush=True)

def verify(ep):
    import re
    sys.path.insert(0, str(ROOT / 'tools'))
    import cbx
    p = ROOT / 'video' / ep
    b = p / 'build'
    sc = json.loads((p / 'script.json').read_text(encoding='utf-8'))
    sched = json.loads((b / 'schedule.json').read_text())
    ids = [s['id'] for s in sc['segments']]
    assert list(sched['segments']) == ids
    en = json.loads((b / 'audio/timings.json').read_text(encoding='utf-8'))
    cfg = cbx.settings(sc, 'en')
    assert set(en) == set(ids), 'Stale English timing IDs'
    for segment in sc['segments']:
        sid = segment['id']
        item = sched['segments'][sid]
        assert en[sid]['key'] == cbx.key(cfg, segment['text']), 'Stale English voice: ' + sid
        assert abs(item['dur'] - en[sid]['duration']) <= .001, 'Stale scheduled duration: ' + sid
        assert abs(item['end'] - item['start'] - en[sid]['duration']) <= .0011, 'Stale scheduled end: ' + sid
        assert item['scene'] == segment['scene'], 'Stale scheduled scene: ' + sid
        assert item['words'] == [{'w': w['w'], 't': round(w['t'], 3)} for w in en[sid]['words']], 'Stale scheduled words: ' + sid
    assert proof_current(b / 'production/render-proof.json', source_hash(ep, render_only=True)), 'No current render proof: run picture'
    assert proof_current(b / 'production/picture-proof.json', source_hash(ep)), 'No current final-media proof: run picture'
    def probe(file):
        return json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(file)]))
    final = probe(b / f'{ep}_final.mp4')
    duration = float(final['format']['duration'])
    import bumpers
    body_duration = float(probe(b / 'video.mp4')['format']['duration'])
    assert abs(body_duration - sched['duration']) < .1, 'Body length differs from schedule'
    assert abs(duration - body_duration - bumpers.INTRO - bumpers.OUTRO) < .2, 'Final length differs from body and bumpers'
    assert any(v['codec_type'] == 'video' and v.get('width') == 1920 and v.get('height') == 1080 and v.get('pix_fmt') == 'yuv420p' for v in final['streams'])
    assert any(v['codec_type'] == 'audio' for v in final['streams'])
    report = {'episode': ep, 'body_seconds': sched['duration'], 'final_seconds': duration, 'dubs': {}, 'subtitles': {}, 'footage': [], 'shorts': short_status(ep)}
    for lang in LANGS:
        dub = json.loads((p / f'dub/{lang}.json').read_text(encoding='utf-8'))
        cache = json.loads((b / f'dub_{lang}/cache.json').read_text())
        assert set(dub['segments']) == set(ids)
        cfg = cbx.settings(dub, lang)
        for i, sid in enumerate(ids):
            assert cache[sid]['key'] == cbx.key(cfg, dub['segments'][sid]), f'{lang} {sid}: stale voice'
            start = sched['segments'][sid]['start']
            end = sched['segments'][ids[i + 1]]['start'] if i + 1 < len(ids) else sched['duration'] - 1.5
            assert cache[sid]['duration'] / (end - start - 0.35) <= 1.031, f'{lang} {sid}: dub would be rushed'
        audio_duration = float(probe(b / f'dub_{lang}.m4a')['format']['duration'])
        assert abs(audio_duration - duration) < 0.2, f'{lang}: audio/video length mismatch'
        report['dubs'][lang] = {'seconds': audio_duration, 'current_segments': len(ids)}
    def seconds(t):
        h, m, sec = t.replace(',', '.').split(':')
        return int(h)*3600 + int(m)*60 + float(sec)
    for lang in ('en', 'tr', 'hi', 'pt', 'es', 'ar', 'de', 'fr', 'id', 'ja', 'ru', 'vi'):
        text = (b / f'{ep}_{lang}.srt').read_text(encoding='utf-8')
        cues = re.findall(r'(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})', text)
        assert cues, f'{lang}: empty subtitles'
        previous = 0
        for a, z in cues:
            a, z = seconds(a), seconds(z)
            assert previous <= a < z <= duration + 0.1, (lang, previous, a, z)
            previous = z
        report['subtitles'][lang] = len(cues)
    clips = json.loads((b / 'clips.json').read_text())
    for clip in clips:
        files = list((ROOT / 'footage' / ep).glob(clip['id'] + '.*'))
        assert files, 'Missing footage: ' + clip['id']
        source_seconds = float(probe(files[0])['format']['duration'])
        needed = (clip['t1'] + .35 - max(0, clip['t0'] - .3)) if clip.get('full') else clip['t1'] - clip['t0']
        assert source_seconds + 0.05 >= needed, f"{clip['id']}: {source_seconds:.2f}s source for {needed:.2f}s slot"
        report['footage'].append({'id': clip['id'], 'source_seconds': source_seconds, 'slot_seconds': needed})
    loc = json.loads((p / 'localize.json').read_text(encoding='utf-8'))
    assert len(loc) == 12
    for lang, entry in loc.items():
        assert len(entry['title']) <= 100 and len(entry['description']) <= 5000
        assert '?' * 2 not in entry['title'] + entry['description'], 'Broken Unicode in ' + lang
        assert chr(0xfffd) not in entry['title'] + entry['description']
    (b / 'production/verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)


def finish(ep):
    verify(ep)
    b = ROOT / 'video' / ep / 'build'
    samples = b / 'dinleme'
    samples.mkdir(exist_ok=True)
    for lang in ('en', *LANGS):
        d = b / ('audio' if lang == 'en' else f'dub_{lang}')
        selected = [d / (sid + '.mp3') for sid in ('s01', 's13', 's35') if (d / (sid + '.mp3')).exists()]
        listing = samples / f'{lang}.txt'
        listing.write_text(chr(10).join("file '" + f.as_posix() + "'" for f in selected), encoding='utf-8')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(listing), '-t', '45', '-c:a', 'libmp3lame', '-b:a', '128k', str(samples / f'{ep}_{lang}_sample.mp3')], check=True)
    package(ep)
    target = ROOT / 'YAYIN' / ep
    shutil.copytree(samples, target / 'dinleme', dirs_exist_ok=True)
    thumbs = target / 'kucuk_resimler'
    thumbs.mkdir(exist_ok=True)
    for variant in ('A', 'B'):
        shutil.copy2(ROOT / 'video/thumbs/build' / f'{ep}_{variant}.png', thumbs)
    shutil.copy2(b / 'production/verification.json', target)


def shorts(ep):
    verify(ep)
    folder = ROOT / 'video/shorts' / ep
    spec = json.loads((folder / 'short.json').read_text(encoding='utf-8'))
    outputs = []
    for lang in ('en', 'tr'):
        py(ep, 'short_' + lang + '_narrate', 'tools/short.py', 'video/shorts/' + ep, lang, '--narrate')
        py(ep, 'short_' + lang + '_retake', 'tools/cbx_retake.py', 'video/shorts/' + ep, lang, '--short')
        py(ep, 'short_' + lang + '_build', 'tools/short.py', 'video/shorts/' + ep, lang)
        out = folder / 'build' / lang
        result = out / (spec['episode'] + '_short_' + lang + '.mp4')
        expected = json.loads((out / 'data.json').read_text(encoding='utf-8'))['schedule']['duration']
        def duration(path):
            return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)]))
        assert abs(duration(out / 'panel.mp4') - expected) <= 1/30 + .001, 'Short panel length mismatch: ' + lang
        assert abs(duration(result) - expected) <= 1/30 + .03, 'Short final length mismatch: ' + lang
        outputs.append(result)
    write_proof(folder / 'build/production-proof.json', short_signature(ep), outputs)
    target = ROOT / 'YAYIN' / ep / 'shorts'
    target.mkdir(parents=True, exist_ok=True)
    for output in outputs:
        shutil.copy2(output, target / output.name)
    if (folder / 'youtube.md').exists():
        shutil.copy2(folder / 'youtube.md', target / 'youtube.md')
    print(f'[{ep}] EN/TR Shorts ready for review', flush=True)


def review(ep):
    verify(ep)
    import bumpers
    from PIL import Image, ImageDraw
    b = ROOT / 'video' / ep / 'build'
    final = b / (ep + '_final.mp4')
    output = b / 'review'
    output.mkdir(exist_ok=True)
    sched = json.loads((b / 'schedule.json').read_text())
    tc = bumpers.cut(ROOT / 'video' / ep)
    samples = [(0.5, 'opening')]
    for index, clip in enumerate(json.loads((b / 'clips.json').read_text())):
        samples.append((bumpers.shift((clip['t0']+clip['t1'])/2, tc), clip['id']+'-middle'))
        samples.append((bumpers.shift(clip['t1']-0.1, tc), clip['id']+'-end'))
    samples.append((bumpers.shift(sched['duration']-2,tc), 'body-end'))
    entries=[]
    for index, (seconds, label) in enumerate(samples):
        target=output / (str(index).zfill(2)+'-'+label+'.png')
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(round(seconds,3)),'-i',str(final),'-frames:v','1','-vf','scale=960:540',str(target)],check=True)
        entries.append({'seconds':seconds,'label':label,'file':target.name})
    for offset in range(0,len(entries),4):
        sheet=Image.new('RGB',(1920,1120),'#0b1220')
        draw=ImageDraw.Draw(sheet)
        for i, entry in enumerate(entries[offset:offset+4]):
            x,y=(i%2)*960,(i//2)*560
            with Image.open(output/entry['file']) as picture:
                sheet.paste(picture,(x,y))
            draw.text((x+10,y+542),str(round(entry['seconds'],2))+'s '+entry['label'],fill='white')
        sheet.save(output/('sheet-'+str(offset//4)+'.png'))
    (output/'index.json').write_text(json.dumps(entries,indent=2),encoding='utf-8')
    print(ep, 'final-video review images:', output, flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('step', choices=('voice', 'schedule', 'stills', 'picture', 'package', 'verify', 'finish', 'shorts', 'review'))
    ap.add_argument('episodes', nargs='+', choices=('ep05', 'ep06'))
    args = ap.parse_args()
    if args.step in ('voice', 'shorts'):
        with gpu_lock():
            for ep in args.episodes:
                globals()[args.step](ep)
    else:
        for ep in args.episodes:
            globals()[args.step](ep)

if __name__ == '__main__':
    main()
