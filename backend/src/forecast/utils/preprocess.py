from typing import List

import torch


def preprocess(context: List[List[float]]):
    processed_data = [torch.tensor(i) for i in context]
    return processed_data
