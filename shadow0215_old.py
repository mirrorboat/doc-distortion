from augraphy import *
import cv2

image = cv2.imread("/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/20250114_testset/GT/ZH/eastmoney_d2bb183f5254ede5760932ac3118524aa7eddad551935713b435541f1525c1ee.pdf_7.jpg")

ink_color_range = (0, 0)
ink_phase = []
paper_phase = []
post_phase = [
    LightingGradient(
        light_position=None,
        direction=None,
        max_brightness=255,
        min_brightness=0,
        mode="gaussian",
        linear_decay_rate=None,
        transparency=None,
    ),
    ShadowCast(
        shadow_vertices_range=(5,10),
        shadow_opacity_range = (0.8, 0.8),
        shadow_width_range=(0.8, 1.0),
        shadow_height_range=(0.8, 1.0),
        p=1,
    ),
]
pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase, ink_color_range=ink_color_range)

augmented_image = pipeline(image)
cv2.imwrite("/mnt/petrelfs/chenjingzhou/cjz/doc-distortion/image1_shadow.jpg", augmented_image)