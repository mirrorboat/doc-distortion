import random
from augraphy import *
import cv2


ink_phase = [
    InkBleed(
        intensity_range=(0.5, 0.6),
        kernel_size=random.choice([(5, 5), (3, 3)]),
        severity=(0.3, 0.8),
        p=0.5,
    ),
    OneOf(
        [    
            InkShifter(),
            InkMottling(),
        ],
        p=1.0,
    ),
    OneOf(
        [
            BleedThrough(
                intensity_range=(0.1, 0.9),
                color_range=(0, 224),
                ksize=(17, 17),
                sigmaX=1,
                alpha=random.uniform(0.9, 1.2),
                offsets=(10, 20),
            ),
            Letterpress(
                n_samples=(100, 400),
                n_clusters=(200, 400),
                std_range=(500, 3000),
                value_range=(150, 224),
                value_threshold_range=(96, 128),
                blur=1,
            ),
        ],
        p=1.0
    ),
    OneOf(
        [
            LowInkRandomLines(
                count_range=(5, 10),
                use_consistent_lines=random.choice([True, False]),
                noise_probability=0.1,
            ),
            LowInkPeriodicLines(
                count_range=(2, 5),
                period_range=(16, 32),
                use_consistent_lines=random.choice([True, False]),
                noise_probability=0.1,
            ),
        ],
        p=0.5,
    ),
]

paper_phase = [
    WaterMark(
        watermark_word="random",
        watermark_font_size=(10, 15),
        watermark_font_thickness=(20, 25),
        watermark_rotation=(0, 360),
        watermark_location="random",
        watermark_color="random",
        watermark_method="darken",
        p=0.33,
    ),
    OneOf(
        [
            DelaunayTessellation(
                n_points_range=(500, 800),
                n_horizontal_points_range=(500, 800),
                n_vertical_points_range=(500, 800),
                noise_type="random",
                color_list="default",
                color_list_alternate="default",
            ),
            PatternGenerator(
                imgx=random.randint(256, 512),
                imgy=random.randint(256, 512),
                n_rotation_range=(10, 15),
                color="random",
                alpha_range=(0.2, 0.4), # 0.5 is too high
            ),
            VoronoiTessellation(
                mult_range=(50, 80),
                seed=19829813472,
                num_cells_range=(500, 1000),
                noise_type="random",
                background_value=(200, 255),
            ),
        ],
        p=0.5,
    ),
    AugmentationSequence(
        [
            NoiseTexturize(
                sigma_range=(3, 10),
                turbulence_range=(2, 5),
            ),
            BrightnessTexturize(
                texturize_range=(0.9, 0.99),
                deviation=0.03,
            ),
        ],
        p=0.8,
    ),
]

post_phase = [
    Geometric(
        rotate_range=(-10, 10),
        p=0.2,
    ),

    ShadowCast(
        shadow_opacity_range = (0.5, 0.9),
        shadow_width_range=(0.5, 1.0),
        shadow_height_range=(0.5, 1.0),
        p=0.5,
    ),

    Folding(
        fold_x=None,
        fold_deviation=(0, 0),
        fold_angle_range=random.choice([(0,0), (90,90),(45,45), (0, 90)]),
        fold_count=random.randint(2, 6),
        fold_noise=random.uniform(0, 0.15),
        gradient_width=(0.1, 0.2),
        gradient_height=(0.01, 0.02),
        p=0.8,
    ),

    OneOf(
        [
            DirtyDrum(
                line_width_range=(1, 6),
                line_concentration=random.uniform(0.05, 0.15),
                direction=random.randint(0, 2),
                noise_intensity=random.uniform(0.6, 0.95),
                noise_value=(180, 200),
                ksize=random.choice([(3, 3), (5, 5), (7, 7)]),
                sigmaX=0,
            ),
            DirtyRollers(
                line_width_range=(2, 32),
                scanline_type=0,
            ),
        ],
        p=0.33,
    ),


    OneOf(
        [
            Markup(
                num_lines_range=(8, 10),
                markup_length_range=(0.5, 1),
                markup_thickness_range=(1, 2),
                markup_type=random.choice(["strikethrough", "crossed", "highlight", "underline"]),
                markup_color="random",
                single_word_mode=False,
                repetitions=1,
            ),
            Scribbles(
                scribbles_type="random",
                scribbles_location="random",
                scribbles_size_range=(250, 600),
                scribbles_count_range=(2, 6),
                scribbles_thickness_range=(1, 3),
                scribbles_brightness_change=[32, 64, 128],
                scribbles_text="random",
                scribbles_text_font="random",
                scribbles_text_rotate_range=(0, 360),
                scribbles_lines_stroke_count_range=(1, 6),
            ),
        ],
        p=0.7,
    ),

    ColorShift(
        color_shift_offset_x_range=(3, 5),
        color_shift_offset_y_range=(3, 5),
        color_shift_iterations=(2, 3),
        color_shift_brightness_range=(0.9, 1.1),
        color_shift_gaussian_kernel_range=(3, 3),
        p = 0.01,
    ),
]



# 删除output文件夹，然后创建一个新的output文件夹
import os
import shutil
if os.path.exists("./output"):
    shutil.rmtree("./output")
os.mkdir("./output")


# input_path="./input/96.png"
# input_path="./input/9.png"
# input_path="./input/image2.jpg"
input_path="./input/image3.png"

image = cv2.imread(input_path)
# # 使用插值法将高度放缩为1024个像素，宽度等比例缩放
# image = cv2.resize(image, (int(2000*image.shape[1]/image.shape[0]), 2000))

for i in range(10):
    pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase)

    # cv2.imshow("image",image)

    augmented_image=pipeline(image)
    # 等待按键
    # cv2.imshow("augmented",augmented_image)
    # cv2.imwrite("augmented_image.jpg",augmented_image)
    # cv2.waitKey(0)

    # 保存图片
    cv2.imwrite(f"./output/augmented_image_{i}.jpg",augmented_image)