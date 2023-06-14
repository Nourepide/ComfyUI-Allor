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
2. `git clone https://github.com/Nourepide/ComfyUI-Allor.git comfyui_allor`
3. `cd comfyui_allor` 
4. `pip install -r requirements.txt`
5. You can also create `fonts` folder in `comfy_extras` or just start `ComfyUI` and folder will create automatically.

## Updating:
1. `cd custom_nodes/comfyui_allor` or `cd custom_nodes/{name of ComfyUI Allor folder}`
2. `git checkout main && git pull`

## Modules:
> Click on `Details` to open/close the drop-down menu with all modules.

<details>
  <summary>Details: 👈</summary>

### Alpha chanel
![alpha_chanel](images/image_alpha_chanel.png)
> Helpers for work with alpha chanel in exiting images.

<details>
  <summary>Nodes:</summary>

### Add
![image_alpha_chanel_add](images/image_alpha_chanel_add.png)
> Adds alpha chanel to images (Convert `RGB` to `RGBA`).

### Add By Mask
![image_alpha_chanel_by_mask](images/image_alpha_chanel_by_mask.png)
> Applies transparency to the images using a mask.

<details>
  <summary>Params:</summary>

* method -
  * default - Standard mask overlay.
  * invert - Inverted mask overlay.

</details>

### As Mask
![image_alpha_chanel_as_mask](images/image_alpha_chanel_as_mask.png)
> Get alpha chanel from first images and returns it as mask.

<details>
  <summary>Params:</summary>

* method -
  * default - Standard mask overlay.
  * invert - Inverted mask overlay.

</details>

### Restore
![image_alpha_chanel_restore](images/image_alpha_chanel_restore.png)
> Add alpha dimension to images. Or restore if it already exists. 

<details>
  <summary>Params:</summary>

* method -
  * default - Apply adding new alpha chanel or restore chanel values to max if it already exists.
  * only_add - Only add new alpha chanel if it does not exist.
  * only_restore - Only restore alpha chanel values to max if it already exists.

</details>

### Remove
![image_alpha_chanel_remove](images/image_alpha_chanel_remove.png)
> Completely removes alpha chanel from images (Convert `RGBA` to `RGB`).

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

### AbsoluteByContainer
> Use it for pixel-perfect images compositing. The size of the container is taken from the outside.

<details>
  <summary>Params:</summary>

* container - Image "donor". Its size will determine the size of the compositing space.
* images_[a, b]_x `[0 - *]` - Images horizontal position. `[left -> right]`.
* images_[a, b]_y `[0 - *]` - Images vertical position. `[top -> bottom]`.

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
* * sum_[width, height] - Sum of width or height from `images_a` and `images_b`.

How it works.

* Images in relative mode cannot go beyond the edges of the container.
* In horizontal [0.0 - images is located on the left of the container], [1.0 - on right of container].
* In vertical [0.0 - images is located on the top of the container], [1.0 - on bottom of container].
* In all cases, [0.5] means that the images will be in the center.

</details>

### RelativeByContainer
> Use it for percentage images compositing. The size of the container is taken from the outside.

<details>
  <summary>Params:</summary>

* container - Image "donor". Its size will determine the size of the compositing space. Can't be smaller then max size of with or height images_[a, b].
* images_[a, b]_x `[0.0 - 1.0]` - First images horizontal offset. `[left edge -> right edge]`.
* images_[a, b]_y `[0.0 - 1.0]` - First images vertical offset. `[top edge -> bottom edge]`.

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
> All nodes has `ByContainer` version.
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

</details>

---
### Image Effects
![image_effects](images/image_effects.png)
> Apply effects to images.

<details>
  <summary>Nodes:</summary>

### Adjustment
![image_effects_adjustment](images/image_effects_adjustment.png)
> Adjust your images with color correction.

<details>
  <summary>Params:</summary>

* brightness `[0.0 - *]` - Adjust brightness of images with scale.
* contrast `[0.0 - *]` - Adjust contrast of images with scale.
* saturation `[0.0 - *]` - Adjust color saturation of an images with scale.
* hue `[0.0 - 1.0]` - Adjust hue of images.
* gamma `[0.0 - *]` - Perform gamma correction on an images with scale.
* sharpness  `[0.0 - *]` - Adjust the sharpness of an images with scale.
* [red, green, blue] - Scale color factor.

</details>

### Grayscale
![image_effects_grayscale](images/image_effects_grayscale.png)
> Turn your images into monochrome.

### Sepia
![image_effects_sepia](images/image_effects_sepia.png)
> Add an antique effect to your images.

### Negative
![image_effects_negative](images/image_effects_negative.png)
> Add negative effect.

### Lens Chromatic Aberration
![image_effects_lens_chromatic_aberration](images/image_effects_lens_chromatic_aberration.png)
> Apply a camera lens color shift to the images.

`Attention`⚡: You can test all params of `Chromatic Aberration` with this  [JSON](images/image_effects_chromatic_aberration.json). The example works using `Image Draw` module and does not require any preparation. Changing the parameters leads to very unusual effects that you will not find anywhere else, so I recommend that you spend time on this and get acquainted as best as possible for incredible results.

