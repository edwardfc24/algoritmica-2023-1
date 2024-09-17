import torch
import torch.nn as nn
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
import os

class CustomDataset(Dataset):
    def __init__(self, data_path, train=True, transform=None, download=False):
        self.data = datasets.MNIST(root=data_path, train=train, transform=transform, download=download)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        image, label = self.data[index]

        
        return image, label

data_path = '../covid_cleaned.csv'

# Define las transformaciones necesarias
transform = transforms.Compose([
    transforms.ToTensor(),
])

# Carga de datos
train_dataset = CustomDataset(data_path, train=True, transform=transform, download=True)
test_dataset = CustomDataset(data_path, train=False, transform=transform, download=True)

# Crea el DataLoader para cargar los datos en lotes
batch_size = 64
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

#Tamaños de entrada y salida
input_size = 784
hidden_size = 100
num_classes = 10

model = NeuralNet(input_size, hidden_size, num_classes)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

num_epochs = 3
total_step = len(train_loader)

for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        images = images.reshape(-1, input_size)
        
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward pass y optimización
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        # Imprimir información del entrenamiento
        if (i+1) % 100 == 0:
            print(f'Epoca [{epoch+1}/{num_epochs}], Paso [{i+1}/{total_step}], Perdida: {loss.item():.4f}')

# Evaluación
model.eval()
with torch.no_grad():
    correct = 0
    total = 0
    
    for images, labels in test_loader:
        images = images.reshape(-1, input_size)
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    accuracy = 100 * correct / total
    print(f'Precision en los test: {accuracy:.2f}%')
