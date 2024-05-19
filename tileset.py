from json import load as loadJSON
from werkzeug.datastructures import FileStorage
from pathlib import Path
from PIL import Image
from PIL.Image import Image as ImageType

class Tileset:
    def __init__(self, inputFiles) -> None:
        self.inputFiles: list[FileStorage] = inputFiles
        self.files: dict[str: any] = dict() # JSON
        self.tilesets: dict[str: ImageType] = dict() # PNGs

        self.tileset_images: dict[str: ImageType] = dict() #PNGs Results

        self.errors: set[str] = set()
        self.missing_tilesets: set[str] = set()

        self.load_files()
    
    # Load files (JSONs) and tilesets (PNGs)
    def load_files(self) -> None:
        for file in self.inputFiles:
            path = Path(file.filename)
            name, format = path.stem, path.suffix

            if format == ".png":
                self.tilesets[name] = Image.open(file)
            elif format == ".json":
                TILESET = loadJSON(file)
                properties = TILESET['properties']
                layers = TILESET['tile_data']
                self.files[name] = [properties, layers]
            else:
                self.errors.add(f"File '{name}' has an usuported format '{format}'.")
        
        # Process Files
        for name in self.files.keys():
            self.processFile(name)


    def processLayer(self, tileset_image: ImageType, layers: dict, layer_z: str, room_pos: tuple, room_name: str) -> None:
        if int(layer_z) < 0:
            return
        for position, info in layers[layer_z].items():
            tile_position = [int(position) for position in position.split('_')]
            tile_position[0] -= room_pos[0]
            tile_position[1] -= room_pos[1]
            tile_positionbox = (tile_position[0], tile_position[1], tile_position[0] + 32, tile_position[1] + 32)


            tile_coord = [int(coord) * 32 for coord in info["coord"]]
            tile_coordbox = (tile_coord[0], tile_coord[1], tile_coord[0] + 32, tile_coord[1] + 32)

            tileset_name = info["tileset"]

            try:
                tile = self.tilesets[tileset_name].crop(tile_coordbox)
                tileset_image.paste(tile, tile_positionbox, tile)
            except KeyError as missingTile:
                self.errors.add(f"Room '{room_name}' is missing tileset: {missingTile}.")
                self.missing_tilesets.add(str(missingTile))     

    def processFile(self, name: str):
        properties, layers = self.files[name]

        ROOM_X = int(properties['roomX'])
        ROOM_Y = int(properties['roomY'])
        ROOM_POS = (ROOM_X, ROOM_Y)
        LEVEL_WIDTH = int(properties['levelWidth'])
        LEVEL_HEIGHT = int(properties['levelHeight'])
        REAL_LEVEL_WIDTH = abs(ROOM_X - LEVEL_WIDTH)
        REAL_LEVEL_HEIGHT = abs(ROOM_Y - LEVEL_HEIGHT)
        SIZE = (REAL_LEVEL_WIDTH, REAL_LEVEL_HEIGHT)

        tileset_image = Image.new("RGBA", SIZE)

        for layer in sorted(layers.keys(), key=int, reverse=True):
            self.processLayer(tileset_image, layers, layer, ROOM_POS, name)
        
        self.tileset_images[name] = tileset_image
