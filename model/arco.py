from dataclasses import dataclass

from model.artista import Artist


@dataclass
class Arco:
    a1: Artist
    a2: Artist