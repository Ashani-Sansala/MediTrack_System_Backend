from flask import Blueprint, jsonify

video_feed_bp = Blueprint('video_feed', __name__)

@video_feed_bp.route('/videos', methods=['GET'])
def get_videos():
    video_mapping = {
        'floor1': {
            'Camera 01': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/The%20Witcher%203_%20Wild%20Hunt%20OST%20-%20Sword%20of%20Destiny%20-%20Main%20Theme%20(online-video-cutter.com).mp4?alt=media",
            'Camera 02': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/Travis%20Scott%20-%20My%20Eyes%20Cut2.mov?alt=media",
            'Camera 03': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/Uyama%20Hiroto%20-%20One%20Day.mp4?alt=media",
            'Camera 04': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/Arctic%20Monkeys%20-%20Do%20I%20Wanna%20Know.mp4?alt=media"
        },
        'floor2': {
            'Camera 01': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/Nujabes%20Shiki%20No%20Uta.mp4?alt=media",
            'Camera 02': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/Nujabes%20Lady%20Brown.mp4?alt=media",
            'Camera 03': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/Sayonara%20Wild%20Hearts%20(Full%20Album%2C%20Continuous%2C%20No%20Fade-out)%20(online-video-cutter.com).mp4?alt=media",
            'Camera 04': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/floor2-camera4.mp4?alt=media"
        },
        'floor3': {
            'Camera 01': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/Nujabes%20Feathers.mp4?alt=media",
            'Camera 02': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/Nujabes%20Battlecry.mp4?alt=media",
            'Camera 03': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/city%20girl-%20chroma%20velocity.mp4?alt=media",
            'Camera 04': "https://firebasestorage.googleapis.com/v0/b/medproject-feab1.appspot.com/o/floor3-camera4.mp4?alt=media"
        }
    }
    return jsonify(video_mapping)



