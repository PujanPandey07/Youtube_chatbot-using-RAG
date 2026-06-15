from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import re


class TranscriptError(Exception):
    """Raised when a transcript cannot be retrieved for any reason."""
    pass


def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None


def get_transcript(video_id):
    try:
        yt_api = YouTubeTranscriptApi()
        transcript_list = yt_api.list(video_id)

        # 1. Try English first
        try:
            transcript = transcript_list.find_transcript(["en"]).fetch()
            text = " ".join(chunk.text for chunk in transcript)
            return text

        except NoTranscriptFound:
            pass

        # 2. Try auto-translated English from any available transcript
        try:
            available = transcript_list.find_transcript(
                [t.language_code for t in transcript_list]
            )
            transcript = available.translate("en").fetch()
            text = " ".join(chunk.text for chunk in transcript)
            return text

        except Exception:
            pass

        # 3. Fall back to whatever language is available (no translation)
        for t in transcript_list:
            transcript = t.fetch()
            text = " ".join(chunk.text for chunk in transcript)
            return text

        raise TranscriptError(
            "No transcript could be retrieved for this video.")

    except TranscriptsDisabled:
        raise TranscriptError("Transcripts are disabled for this video.")
    except Exception as e:
        if isinstance(e, TranscriptError):
            raise
        raise TranscriptError(f"Could not fetch transcript: {str(e)}")
