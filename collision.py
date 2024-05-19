from json import load as loadJSON
from werkzeug.datastructures import FileStorage
from pathlib import Path

class Collision:
    def __init__(self, inputFiles) -> None:
        self.inputFiles: list[FileStorage] = inputFiles
        self.files: dict[str: dict] = dict() # JSON

        self.errors: set[str] = set()

        self.load_files()
    
    # Load files (JSONs)
    def load_files(self) -> None:
        for file in self.inputFiles:
            path = Path(file.filename)
            name, format = path.stem, path.suffix

            if format == ".json":
                self.files[name] = loadJSON(file)
            else:
                self.errors.add(f"File '{name}' has an usuported format '{format}'.")
        
        # Process Files
        for name in self.files.keys():
            self.processFile(name) 

    def processFile(self, name: str):
        TILESET = self.files[name]
        instances = TILESET['instances']

        for instance in instances:
            variables = instance['variables']
            objectID = instance['object']

            if objectID == 517.0:
                variables['visible'] = "false"