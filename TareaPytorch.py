
import torch
import torch.nn as nn
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset

# Define tu clase de Dataset personalizado
class CustomDataset(Dataset):
    def __init__(self, data_path, train=True, transform=None, download=False):
        self.data = datasets.MNIST(root=data_path + "/data", train=train, transform=transform, download=download)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        image, label = self.data[index]
        
        return image, label

# Especifica la ruta de tu conjunto de datos personalizado
data_path = '../positivos_covid.csv'  # Ruta donde guardarás tus datos personalizados

# Define las transformaciones necesarias
transform = transforms.Compose([
    transforms.ToTensor(),
])

# Carga tu conjunto de datos personalizado
train_dataset = CustomDataset(data_path, train=True, transform=transform, download=True)
test_dataset = CustomDataset(data_path, train=False, transform=transform, download=True)

# Crea el DataLoader para cargar los datos en lotes
batch_size = 64
train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

# Define tu modelo de red neuronal
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

# Especifica los tamaños de entrada y salida de tu modelo
input_size = 784
hidden_size = 100
num_classes = 10

# Crea una instancia de tu modelo
model = NeuralNet(input_size, hidden_size, num_classes)

# Define la función de pérdida y el optimizador
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Entrenamiento
num_epochs = 2
total_step = len(train_loader)

for epoch in range(num_epochs):
    for i, (images, labels) in enumerate(train_loader):
        # Aplanar las imágenes
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
            print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{total_step}], Loss: {loss.item():.4f}')

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
    print(f'Accuracy on test images: {accuracy:.2f}%')