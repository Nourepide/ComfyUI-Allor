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
* Allor is a plugin for ComfyUI with an emphasis on transparency and performance.
* All modules support transparency, multi-image and are easy to use.
* One of the main features is the ability to combine several images of different sizes.
* Almost all functionality is implemented in tensor space without transformation into an image, where possible. This allows you to achieve an incredible speed of work, in some places the speed increases from 1-2 seconds to 4-6 milliseconds.

## Installation:
1. `cd custom_nodes`
2. `git clone https://github.com/Nourepide/comfyui_allor.git comfyui_allor`
3. `cd comfyui_allor` 
4. `pip install -r requirements.txt`
5. You can also create `fonts` folder in `comfy_extras` or just start `ComfyUI` and folder will create automatically.

## Updating:
1. `cd custom_nodes/comfyui_allor` or `cd custom_nodes/{name of ComfyUI Allor folder}`
2. `git checkout main && git pull`

## Modules:
<details>
  <summary>Details:</summary>

### Alpha chanel
![alpha_chanel](images/alpha_chanel.png)
> Helpers for work with alpha chanel in exiting images.

<details>
  <summary>Nodes:</summary>

### By Mask
![alpha_chanel_by_mask](images/alpha_chanel_by_mask.png)
> Applies transparency to the image using a mask.

<details>
  <summary>Params:</summary>

* method -
  * default - Standard mask overlay.
  * invert - Inverted mask overlay.

</details>

### As Mask
![alpha_chanel_as_mask](images/alpha_chanel_as_mask.png)
> Get alpha chanel from first image and returns it as mask.

<details>
  <summary>Params:</summary>

* method -
  * default - Standard mask overlay.
  * invert - Inverted mask overlay.

</details>

### Restore
![alpha_chanel_restore](images/alpha_chanel_restore.png)
> Add alpha dimension to images. Or restore if it already exists. 

<details>
  <summary>Params:</summary>

* method -
  * default - Apply adding new alpha chanel or restore chanel values to max if it already exists.
  * only_add - Only add new alpha chanel if it does not exist.
  * only_restore - Only restore alpha chanel values to max if it already exists.

</details>

</details>

---
### Image Container
![image_container](images/image_container.png)
> Creating blank images of fixed or inherited size.

<details>
  <summary>Nodes:</summary>

#### All
* [red, green, blue] `[0 - 255]` - Color of the container in RGB. 
* alpha `[0.0 - 1.0]` - Transparency of the container.

### Default
> Create an empty container.

<details>
  <summary>Params:</summary>

* [width, height] `[1 - *]` - Size of a new container.

</details>

### Inheritance Add
> Get images size and create a container with adding value to this size.

<details>
  <summary>Params:</summary>

* add_[width, height] `[0 - *]` - The value that will then be added to the size of the container.

</details>

### Inheritance Scale
> Get images size and create a container with scaling this size.

<details>
  <summary>Params:</summary>

* scale_[width, height] `[0.0 - *]` - Scale factor that will then be change the size of the container.

</details>

### Inheritance Max
> Get max width and max height from `images_a` and `images_b` and create a new container with this size.
 
### Inheritance Sum
> Get width and/or height from `images_a` and `images_b` and create a new container with a sum this size.

</details>

#### PS:
The first letter `i` in the word `Inheritance` is barely noticeable. But in the end, I decided to leave it as it is. At first, I thought to replace this word with the word `Extended`, but one would think that this node expands the incoming images by adding size to it, and does not create a new image inheriting size from the incoming images.

---
### Image Composite
![image_composite](images/image_composite.png)
> Allows you to place one image on top of another.

<details>
  <summary>Nodes:</summary>

#### All
* background - The placement order of images in the container.
* method - The method of connecting images makes sense only when 2 or more images are passed to the input.

<details>
  <summary>Methods:</summary>

    Inputs - [a1, a2, a3] and [b1, b2, b3].
    Outputs -
        pair: [a1, b1], [a2, b2], [a3, b3]
        matrix: [a1, b1], [a1, b2], [a1, b3]
                [a2, b1], [a2, b2], [a2, b3]
                [a3, b1], [a3, b2], [a3, b3]

![image_composite_methods](images/image_composite_methods.png)

</details>

### Absolute
> Use it for pixel-perfect images compositing.

<details>
  <summary>Params:</summary>

* images_[a, b]_x `[0 - *]` - Images horizontal position. `[left -> right]`.
* images_[a, b]_y `[0 - *]` - Images vertical position. `[top -> bottom]`.
* container_[width, height] `[0 - *]` - Container size. If 0, then the container will be with the maximum width and height of the images.
</details>

