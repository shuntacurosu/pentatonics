from multiprocessing import Process, Queue, Value
import random
import time
import traceback

from Logger import Logger
from Midi import midi_process_func, setup_midi_device
from Pentatonics import Pentatonics
logger = Logger(__name__, Logger.DEBUG)

def main():
    queue = Queue()
    isFinish = Value('i', 0)

    # MIDI入力受付け開始
    hw_input_id, in_key = setup_midi_device()
    midi_process = Process(target=midi_process_func, args=(in_key, hw_input_id, queue, isFinish))
    midi_process.start()

    try:
        # 入力音がペンタトニックかチェックする(ブロッキング)
        check_pentatocnic_note(queue, isFinish)
    except KeyboardInterrupt:
        pass
    except Exception:
        logger.error(traceback.format_exc())
    finally:
        # 終了        
        isFinish.value = 1
        midi_process.join()

def check_pentatocnic_note(queue, isFinish):

    time.sleep(2) # pygameの出力までちょっと待つ
    
    while(True):
        chord = Pentatonics.notes[random.randint(0,len(Pentatonics.notes)-1)]
        deg = Pentatonics.penta_deg[random.randint(0,len(Pentatonics.penta_deg)-1)]

        # chord対応するペンタトニックスケール
        penta = Pentatonics(chord)

        # マイナー7thペンタ
        logger.info(f"=======================================")
        logger.info(f"chord: {penta.chord}m")
        logger.info(f"1st_deg: {deg}\n")
        logger.info(f"minor_pente_scale: {penta.minor7th_scale}")
        logger.info(f"ascending_notes: {penta.minor7th_ascending_notes(deg)}")
        logger.info(f"descending_notes: {penta.minor7th_descending_notes(deg)}")

        is_used_note = [False for _ in range(Pentatonics.penta_len)]

        while(not isFinish.value):
            note = queue.get()
            logger.info(f"note: {note}")

            try:
                penta_idx = penta.minor7th_scale.index(note)
                is_used_note[penta_idx] = True
            except ValueError:
                pass

            # すべてのペンタトニックを鳴らしたら次のコードに進む
            if all(is_used_note):
                break

if __name__ == "__main__":
    main()