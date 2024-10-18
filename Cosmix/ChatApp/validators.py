from django.core.exceptions import ValidationError
import moviepy.editor as mp
import mutagen

def MaxDurationValidator(max_duration):
    def validator(file):
        try:
            # Check the duration of the file
            if file.name.endswith(('mp4', 'mov', 'avi')):
                video = mp.VideoFileClip(file.temporary_file_path())
                if video.duration > max_duration:
                    raise ValidationError(f"Video duration exceeds {max_duration} seconds.")
            elif file.name.endswith(('mp3', 'wav', 'ogg')):
                audio = mutagen.File(file.temporary_file_path())
                if audio.info.length > max_duration:
                    raise ValidationError(f"Audio duration exceeds {max_duration} seconds.")
        except AttributeError:
            raise ValidationError("File format not supported or invalid file.")
    return validator
