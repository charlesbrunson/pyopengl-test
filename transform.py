import affine

class Transform:
  def __init__(self, 
               position: list[float] = [0, 0, 0], 
               rotation: list[float] = [0, 0, 0], 
               scale:    list[float] = [1, 1, 1]):
    self.pos = position
    self.rot = rotation
    self.scale = scale
  
  def matrix(self):
    return affine.identity() \
         @ affine.scale(*self.scale) \
         @ affine.rotate(*self.rot) \
         @ affine.translation(*self.pos)