<details>
  <summary>Params:</summary>

* shift `[0 - *]` - Color shift in PX.
* method `[reflect, edge, constant]` - Method for fill new empty space around image while effect applying. The new space does not fall into the final result and is only needed to avoid artifacts.
* shift_type `[1 - 4]` - Type of chromatic aberration.
* mixing_type `[1 - 4]` - Type of method for shifting colors.
* transpose `[none, rotate, reflect]` - Shifting direction, where `none` is without changes, `rotate` is in alternative direction and `reflect` in both directions at the same time.
* colors `[rb, rg, gb]`- The color layers that will be shifted. 
* lens_curvy `[0.0 - 15.0]` - The value of the curve during the propagation of the effect, where 1.0 is linear. Not work with shift_type 4.

<details>
  <summary>lens_curvy in details:</summary>

![lens_curvy](images/lens_curvy.png)
  
</details>

</details>

### Lens Optic Axis
![image_effects_lens_optic_axis](images/image_effects_lens_optic_axis.png)
> Apply a camera lens distort to the images.

<details>
  <summary>Params:</summary>

* lens_shape `[circle, square, rectangle, corners]` - Form of lens.

<details>
  <summary>lens_shape in details:</summary>

![lens_shape](images/lens_shape.png)
  
</details>

* lens_edge `[around, symmetric]` - If `around` is selected, the lens will adjust to the proportions of the image.
* lens_curvy `[0.0 - 15.0]` - The value of the curve during the propagation of the effect, where 1.0 is linear.

<details>
  <summary>lens_curvy in details:</summary>

![lens_curvy](images/lens_curvy.png)
  
</details>

* lens_zoom `[0 - *]` - How close lens are to the center of images.
* lens_aperture `[0 - *]` - How much lens will distort images.
* blur_intensity `[0.0 - *]` - Strength of blur due to lens.

</details>

### Lens Vignette
![image_effects_lens_vignette](images/image_effects_lens_vignette.png)
> Apply a camera lens decreasing in the brightness and saturation to the images.

<details>
  <summary>Params:</summary>

* lens_shape `[circle, rectangle]` - Form of lens.

<details>
  <summary>lens_shape in details:</summary>

![lens_shape](images/lens_shape.png)
  
</details>

* lens_edge `[around, symmetric]` - If `around` is selected, the lens will adjust to the proportions of the image.
* lens_curvy `[0.0 - 15.0]` - The value of the curve during the propagation of the effect, where 1.0 is linear.

<details>
  <summary>lens_curvy in details:</summary>

![lens_curvy](images/lens_curvy.png)
  
</details>

* lens_zoom `[0 - *]` - How close lens are to the center of images.
* brightness `[0.0 - *]` - Adjust brightness of images with scale.
* saturation `[0.0 - *]` - Adjust color saturation of an images with scale.

</details>

</details>

---
### Image Filter
![image_filter](images/image_filter.png)
> Apply filters to images.

<details>
  <summary>Nodes:</summary>

`Warning` Some changes are difficult to notice without detailed consideration.You can load this [JSON](images/image_filter.json) and look at the changes in detail.

### Smooth
![image_draw_polygon](images/image_filter_smooth.png)
> Anti-Aliasing of image artifacts.

### Smooth More
![image_filter_smooth_more](images/image_filter_smooth_more.png)
> Improved Anti-Aliasing of image artifacts.

### Blur
![image_filter_blur](images/image_filter_blur.png)
> Blurring the image.
 
<details>
  <summary>Params:</summary>

* size_[x, y] `[1 - *]` - The strength of the blur application for horizontal and vertical direction.

</details>

### Box Blur
![image_filter_box_blur](images/image_filter_box_blur.png)
> Blurring the image by box algorithm.

<details>
  <summary>Params:</summary>

* size_[x, y] `[1 - *]` - The strength of the blur application for horizontal and vertical direction.

</details>

### Gaussian Blur
![image_filter_gaussian_blur](images/image_filter_gaussian_blur.png)
> Blurring the image by gaussian algorithm.

<details>
  <summary>Params:</summary>

#### All
* size_[x, y] `[1 - *]` - The strength of the blur application for horizontal and vertical direction.

#### Advanced
* sigma_[x, y] `[1 - *]` - The scale of the blur deviation.

</details>

### Stack Blur
![image_filter_stack_blur](images/image_filter_stack_blur.png)
> Blurring the image by stack algorithm.

<details>
  <summary>Params:</summary>

* size_[x, y] `[1 - *]` - The strength of the blur application for horizontal and vertical direction.

</details>

### Median Blur
![image_filter_median_blur](images/image_filter_median_blur.png)
> Blurring the image by median algorithm.

<details>
  <summary>Params:</summary>

* size_[x, y] `[1 - *]` - The strength of the blur application for horizontal and vertical direction.

</details>

### Bilateral Blur
![image_filter_box_blur](images/image_filter_box_blur.png)
> Blurring the image by bilateral algorithm. Keeps the image sharp at the edges.

<details>
  <summary>Params:</summary>

