![logo](images/logo.png)

<details>
  <summary>This image from start to end was done in ComfyUI. How?</summary>

1. Install plugin.
2. Load fonts [Overlock SC](https://fonts.google.com/specimen/Overlock+SC) and [Merienda](https://fonts.google.com/specimen/Merienda).
3. Put `OverlockSC-Regular.ttf` and `Merienda-Regular.ttf` in to `fonts` folder.
4. Load [RealESRNet_x4plus.pth](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth) and put in to `models/upscale` folder.
5. Load [AOM3A1B_orangemixs.safetensors](https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/Models/AbyssOrangeMix3/AOM3A1B_orangemixs.safetensors) and put in to `models/chekpoints` folder.
6. Load [orangemix.vae.pt](https://huggingface.co/WarriorMama777/OrangeMixs/resolve/main/VAEs/orangemix.vae.pt) and put in to `models/vae` folder.
7. Drag-and-drop this [image](images/logo.png) to ComfyUI or load [JSON](images/logo.json).
8. Press the `Queue Promt` button.

</details>

## About Allor:
* Allor is a high-performance ComfyUI plugin designed for image processing.
* It comprises more than 90 nodes, each with numerous parameters for your needs.
* It supports transparency and multi-image processing across all modules and nodes.
* Allor is fully configurable, offering the option to disable any functionality that is not required.
* The majority of its operations are implemented in tensor space to avoid unnecessary data transformations.

## Documentation

We are pleased to present to you our [new documentation](https://nourepide.github.io/ComfyUI-Allor-Doc/).

The [documentation](https://nourepide.github.io/ComfyUI-Allor-Doc/) includes information about **installation**, **updating**, all **nodes** including their parameters and much more.

## Contributing:
ComfyUI Allor is an open source project and I welcome any contributions from the community.

* **Suggest ideas**: If you have thoughts on improving this plugin, feel free to share them on GitHub.

* **Report bugs**: If you find a bug or problem, please report it in the Issue with steps to reproduce it.

* **Make pull requests**: If you’d like to help with the plugin’s code, you can copy this repository, make your changes, and I’ll check and include them if they work well with the plugin.

## Jupiter Notebook:

To run Allor on another cloud service, you can use this [Jupiter Notebook](notebooks/ComfyUI_Allor.ipynb).

If you have a subscription to [Colab Pro](https://colab.research.google.com/signup), then you can run Allor in [Google Colab](https://colab.research.google.com/drive/1qOALtMEG_f6DN0o9mxUih6x_7PTPYM8X?usp=sharing).
