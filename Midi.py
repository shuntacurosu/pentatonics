from multiprocessing import Process, Queue, Value
import traceback
import pygame.midi

from Logger import Logger
from Pentatonics import Pentatonics
logger = Logger(__name__, Logger.DEBUG)

class Const:
    NOTE_ON = 0x90  # midiステータス
    NOTE_OFF = 0x80 # midiステータス
    TONE_NUM = 12   # 12律

def midi_process_func(in_key, hw_input_id, note_queue, isFinish):
    """ midi入力機器から入力されたノートをQueueに入れる """
    pygame.midi.init()
    midi_input = pygame.midi.Input(hw_input_id)

    offset = -1 * Pentatonics.notes.index(in_key)

    try:
        while (not isFinish.value):
            # キーボードからの入力値を取得
            if midi_input.poll():
                midi_events = midi_input.read(1)
                status = midi_events[0][0][0]
                midi_note = midi_events[0][0][1] + offset

                if status == Const.NOTE_ON:
                    note = pygame.midi.midi_to_ansi_note(midi_note%Const.TONE_NUM)[:-2]
                    note_queue.put(note)

            pygame.time.wait(10)

    except KeyboardInterrupt:
            pass
    finally:
        pygame.midi.Input.close(midi_input)
        pygame.midi.quit()

def setup_midi_device():
    """ 入力MIDIデバイスを選択する。入力MIDIデバイスのIDとキー(移調楽器用)を返す """
    # midi入力デバイス一覧を取得
    hw_input_list = get_midi_input_device_dict()
    if len(hw_input_list) == 0:
        logger.error("midi入力デバイスが見つかりませんでした")
        exit()
    logger.info("===== midi device list =====")
    for k, v in hw_input_list.items():
        logger.info(f"{k} : {v}")

    # リスト内のデバイスをユーザに入力させる
    hw_input_id = input_midi_device_id(hw_input_list)
    
    # 移調楽器用にキーを入力させる
    key = input_key()
    
    logger.info("midiデバイスの設定が完了しました")
    logger.info(f"デバイス: {hw_input_list[hw_input_id]}")
    logger.info(f"Key: in {key}")

    return hw_input_id, key

def get_midi_input_device_dict():
    """ 全てのmidi入力デバイスを取得 """
    pygame.midi.init()
    hw_input_dict = {}
    for i in range(pygame.midi.get_count()):
        device_info = pygame.midi.get_device_info(i)
        if device_info[2] ==  1: # is InputDevice?
            hw_input_dict[i] = device_info[1]

    return hw_input_dict

def input_midi_device_id(hw_input_dict):
    """ hw_input_list内からデバイスIDを選択する """

    while True:
        try:
            hw_input_id = int(input("midi入力デバイスIDを入力してください: "))            
            if hw_input_id in list(hw_input_dict.keys()):
                hw_input_id = hw_input_id
                break
            else:
                logger.warning("midi入力デバイスIDが正しくありません")    

        except ValueError:
            logger.warning("midi入力デバイスIDが正しくありません")
    
    return hw_input_id

def input_key():
    """ 楽器のキーを選択する """

    while True:
        key = input("楽器のキーを入力してください: ")
        try:
            _ = list(Pentatonics.notes).index(key)
            break
        except ValueError:
            logger.warning("キーが正しくありません。以下の中から選択してください")
            logger.warning(f"{Pentatonics.notes}")
    
    return key

if __name__ == "__main__":
    try:
        queue = Queue()
        isFinish = Value('i', 0)

        # midi入力デバイス一覧を取得
        hw_input_list = get_midi_input_device_dict()
        if len(hw_input_list) == 0:
            logger.error("midi入力デバイスが見つかりませんでした")
            exit()

        logger.info("===== midi device list =====")
        for k, v in hw_input_list.items():
            logger.info(f"{k} : {v}")

        # リスト内のデバイスをユーザに入力させる
        hw_input_id = input_midi_device_id(hw_input_list)
        
        logger.info("midiデバイスの設定が完了しました")
        logger.info(f"デバイス: {hw_input_list[hw_input_id]}")

        # midi入力受付け開始
        midi_process = Process(target=midi_process_func, args=('C', hw_input_id, queue, isFinish))
        midi_process.start()

        for i in range(10):
            note = queue.get()
            logger.info(f"note: {note}")

        # 終了        
        isFinish.value = 1
        midi_process.join()

    except KeyboardInterrupt:
        pass
    except Exception:
        logger.error(traceback.format_exc())

