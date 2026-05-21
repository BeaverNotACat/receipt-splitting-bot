import asyncio
from pathlib import Path

from langchain_core.callbacks import UsageMetadataCallbackHandler
from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

from metrics.utils.f1 import f1, tp_fp_fn
from metrics.utils.levenstein import levenstein
from src.application.common.ocr import OpticalCharacterRecognizerI
from src.presentation.dependencies import container


@dataclass
class Metrics:
    cer: float
    price_f1: float
    mean_token_input: float
    mean_token_output: float


async def calculate_metrics(  # noqa: PLR0914
    image_folder_path: Path, references_path: Path
) -> Metrics:
    recognizer = await container.get(OpticalCharacterRecognizerI)

    total_levenstein = 0
    total_len = 0
    tp = fp = fn = 0
    input_tokens = 0
    output_tokens = 0

    image_paths = list(image_folder_path.iterdir())  # noqa: ASYNC240
    num_samples = len(image_paths)

    for image_path in image_paths:
        reference = references_path / f"{image_path.stem}.txt"

        with image_path.open("r+b") as request:
            metadata_callback = UsageMetadataCallbackHandler()
            recognized_image = await recognizer.call_langchain(
                image=request, callbacks=[metadata_callback]
            )

        with reference.open("r", encoding="utf-8") as reference_file:
            reference_text = reference_file.read()

        total_levenstein += levenstein(reference_text, recognized_image)
        total_len += len(reference_text)

        tpi, fpi, fni = tp_fp_fn(reference_text, recognized_image)
        tp += tpi
        fp += fpi
        fn += fni

        inner = next(iter(metadata_callback.usage_metadata.values()))
        input_tokens += inner["input_tokens"]
        output_tokens += inner["output_tokens"]

    return Metrics(
        cer=total_levenstein / max(total_len, 1),
        price_f1=f1(tp, fp, fn),
        mean_token_input=input_tokens / max(num_samples, 1),
        mean_token_output=output_tokens / max(num_samples, 1),
    )


BASE_DIR = Path(__file__).resolve().parents[1]
IMAGES = BASE_DIR / "data" / "ocr_metrics" / "images"
REFERENCES = BASE_DIR / "data" / "ocr_metrics" / "references"
OUTPUT_FILE = BASE_DIR / "data" / "ocr_metrics" / "metrics.json"


async def main() -> None:
    metrics = await calculate_metrics(IMAGES, REFERENCES)
    metrics_adapter = TypeAdapter(Metrics)
    with OUTPUT_FILE.open("w+b") as metrics_file:
        metrics_file.write(metrics_adapter.dump_json(metrics))


if __name__ == "__main__":
    asyncio.run(main())
