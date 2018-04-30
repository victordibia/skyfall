## Author: Victor Dibia
## Loads models, establishes socket


from utils import detector_utils as detector_utils
from utils import object_id_utils as id_utils
import cv2
import tensorflow as tf
import multiprocessing
from multiprocessing import Queue, Pool
from utils.detector_utils import WebcamVideoStream
import time 
import datetime
import argparse
#from utils import web_socket
#from utils import web_socket_client 

frame_processed = 0
score_thresh = 0.7
num_hands_detect = 10
num_classes = 1

#web_socket_client.socket_init("ws://localhost:5006")

# Create a worker thread that loads graph and
# does detection on images in an input queue and puts it on an output queue

label_path = "hand_inference_graph/hand_label_map.pbtxt"
frozen_graph_path = "hand_inference_graph/frozen_inference_graph.pb"


object_refresh_timeout = 3
seen_object_list = {}

def worker(input_q, output_q, cap_params, frame_processed):
    print(">> loading frozen model for worker")
    
    detection_graph, sess, category_index = detector_utils.load_inference_graph(num_classes, frozen_graph_path, label_path)
    sess = tf.Session(graph=detection_graph)
    while True:
        #print("> ===== in worker loop, frame ", frame_processed)
        frame = input_q.get()
        if (frame is not None):
            # actual detection
            boxes, scores, classes = detector_utils.detect_objects(
                frame, detection_graph, sess)
            
            tags = detector_utils.get_tags(classes, category_index, num_hands_detect, score_thresh, scores, boxes, frame)
            
            
            if (len(tags) > 0):
                id_utils.get_id(tags, seen_object_list)
               
            id_utils.refresh_seen_object_list(seen_object_list, object_refresh_timeout)
            detector_utils.draw_box_on_image_id(tags, frame)

            #if (len(tags) > 0):
                #web_socket_client.send_message(tags,"hand")
            
            output_q.put(frame)
            frame_processed += 1
        else:
            output_q.put(frame)
    sess.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-src', '--source', dest='video_source', type=int,
                        default=0, help='Device index of the camera.')
    parser.add_argument('-nhands', '--num_hands', dest='num_hands', type=int,
                        default=2, help='Max number of hands to detect.')
    parser.add_argument('-fps', '--fps', dest='fps', type=int,
                        default=1, help='Show FPS on detection/display visualization')
    parser.add_argument('-wd', '--width', dest='width', type=int,
                        default=300, help='Width of the frames in the video stream.')
    parser.add_argument('-ht', '--height', dest='height', type=int,
                        default=200, help='Height of the frames in the video stream.')
    parser.add_argument('-ds', '--display', dest='display', type=int,
                        default=1, help='Display the detected images using OpenCV. This reduces FPS')
    parser.add_argument('-num-w', '--num-workers', dest='num_workers', type=int,
                        default=2, help='Number of workers.')
    parser.add_argument('-q-size', '--queue-size', dest='queue_size', type=int,
                        default=5, help='Size of the queue.')
    args = parser.parse_args()

    input_q = Queue(maxsize=args.queue_size)
    output_q = Queue(maxsize=args.queue_size)

    #args.video_source = "tx2"
    video_device_id =  "nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)320, height=   (int)240,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"

    video_capture = WebcamVideoStream(src=video_device_id,
                                      width=args.width,
                                      height=args.height).start()

    cap_params = {}
    frame_processed = 0
    cap_params['im_width'], cap_params['im_height'] = (320,240)
    cap_params['score_thresh'] = score_thresh

    # max number of hands we want to detect/track
    cap_params['num_hands_detect'] = args.num_hands

    print(cap_params, args)

    # spin up workers to paralleize detection.
    pool = Pool(2, worker,
                (input_q, output_q, cap_params, frame_processed))

    start_time = datetime.datetime.now()
    num_frames = 0
    fps = 0
    index = 0

    while True:
        frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        index += 1

        input_q.put(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        output_frame = output_q.get()

        output_frame = cv2.cvtColor(output_frame, cv2.COLOR_RGB2BGR)

        elapsed_time = (datetime.datetime.now() -
                        start_time).total_seconds()
        num_frames += 1
        fps = num_frames / elapsed_time
        # print("frame ",  index, num_frames, elapsed_time, fps)

        if (output_frame is not None):
            if (args.display > 0):
                if (args.fps > 0):
                    detector_utils.draw_fps_on_image(
                        "FPS : " + str(int(fps)), output_frame)
                cv2.imshow('Muilti - threaded Detection', output_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                if (num_frames == 400):
                    num_frames = 0
                    start_time = datetime.datetime.now()
                else:
                    print("frames processed: ",  index,
                          "elapsed time: ", elapsed_time, "fps: ", str(int(fps)))
        else:
            # print("video end")
            break
    elapsed_time = (datetime.datetime.now() -
                    start_time).total_seconds()
    fps = num_frames / elapsed_time
    print("fps", fps)
    pool.terminate()
    video_capture.stop()
    cv2.destroyAllWindows()
