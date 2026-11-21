"""Pre-download the take scorers (run with .venv-score python): ECAPA speaker similarity + UTMOSv2 naturalness."""
from speechbrain.inference.speaker import EncoderClassifier
from speechbrain.utils.fetching import LocalStrategy
EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="tools/models/ecapa", local_strategy=LocalStrategy.COPY)
print("ecapa ok", flush=True)
import utmosv2
utmosv2.create_model(pretrained=True)
print("utmosv2 ok", flush=True)
