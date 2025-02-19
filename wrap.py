from augraphy import *

class wrap(doc_distortion):
    def __init__(self, ink_color_range=(-1, -1)):
        self.ink_color_range = ink_color_range
        self.ink_phase = []
        self.paper_phase = []
        self.post_phase = [
            Geometric(
                rotate_range=(-5, 5),
                p=0.2,
            ),
            Folding(
                fold_x=None,
                fold_deviation=(0, 0),
                fold_angle_range=random.choice([(0,0), (90,90),(45,45), (0, 90)]),
                fold_count=random.randint(2, 5),
                fold_noise=random.uniform(0, 0.15),
                gradient_width=(0.1, 0.2),
                gradient_height=(0.01, 0.02),
            ),
        ]
        self.pipeline = AugraphyPipeline(ink_phase=self.ink_phase, paper_phase=self.paper_phase, post_phase=self.post_phase, ink_color_range=self.ink_color_range)

    def distortion(self, image):
        augmented_image = self.pipeline(image)
        return augmented_image