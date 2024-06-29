import torch
import torch.nn as nn

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, padding=1):
        super(ResidualBlock, self).__init__()

        self.convolution = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size, padding=padding),
            nn.ReLU(inplace=True),
            nn.GroupNorm(num_groups=8, num_channels=out_channels),

            nn.Conv2d(out_channels, out_channels, kernel_size, padding=padding),
            nn.ReLU(inplace=True),
            nn.GroupNorm(num_groups=8, num_channels=out_channels)
        )

        self.skip = nn.Conv2d(in_channels, out_channels, kernel_size=1) if in_channels != out_channels else nn.Identity()

    def forward(self, x):
        identity = self.skip(x)
        out = self.convolution(x)
        out += identity
        return out

class SpatialAttention(nn.Module):
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        self.conv1 = nn.Conv2d(2, 1, kernel_size, padding=(kernel_size - 1) // 2, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        x = torch.cat([avg_out, max_out], dim=1)
        x = self.conv1(x)
        return self.sigmoid(x)

class ImprovedPDNMedium(nn.Module):
    def __init__(self, out_channels=384, padding=False):
        super(ImprovedPDNMedium, self).__init__()
        pad_mult = 1 if padding else 0
        
        self.conv_tree = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, padding=pad_mult),
            nn.ReLU(inplace=True),

            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=pad_mult),
            nn.ReLU(inplace=True),

            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=pad_mult),
            nn.ReLU(inplace=True),
            nn.GroupNorm(num_groups=8, num_channels=256)
        )

        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.block1 = ResidualBlock(in_channels=256, out_channels=512, kernel_size=3, padding=pad_mult)
        
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.block2 = ResidualBlock(in_channels=512, out_channels=512, kernel_size=3, padding=pad_mult)
        
        self.conv_2 = nn.Sequential(
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, padding=pad_mult),
            nn.ReLU(inplace=True),
            nn.GroupNorm(num_groups=8, num_channels=512)
        )
        
        self.conv_final = nn.Conv2d(512, out_channels, kernel_size=5, padding=2 * pad_mult)
        
        self.spatial_attention = SpatialAttention()

    def forward(self, x):
        x = self.conv_tree(x)
        x = self.pool1(x)
        
        x = self.block1(x)
        
        x = self.pool2(x)
        
        x = self.block2(x)
        x = self.conv_2(x)
        
        x = self.conv_final(x)
        
        x = x * self.spatial_attention(x)
        
        return x