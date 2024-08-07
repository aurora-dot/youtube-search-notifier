"""
Methods which collect and save YouTube videos to store into the database
"""

import traceback
from datetime import datetime

from sentry_sdk import capture_exception

from notifier import models
from notifier.lib.collect import Collector
from notifier.lib.logger import LOGGER

collector = Collector()


def add_new_search_query(search_query):
    """
    Gets the newest YouTube video from a given search query
    Creates a new YouTube objects to save the data into the database

    Args:
        search_query: The query to search for on YouTube
    """
    initial_videos = collector.get_initial_video_for_query(search_query)
    query, _ = models.YouTubeQuery.objects.get_or_create(query=search_query)
    # TODO: if save data breaks while using this method, it breaks the whole query
    _save_data(initial_videos, query)


def collect_new_videos():
    """
    Gets the newest YouTube data for each YouTubeQuery object in the database
    Loops through the newest videos until hitting the
        previous latest video from last call
    Saves the data back into the db and updates the query object with the latest video
    """
    youtube_search_queries = models.YouTubeQuery.objects.all().prefetch_related(
        "latest"
    )

    LOGGER.info("Collector - %s: Started collecting...", datetime.now())

    for search_query in youtube_search_queries:
        latest_video_ids = (
            models.YouTubeVideo.objects.filter(youtube_query=search_query)
            .order_by("-created_at")
            .values_list("video_id", flat=True)[:15]
        )
        try:
            LOGGER.info(
                "Collector - %s: collecting videos for query '%s' (id: %s), stopping at %s",
                datetime.now(),
                search_query.query,
                search_query.id,
                latest_video_ids[0],
            )

            collected_videos = collector.get_latest_videos(
                search_query.query, latest_video_ids
            )

            LOGGER.info(
                "Collector - %s: collected videos for query '%s' (id: %s)",
                datetime.now(),
                search_query.query,
                search_query.id,
            )

        except Exception as error:  # pylint: disable=W0718
            capture_exception(error)
            error_text = f"{datetime.now()}: {error.__class__.__name__} - {error}, Query ID: {search_query.id}, Query Str: '{search_query.query}'"  # pylint: disable=C0301
            traceback_str = traceback.format_exc()
            LOGGER.error(error_text)
            LOGGER.error(traceback_str)

            # skip rest of iteration code
            continue

        if collected_videos:
            _save_data(collected_videos, search_query)
        else:
            LOGGER.info(
                "Collector - %s: No new videos for query '%s'",
                datetime.now(),
                search_query.query,
            )

    LOGGER.info(
        "Collector - %s: Completed collection!",
        datetime.now(),
    )


def _save_data(collected_videos, search_query):
    videos = []
    LOGGER.info("Collector - %s: Saving data into db...", datetime.now())
    for video in reversed(collected_videos):
        channel, _ = models.YouTubeChannel.objects.get_or_create(
            channel_link=video["channel"].pop("channel_link"), defaults=video["channel"]
        )
        videos.append(
            models.YouTubeVideo(
                **video["video"],
                youtube_query=search_query,
                youtube_channel=channel,
                created_at=datetime.now(),
            )
        )

    # TODO if this breaks, and query has no videos, delete query
    models.YouTubeVideo.objects.bulk_create(videos, ignore_conflicts=True)

    newest_video = models.YouTubeVideo.objects.get(video_id=videos[0].video_id)
    search_query.latest = newest_video
    search_query.save()
    LOGGER.info(
        "Collector - %s: Saved into db! Newest video id for query is '%s'",
        datetime.now(),
        newest_video.video_id,
    )
