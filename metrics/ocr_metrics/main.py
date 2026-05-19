import asyncio
from pathlib import Path

from langchain_core.callbacks import UsageMetadataCallbackHandler
from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

from metrics.utils.levenstein import levenstein
from src.adapters.ocr import OpticalCharacterRecognizerI
from src.presentation.dependencies import container


@dataclass
class Metrics:
    mean_levenstein: float
    mean_token_input: float
    mean_token_output: float


async def calculate_metrics(
    image_folder_path: Path, recognized_image_path: Path
) -> Metrics:
    recognizer = await container.get(OpticalCharacterRecognizerI)
    metadata_callback = UsageMetadataCallbackHandler()

    levenstein_summ = 0
    input_tokens = 0
    output_tokens = 0

    for image in image_folder_path.iterdir():  # noqa: ASYNC240
        reference = recognized_image_path / f"{image.stem}.txt"
        with image.open("b+r") as request:
            recognized_image = await recognizer.call_langchain(
                image=request, callbacks=[metadata_callback]
            )

        with reference.open("r", encoding="utf-8") as text:
            levenstein_distance = levenstein(recognized_image, text.read())
        levenstein_summ += levenstein_distance
        inner = next(iter(metadata_callback.usage_metadata.values()))
        input_tokens += inner["input_tokens"]
        output_tokens += inner["output_tokens"]
    num_samples = len(list(image_folder_path.iterdir()))  # noqa: ASYNC240

    return Metrics(
        mean_levenstein=levenstein_summ / max(num_samples, 1),
        mean_token_input=input_tokens / max(num_samples, 1),
        mean_token_output=output_tokens / max(num_samples, 1),
    )


async def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]  # noqa: ASYNC240
    images = base_dir / "data" / "ocr_metrics" / "images"
    references = base_dir / "data" / "ocr_metrics" / "references"
    output_file = base_dir / "data" / "ocr_metrics" / "metrics.json"

    metrics = await calculate_metrics(images, references)
    metrics_adapter = TypeAdapter(Metrics)
    with output_file.open("w+b") as metrics_file:
        metrics_file.write(metrics_adapter.dump_json(metrics))


if __name__ == "__main__":
    asyncio.run(main())
