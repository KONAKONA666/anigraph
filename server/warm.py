import json
import numpy as np

from typing import List, Tuple, Dict, Any, Optional


from gensim.models.doc2vec import Doc2Vec


_model = None


def clean() -> None:
    global _model
    _model = None


def warm(model_path: str) -> None:
    global _model
    if _model is None:
        _model = Doc2Vec.load(model_path)


def get_closest(title: str, top: int) -> List[Tuple[str, float]]:
    model: Doc2Vec = _model

    if model is None:
        raise RuntimeError('Model is not found!')

    anime_list = model.docvecs.most_similar([title], topn=top)
    return anime_list


def calc_analogy(base_title: str, rel_title: str, req_title: str) -> List[Tuple[str, float]]:
    model: Doc2Vec = _model

    if model is None:
        raise RuntimeError('Model is not found!')

    anime_list = model.docvecs.most_similar(positive=[base_title, req_title], negative=[rel_title])
    return anime_list