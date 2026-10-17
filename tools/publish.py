"""Push an episode's subtitles and translated titles/descriptions to YouTube.

The video itself and the dubbed audio tracks are uploaded by hand in YouTube Studio
(the API cannot add audio tracks, and uploads from unaudited API projects stay private).

One-time setup: put the OAuth client file from Google Cloud (YouTube Data API v3,
"Desktop app" client) at .secrets/client_secret.json, then:
  python tools/publish.py auth                       # opens the browser once, saves .secrets/token.json

Per episode:
  python tools/publish.py video/ep01 <VIDEO_ID>      # all build/<ep>_<lang>.srt + <ep>/localize.json
  python tools/publish.py video/ep01 <VIDEO_ID> --dry-run

localize.json: {"en": {"title": "...", "description": "..."}, "tr": {...}, ...}
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECRETS = ROOT / ".secrets"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
# our file codes -> YouTube language codes
YT_LANG = {"pt": "pt-BR", "es": "es-419"}


def creds():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    tok = SECRETS / "token.json"
    c = Credentials.from_authorized_user_file(str(tok), SCOPES) if tok.exists() else None
    if c and c.expired and c.refresh_token:
        c.refresh(Request())
    elif not c or not c.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(SECRETS / "client_secret.json"), SCOPES)
        c = flow.run_local_server(port=0)
    tok.write_text(c.to_json(), encoding="utf-8")
    return c


def youtube():
    from googleapiclient.discovery import build
    return build("youtube", "v3", credentials=creds())


def captions(yt, ep: Path, vid: str, dry: bool):
    from googleapiclient.http import MediaFileUpload

    existing = yt.captions().list(part="snippet", videoId=vid).execute().get("items", []) if not dry else []
    for srt in sorted((ep / "build").glob(f"{ep.name}_*.srt")):
        lang = YT_LANG.get(srt.stem.split("_")[-1], srt.stem.split("_")[-1])
        print(f"captions {lang}: {srt.name}")
        if dry:
            continue
        for c in existing:  # replace our own track for this language, keep YouTube's auto captions
            if c["snippet"]["language"] == lang and c["snippet"].get("trackKind") != "asr":
                yt.captions().delete(id=c["id"]).execute()
        yt.captions().insert(part="snippet", body={"snippet": {"videoId": vid, "language": lang, "name": "", "isDraft": False}},
                             media_body=MediaFileUpload(str(srt), mimetype="application/octet-stream")).execute()


def localize(yt, ep: Path, vid: str, dry: bool):
    f = ep / "localize.json"
    if not f.exists():
        print("no localize.json, titles left as they are")
        return
    loc = json.loads(f.read_text(encoding="utf-8"))
    print("titles/descriptions:", ", ".join(loc))
    if dry:
        return
    v = yt.videos().list(part="snippet,localizations", id=vid).execute()["items"][0]
    sn = v["snippet"]
    sn["defaultLanguage"] = "en"
    sn["title"], sn["description"] = loc["en"]["title"], loc["en"]["description"]
    body = {"id": vid, "snippet": {k: sn[k] for k in ("title", "description", "categoryId", "defaultLanguage", "tags") if k in sn},
            "localizations": {YT_LANG.get(k, k): v for k, v in loc.items()}}
    yt.videos().update(part="snippet,localizations", body=body).execute()


def main(args):
    if args[:1] == ["auth"]:
        creds()
        print("ok:", SECRETS / "token.json")
        return
    ep, vid = (ROOT / args[0]).resolve(), args[1]
    dry = "--dry-run" in args
    yt = None if dry else youtube()
    captions(yt, ep, vid, dry)
    localize(yt, ep, vid, dry)


if __name__ == "__main__":
    main(sys.argv[1:])
