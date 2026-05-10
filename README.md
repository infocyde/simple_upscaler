# simple_upscaler

A small Streamlit web app that upscales images using AI super-resolution (EDSR). Quality is pretty decent — not state of the art, but easy to run locally. The first run will take a while as the model weights are downloaded.

## Features

- Drag-and-drop upload for PNG / JPG / JPEG
- 2× or 4× upscale factor
- Optional "keep same output size" toggle that resizes the upscaled result back to the original dimensions (useful for cleaning up an image without changing its size)
- Originals are saved to `input/`, results are saved to `output/`
- Download button for the upscaled PNG

## Model

Uses [`eugenesiow/edsr-base`](https://huggingface.co/eugenesiow/edsr-base) via the [`super-image`](https://pypi.org/project/super-image/) library. Weights are pulled from Hugging Face on first run and cached locally.

## Requirements

- Python 3.9+
- A GPU is not required, but larger images / higher scale factors will be slow on CPU.

Install dependencies:

```bash
pip install -r requirements.txt
```

> On Windows with an NVIDIA GPU, you may want to install `torch` / `torchvision` separately from the [PyTorch index](https://pytorch.org/get-started/locally/) to get a CUDA-enabled build before running the command above.

## Run

From the project root:

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (typically <http://localhost:8501>).

## How it works

1. Upload an image — it's written to `input/<original_name>`.
2. Pick a scale factor (2 or 4) in the sidebar.
3. Click **Upscale Image**. The EDSR model runs, the tensor is converted back to a PIL image, and the result is saved to `output/upscaled_x<scale>_<original_name>`.
4. Optionally tick **Keep same output size** to LANCZOS-resize the upscaled image back to the original dimensions.
5. Download the result via the in-app button.
