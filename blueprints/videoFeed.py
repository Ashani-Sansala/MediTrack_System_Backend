from flask import Blueprint, jsonify

video_feed_bp = Blueprint('video_feed', __name__)

@video_feed_bp.route('/videos', methods=['GET'])
def get_videos():
    video_mapping = {
        'floor1': {
            'Camera 01': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/7e61b995-92f1-452f-b897-5324477070a3.mp4?alt=media&token=8f95925c-6f10-4a97-b08b-efdbf0628fbb",
            'Camera 02': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/bb06f041-4bb7-4f6c-bc5f-56a207b508a5.mp4?alt=media&token=eb372aa3-bd82-4636-b60a-961bd517e4dc",
            'Camera 03': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/eed1a9b2-b5f0-4539-bd13-b035f9e26273.mp4?alt=media&token=43f1dcde-95a8-42e2-b25d-c8cb4ca245d1",
            'Camera 04': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/7e61b995-92f1-452f-b897-5324477070a3.mp4?alt=media&token=8f95925c-6f10-4a97-b08b-efdbf0628fbb"
        },
        'floor2': {
            'Camera 01': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/111.mp4?alt=media&token=7a48496d-c1de-44c3-96fe-3c2d9847248a",
            'Camera 02': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/112.mp4?alt=media&token=df0f565c-5cdf-4f06-9d9d-e381024e169d",
            'Camera 03': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/113.mp4?alt=media&token=44436d30-db83-43d5-9284-f9e104b7c259",
            'Camera 04': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/113.mp4?alt=media&token=44436d30-db83-43d5-9284-f9e104b7c259"
        },
        'floor3': {
            'Camera 01': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/111.mp4?alt=media&token=7a48496d-c1de-44c3-96fe-3c2d9847248a",
            'Camera 02': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/113.mp4?alt=media&token=44436d30-db83-43d5-9284-f9e104b7c259",
            'Camera 03': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/112.mp4?alt=media&token=df0f565c-5cdf-4f06-9d9d-e381024e169d",
            'Camera 04': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/113.mp4?alt=media&token=44436d30-db83-43d5-9284-f9e104b7c259"
        }
    }
    return jsonify(video_mapping)

