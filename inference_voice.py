import os
import shutil
import uuid
import datetime
from utils import *
from PredictionInfo import *
from mysqlhelper import *

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def get_voice_interference(test_filepath, user='101'):
    unlabeled_dir = "data/inference_data/unlabeled"
    data_dir = "data/inference_data/"
    mode = "unlabeled"
    pretrained_model_name = 'best_model.h5'
    inf_metadata = dict()

    shutil.copy(test_filepath, unlabeled_dir)
    print(f"Loading inference data from {os.path.join(data_dir,mode)}")
    print(f"Loading pretrained model {pretrained_model_name}")

    processed_data = preprocess_from_ray_parallel_inference(data_dir, mode, use_parallel=True)
    processed_data = sorted(processed_data, key=lambda x: len(x[0]))
    voice = Voice_Model(load_pretrained=True, saved_model_name=pretrained_model_name,
                                        real_test_mode=False)

    prob = voice.predict_labels(processed_data, raw_prob=True, batch_size=20)[0][0]

    print(prob)

    inf_metadata['pred_id'] = str(uuid.uuid1())
    inf_metadata['user_id'] = str(user)
    inf_metadata['time_stamp'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    inf_metadata['prob'] = str(prob * 10000)
    inf_metadata['stype'] = str('A')
    print(inf_metadata['pred_id'], inf_metadata['user_id'], inf_metadata['time_stamp'], inf_metadata['prob'])

    wav_filenames = os.listdir(os.path.join(data_dir, mode))
    for wav_filename in wav_filenames:
         wav_path = str(os.path.join(data_dir, mode) + '/' + wav_filename)
         plot_spectogram_amp(wav_path, path='/Applications/XAMPP/xamppfiles/htdocs/fakelab_xampp/spectogram/', pname=inf_metadata['pred_id'])
         plot_spectogram_spc(wav_path, path='/Applications/XAMPP/xamppfiles/htdocs/fakelab_xampp/spectogram/', pname=inf_metadata['pred_id'])

    """Write to Local MySql Database"""

    insert_sql_value = PredictionInfo(inf_metadata['pred_id'], inf_metadata['user_id'], inf_metadata['time_stamp'], inf_metadata['prob'],
                                      inf_metadata['stype']);

    # create a database connection
    conn = create_connection()
    # create a new prediction
    create_prediction(conn, insert_sql_value)


get_voice_interference('/Users/sai/Desktop/FakeLabVoice/data/inference_data/realtalk/fake/JREa633-0023.wav',
                       '101')
