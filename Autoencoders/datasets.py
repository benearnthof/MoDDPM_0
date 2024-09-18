import torch
from torch import nn
from pathlib import Path
from torch.utils.data import Dataset
import torchvision.transforms as T
from PIL import Image


class ImageDataset(Dataset):
    def __init__(
        self,
        folder: str | Path,
        image_size: int,
        exts: List[str] = ["jpg", "jpeg", "png", "tiff"],
        augment_horizontal_flip=False,
        convert_image_to=None,
    ):
        super().__init__()
        if isinstance(folder, str):
            folder = Path(folder)
        assert folder.is_dir()
        self.folder = folder
        self.image_size = image_size
        self.paths = [p for ext in exts for p in folder.glob(f"**/*.{ext}")]

        def convert_image_to_fn(img_type, image):
            if image.mode == img_type:
                return image

            return image.convert(img_type)

        maybe_convert_fn = (
            partial(convert_image_to_fn, convert_image_to)
            if exists(convert_image_to)
            else nn.Identity()
        )

        self.transform = T.Compose(
            [
                T.Lambda(maybe_convert_fn),
                T.Resize(image_size),
                T.RandomHorizontalFlip() if augment_horizontal_flip else nn.Identity(),
                T.CenterCrop(image_size),
                T.ToTensor(),
            ]
        )

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, index):
        path = self.paths[index]
        img = Image.open(path)
        return self.transform(img)
