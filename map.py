from typing import Tuple, List, Dict, Iterable
from pygame.math import Vector2  # prefer using tuples instead for memory efficiency
import pygame
from PIL import Image
import json
from utils import path as p

# name: (type: ("textures" => 0|"animator" => 1), texture: (texture|animator))
tiles_textures = {
    "stone_brick": {
        "type": "texture",
        "texture": pygame.transform.scale2x(pygame.image.load(p('/assets/textures/stone_bricks.png')))
    }
}


def load_map(map_id: int) -> List[List[Dict]]:
    map_img = Image.open(p('/maps/{0}.png'.format(map_id)), 'r').convert('RGB')
    w, h = map_img.size
    map_buffer = [[{} for y in range(0, h)] for x in range(0, w)]
    for x in range(0, w):
        for y in range(0, h):
            map_buffer[x][y] = load_block_by_color(map_img.getpixel((x, y)), (x, y), map_id)

    return map_buffer


def load_block_by_color(color: Tuple[int, int, int], pos: Tuple[int, int], map_id: int) -> Dict:
    """
    color => (0, 1, 2)
    2 => type => 0: Air, 100: Wall
    1 => variant => type 10: [20: stone_brick]
    0 => 0 => don't use special args, 10 => use special args (from map.json file)
    """
    t = {}
    if color[2] == 100:
        if color[1] == 20:
            t = {'x': pos[0], 'y': pos[1], 'id': 'stone_brick_wall', 'texture': 'stone_brick', 'collision': True}
    else:
        t = {'x': pos[0], 'y': pos[1], 'id': 'air', 'texture': None, 'collision': False}

    if color[0] == 1:
        attrs = load_block_infos(map_id)
        for attr in attrs:
            t[attr] = attrs[attr]

    return t


def render_tile(screen: pygame.Surface, tile_dict: Dict, offset: Vector2):
    # TODO: we can't use type animator yet for textures
    if tile_dict['texture'] is not None:
        t = tiles_textures[tile_dict['texture']]['texture']
        x, y = tile_dict['x'], tile_dict['y']
        screen.blit(t, ((x - offset.x) * 32, (y - offset.y) * 32))


def load_block_infos(path, pos: Tuple[int, int]):
    """
    json format:
    "X:Y" => {attrs to add}
    attrs:
    """
    with open(path, 'r') as f:
        map_json = json.load(f.read())
        attrs = map_json['{0}:{1}'.format(pos[0], pos[1])]
    return attrs
