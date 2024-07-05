from mmpretrain.models.backbones import MobileNetV3
import torch
import numpy as np
import onnxruntime
from onnx import load_model, save_model
import onnx

def MobileNet():
    return MobileNetV3(arch='small')

model = MobileNet().cuda()
modelfile = r"C:\Users\Ryan\OneDrive - 中山醫學大學\桌面\SunBone開發日誌\ncc\model_lr_0.001_momentum_0.9.pth"
checkpoint = torch.load(modelfile, map_location='cuda:0')
state = checkpoint
state_keys = list(state.keys())

for i, key in enumerate(state_keys):
    if "backbone." in key and not ("neck." in key) and not ("head." in key):
        newkey = key.replace("backbone.", "")
        state[newkey] = state.pop(key)
    else:
        state.pop(key)

model_dict_load = model.state_dict()
model_dict_load.update(state)
model.load_state_dict(model_dict_load)

model.eval()

x = torch.rand(1, 3, 224, 224).cuda()  # 使用随机输入
export_onnx_file = r"C:\Users\Ryan\OneDrive - 中山醫學大學\桌面\SunBone開發日誌\ncc\model_lr_0.001_momentum_0.9.onnx"  # 导出ONNX文件路径
torch.onnx.export(model,
                  x,
                  export_onnx_file,
                  export_params=True,
                  opset_version=12,  # ONNX opset版本
                    )