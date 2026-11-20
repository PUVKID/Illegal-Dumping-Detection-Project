"""보존 파일명과 동일 공식 주석의 ID 대응을 엄격하게 확인합니다."""
import hashlib
import json
from pathlib import PurePosixPath
import re

STREET_URL = 'https://zenodo.org/api/records/8288500/files/images.zip/content'


def legacy_match(value):
    """경로의 마지막 이름만 읽고 접두사와 확장자를 완전 매칭합니다."""
    if not isinstance(value, str):
        return None
    name = PurePosixPath(value.replace('\\', '/')).name
    return re.fullmatch(r'(?:plitter|street)_([1-9][0-9]*)\.jpg', name)


def canonical_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False,
                       separators=(',', ':')) + '\n').encode('utf-8')


def _images(annotation):
    result = {}
    for image in annotation['images']:
        identity = image.get('id')
        if type(identity) is not int or identity <= 0 or str(identity) in result:
            raise ValueError('공식 주석에 모호하거나 중복된 이미지 ID가 있습니다.')
        if not isinstance(image.get('file_name'), str) or not image['file_name']:
            raise ValueError('공식 이미지 이름이 없습니다.')
        if any(type(image.get(key)) is not int or image[key] <= 0 for key in ('width', 'height')):
            raise ValueError('공식 이미지 크기가 올바르지 않습니다.')
        result[str(identity)] = image
    return result


def provenance_map(rows, previous_annotation, current_annotation, previous_ids=()):
    """보존 JPEG 해시와 복원 원본 해시를 서로 바꾸지 않습니다."""
    if previous_annotation != current_annotation:
        raise ValueError('이전 공식 주석과 현재 공식 주석의 내용이 다릅니다.')
    images = _images(current_annotation)
    mapped = {}
    for row in rows:
        if row.get('source') != 'pLitterStreet':
            continue
        match = legacy_match(row.get('image'))
        if match is None or row.get('url') != STREET_URL:
            raise ValueError('보존 pLitter 파일명 또는 공식 출처를 확인할 수 없습니다.')
        identity = match.group(1)
        if identity not in images or identity in mapped:
            raise ValueError('보존 ID가 공식 주석에 없거나 중복됩니다.')
        old_hash = row.get('sha256')
        if not isinstance(old_hash, str) or not re.fullmatch('[a-f0-9]{64}', old_hash):
            raise ValueError('보존 JPEG의 SHA-256 형식이 올바르지 않습니다.')
        image = images[identity]
        mapped[identity] = {'id': identity,
                            'legacy_basename': PurePosixPath(row['image'].replace('\\', '/')).name,
                            'legacy_encoded_sha256': old_hash,
                            'official_file_name': image['file_name'], 'official_path': image.get('path'),
                            'width': image['width'], 'height': image['height']}
    if not mapped:
        raise ValueError('대응할 보존 pLitter 자료가 없습니다.')
    previous_ids = set(map(str, previous_ids))
    if not previous_ids <= set(images):
        raise ValueError('이전 5차 ID가 공식 주석에 없습니다.')
    prior = set(mapped)
    return {'schema': 1, 'source': 'pLitterStreet',
            'identity_basis': 'preserved producer image.id -> basename; identical official annotations',
            'limits': ['legacy SHA describes re-encoded JPEG, not the newly restored official raw bytes',
                       'missing historical JPEG bytes cannot be certified as identical'],
            'counts': {'prior': len(prior), 'previous_round5': len(previous_ids),
                       'overlap': len(prior & previous_ids), 'union': len(prior | previous_ids)},
            'rows': [mapped[key] for key in sorted(mapped, key=int)]}


def map_digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()

