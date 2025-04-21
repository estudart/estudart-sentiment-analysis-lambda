from src.services.crypto.video_analyzer.analyzer import VideoAnalyzer



if __name__ == '__main__':
    analyzer_instance = VideoAnalyzer(
        channel_title="Investidor Moderno", 
        number_of_videos=2
    )
    analyzer_instance.run()