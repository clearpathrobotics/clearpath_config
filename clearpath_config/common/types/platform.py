class PACSProfile:
    def __init__(
            self,
            rows: int,
            columns: int
            ) -> None:
        self.rows = rows
        self.columns = columns


class IndexingProfile:
    def __init__(
            self,
            camera: int = 0,
            gps: int = 0,
            imu: int = 0,
            lidar2d: int = 0,
            lidar3d: int = 0
            ) -> None:
        self.camera = camera
        self.gps = gps
        self.imu = imu
        self.lidar2d = lidar2d
        self.lidar3d = lidar3d


# Platform
# - all supported platforms
class Platform:
    # Dingo D V1
    DD100 = "dd100"
    # Dingo O V1
    DO100 = "do100"
    # Jackal V1
    J100 = "j100"
    # Husky V2
    A200 = "a200"
    # Ridgeback V1
    R100 = "r100"
    # Warthog V2
    W200 = "w200"
    # Genric Robot
    GENERIC = "generic"

    ALL = [DD100, DO100, J100, A200, R100, W200, GENERIC]

    PACS = {
        GENERIC: PACSProfile(rows=100, columns=100),
        A200: PACSProfile(rows=8, columns=7),
        J100: PACSProfile(rows=4, columns=2),
    }

    INDEX = {
        GENERIC: IndexingProfile(),
        A200: IndexingProfile(),
        J100: IndexingProfile(gps=1, imu=1),
    }
