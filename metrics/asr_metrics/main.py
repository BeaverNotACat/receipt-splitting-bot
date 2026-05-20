import asyncio
from pathlib import Path

from langchain_core.callbacks import UsageMetadataCallbackHandler
from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

from metrics.utils.levenstein import levenstein
from src.application.common.asr import SpeechRecognizerI
from src.presentation.dependencies import container


@dataclass
class Metrics:
    cer: float
    mean_token_input: float
    mean_token_output: float


async def calculate_metrics(
    audio_folder_path: Path, recognized_audio_path: Path
) -> Metrics:
    recognizer = await container.get(SpeechRecognizerI)

    total_levenstein = 0
    total_len = 0
    input_tokens = 0
    output_tokens = 0

    audio_paths = list(audio_folder_path.iterdir())  # noqa: ASYNC240
    num_samples = len(audio_paths)

    for audio_path in audio_paths:
        reference = recognized_audio_path / f"{audio_path.stem}.txt"

        with audio_path.open("r+b") as request:
            metadata_callback = UsageMetadataCallbackHandler()
            recognized_audio = await recognizer.call_langchain(
                audio=request, callbacks=[metadata_callback]
            )

        with reference.open("r", encoding="utf-8") as reference_file:
            reference_text = reference_file.read()

        total_levenstein += levenstein(recognized_audio, reference_text)
        total_len += len(reference_text)

        inner = next(iter(metadata_callback.usage_metadata.values()))
        input_tokens += inner["input_tokens"]
        output_tokens += inner["output_tokens"]

    return Metrics(
        cer=total_levenstein / max(total_len, 1),
        mean_token_input=input_tokens / max(num_samples, 1),
        mean_token_output=output_tokens / max(num_samples, 1),
    )


BASE_DIR = Path(__file__).resolve().parents[1]
AUDIOS = BASE_DIR / "data" / "asr_metrics" / "audios"
REFERENCES = BASE_DIR / "data" / "asr_metrics" / "references"
OUTPUT_FILE = BASE_DIR / "data" / "asr_metrics" / "metrics.json"


async def main() -> None:
    metrics = await calculate_metrics(AUDIOS, REFERENCES)
    metrics_adapter = TypeAdapter(Metrics)
    with OUTPUT_FILE.open("w+b") as metrics_file:
        metrics_file.write(metrics_adapter.dump_json(metrics))


if __name__ == "__main__":
    asyncio.run(main())
