from torch.utils.data import Dataset, DataLoader
import os
from PIL import Image
from torchvision import transforms as T

class UTKFaceDataset(Dataset):
    def __init__(self, root_dir, transform = None):
        super().__init__()
        
        self.root_dir = root_dir
        self.transform = transform
        self.filename_list = os.listdir(root_dir)
        
    def __len__(self):
        return len(self.filename_list)
    
    def __getitem__(self, idx):
        filename = self.filename_list[idx]
        
        info = filename.split("_")
        age = int(info[0])
        gender = int(info[1])
        
        filename = os.path.join(self.root_dir, filename)
        
        image = Image.open(filename)
        
        if self.transform:
            image = self.transform(image)
        
        return image, gender, age

if __name__ == '__main__':
    
    image_size = (64,64)
    root_dir = '/kaggle/input/utkface-new/UTKFace'
    batch_size = 512
    num_workers = os.cpu_count()
    
    train_transform = T.Compose(
        [
            T.Resize(image_size),
            T.RandomHorizontalFlip(0.2),
            T.RandomRotation(10),
            T.ToTensor(),
            T.Normalize(mean = [0.5, 0.5, 0.5], std = [0.5, 0.5, 0.5])
        ]
    )

    train_dataset = UTKFaceDataset(root_dir, transform = train_transform)
    trainloader = DataLoader(train_dataset, batch_size = batch_size, shuffle = True, num_workers = num_workers, drop_last = True)

    for images, genders, ages in trainloader:
        print(images.shape, genders.shape, ages.shape)
        break

