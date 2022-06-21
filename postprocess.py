# Preprocessing operations on the skins generated by DALL-E
import cv2, os, sys

def clearWhiteZones(skin):
  """
  Clears the zones that are supposed to be white from the skin.
  @param skin: The skin image to be cleared in opencv format.
  """
  whiteZones = [
    [[0,8], [0,8]],     # Top left corner
    [[0,8], [56,64]],   # Top right corner
    [[0,8], [24,40]],   # Top middle space
    [[16,20], [0,4]],   # Mid left space 1
    [[32,36], [0,4]],   # Mid left space 2
    [[48,52], [0,4]],   # Mid left space 3
    [[16,20], [52,56]], # Mid right space 1
    [[32,36], [52,56]], # Mid right space 2
    [[16,20], [12,20]], # Middle space 1
    [[16,20], [36,44]], # Middle space 2
    [[32,36], [12,20]], # Middle space 3
    [[32,36], [36,44]], # Middle space 4
    [[48,52], [12,20]], # Middle space 5
    [[48,52], [28,36]], # Middle space 6
    [[48,52], [44,52]], # Middle space 7
    [[16,48], [56,60]], # Big right space 1
    [[16,52], [60,64]]  # Big right space 2
  ]

  for zone in whiteZones:
    skin[zone[0][0]:zone[0][1], zone[1][0]:zone[1][1]] = [0, 0, 0, 0]

def removeBodyTransparency(skin):
  """
  Removes the transparency of the body (first layer) from the skin.
  @param skin: The skin image to be cleared in opencv format.
  """
  body = [
    [[0,8], [8,24]],    # Top and bottom head
    [[8,16], [0,32]],   # Head sides
    [[16,20], [4,12]],  # Top and bottom right leg
    [[16,20], [20,36]], # Top and bottom torso
    [[16,20], [44,52]], # Top and bottom right arm
    [[20,32], [0,56]],  # Right leg, torso and right arm sides
    [[48,52], [20,28]], # Top and bottom left leg
    [[48,52], [36,44]], # Top and bottom left arm
    [[52,64], [16,48]]  # Left leg, torso and left arm sides
  ]

  for zone in body:
    for x in range(zone[1][0], zone[1][1]):
      for y in range(zone[0][0], zone[0][1]):
        skin[y, x][3] = 255

def setBinaryTransparency(skin):
  """
  Sets the skin's second layer transparency to be either 0 or 255.
  @param skin: The skin image to be cleared in opencv format.
  """
  for x in range(0, 64):
    for y in range(0, 64):
      if skin[y, x][3] >= 200:
        skin[y, x][3] = 255
      else:
        skin[y, x][3] = 0

def postprocess(skin_dir, save_dir = './app/skins/'):
  """
  Main function, calls the other functions to postprocess the skins in the specified folder.
  """
  print("Postprocessing files in " + skin_dir)
  for file in os.listdir(skin_dir):
    if file.endswith('.png'):
      skin = cv2.imread(skin_dir + file, cv2.IMREAD_UNCHANGED)
      # Postprocessing operations
      clearWhiteZones(skin)
      removeBodyTransparency(skin)
      setBinaryTransparency(skin)
      # Save the skin
      cv2.imwrite(save_dir + file, skin)

if __name__ == '__main__':
  if len(sys.argv) == 1:
    postprocess(sys.argv[1])
  elif len(sys.argv) == 2:
    postprocess(sys.argv[1], sys.argv[2])
  else:
    print("Incorrect number of arguments.")
    sys.exit(1)