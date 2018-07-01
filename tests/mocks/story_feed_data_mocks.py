current_epochs_mock = 1529779604000

bad_story_feed_data_mock = {
    "story_id": 'badstory741a63a89a237e670',
    "title": 'some title',
    "description": 'description',
    "likes": 0,
    "dislikes": 3,
    "funnies": 0,
    "number of comments": 0,
    "borings": 0,
    "location": 'some_magic_maps_location',
    "timestamp": current_epochs_mock - 9999999999,
    "is_private": 'false',
    "uploader": 'martin.errazquin',
    "friend_ids": set(),
    "number of friends": 0,
    "number of stories": 1
}

good_story_feed_data_mock = {
    "story_id": 'goodstory741a63a89a237e67',
    "title": 'some title',
    "description": 'description',
    "likes": 100,
    "dislikes": 0,
    "funnies": 0,
    "borings": 0,
    "number of comments": 4,
    "location": 'some_magic_maps_location',
    "timestamp": current_epochs_mock - 259200000,
    "is_private": 'false',
    "uploader": 'martin.errazquin',
    "friend_ids": set(),
    "number of friends": 0,
    "number of stories": 1
}

hot_story_feed_data_mock = {
    "story_id": 'hotstory741a63a89a237e670',
    "title": 'some title',
    "description": 'description',
    "likes": 50,
    "dislikes": 0,
    "funnies": 0,
    "borings": 0,
    "number of comments": 0,
    "location": 'some_magic_maps_location',
    "timestamp": current_epochs_mock - 4000,
    "is_private": 'false',
    "uploader": 'martin.errazquin',
    "friend_ids": set(),
    "number of friends": 0,
    "number of stories": 1
}
