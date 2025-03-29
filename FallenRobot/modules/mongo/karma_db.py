from typing import Dict, List, Union
from .db import karma

def add_karma(chat_id: int, user_id: int, amount: int = 1) -> int:
    """Add/subtract karma points and return new total"""
    result = karma.find_one_and_update(
        {'chat_id': str(chat_id), 'user_id': user_id},
        {'$inc': {'karma': amount}},
        upsert=True,
        return_document=True
    )
    return result.get('karma', amount)

def get_karma(chat_id: int, user_id: int) -> int:
    """Get karma points for a user"""
    result = karma.find_one({'chat_id': str(chat_id), 'user_id': user_id})
    return result['karma'] if result else 0

def get_top_karma(chat_id: int, limit: int = 10) -> List[Dict[str, Union[int, str]]]:
    """Get top karma users in a chat"""
    results = karma.find(
        {'chat_id': str(chat_id)},
        {'user_id': 1, 'karma': 1, '_id': 0}
    ).sort('karma', -1).limit(limit)
    return list(results)

def reset_karma(chat_id: int, user_id: int) -> bool:
    """Reset karma for a user"""
    result = karma.delete_one({'chat_id': str(chat_id), 'user_id': user_id})
    return result.deleted_count > 0