* size_[x, y] `[1 - *]` - The strength of the blur application for horizontal and vertical direction.

</details>

### Contour
![image_filter_contour](images/image_filter_contour.png)
> Find the contours of the image.

### Detail
![image_filter_detail](images/image_filter_detail.png)
> Image detailing.

### Edge Enhance
![image_filter_edge_enhance](images/image_filter_edge_enhance.png)
> Clarity of the image boundaries.

### Edge Enhance More
![image_filter_edge_enhance_more](images/image_filter_edge_enhance_more.png)
> Improved clarity of image boundaries.

### Emboss
![image_filter_emboss](images/image_filter_emboss.png)
> Embossed image.

### Find Edges
![image_filter_find_edges](images/image_filter_find_edges.png)
> Identifies the boundaries of the image.

### Sharpen
![image_filter_sharpen](images/image_filter_sharpen.png)
> Sharpness improvement.

### Rank
![image_filter_rank](images/image_filter_rank.png)
> Rank filter sorts all pixels in a window of a given size.

<details>
  <summary>Params:</summary>

* size `[0 - *]` - The size of the core in PX.
* rank `[0 - *]` - Which pixel value to choose.

</details>

### Min
![image_filter_min](images/image_filter_min.png)
> Selects the smallest pixel value in the window at the specified size.

<details>
  <summary>Params:</summary>

* size `[0 - *]` - The size of the core in PX.

</details>

### Max
![image_filter_max](images/image_filter_max.png)
> Selects the largest pixel value in the window at the specified size.

<details>
  <summary>Params:</summary>

* size `[0 - *]` - The size of the core in PX.

</details>

### Mode
![image_filter_mode](images/image_filter_mode.png)
> Selects the most common pixel value in a field of the specified size.

<details>
  <summary>Params:</summary>

* size `[0 - *]` - The size of the core in PX.

</details>

</details>

---
### Image Transform
![image_transform](images/image_transform.png)
> Transform your images.

<details>
  <summary>Nodes:</summary>

### Resize
![image_transform_resize](images/image_transform_resize.png)
> Change size of images.

<details>
  <summary>Params:</summary>

#### Absolute
* [width, height] `[1 - *]` - New size of images.

#### Relative
* scale_[width, height] `[0.0 - 1.0]` - New size of images.

</details>

### Crop
![image_transform_crop](images/image_transform_crop.png)
> Returns area from images.

<details>
  <summary>Params:</summary>

#### Absolute
* start_[x, y] `[1 - *]` - Start of rectangle point.
* end_[x, y] `[1 - *]` - End of rectangle point.

#### Relative
* start_[x, y] `[0.0 - 1.0]` - Start of rectangle point.
* end_[x, y] `[0.0 - 1.0]` - End of rectangle point.

</details>

### Crop Corners
![image_transform_crop_corners](images/image_transform_crop_corners.png)
> Round corners of your images.

<details>
  <summary>Params:</summary>

* radius `[0 -360]` - Radius of the corners.
* [top_left, top_right, bottom_right, bottom_left]_corner `[boolean]` - The ability to choose for which angle to apply the radius.
* SSAO [1 - 16] - [Super Sampling Anti-Aliasing](https://en.wikipedia.org/wiki/Supersampling). The figure is drawn initially at a higher resolution, and then compressed to the specified resolution.

</details>

### Padding
![image_transform_padding](images/image_transform_padding.png)
> Expand your images.

### Rotate
![image_transform_rotate](images/image_transform_rotate.png)
> Rotate your images.

<details>
  <summary>Params:</summary>

* angle `[0 -360]` - Angle in degrees. Angles are measured from 3 o’clock, increasing clockwise.
* expand `[boolean]` - If "true" when rotating, change the size of the image to fit into it.
* SSAO [1 - 16] - [Super Sampling Anti-Aliasing](https://en.wikipedia.org/wiki/Supersampling). The figure is drawn initially at a higher resolution, and then compressed to the specified resolution.

</details>

### Transpose
![image_transform_transpose](images/image_transform_transpose.png)
> Transpose your images.

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
* fonts_folder_path - Array with a relative path to fonts folder, by default is `["comfy_extras", "fonts"]`. (Converted to `ComfyUI/comfy_extras/fonts` for Unix and `ComfyUI\comfy_extras\fonts` for Windows).
* modules - You can disable (or enable) modules at will. Nodes from disabled modules will not be loaded during the start of ComfyUI.
* override - If the nested value is set to `true`, similar functionality from the original nodes is disabled.
* * postprocessing - Disable `image/postprocessing` nodes. (See `ImageFilter` module)
* * transform - Disable `ImageScale` and `ImageInvert` nodes. (See `ImageTransform` module)

## Examples:
![example](images/example.png)
> Ready to create your own masterpiece?

<details>
  <summary>Just see how easy it is to do:</summary>

`Warning` Google Collab can't reproduce those examples.

|            Image            |             Nodes              |
|:---------------------------:|:------------------------------:|
| ![1](images/examples/1.png) | [JSON](images/examples/1.json) |
| ![2](images/examples/2.png) | [JSON](images/examples/2.json) |

</details>
