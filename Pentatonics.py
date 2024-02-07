from dataclasses import dataclass

@dataclass
class Pentatonics:
    chord: str
    first_note: int
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    notes_len = len(notes)
    penta_deg = [1, 3, 4, 5, 7]
    penta_len = 5

    def __init__(self, chord: str, first_note: int = 0):
        self.chord = chord
        self.first_note = first_note
        self.first_degree = self.penta_deg[first_note]

    def minor7th_ascending_notes(self, deg):
        idx = self.penta_deg.index(deg)
        return [self.minor7th_scale[idx%self.penta_len], self.minor7th_scale[(idx+1)%self.penta_len], self.minor7th_scale[(idx+2)%self.penta_len], self.minor7th_scale[(idx+3)%self.penta_len], self.minor7th_scale[(idx+4)%self.penta_len]]

    def minor7th_descending_notes(self, deg):
        idx = self.penta_deg.index(deg)
        return [self.minor7th_scale[idx%self.penta_len], self.minor7th_scale[(idx+4)%self.penta_len], self.minor7th_scale[(idx+3)%self.penta_len], self.minor7th_scale[(idx+2)%self.penta_len], self.minor7th_scale[(idx+1)%self.penta_len]]

    @property
    def minor7th_scale(self):
        idx = self.notes.index(self.chord)
        minor_penta_idx = [idx%self.notes_len, (idx+3)%self.notes_len, (idx+5)%self.notes_len, (idx+7)%self.notes_len, (idx+10)%self.notes_len]
        minor_penta = [self.notes[i] for i in minor_penta_idx]
        return minor_penta
