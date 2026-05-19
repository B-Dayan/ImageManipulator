import cv2

def RetrieveImage():
    needToRetrieveImage = True
    while needToRetrieveImage:
        fileName = (input("What is the file name of the image you wish to process? Remember to include the file extension. "))
        img = cv2.imread(fileName, 1)

        if img is None: 
            print("Error: The image couldn't be found. Did you remember to include the file extension and use correct capitalization? ")
        else:
            needToRetrieveImage = False

    return (img, fileName)


def ResizeImage(img):
    resizeStyle = int(input("Do you want to set the image to a fixed size (Press 1) or increase/decrease it by a set factor (Press 2)? "))
    if resizeStyle == 1:
        try:
            width = int(input(f"What should the new width of the image be? (Must be positive. The current width is {img.shape[1]} pixels). "))
        except ValueError:
            raise NotIntegerException

        if width <= 0:
            raise NotPositiveException()
        else:
            try:
                height = int(input(f"What should the new height of the image be? (Must be positive. The current height is {img.shape[0]} pixels). "))
            except ValueError:
                raise NotIntegerException
    
            if height <= 0:
                raise NotPositiveException()
            else:
                img = cv2.resize(img, (width, height))
                return img

    elif resizeStyle == 2:
        deltaX = float(input("What number should the width of the image be multiplied by? (Must be positive). "))
        if deltaX <= 0:
            raise NotPositiveException()
        else:
            deltaY = float(input("What number should the height of the image be multiplied by? (Must be positive). "))
            if deltaY <= 0:
                raise NotPositiveException()
            else:
                img = cv2.resize(img, None, fx = deltaX, fy = deltaY)
                return img
    else:
        raise NotOptionException()


def FlipImage(img):
    flipStyle = int(input("Do you want to flip the image horizontally (Press 1), vertically (Press 0), or both (Press -1)? "))
    if flipStyle != 0 and flipStyle != 1 and flipStyle != -1:
        raise NotOptionException()
    else:
        img = cv2.flip(img, flipStyle)
        return img


def RotateImage(img):
    rAngle = float(input("What angle should the image be rotated by? (In degrees, positive to rotate counter-clockwise). "))

    height, width = img.shape[:2]

    askForCenter = int(input("Do you want to rotate the image around the center point? (Press 1 for \"yes\", or 0 for \"no\"). "))
    if askForCenter == 1:
        centerX = width / 2
        centerY = height / 2
    elif askForCenter == 0:
        centerX = float(input(f"What x coordinate should the image be rotated around? (Must be between 0 and {width}). "))
        centerY = float(input(f"What y coordinate should the image be rotated around? (Must be between 0 and {height}). "))
    else:
        raise NotOptionException()
                
    askForScale = int(input("Do you also want to resize the image? (Press 1 for \"yes\", or 0 for \"no\"). "))
    if askForScale == 0:
        rScale = 1
    elif askForScale == 1:
        rScale = float(input("What factor should the image be scaled by? (Must be positive). "))
        if rScale <= 0:
            raise NotPositiveException()
    else:
        raise NotOptionException()

    matrix = cv2.getRotationMatrix2D((centerX, centerY), rAngle, rScale)
    img = cv2.warpAffine(img, matrix, (height, width))
    return img


class NotOptionException(Exception):
    message = "Error: Your input is not one of the available options."
    def __init__(self):
        super().__init__(self.message)

class NotPositiveException(Exception):
    message = "Error: Your input is not a positive, non-zero number."
    def __init__(self):
        super().__init__(self.message)

class NotIntegerException(Exception):
    message = "Error: Your input is not an integer."
    def __init__(self):
        super().__init__(self.message)


class Main():
    def MainMethod(self):
        img, fileName = RetrieveImage()
        operationsList = (ResizeImage, FlipImage, RotateImage)

        #splitFileName will be used to append notes onto the file name before the extension (e.g. "image.png" to "image_flipped_1.png")
        splitFileName = fileName.split(".")
        splitFileName[1] = "." + splitFileName[1] #Append a dot onto the beginning of the file extension string
        changesCounter = 1 #This variable will be appended onto new file names to ensure each has a unique name, even if the same process is done twice
        operationStr = ("_resized_", "_flipped_", "_rotated_", "") #The blank string is added so an IndexError won't be raised when the user exits the program.

        shouldRun = True #Whether the program should run

        while shouldRun:
            noErrors = True #Whether there have been any errors while processing the image. If False, the current iteration of the while-loop is skipped.
            operationIndex = int(input("How do want to process this image? (Press 1 to resize, 2 to flip, 3 to rotate, or 4 to quit the application). "))

            if operationIndex < 4 and operationIndex > 0:
                try:
                    img = operationsList[operationIndex - 1](img)
                except (NotOptionException, NotPositiveException, NotIntegerException) as err:
                    print(err.message)
                    noErrors = False
            elif operationIndex == 4:
                print("Goodbye!")
                shouldRun = False
            else:
                print(NotOptionException.message)
                noErrors = False

            # Only display the processed image if the program actually processed an image, not if the user selected Quit.
            if noErrors:
                newFileName = splitFileName[0] + operationStr[operationIndex - 1] + str(changesCounter) + splitFileName[1]
                cv2.imwrite(newFileName, img)

                print("The image has been opened in a new window. Press any key to continue.")
                cv2.imshow("Your New Image: " + newFileName, img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                changesCounter += 1

            print("") # Empty line

if __name__ == "__main__":    
    main = Main()
    main.MainMethod()