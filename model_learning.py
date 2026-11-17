import torch
import torch.nn as nn
from torchvision import datasets,models,transforms
from torch.utils.data import DataLoader

device= torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform=transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_data=datasets.ImageFolder("Dataset_Proiect_Split/train",transform=transform)
val_data=datasets.ImageFolder("Dataset_Proiect_Split/val",transform=transform)

train_loader=DataLoader(train_data,batch_size=16,shuffle=True)
val_loader=DataLoader(val_data,batch_size=16)

model=models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
for param in model.parameters():
    param.requires_grad=False

model.fc=nn.Linear(model.fc.in_features,len(train_data.classes))
model=model.to(device)

criterion=nn.CrossEntropyLoss()
optimizer=torch.optim.Adam(model.fc.parameters(),lr=0.001)

for epoch in range(10):
    model.train()
    running_loss = 0.0
    for images,labels in train_loader:
        images,labels=images.to(device),labels.to(device)
        optimizer.zero_grad()
        outputs=model(images)
        loss=criterion(outputs,labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * images.size(0)
    epoch_loss = running_loss / len(train_loader.dataset)
    print(f"Epoca {epoch+1}/10 finalizata. Pierdere medie: {epoch_loss:.4f}")

    model.eval()
    running_val_loss=0.0
    correct_val=0
    total_val=0

    with torch.no_grad():
        for images,labels in val_loader:
            images,labels=images.to(device),labels.to(device)
            outputs=model(images)
            loss=criterion(outputs,labels)
            running_val_loss+=loss.item()*images.size(0)
            _,preds=torch.max(outputs,1)
            correct_val+=(preds==labels).sum().item()
            total_val+=labels.size(0)
    val_loss=running_val_loss/len(val_loader.dataset)
    val_acc=(correct_val/total_val)*100
    print(f"Epoca {epoch+1}/10 | Val Acc: {val_acc:.2f}%")
torch.save(model.state_dict(), 'best_model.pth')