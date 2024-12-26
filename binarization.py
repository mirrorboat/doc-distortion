from augraphy import *
import cv2
import os
import random

HEIGHT_THRESHOLD = 1200

input_folder="./input/GT/EN"
output_folder="./testset/EN"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# 遍历input_folder，处理其中的所有图片，然后保存到output_folder
for i, filename in enumerate(os.listdir(input_folder)):
    if filename.endswith(".jpg") or filename.endswith(".png"):

        ink_phase = [
            # OneOf(
            #     [
            #         InkShifter(),
            #         InkMottling(),
            #     ],
            #     p=1.0,
            # ),


            OneOf(
                [
                    BleedThrough(
                        intensity_range=(0.6, 0.9),
                        color_range=(0, 224),
                        ksize=(17, 17),
                        sigmaX=1,
                        alpha=random.uniform(0.2, 0.3),
                        offsets=(10, 20),
                    ),
                    InkBleed(
                        intensity_range=(0.5, 0.6),
                        kernel_size=random.choice([(5, 5), (3, 3)]),
                        severity=(0.5, 0.6),
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
        ]


        paper_phase = [
            OneOf(
                [
                    # PaperFactory(
                    #     generate_texture_background_type = random.choice(["rough_stains", "fine_stains", "severe_stains", "light_stains", "dot_granular", "light_granular", "rough_granular"]),
                    #     generate_texture_edge_type = "curvy_edge",
                    # ),
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
                        alpha_range=(0.15, 0.2),
                    ),
                    VoronoiTessellation(
                        mult_range=(50, 80),
                        seed=19829813472,
                        num_cells_range=(500, 1000),
                        noise_type="random",
                        background_value=(200, 255),
                    ),
                ],
            ),
        ]

        post_phase = []

        input_path=os.path.join(input_folder, filename)
        image = cv2.imread(input_path)


        height=0
        weight=0
        if image.shape[0]>HEIGHT_THRESHOLD:
            height=image.shape[0]
            weight=image.shape[1]
            image = cv2.resize(image, (HEIGHT_THRESHOLD, int(HEIGHT_THRESHOLD*image.shape[1]/image.shape[0])))


        seed=random.randint(0,100000)
        print(f"seed {seed}")
        pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase,random_seed=seed, ink_color_range=(0,0))
        augmented_image=pipeline(image)
        if height>0:
            augmented_image = cv2.resize(augmented_image, (weight, height))
        cv2.imwrite(f"{output_folder}/{filename}",augmented_image)
