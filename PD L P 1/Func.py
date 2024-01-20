 

from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw

def open_and_resize_image(file_path):
    image = Image.open(file_path)
    width, height = int(image.width * 2), int(image.height * 2)
    return image.resize((width, height), Image.ANTIALIAS if hasattr(Image, 'ANTIALIAS') else Image.BICUBIC)

def apply_selected_filter(image, selected_filter):
    if selected_filter == "Black and White":
        return ImageOps.grayscale(image)
    elif selected_filter == "Blur":
        return image.filter(ImageFilter.BLUR)
    elif selected_filter == "Sharpen":
        return image.filter(ImageFilter.SHARPEN)
    elif selected_filter == "Smooth":
        return image.filter(ImageFilter.SMOOTH)
    elif selected_filter == "Emboss":
        return image.filter(ImageFilter.EMBOSS)
    else:
        return image

def rotate_image(image, angle):
    return image.rotate(angle)

def flip_image(image, direction):
    if direction == "Vertical":
        return ImageOps.flip(image)
    elif direction == "Horizontal":
        return ImageOps.mirror(image)
    else:
        return image

def crop_image(image, x1, y1, x2, y2):
    return image.crop((x1, y1, x2, y2))

def draw_on_image(image, x1, y1, x2, y2, color, size):
    draw = ImageDraw.Draw(image)
    draw.ellipse([x1, y1, x2, y2], fill=color, outline=color)
     

def save_image(image, file_path):
    if file_path:
        try:
            image.save(file_path)
        except ValueError as e:
            # Handle cases where the file extension is unknown
            if "unknown file extension" in str(e):
                # Provide a default extension like ".png"
                default_save_path = file_path + ".png"
                image.save(default_save_path)
                return default_save_path
            else:
                # If it's another ValueError, raise it
                raise

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

