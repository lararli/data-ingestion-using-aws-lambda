from spotify_data import track_df, album_df, artist_info_df, related_artists_df
from util import upload_s3


files = {'tracks': track_df, 'albums': album_df, 'artist_info': artist_info_df, 'related_artists': related_artists_df}

dict_keys = files.keys()

def lambda_handler(event, context):
    for key in dict_keys:
        file = key
        upload_data = upload_s3(
            body=files[key].to_csv(),
            bucket='spotify-data-ingestion',
            file=file + '.csv'
        )
    return upload_data







