"""Command-aware timing for the GitHub profile SVG.

The number of output rows affects layout, never execution pacing.
"""
from dataclasses import dataclass

CHARACTER_MS = 62
NEXT_PROMPT_GAP_MS = 65
NEXT_TYPING_PAUSE_MS = 230
FINAL_PROMPT_GAP_MS = 95
EXECUTION_DELAY_MS = {"neofetch": 165, "ls": 125}


@dataclass(frozen=True)
class Cue:
    command: str
    prompt_at_ms: int
    typing_at_ms: int
    typing_done_ms: int
    result_at_ms: int


@dataclass(frozen=True)
class Timeline:
    cues: tuple[Cue, ...]
    final_prompt_at_ms: int


def build_timeline(commands: tuple[str, ...]) -> Timeline:
    if not commands or any(not command.strip() for command in commands):
        raise ValueError("Demo requires non-empty commands")
    cues = []
    prompt_ms, typing_ms = 0, 300
    for command in commands:
        name = command.split(maxsplit=1)[0]
        done_ms = typing_ms + max(180, min(850, len(command) * CHARACTER_MS))
        result_ms = done_ms + EXECUTION_DELAY_MS.get(name, 160)
        cues.append(Cue(command, prompt_ms, typing_ms, done_ms, result_ms))
        prompt_ms = result_ms + NEXT_PROMPT_GAP_MS
        typing_ms = result_ms + NEXT_TYPING_PAUSE_MS
    return Timeline(tuple(cues), cues[-1].result_at_ms + FINAL_PROMPT_GAP_MS)


def clip_animation(command: str, start_ms: int, end_ms: int) -> str:
    """SMIL clip grows cell by cell, stops, and never rewinds."""
    cells = 9.03
    length = len(command)
    widths = [0.0] + [i * cells + 1 for i in range(1, length + 1)]
    widths[-1] = length * cells + 9
    values = ";".join(f"{value:.2f}" for value in widths)
    fractions = ";".join(f"{i/length:.5f}" for i in range(length + 1))
    return (
        f'<animate attributeName="width" values="{values}" '
        f'keyTimes="{fractions}" begin="{start_ms/1000:.3f}s" '
        f'dur="{(end_ms-start_ms)/1000:.3f}s" calcMode="discrete" fill="freeze"/>'
    )


def reveal_css(name: str, when_ms: int) -> str:
    return (
        f'.{name}{{opacity:0;animation:reveal .01s steps(1,end) '
        f'{when_ms/1000:.3f}s 1 forwards}}'
    )
