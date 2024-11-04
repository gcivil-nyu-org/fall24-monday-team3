from anomalib.models.image.patchcore.torch_model import PatchcoreModel
layers = ["layer2", "layer3"]
model = PatchcoreModel(layers, backbone='wide_resnet50_2', pre_trained=True, num_neighbors=9)