from dataclasses import dataclass

@dataclass
class SabreArgs():
    network: str = 'src/ABR/network.json'
    network_multiplier: float = 1
    movie: str = 'src/ABR/videos/video1/manifest.json'
    movie_length: float = None
    abr: str = 'custom'
    abr_basic: bool = False
    abr_osc: bool = False
    gamma_p: float = 5
    no_insufficient_buffer_rule: bool = False
    moving_average: str = 'ewma'
    window_size: tuple = (3)
    half_life: tuple = (3., 8.)
    seek: list = None
    replace: str = 'none'
    max_buffer: float = 25
    no_abandon: bool = False
    rampup_threshold: int = None
    verbose: bool = False