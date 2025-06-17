import os
import cv2
import argparse
from PIL import Image, ImageOps, ImageChops, ImageDraw
import numpy as np
import random

from augraphy import *

HEIGHT_THRESHOLD = 3500

# 添加噪声
def add_pepper_salt_noise(image, prob=0.02):
    noisy_image = image.copy()
    total_pixels = image.size
    num_salt = int(prob * total_pixels * 0.5)  # 盐噪声的像素点数量
    num_pepper = int(prob * total_pixels * 0.5)  # 椒噪声的像素点数量

    salt_coords = [
        np.random.randint(0, dim, num_salt) for dim in image.shape[:2]
    ]
    noisy_image[salt_coords[0], salt_coords[1]] = 255

    pepper_coords = [
        np.random.randint(0, dim, num_pepper) for dim in image.shape[:2]
    ]
    noisy_image[pepper_coords[0], pepper_coords[1]] = 0

    return noisy_image

def add_scan_lines(image, line_intensity_range=(0, 50), line_probability=0.2, line_density=0.7, 
                   line_imbalance=0.3, line_thickness_range=(1, 3)):
    """
    参数：
    - image: 输入图像（numpy 数组）。
    - line_intensity_range: 分割线强度范围 (min, max)，默认 (0, 50)。
    - line_probability: 每一行或列添加分割线的概率，默认 0.2。
    - line_density: 分割线密度，范围 [0, 1]，默认 1.0（密度越高，分割线越密集）。
    - line_imbalance: 分割线分布均衡性，范围 [0, 1]，默认 0.3（0.0 为完全随机，1.0 为完全均匀）。
    - line_thickness_range: 分割线粗细范围 (min, max)，默认 (1, 3)。
    """
    noisy_image = image.copy()
    height, width = image.shape[:2]
    
    # 随机选择分割线类型：1-只添加横线，2-只添加纵线
    line_type = np.random.choice([1, 2])

    # 根据密度计算需要添加分割线的数量
    num_rows = int(height * line_density)
    num_cols = int(width * line_density)

    # 根据均衡性选择分割线的分布
    if line_imbalance > 0:  # 均匀分布
        row_positions = np.linspace(0, height - 1, num=num_rows, dtype=int)  # 横线均匀分布
        col_positions = np.linspace(0, width - 1, num=num_cols, dtype=int)  # 纵线均匀分布
    else:  # 随机分布
        row_positions = np.random.choice(height, size=num_rows, replace=False)
        col_positions = np.random.choice(width, size=num_cols, replace=False)

    # 添加横线
    if line_type == 1:  # 横线
        for i in row_positions:
            if np.random.rand() < line_probability:  # 按概率决定是否添加分割线
                thickness = np.random.randint(*line_thickness_range)  # 随机选择分割线粗细
                intensity = np.random.randint(*line_intensity_range)  # 随机选择分割线强度
                start_row = max(0, i - thickness // 2)  # 确保起始位置不超出图像边界
                end_row = min(height, i + thickness // 2 + 1)  # 确保结束位置不超出图像边界
                noisy_image[start_row:end_row, :] = np.clip(noisy_image[start_row:end_row, :] - intensity, 0, 255)

    # 添加纵线
    if line_type == 2:  # 纵线
        for j in col_positions:
            if np.random.rand() < line_probability:  # 按概率决定是否添加分割线
                thickness = np.random.randint(*line_thickness_range)  # 随机选择分割线粗细
                intensity = np.random.randint(*line_intensity_range)  # 随机选择分割线强度
                start_col = max(0, j - thickness // 2)  # 确保起始位置不超出图像边界
                end_col = min(width, j + thickness // 2 + 1)  # 确保结束位置不超出图像边界
                noisy_image[:, start_col:end_col] = np.clip(noisy_image[:, start_col:end_col] - intensity, 0, 255)

    return noisy_image

def apply_random_rotation(image):
    # 随机生成一个旋转角度，范围为 -5° 到 5°
    angle = random.uniform(-3, 3)
    
    # 进行旋转，expand=True 保证旋转后图像不会被裁剪
    rotated_image = image.rotate(angle, resample=Image.BICUBIC, expand=True, fillcolor=(255, 255, 255))
    
    return rotated_image

def apply_texture(image, alpha=0.8, beta=0.2):
    """
    将纸张纹理叠加到图像上，生成做旧效果。

    参数：
    - img_path (str): 输入的文档图像路径。
    - texture_path (str): 纸张纹理图像路径。
    - output_path (str): 输出图像保存路径。
    - alpha (float): 文档图像的权重（默认 0.8）。
    - beta (float): 纹理图像的权重（默认 0.2）。

    返回：
    - aged_img (numpy.ndarray): 处理后的图像。
    """
    # 读取文档图像和纹理图像
    text_root = "./paper_texture"
    texture_files = [f for f in os.listdir(text_root) if os.path.isfile(os.path.join(text_root, f))]
    if not texture_files:
        raise ValueError(f"纹理文件夹中没有可用的图像文件: {text_root}")
    
    texture_path = os.path.join(text_root, random.choice(texture_files))
    
    texture = cv2.imread(texture_path)

    # 调整纹理大小与文档图像一致
    texture = cv2.resize(texture, (image.shape[1], image.shape[0]))
    # 如果输入图像是灰度图，将其转换为彩色图
    if len(image.shape) == 2:  # 单通道（灰度图）
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # 如果纹理图像是灰度图，将其转换为彩色图
    if len(texture.shape) == 2:  # 单通道（灰度图）
        texture = cv2.cvtColor(texture, cv2.COLOR_GRAY2BGR)


    # 调整透明度，叠加纹理
    aged_img = cv2.addWeighted(image, alpha, texture, beta, 0)
    
    return aged_img

def binarization(image):
    ink_phase = [
        OneOf(
            [
                BleedThrough(
                    intensity_range=(0.1, 0.3),
                    color_range=(100, 255), # 深透区域的颜色
                    ksize=(17, 17), # 改小了会容易报错，默认17 * 17，改小了会更清楚
                    sigmaX=1,
                    alpha=random.uniform(0.1, 0.2),
                    offsets=(10, 20),
                    # p = 0.4
                ),
                InkBleed(
                    intensity_range=(0.2, 0.5), # 墨水的扩散
                    kernel_size=random.choice([(5, 5), (3, 3)]),
                    severity=(0.1, 0.2), # 控制深透区域的偏移程度
                    # p = 0.4
                ),
                Letterpress(
                    n_samples=(50, 100), # ***
                    n_clusters=(100, 200), # ***
                    std_range=(100, 500),
                    value_range=(150, 224),
                    value_threshold_range=(96, 128),
                    blur=1,
                ),
            ],
            p=1.0
        ),
    ]

    paper_phase = []
    # paper_phase = [
    #     OneOf(
    #         [
    #             DelaunayTessellation(
    #                 n_points_range=(100, 500),
    #                 n_horizontal_points_range=(100, 500),
    #                 n_vertical_points_range=(100, 500),
    #                 noise_type="random",
    #                 color_list="default", # 灰度值
    #                 color_list_alternate="default",
    #             ),
    #             PatternGenerator(
    #                 imgx=random.randint(256, 512),
    #                 imgy=random.randint(256, 512),
    #                 n_rotation_range=(10, 15),
    #                 color="random",
    #                 alpha_range=(0.1, 0.3),
    #             ),
    #             VoronoiTessellation(
    #                 mult_range=(10, 50),
    #                 seed=19829813472,
    #                 num_cells_range=(500, 1000),
    #                 noise_type="random",
    #                 background_value=(220, 255),
    #             ),
    #         ],
    #         p = 0.5
    #     )
    # ]

    post_phase = []

    height, weight = 0, 0
    if image.shape[0] > HEIGHT_THRESHOLD:
        height, weight = image.shape[:2]
        image = cv2.resize(image, (HEIGHT_THRESHOLD, int(HEIGHT_THRESHOLD*image.shape[1]/image.shape[0])))

    seed = random.randint(0, 100000)
    # print(f"seed {seed}")
    pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase, random_seed=seed, ink_color_range=(0,0))
    augmented_image = pipeline(image)
    
    if height > 0:
        augmented_image = cv2.resize(augmented_image, (weight, height))
    
    return augmented_image

def read_psf(psf_path):
    psf_image = cv2.imread(psf_path, cv2.IMREAD_GRAYSCALE)
    if psf_image.shape[0] % 2 == 0 or psf_image.shape[1] % 2 == 0:
        raise ValueError("PSF image dimensions must be odd.")
    
    # 定义多个缩放因子，随机选择一个
    scale_factors = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    scale_factor = random.choice(scale_factors)  # 随机选择一个缩放因子
    new_size = (int(psf_image.shape[1] * scale_factor), int(psf_image.shape[0] * scale_factor))
    psf_image = cv2.resize(psf_image, new_size, interpolation=cv2.INTER_LINEAR)
    
    # 确保 PSF 图像尺寸为奇数
    if psf_image.shape[0] % 2 == 0 or psf_image.shape[1] % 2 == 0:
        psf_image = cv2.resize(psf_image, (psf_image.shape[1] + 1, psf_image.shape[0] + 1))
    
    psf = psf_image / np.sum(psf_image)
    return psf

def wrap(image):
    ink_phase = []
    paper_phase = []
    post_phase = [
        Geometric(  # 几何变换
            # 增大rotate_range的值可以增强旋转程度
            rotate_range=(-2, 2),
            # p=0.2,
        ),
        Folding(  # 折叠效果
            fold_x=None,
            fold_deviation=(0, 0),
            fold_angle_range=random.choice([
                (90, 90),      # 垂直折叠
                (45, 45),      # 45度折叠
                (0, 90),       # 从水平到垂直的随机折叠
                (-45, 45),     # 从 -45 度到 45 度之间的随机折叠
                (30, 60),      # 30 到 60 度之间的折叠
                (-180, 180),   # 全角度范围的随机折叠（包括正负方向）
                (10, 20),      # 小角度的轻微折叠
                (-10, 10),     # 小范围内的正负折叠
            ]),
            fold_count=random.randint(1, 3), # 折叠次数
            fold_noise=random.uniform(0, 0.1), # 折叠噪声
            gradient_width=(0.1, 0.2),
            gradient_height=(0.01, 0.02),
        ),
    ]
    
    pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase)
    augmented_image = pipeline(image)
    return augmented_image   

def psf_blur(image):
    psf_folder = "./psf"
    # num_psf=100

    psf_files = [os.path.join(psf_folder, f) for f in os.listdir(psf_folder) if os.path.isfile(os.path.join(psf_folder, f))]
    psf_path = random.choice(psf_files)
    psf = read_psf(psf_path)  # 循环使用PSF
    
    b, g, r = cv2.split(image)
    blurred_b = cv2.filter2D(b, -1, psf)
    blurred_g = cv2.filter2D(g, -1, psf)
    blurred_r = cv2.filter2D(r, -1, psf)
    blurred_image = cv2.merge((blurred_b, blurred_g, blurred_r))
    return blurred_image

def shadow(image):
    # 定义图像处理pipeline
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
            shadow_vertices_range=(3,6), # 表示阴影的多边形顶点数的随机选择范围
            shadow_opacity_range = (0.1, 0.4), # 阴影的不透明度范围，值在 0 到 1 之间
            shadow_width_range=(0.5, 0.9), # 表示阴影宽度为图像宽度的 80% 到 100%。
            shadow_height_range=(0.5, 0.8), # 阴影高度为图像高度的 80% 到 100%。
            p=1, # 应用此增强的概率（取值范围为 0 到 1）。
        ),
    ]

    pipeline = AugraphyPipeline(ink_phase=ink_phase, paper_phase=paper_phase, post_phase=post_phase)
    augmented_image = pipeline(image)
    return augmented_image
    