### Relative
> Use it for percentage images compositing.

<details>
  <summary>Params:</summary>

* images_[a, b]_x `[0.0 - 1.0]` - First images horizontal offset. `[left edge -> right edge]`.
* images_[a, b]_y `[0.0 - 1.0]` - First images vertical offset. `[top edge -> bottom edge]`.
* container_size_type
* * max - Maximum of width and height from `images_a` and `images_b`.
* * sum - Sum of width and height from `images_a` and `images_b`.
* * sum_[width, height] -

How it works.

* Images in relative mode cannot go beyond the edges of the container.
* In horizontal [0.0 - images is located on the left of the container], [1.0 - on right of container].
* In vertical [0.0 - images is located on the top of the container], [1.0 - on bottom of container].
* In all cases, [0.5] means that the images will be in the center.

</details>

</details>

---
### Image Segmentation
![image_segmentation](images/image_segmentation.png)
> Removes background from image.

<details>
  <summary>Nodes:</summary>

#### All
* alpha_matting `[boolean]` - Alpha matting is a post-processing step that can be used to improve the quality of the output.
* alpha_matting_foreground_threshold `[0 - 250]` - Trimap foreground threshold.
* alpha_matting_background_threshold `[0 - 250]` - Trimap background threshold.
* alpha_matting_erode_size `[0 - *]` - How far will the transparency spread from the original mask.
* post_process_mask `[boolean]` - Post-processing mask, makes it rougher.

### Default
> Allows you to select a model with pre-specified settings.:

<details>
  <summary>Params:</summary>

