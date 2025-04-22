from src.services.crypto.video_analyzer.analyzer import VideoAnalyzer



if __name__ == '__main__':
    analyzer_instance = VideoAnalyzer(
        channel_title="Augusto Backes"
    )
    analyzer_instance.run()