def process_folder(input_folder, output_folder, n):
    """
    递归处理文件夹中的所有图片，每张图片随机选择 n 种失真处理方式，并保存结果。
    :param input_folder: 输入文件夹路径
    :param output_folder: 输出文件夹路径
    :param n: 每张图片随机选择的失真处理方式数量
    """
    # 定义所有可用的失真处理方式
    distortion_functions = {
        "pepper_salt_noise": add_pepper_salt_noise,
        "scan_lines": add_scan_lines,
        "texture": apply_texture,
        "binarization": binarization,
        "psf_blur": psf_blur,
        "wrap": wrap,
        "shadow": shadow,
        "random_rotation": apply_random_rotation,
    }

    # 遍历输入文件夹中的所有文件和子文件夹
    for root, dirs, files in os.walk(input_folder):
        # 计算当前子文件夹对应的输出文件夹路径
        relative_path = os.path.relpath(root, input_folder)
        current_output_folder = os.path.join(output_folder, relative_path)

        # 确保输出文件夹存在
        os.makedirs(current_output_folder, exist_ok=True)

        # 处理当前文件夹中的所有图片文件
        for filename in files:
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):  # 支持多种图片格式
                input_path = os.path.join(root, filename)
                output_filename = os.path.splitext(filename)[0]  # 获取文件名（不含扩展名）

                # 读取图像
                image = cv2.imread(input_path)
                if image is None:
                    print(f"无法读取文件: {input_path}，跳过处理")
                    continue

                # 随机选择 n 种失真处理函数
                selected_distortions = random.sample(list(distortion_functions.items()), min(n, len(distortion_functions)))

                # 应用失真处理
                processed_image = image
                applied_methods = []  # 用于记录应用的失真方法名称

                for distortion_name, distortion_function in selected_distortions:
                    try:
                        if distortion_name == "random_rotation":
                            # 特殊处理 PIL 图像的情况
                            pil_image = Image.fromarray(processed_image)
                            processed_image = distortion_function(pil_image)
                            processed_image = np.array(processed_image)  # 直接转换为 NumPy 数组
                        else:
                            processed_image = distortion_function(processed_image)

                        applied_methods.append(distortion_name)
                    except Exception as e:
                        print(f"处理方法 {distortion_name} 时出错: {e}，跳过该处理")

                # 保存处理后的图像
                output_file = os.path.join(current_output_folder, f"{output_filename}_{'_'.join(applied_methods)}.png")
                cv2.imwrite(output_file, processed_image)

                print(f"已处理文件: {filename}，应用的处理方法: {', '.join(applied_methods)}")


# 主程序入口
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="文档图像退化处理工具")
    parser.add_argument("--input", required=True, help="输入图片文件夹路径")
    parser.add_argument("--output", required=True, help="输出图片文件夹路径")
    parser.add_argument("--n", type=int, default=1, help="每张图片随机选择的失真处理方式数量（默认为1）")
    
    args = parser.parse_args()
    process_folder(args.input, args.output, args.n)
    
"""
python my_distortion.py --input /mnt/petrelfs/zhangqintong/ZQT_RAG/Dataset/RAG_Image_Dataset_pro --output /mnt/petrelfs/zhangqintong/ZQT_RAG/rebuttal/distortion_images_1 --n 1

python my_distortion.py --input /mnt/petrelfs/zhangqintong/ZQT_RAG/Dataset/RAG_Image_Dataset_pro --output /mnt/petrelfs/zhangqintong/ZQT_RAG/rebuttal/distortion_images_2 --n 2

python my_distortion.py --input /mnt/petrelfs/zhangqintong/ZQT_RAG/Dataset/RAG_Image_Dataset_pro --output /mnt/petrelfs/zhangqintong/ZQT_RAG/rebuttal/distortion_images_3 --n 3

"""