* u2net - [GitHub](https://github.com/xuebinqin/U-2-Net)
* u2netp - [GitHub](https://github.com/xuebinqin/U-2-Net)
* u2net_human_seg - [GitHub](https://github.com/xuebinqin/U-2-Net)
* u2net_cloth_seg - [GitHub](https://github.com/levindabhi/cloth-segmentation)
* silueta - [GitHub](https://github.com/xuebinqin/U-2-Net/issues/295)
* isnet-general-use - [GitHub](https://github.com/xuebinqin/DIS)
* isnetis - [GitHub](https://github.com/SkyTNT/anime-segmentation) (I recommend `alpha_matting` parameter set to `false`)
* modnet-p - [GitHub](https://github.com/ZHKKKe/MODNet) (Not calibrated)
* modnet-w - [GitHub](https://github.com/ZHKKKe/MODNet) (Not calibrated)

</details>

### Custom
> Allows you to select a model from the onnx folder and specify the parameters yourself.

<details>
  <summary>Params:</summary>

* model `[*.onnx]` - Your model in `ComfyUI/models/onnx` folder.
* mean `[0.0 - 1.0]` - Clarifying value.
* std `[0.0 - 1.0]` - The divisor of the final value. I recommend leaving it at 1.0.
* size `[0 - *]` - Title size. Different models support different sizes. Or their multiple values [512 -> 1024 -> 2048...]. If the size does not match the desired one, you will see a notification in the console.

</details>

### Custom Advanced
> Allows you to select a model from the onnx folder and `finely` specify the parameters yourself.

<details>
  <summary>Params:</summary>

* model `[*.onnx]` - Your model in `ComfyUI/models/onnx` folder.
* mean_r `[0.0 - 1.0]` - Clarifying value. Red chanel.
* mean_g `[0.0 - 1.0]` - Clarifying value. Green chanel.
* mean_b `[0.0 - 1.0]` - Clarifying value. Blue chanel.
* std_r `[0.0 - 1.0]` - The divisor of the final value. Red chanel.
* std_g `[0.0 - 1.0]` - The divisor of the final value. Green chanel.
* std_b `[0.0 - 1.0]` - The divisor of the final value. Blue chanel.
* width `[0 - *]` - Width of title size.
* height `[0 - *]` - Height of title size.

Some models support non-standard title size. For example [w:1024 - h:2048].

</details>

</details>

#### PS:
Made on [rembg](https://github.com/danielgatis/rembg). The solution of some problems may be dependent on the rembg developer.

---
### ImageText
![image_text](images/image_text.png)
> Creating text as image.

Fonts should be contained in `ComfyUI/comfy_extras/fonts`.

You also can change the fonts folder in config.

<details>
  <summary>Nodes:</summary>

### Default
![image_text_default](images/image_text_default.png)
> Create an image with text.

<details>
  <summary>Params:</summary>

* text - Your input. Shouldn't be empty.
* font `[*.otf, *.ttf]` - Font from `ComfyUI/comfy_extras/fonts` folder.
* size `[1 - *]` - Font size in `SP`. `Warning!`: It's not `PX` size of the container. The size of the container is calculated using a variety of parameters. Example: `o` and `j` will have different height and exactly different size compared to `树`.   
* [red, green, blue] `[0 - 255]` - Color of the text in `RGB`. 
* alpha `[0.0 - 1.0]` - Transparency of the text. 
* margin_x `[0 - *]` - Horizontal offset. 
* margin_y `[0 - *]` - Vertical offset.

</details>

### Outlined
![image_text_outlined](images/image_text_outlined.png)
> Create an image with outlined text.

<details>
  <summary>Params:</summary>

* outline_size `[0 - *]` - Outline size in `PX`. 
* outline_[red, green, blue] `[0 - 255]` - Color of the outline in `RGB`. 

</details>

</details>

---
### ImageDraw
![image_draw](images/image_draw.png)
> Draw figures as image.

<details>
  <summary>Nodes:</summary>

#### All
* SSAO [1 - 16] - [Super Sampling Anti-Aliasing](https://en.wikipedia.org/wiki/Supersampling). The figure is drawn initially at a higher resolution, and then compressed to the specified resolution.

<details>
  <summary>The difference of SSAA strength:</summary>

> From left to right, x1, x2, x4, x8, x16. Image container size 256x256px.

![SSAA](images/ssaa.png)

</details>

### Arc
![image_draw_arc](images/image_draw_arc.png)
> Draws an arc (a portion of a circle outline) between the start and end angles, inside the given bounding box.

<details>
  <summary>Params:</summary>

* [width, height] `[1 - *]` - Size of image container.
* size `[1 - *]` - contour width.
* start_[x, y] `[0.0 - 1.0]` - Start points to define the bounding box in percent of image container. 
* end_[x, y] `[0.0 - 1.0]` - End points to define the bounding box in percent of image container.
* [start, end] `[0 - 360]` - Starting and ending angle, in degrees. Angles are measured from 3 o’clock, increasing clockwise.
* [red, green, blue] `[0 - 255]` - Color of the figure in RGB. 
* alpha `[0.0 - 1.0]` - Transparency of the figure.

</details>

### Chord
![image_draw_chord](images/image_draw_chord.png)
> Same as Arc, but connects the end points with a straight line.

<details>
  <summary>Params:</summary>

* [width, height] `[1 - *]` - Size of image container.
* size `[1 - *]` - contour width.
* start_[x, y] `[0.0 - 1.0]` - Start points to define the bounding box in percent of image container. 
* end_[x, y] `[0.0 - 1.0]` - End points to define the bounding box in percent of image container.
* [start, end] `[0 - 360]` - Starting and ending angle, in degrees. Angles are measured from 3 o’clock, increasing clockwise.
* [red, green, blue] `[0 - 255]` - Color of the figure in RGB. 
* alpha `[0.0 - 1.0]` - Transparency of the figure.

</details>

### Ellipse
![image_draw_ellipse](images/image_draw_ellipse.png)
> Draws an ellipse inside the given bounding box.

<details>
  <summary>Params:</summary>

* [width, height] `[1 - *]` - Size of image container.
* start_[x, y] `[0.0 - 1.0]` - Start points to define the bounding box in percent of image container. 
* end_[x, y] `[0.0 - 1.0]` - End points to define the bounding box in percent of image container.
* outline_size `[0 - *]` - Outline size in PX.
* outline_[red, green, blue] `[0 - 255]` - Color of the outline in RGB. 
* outline_alpha `[0.0 - 1.0]` - Transparency of the outline.
* fill_[red, green, blue] `[0 - 255]` - Color of the fill in RGB. 
* fill_alpha `[0.0 - 1.0]` - Transparency of the fill.

</details>

### Line
![image_draw_line](images/image_draw_line.png)
> Draws a line between the coordinates.

<details>
  <summary>Params:</summary>

* [width, height] `[1 - *]` - Size of image container.
* size `[1 - *]` - contour width.
* start_[x, y] `[0.0 - 1.0]` - Starting point of line. 
* end_[x, y] `[0.0 - 1.0]` - Ending point of line.
* [red, green, blue] `[0 - 255]` - Color of the line in RGB. 
* alpha `[0.0 - 1.0]` - Transparency of the line.

</details>

### Pieslice
![image_draw_pieslice](images/image_draw_pieslice.png)
> Same as Arc, but also draws straight lines between the end points and the center of the bounding box.

<details>
  <summary>Params:</summary>

* [width, height] `[1 - *]` - Size of image container.
* start_[x, y] `[0.0 - 1.0]` - Start points to define the bounding box in percent of image container. 
* end_[x, y] `[0.0 - 1.0]` - End points to define the bounding box in percent of image container.
* [start, end] `[0 - 360]` - Starting and ending angle, in degrees. Angles are measured from 3 o’clock, increasing clockwise.
* outline_size `[0 - *]` - Outline size in PX.
* outline_[red, green, blue] `[0 - 255]` - Color of the outline in RGB. 
* outline_alpha `[0.0 - 1.0]` - Transparency of the outline.
* fill_[red, green, blue] `[0 - 255]` - Color of the fill in RGB. 
* fill_alpha `[0.0 - 1.0]` - Transparency of the fill.

</details>

### Polygon
![image_draw_polygon](images/image_draw_polygon.png)
> Draws a polygon.

<details>
  <summary>Params:</summary>

* size `[1 - *]` - Size of image.
* sides `[3 - *]` - Sides of polygon.
* rotation `[0 - 360]` - Apply an arbitrary rotation to the polygon in degree. 
* outline_size `[0 - *]` - Outline size in PX.
* outline_[red, green, blue] `[0 - 255]` - Color of the outline in RGB. 
* outline_alpha `[0.0 - 1.0]` - Transparency of the outline.
* fill_[red, green, blue] `[0 - 255]` - Color of the fill in RGB. 
* fill_alpha `[0.0 - 1.0]` - Transparency of the fill.

</details>

### Rectangle
![image_draw_rectangle](images/image_draw_rectangle.png)
> Draws a rectangle.

<details>
  <summary>Params:</summary>

* [width, height] `[1 - *]` - Size of image container.
* start_[x, y] `[0.0 - 1.0]` - Start points to define the bounding box in percent of image container. 
* end_[x, y] `[0.0 - 1.0]` - End points to define the bounding box in percent of image container.
* outline_size `[0 - *]` - Outline size in PX.
* outline_[red, green, blue] `[0 - 255]` - Color of the outline in RGB. 
* outline_alpha `[0.0 - 1.0]` - Transparency of the outline.
* fill_[red, green, blue] `[0 - 255]` - Color of the fill in RGB. 
* fill_alpha `[0.0 - 1.0]` - Transparency of the fill.

</details>

### Rectangle Rounded
![image_draw_rectangle_rounded](images/image_draw_rectangle_rounded.png)
> Draws a rounded rectangle.

<details>
  <summary>Params:</summary>

* [width, height] `[1 - *]` - Size of image container.
* start_[x, y] `[0.0 - 1.0]` - Start points to define the bounding box in percent of image container. 
* end_[x, y] `[0.0 - 1.0]` - End points to define the bounding box in percent of image container.
* radius `[0 -360]` - Radius of the corners.
* outline_size `[0 - *]` - Outline size in PX.
* outline_[red, green, blue] `[0 - 255]` - Color of the outline in RGB. 
* outline_alpha `[0.0 - 1.0]` - Transparency of the outline.
* fill_[red, green, blue] `[0 - 255]` - Color of the fill in RGB. 
* fill_alpha `[0.0 - 1.0]` - Transparency of the fill.
* [top_left, top_right, bottom_right, bottom_left]_corner `[boolean]` - The ability to choose for which angle to apply the radius.

</details>

</details>

---
### Clamp
![clamp](images/clamp.png)
> Clamps help to control the "web" of nodes and improve readability.

<details>
  <summary>Nodes:</summary>

* ClipClamp
* ClipVisionClamp
* ClipVisionOutputClamp
* ConditioningClamp
* ControlNetClamp
* GligenClamp
* ImageClamp
* LatentClamp
* MaskClamp
* ModelClamp
* StyleModelClamp
* UpscaleModelClamp
* VaeClamp

</details>

</details>

## Configuration:
You can configurate Allor with `config.json`.
* `fonts_folder_path` - Array with a relative path to fonts folder, by default is `["comfy_extras", "fonts"]`. (Converted to `ComfyUI/comfy_extras/fonts` for Unix and `ComfyUI\comfy_extras\fonts` for Windows).
* `modules` - You can disable (or enable) modules at will. Nodes from disabled modules will not be loaded during the start of ComfyUI.
