# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_repr_rgb.ipynb.

# %% auto 0
__all__ = ['rgb']

# %% ../nbs/01_repr_rgb.ipynb 4
from typing import Union 
import numpy as np
from PIL import Image
import lovely_numpy as lnp

from .utils.tile2d import hypertile

# %% ../nbs/01_repr_rgb.ipynb 5
# This is here for the monkey-patched tensor use case.

# I want to be able to call both `tensor.rgb` and `tensor.rgb(stats)`. For the
# first case, the class defines `_repr_png_` to send the image to Jupyter. For
# the later case, it defines __call__, which accps the argument.

class RGBProxy():
    """Flexible `PIL.Image.Image` wrapper"""
    
    def __init__(self, t:np.ndarray):
        super().__init__()
        # assert t.ndim == 3, f"Expecting a 3-dim array, got {t.shape}={t.ndim}"
        self.t = t

    
    def __call__(self, denorm=None, cl: Union[int, bool]=True, 
                    gutter_px=3, frame_px=1, view_width=966):
        t = self.t

        # swap channels if it's not channe-last already
        if not cl:
            # Is there any easy way to .permute() without knowing the number of dims?
            t = np.swapaxes(np.swapaxes(t, -3, -1), -3, -2)
            
        n_ch = t.shape[-1]
        assert n_ch in (3, 4), f"Expecting 3 (RGB) or 4 (RGBA) channels, got {n_ch}" 
        if denorm:
            means = np.array(denorm[0])
            stds = np.array(denorm[1])
            t = t * stds + means

        if t.ndim > 3:
            t = hypertile(  t=t,
                            gutter_px=gutter_px,
                            frame_px=frame_px,
                            view_width=view_width)

        return Image.fromarray((t * 255).astype(np.uint8))
    
    def _repr_png_(self):
        return self.__call__()._repr_png_()


# %% ../nbs/01_repr_rgb.ipynb 6
def rgb(t: np.ndarray, # Tensor to display. [[...], C,H,W] or [[...], H,W,C]
            denorm=None, # Reverse per-channel normalizatoin
            cl: Union[int, bool]=True,    # Channel-last
            gutter_px = 3,  # If more than one tensor -> tile with this gutter width
            frame_px=1,  # If more than one tensor -> tile with this frame width
            view_width=966): # targer width of the image
    return RGBProxy(t)( denorm=denorm, cl=cl,
                        gutter_px=gutter_px,
                        frame_px=frame_px,
                        view_width=view_width)
