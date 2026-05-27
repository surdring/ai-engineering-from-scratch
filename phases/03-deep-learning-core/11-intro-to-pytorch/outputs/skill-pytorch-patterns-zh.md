---
name: skill-pytorch-patterns
description: PyTorch 训练、评估和部署的参考模式
version: 1.0.0
phase: 03
lesson: 11
tags: [pytorch, 训练, 深度学习, gpu, 模式]
---

## 标准训练循环

```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Model().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)

for epoch in range(num_epochs):
    model.train()
    for inputs, targets in train_loader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

    model.eval()
    with torch.no_grad():
        for inputs, targets in val_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
```

## 混合精度训练

```python
from torch.amp import autocast, GradScaler

scaler = GradScaler()
for inputs, targets in train_loader:
    inputs, targets = inputs.to(device), targets.to(device)
    optimizer.zero_grad()
    with autocast(device_type="cuda"):
        outputs = model(inputs)
        loss = criterion(outputs, targets)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

使用场景：在支持 float16 的 GPU 硬件（V100、A100、H100、RTX 3090+）上训练。预期提速约 1.5-2 倍，内存减少约 50%。

## 梯度累积

```python
accumulation_steps = 4
optimizer.zero_grad()
for i, (inputs, targets) in enumerate(train_loader):
    inputs, targets = inputs.to(device), targets.to(device)
    outputs = model(inputs)
    loss = criterion(outputs, targets) / accumulation_steps
    loss.backward()
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

使用场景：有效的批量大小需要超过 GPU 显存容量。将损失除以 accumulation_steps 保持梯度尺度一致。

## 保存与加载

```python
torch.save({
    "epoch": epoch,
    "model_state_dict": model.state_dict(),
    "optimizer_state_dict": optimizer.state_dict(),
    "loss": loss.item(),
}, "checkpoint.pt")

checkpoint = torch.load("checkpoint.pt", weights_only=True)
model.load_state_dict(checkpoint["model_state_dict"])
optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
```

始终保存优化器状态以便恢复训练。仅用于推理时，只保存 `model.state_dict()`。

## 自定义数据集

```python
class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, data_dir, transform=None):
        self.samples = self._load_samples(data_dir)
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        x, y = self.samples[idx]
        if self.transform:
            x = self.transform(x)
        return x, y

    def _load_samples(self, data_dir):
        ...
```

## DataLoader 配置

```python
train_loader = torch.utils.data.DataLoader(
    dataset,
    batch_size=64,
    shuffle=True,
    num_workers=4,
    pin_memory=True,
    drop_last=True,
    persistent_workers=True,
)
```

| 参数 | 功能 | 何时使用 |
|------|------|---------|
| num_workers=4 | 并行数据加载 | 始终在多核机器上使用 |
| pin_memory=True | 页锁定 CPU 内存 | GPU 训练时使用 |
| drop_last=True | 丢弃不完整的最后一个批次 | 使用 BatchNorm 时 |
| persistent_workers=True | 跨 epoch 保持 worker 存活 | num_workers > 0 时 |

## 学习率调度

```python
scheduler = torch.optim.lr_scheduler.OneCycleLR(
    optimizer,
    max_lr=1e-3,
    total_steps=num_epochs * len(train_loader),
    pct_start=0.1,
)

for epoch in range(num_epochs):
    for inputs, targets in train_loader:
        ...
        optimizer.step()
        scheduler.step()
```

OneCycleLR：大多数任务的最佳默认选择。预热到 max_lr，然后余弦衰减。在每个批次（而非每个 epoch）后调用 `scheduler.step()`。

## 权重初始化

```python
def init_weights(module):
    if isinstance(module, nn.Linear):
        nn.init.kaiming_normal_(module.weight, nonlinearity="relu")
        if module.bias is not None:
            nn.init.zeros_(module.bias)
    elif isinstance(module, nn.Conv2d):
        nn.init.kaiming_normal_(module.weight, mode="fan_out", nonlinearity="relu")

model.apply(init_weights)
```

## 推理模式

```python
model.eval()

with torch.inference_mode():
    outputs = model(inputs)
```

`torch.inference_mode()` 比 `torch.no_grad()` 更快，因为它完全禁用 autograd 而非仅抑制梯度计算。

## 常见错误清单

1. 在 CrossEntropyLoss 之前应用 softmax（它内部已包含 log_softmax）
2. 验证时忘记调用 model.eval()
3. 忘记将张量移动到与模型相同的设备上
4. 不调用 optimizer.zero_grad()（梯度默认累积）
5. 训练时使用 torch.no_grad()（禁用梯度计算）
6. 设置 num_workers 过高（产生过多进程，耗尽内存）
7. GPU 训练时不使用 pin_memory=True
8. 保存完整模型对象而非 state_dict（重构时会出错）