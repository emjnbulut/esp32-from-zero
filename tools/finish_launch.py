"""Complete existing episode 1-3 metadata/captions; never uploads a new video.
Run from the repository root with its main venv. Results are written in build/.
"""
import json
from pathlib import Path
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import publish
import sitelink

ROOT = Path(__file__).resolve().parent.parent
EPISODES = [("ep01", "RyR4OEA7ESA", "C"), ("ep02", "NwtftTFs_Og", "A"), ("ep03", "doPDxOPFjQg", "A")]
CHANNEL = "UCOGFzocCfvfYWiA5-MfHHwQ"
RESULT = ROOT / "build" / "launch_completion.json"


def reason(error):
    try:
        obj = json.loads(error.content)["error"]
        return {"status": error.resp.status, "reason": obj.get("errors", [{}])[0].get("reason", "unknown"), "message": obj.get("message")}
    except (KeyError, ValueError):
        return {"status": error.resp.status, "reason": "unknown"}


def main():
    yt = publish.youtube()
    own = yt.channels().list(part="id", mine=True).execute().get("items", [])
    assert any(x["id"] == CHANNEL for x in own), "Wrong channel"
    result = {"episodes": {}, "pending_captions": []}
    for ep, vid, thumb in EPISODES:
        loc = json.loads((ROOT / "video" / ep / "localize.json").read_text(encoding="utf-8"))
        for lang, entry in loc.items():
            assert len(entry["title"]) <= 100, (ep, lang, "title too long")
            entry["description"] = sitelink.apply(entry["description"], lang)
            assert len(entry["description"]) <= 5000
        v = yt.videos().list(part="snippet,localizations,status", id=vid).execute()["items"][0]
        assert v["snippet"]["channelId"] == CHANNEL
        sn = {k: v["snippet"][k] for k in ("title", "description", "categoryId", "tags") if k in v["snippet"]}
        sn.update(title=loc["en"]["title"], description=loc["en"]["description"], categoryId="27", defaultLanguage="en", defaultAudioLanguage="en")
        translations = dict(v.get("localizations", {}))
        translations.update({publish.YT_LANG.get(k, k): value for k, value in loc.items() if k != "en"})
        yt.videos().update(part="snippet,localizations", body={"id": vid, "snippet": sn, "localizations": translations}).execute()
        state = {"video_id": vid, "metadata": "updated", "scheduled_publish_at": v["status"].get("publishAt")}
        print(ep, "metadata updated; 11 translations + English; Education", flush=True)
        try:
            path = ROOT / "YAYIN" / ep / "kucuk_resimler" / f"{ep}_{thumb}.png"
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(path), mimetype="image/png")).execute()
            state["thumbnail"] = "uploaded " + path.name
            print(ep, state["thumbnail"], flush=True)
        except HttpError as e:
            state["thumbnail_error"] = reason(e)
            print(ep, "thumbnail", json.dumps(reason(e)), flush=True)
        result["episodes"][ep] = state
    RESULT.parent.mkdir(exist_ok=True)
    RESULT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    existing = {}
    for ep, vid, _ in EPISODES:
        existing[vid] = {c["snippet"]["language"] for c in yt.captions().list(part="snippet", videoId=vid).execute().get("items", []) if c["snippet"].get("trackKind") != "asr" and c["snippet"].get("status") != "failed"}
    jobs = [(ep, vid, lang) for lang in ["en", "tr", "hi", "pt", "es", "de", "fr", "ar", "id", "ja", "ru", "vi"] for ep, vid, _ in EPISODES]
    quota = False
    for ep, vid, lang in jobs:
        code = publish.YT_LANG.get(lang, lang)
        if code in existing[vid]:
            print(ep, code, "already present", flush=True)
            continue
        if quota:
            result["pending_captions"].append({"episode": ep, "video_id": vid, "language": lang})
            continue
        try:
            f = ROOT / "video" / ep / "build" / f"{ep}_{lang}.srt"
            response = yt.captions().insert(part="snippet", body={"snippet": {"videoId": vid, "language": code, "name": "", "isDraft": False}}, media_body=MediaFileUpload(str(f), mimetype="application/octet-stream")).execute()
            print(ep, code, "caption uploaded", response["id"], flush=True)
        except HttpError as e:
            error = reason(e)
            print(ep, code, "caption error", json.dumps(error), flush=True)
            result["pending_captions"].append({"episode": ep, "video_id": vid, "language": lang, "error": error})
            if error["reason"] == "quotaExceeded": quota = True
        RESULT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    for ep, vid, _ in EPISODES:
        cs = yt.captions().list(part="snippet", videoId=vid).execute().get("items", []) if not quota else []
        result["episodes"][ep]["captions"] = [{"id": c["id"], "language": c["snippet"]["language"], "status": c["snippet"].get("status"), "kind": c["snippet"].get("trackKind")} for c in cs]
    RESULT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("Report:", RESULT, "pending captions:", len(result["pending_captions"]), flush=True)

if __name__ == "__main__": main()
