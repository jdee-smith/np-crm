import torch


def postprocess(preds):
    processed_preds = torch.mean(preds, axis=1).flatten().tolist()
    return processed_preds
