import pysnooper

from PIL import Image
from stegano import lsb

# Example usage:
image_path = "Regards.jpg"
output_image_path = "hips.Regards.jpg"
message_to_hide = "This is a hidden message."


@pysnooper.snoop()
def detect_steganography(image_path):
    try:
        image = Image.open(image_path)
        decoded_text = lsb.reveal(image)

        if decoded_text:
            print("Steganography detected!")
            print("Hidden message:", decoded_text)
        else:
            print("No steganography detected.")

    except Exception as e:
        print("Error:", e)

@pysnooper.snoop()
def add_steganography(image_path, output_path, message):
    try:
        # Open the image
        image = Image.open(image_path)

        # Encode the message into the image using LSB steganography
        encoded_image = lsb.hide(image, message)

        # Save the output image
        encoded_image.save(output_path)

        print("Steganography message added successfully!")

    except Exception as e:
        print("Error:", e)

add_steganography(image_path, output_image_path, message_to_hide)
detect_steganography(image_path)


