import torch
import torch.nn as nn
import torch.nn.functional as F

class AudioCNN(nn.Module):
    """
    CNN for processing Audio Spectrograms or MFCCs.
    Input shape: (Batch, Channels, Freq, Time)
    """
    def __init__(self, num_classes=2):
        super(AudioCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 16 * 16, 128) # Placeholder dimensions
        self.fc2 = nn.Linear(128, num_classes)
        
    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = torch.flatten(x, 1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

class PhysioLSTM(nn.Module):
    """
    LSTM for processing sequential Physiological data (HR, SpO2, PPG).
    Input shape: (Batch, Seq_Length, Features)
    """
    def __init__(self, input_size, hidden_size=64, num_layers=2, num_classes=2):
        super(PhysioLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        out, _ = self.lstm(x, (h0, c0))
        # Decode the hidden state of the last time step
        out = self.fc(out[:, -1, :])
        return out

class VisionMLP(nn.Module):
    """
    MLP for processing extracted tabular Vision features (deltas, means, stds).
    Input shape: (Batch, Features)
    """
    def __init__(self, input_size=16, hidden_size=64, num_classes=2):
        super(VisionMLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc3 = nn.Linear(hidden_size // 2, num_classes)
        self.dropout = nn.Dropout(0.3)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

class LateFusionModel(nn.Module):
    """
    Late Fusion Model combining the outputs (embeddings/probabilities) of the individual networks.
    """
    def __init__(self, input_dim=6, hidden_dim=32, num_classes=2):
        super(LateFusionModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, num_classes)
        
    def forward(self, audio_preds, physio_preds, vision_preds):
        # Concatenate predictions from individual modality models
        x = torch.cat((audio_preds, physio_preds, vision_preds), dim=1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
